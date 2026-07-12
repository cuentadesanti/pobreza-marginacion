#!/usr/bin/env python
"""
Vista E — cofactores fiscales 2020 (estatal y municipal).

Insumos (NO versionados; URLs en RAW_DATA_MANIFEST.md):
  - EFIPEM estatal y municipal 2020 (INEGI, datos abiertos CSV)
  - PIBE 2020 preliminar, base 2013 (INEGI, boletín dic. 2021): montos exactos para las 11
    entidades listadas en la nota técnica; el resto reconstruido de la estructura porcentual
    (precisión 1 decimal de punto porcentual -> flag pibe_aprox)

Salidas en data/processed/:
  - estatales_2020.csv        32 estados: PIBE, gasto estatal EFIPEM, per cápita y razones
  - finanzas_mun_2020.parquet municipios EFIPEM (~2,250 de 2,469): ingresos, transferencias,
                              ingresos propios, egresos, inversión pública, per cápita,
                              dependencia de transferencias

ADVERTENCIA DE USO (ver reports/reporte_dgp_dag.md, dependencia 5): las APORTACIONES municipales
contienen FAIS, que se asigna por fórmula sobre la pobreza extrema municipal de CONEVAL ->
circularidad. Sirven para VALIDACIÓN/política, no como cofactor del espacio latente. Las
PARTICIPACIONES (Ramo 28, fórmula por población/recaudación) y los INGRESOS PROPIOS son menos
endógenos, pero la dependencia de transferencias sigue correlacionada con la capacidad fiscal.
"""
import os, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "."

# --- PIBE 2020 preliminar (millones de pesos corrientes, precios básicos). INEGI boletín.
PIBE_TOTAL = 21_884_029
PIBE_EXACTO = {  # 11 entidades con monto explícito en la nota técnica
    "09": 3_464_828, "15": 1_993_874, "19": 1_744_370, "14": 1_591_000, "30": 988_915,
    "11": 949_404, "02": 801_564, "05": 789_863, "08": 786_176, "26": 784_273, "21": 710_095,
}
PIBE_SHARE = {  # estructura porcentual (Gráfica 1)
    "01": 1.4, "02": 3.7, "03": 0.8, "04": 2.1, "05": 3.6, "06": 0.6, "07": 1.5, "08": 3.6,
    "09": 15.8, "10": 1.2, "11": 4.3, "12": 1.4, "13": 1.6, "14": 7.3, "15": 9.1, "16": 2.5,
    "17": 1.1, "18": 0.7, "19": 8.0, "20": 1.6, "21": 3.2, "22": 2.3, "23": 1.3, "24": 2.3,
    "25": 2.3, "26": 3.6, "27": 2.3, "28": 3.1, "29": 0.6, "30": 4.5, "31": 1.5, "32": 1.0,
}

ING_PROPIOS = ["Impuestos", "Derechos", "Productos", "Aprovechamientos", "Contribuciones de Mejoras"]


def load_efipem(path, municipal=False):
    df = pd.read_csv(path, dtype={"ID_ENTIDAD": str, "ID_MUNICIPIO": str})
    df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce")
    if municipal:
        df["cvegeo"] = df["ID_ENTIDAD"] + df["ID_MUNICIPIO"]
    return df


def pick(df, tema, cat, descr, by):
    sub = df[(df["TEMA"] == tema) & (df["CATEGORIA"] == cat) & (df["DESCRIPCION_CATEGORIA"].isin(descr))]
    return sub.groupby(by)["VALOR"].sum()


