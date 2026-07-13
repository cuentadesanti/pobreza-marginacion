#!/usr/bin/env python
"""
Tarea B (datos) — piso 2013 e importes 2020 del FISM por municipio.

Uso:
    python scripts/build_b_fism_piso.py <dir_xlsx_2013> <ejercicio_del_gasto_2020.csv>

Insumos (ver RAW_DATA_MANIFEST.md, no se versionan):
  - 32 XLSX estatales del Anexo XXI, Informes Trimestrales 2013-T4, carpeta
    Gasto_federalizado_Nivel_Fondo (Transparencia Presupuestaria).
  - CSV "ejercicio del gasto" del SRFT, reporte 2020-T4 (latin-1, 180 MB).

Salidas:
  - outputs/fism_2013_municipal.parquet   (cvegeo, monto_2013, pagado_2013,
        cobertura_estatal, ejecutor_n, flag_captura)
  - outputs/fism_fortamun_2020_municipal.parquet (cvegeo, fais_2020, fortamun_2020,
        fais_pagado_2020, trimestre_reporte_fais)

Trampas cubiertas: cvegeo con zfill (estados 01-09), '0-COBERTURA ESTATAL'
excluido del test municipal (bandera, no imputación), duplicados por ejecutor,
outliers de captura listados sin borrarse.
"""
import os
import re
import sys
import glob

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")
PROC = os.path.join(HERE, "data", "processed")

PAT_FISM = re.compile(r"FISM|INFRAESTRUCTURA SOCIAL MUNICIPAL|FAIS MUNICIPAL|FONDO III", re.I)
# FISM = 2.2228/2.5294 = 87.879% del FAIS (art. 32 LCF); FAIS PEF 2013 = $53,090.8 M,
# FAIS PEF 2020 = $85,853.8 M
FISM_2013_OFICIAL = 46_655e6
FISM_2020_OFICIAL = 75_447e6


def parse_estado_2013(path):
    xl = pd.ExcelFile(path)
    sheet = xl.sheet_names[0]                      # '2013|TRIM 4|8-CHIHUAHUA' o '...|3.BAJA...'
    df = xl.parse(sheet, header=None)
    m = re.match(r"\s*(\d+)", sheet.split("|")[-1])
    if m is None:                                  # hojas 'Recuperado_Hoja1' (Coahuila, Querétaro):
        for v in df.head(12).to_numpy().ravel():   # el título 'N-ESTADO RECURSO 2013' va dentro
            t = re.match(r"\s*(\d+)-.*RECURSO 2013", str(v))
            if t:
                m = t
                break
    ent = int(m.group(1))

    # encabezado: localizar columnas por texto (Morelos viene corrido una columna)
    muncol = totcol = pagcol = hdr = None
    for i in range(min(15, len(df))):
        for j, v in df.iloc[i].items():
            if isinstance(v, str):
                if v.startswith("Municipio, dependencia"):
                    hdr, muncol = i, j
                elif v.strip() == "Total Anual":
                    totcol = j
                elif v.strip() == "Pagado" and totcol is not None and j > totcol:
                    pagcol = j
    assert None not in (hdr, muncol, totcol, pagcol), f"encabezado no hallado en {path}"

    rows = []
    for i in range(hdr, len(df)):
        fondo = next((str(v) for j, v in df.iloc[i].items()
                      if j < muncol and isinstance(v, str) and PAT_FISM.search(v)), None)
        mun_raw = df.iat[i, muncol]
        if fondo is None or pd.isna(mun_raw):
            continue
        mun_raw = str(mun_raw).strip()
        head = mun_raw.split("-")[0].strip()
        mun_id = int(head) if head.isdigit() else 0   # sin clave numérica ⇒ estatal
        rows.append({
            "ent": ent,
            "cvegeo": f"{ent:02d}{mun_id:03d}",
            "municipio_txt": mun_raw,
            "ejecutora": str(df.iat[i, muncol + 1]).strip(),
            "monto": pd.to_numeric(df.iat[i, totcol], errors="coerce"),
            "pagado": pd.to_numeric(df.iat[i, pagcol], errors="coerce"),
            "cobertura_estatal": mun_id == 0,
        })
    return pd.DataFrame(rows)