def main():
    comp = pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet"),
                           columns=["cvegeo", "cve_ent", "pob_conapo"])
    comp["cve_ent"] = comp["cvegeo"].str[:2]
    pob_ent = comp.groupby("cve_ent")["pob_conapo"].sum()

    # ---------- estatal ----------
    est = load_efipem(os.path.join(SCRATCH, "efipem_estatal/conjunto_de_datos/efipem_estatal_anual_tr_cifra_2020.csv"))
    gasto = pick(est, "Egresos", "Tema", ["Total de egresos"], "ID_ENTIDAD")
    # index = las 32 entidades; CDMX (09) no reportó EFIPEM estatal 2020 -> gasto NaN documentado
    e = pd.DataFrame({"gasto_estatal_pesos": gasto}, index=sorted(PIBE_SHARE))
    e.index.name = "cve_ent"
    e["pibe_mdp"] = pd.Series({k: PIBE_EXACTO.get(k, round(PIBE_SHARE[k] / 100 * PIBE_TOTAL)) for k in PIBE_SHARE})
    e["pibe_aprox"] = [int(k not in PIBE_EXACTO) for k in e.index]
    e["pob"] = pob_ent
    e["pibe_pc_mxn"] = e["pibe_mdp"] * 1e6 / e["pob"]
    e["gasto_estatal_pc_mxn"] = e["gasto_estatal_pesos"] / e["pob"]
    e["gasto_pibe_pct"] = 100 * e["gasto_estatal_pesos"] / (e["pibe_mdp"] * 1e6)
    e.round(2).to_csv(os.path.join(PROC, "estatales_2020.csv"))
    print("estatales_2020.csv:", e.shape)
    print(e[["pibe_pc_mxn", "gasto_estatal_pc_mxn", "gasto_pibe_pct"]].describe().round(1))

    # ---------- municipal ----------
    mun = load_efipem(os.path.join(SCRATCH, "efipem_municipal/conjunto_de_datos/efipem_municipal_anual_tr_cifra_2020.csv"),
                      municipal=True)
    m = pd.DataFrame({
        "ingresos_tot": pick(mun, "Ingresos", "Tema", ["Total de ingresos"], "cvegeo"),
        "participaciones": pick(mun, "Ingresos", "Capítulo", ["Participaciones federales"], "cvegeo"),
        "aportaciones": pick(mun, "Ingresos", "Capítulo", ["Aportaciones federales y estatales"], "cvegeo"),
        "ingresos_propios": pick(mun, "Ingresos", "Capítulo", ING_PROPIOS, "cvegeo"),
        "egresos_tot": pick(mun, "Egresos", "Tema", ["Total de egresos"], "cvegeo"),
        "inversion_publica": pick(mun, "Egresos", "Capítulo", ["Inversión pública"], "cvegeo"),
    })
    m = m.join(comp.set_index("cvegeo")["pob_conapo"], how="inner")
    for c in ["ingresos_tot", "participaciones", "aportaciones", "ingresos_propios",
              "egresos_tot", "inversion_publica"]:
        m[c + "_pc"] = m[c] / m["pob_conapo"]
    m["dep_transferencias_pct"] = 100 * (m["participaciones"].fillna(0) + m["aportaciones"].fillna(0)) / m["ingresos_tot"]
    m["autonomia_fiscal_pct"] = 100 * m["ingresos_propios"].fillna(0) / m["ingresos_tot"]
    m.index.name = "cvegeo"
    m.reset_index().to_parquet(os.path.join(PROC, "finanzas_mun_2020.parquet"), index=False)
    print("\nfinanzas_mun_2020.parquet:", m.shape,
          f"| cobertura {len(m)}/{len(comp)} = {100*len(m)/len(comp):.1f}%")
    print(m[["dep_transferencias_pct", "autonomia_fiscal_pct", "inversion_publica_pc"]].describe().round(1))
    # ¿el faltante es aleatorio? no: reportar tamaño mediano de los municipios sin dato
    faltan = comp[~comp["cvegeo"].isin(m.index)]
    print(f"\nMunicipios sin EFIPEM: {len(faltan)}; mediana pob = {faltan['pob_conapo'].median():.0f} "
          f"(vs {comp['pob_conapo'].median():.0f} global); por estado:\n",
          faltan.groupby("cve_ent").size().sort_values(ascending=False).head(8).to_string())


if __name__ == "__main__":
    main()