def build_2013(dir_xlsx):
    files = sorted(glob.glob(os.path.join(dir_xlsx, "*.xlsx")))
    assert len(files) == 32, f"esperaba 32 XLSX estatales, hay {len(files)}"
    raw = pd.concat([parse_estado_2013(f) for f in files], ignore_index=True)

    n0 = len(raw)
    raw = raw.drop_duplicates(subset=["cvegeo", "municipio_txt", "ejecutora", "monto", "pagado"])
    print(f"2013: {n0} filas FISM, {n0 - len(raw)} duplicados exactos eliminados")

    g = (raw.groupby(["cvegeo", "cobertura_estatal"], as_index=False)
            .agg(monto_2013=("monto", "sum"), pagado_2013=("pagado", "sum"),
                 ejecutor_n=("ejecutora", "nunique")))

    # trampa 1: los estados 01-09 deben estar (el bug histórico del zfill)
    assert g["cvegeo"].str.startswith("0").any(), "no hay claves con prefijo 0 — bug de zfill"

    # trampa 4: outliers de captura (per cápita fuera de [p1,p99], monto 0, >10x mediana estatal)
    pob = pd.read_parquet(os.path.join(PROC, "diagnostico_municipal_v1.parquet"))[
        ["cvegeo", "pob_conapo", "nom_mun"]]
    g = g.merge(pob, on="cvegeo", how="left")
    mun = g[~g["cobertura_estatal"]].copy()
    mun["pc"] = mun["monto_2013"] / mun["pob_conapo"]
    p1, p99 = mun["pc"].quantile([0.01, 0.99])
    med_ent = mun.assign(ent=mun["cvegeo"].str[:2]).groupby("ent")["pc"].transform("median")
    flag = (mun["monto_2013"] <= 0) | (mun["pc"] < p1) | (mun["pc"] > p99) | \
           (mun["pc"] > 10 * med_ent.values)
    g["flag_captura"] = False
    g.loc[mun.index, "flag_captura"] = flag.values
    sosp = g[g["flag_captura"]]
    print(f"2013: {len(sosp)} municipios sospechosos de captura (se listan, no se borran):")
    print(sosp[["cvegeo", "nom_mun", "monto_2013", "pob_conapo"]].to_string(index=False))

    est = g[g["cobertura_estatal"]]
    print(f"\n2013: {(~g['cobertura_estatal']).sum()} municipios con desglose, "
          f"{len(est)} filas de cobertura estatal (entidades: "
          f"{sorted(est['cvegeo'].str[:2].unique())})")
    tot = g["monto_2013"].sum()
    print(f"2013: suma nacional ${tot/1e6:,.0f} M = {tot/FISM_2013_OFICIAL:.1%} del FISM "
          f"oficial (${FISM_2013_OFICIAL/1e6:,.0f} M); solo desglose municipal: "
          f"{g.loc[~g['cobertura_estatal'], 'monto_2013'].sum()/FISM_2013_OFICIAL:.1%}")

    out = g[["cvegeo", "monto_2013", "pagado_2013", "cobertura_estatal",
             "ejecutor_n", "flag_captura"]]
    out.to_parquet(os.path.join(OUT, "fism_2013_municipal.parquet"), index=False)
    return out


def build_2020(csv_path):
    usecols = ["TRIMESTRE", "CICLO_RECURSO", "PROGRAMA_FONDO_CONVENIO_ESPECIFICO",
               "ID_ENTIDAD_FEDERATIVA", "ID_MUNICIPIO", "INSTITUCION_EJECUTORA",
               "MONTO_APROBADO", "MONTO_PAGADO"]
    df = pd.read_csv(csv_path, encoding="latin-1", usecols=usecols)
    df = df[df["CICLO_RECURSO"] == 2020]
    prog = df["PROGRAMA_FONDO_CONVENIO_ESPECIFICO"].astype(str)
    df = df[prog.str.contains("FAIS Municipal", na=False) | (prog == "FORTAMUN")].copy()
    df["fondo"] = np.where(prog.loc[df.index].str.contains("FAIS Municipal"),
                           "fais", "fortamun")
    df = df.dropna(subset=["ID_MUNICIPIO"])
    df["cvegeo"] = (df["ID_ENTIDAD_FEDERATIVA"].astype(int).astype(str).str.zfill(2)
                    + df["ID_MUNICIPIO"].astype(int).astype(str).str.zfill(3))
    assert df["cvegeo"].str.startswith("0").any(), "no hay claves con prefijo 0 — bug de zfill"

    # MONTO_APROBADO es el anual reportado en cada corte trimestral: tomar el último
    # trimestre con reporte por municipio-fondo (el T4 solo pierde a quien dejó de reportar)
    df = df.drop_duplicates()
    last = df.groupby(["cvegeo", "fondo"])["TRIMESTRE"].transform("max")
    snap = df[df["TRIMESTRE"] == last]
    g = (snap.groupby(["cvegeo", "fondo"], as_index=False)
             .agg(aprobado=("MONTO_APROBADO", "sum"), pagado=("MONTO_PAGADO", "sum"),
                  trimestre=("TRIMESTRE", "first")))
    wide = g.pivot(index="cvegeo", columns="fondo", values="aprobado").rename(
        columns={"fais": "fais_2020", "fortamun": "fortamun_2020"})
    extra = g[g["fondo"] == "fais"].set_index("cvegeo")[["pagado", "trimestre"]].rename(
        columns={"pagado": "fais_pagado_2020", "trimestre": "trimestre_reporte_fais"})
    wide = wide.join(extra).reset_index()

    nf = wide["fais_2020"].notna().sum()
    print(f"\n2020: FAIS Municipal en {nf} municipios, suma "
          f"${wide['fais_2020'].sum()/1e6:,.0f} M (fondo oficial FISMDF 2020: "
          f"${FISM_2020_OFICIAL/1e6:,.0f} M → cobertura "
          f"{wide['fais_2020'].sum()/FISM_2020_OFICIAL:.1%}); "
          f"FORTAMUN en {wide['fortamun_2020'].notna().sum()} municipios, "
          f"${wide['fortamun_2020'].sum()/1e6:,.0f} M")
    wide.to_parquet(os.path.join(OUT, "fism_fortamun_2020_municipal.parquet"), index=False)
    return wide


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    build_2013(sys.argv[1])
    build_2020(sys.argv[2])
