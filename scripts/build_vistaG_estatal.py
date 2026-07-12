#!/usr/bin/env python
"""
Vista G estatal — capa contemporánea desde el export AGREGADO de ACLED (auditado: ADMIN1).

⚠ Este export NO es municipal (semana × estado × tipo de evento; sin actores ni coordenadas
de evento). Rol: state_context contemporáneo 2018+ (nivel 2 jerárquico, interacciones,
validación temporal) — complementa a BACRIM (tipología 2020) y NO sustituye el export de
eventos municipal, que sigue pendiente de credencial ACLED.

Entrada: data/raw/acled_agregado_admin1_lac.xlsx
Salida:  data/processed/vistaG_crimen_estatal.parquet
         (cve_ent, anio, eventos violencia política, fatalidades, batallas)
"""
import os, sys, unicodedata
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "data", "raw",
                                                         "acled_agregado_admin1_lac.xlsx")
EST = {"aguascalientes": "01", "baja california": "02", "baja california sur": "03",
       "campeche": "04", "coahuila": "05", "coahuila de zaragoza": "05", "colima": "06",
       "chiapas": "07", "chihuahua": "08", "ciudad de mexico": "09", "mexico city": "09",
       "distrito federal": "09", "durango": "10", "guanajuato": "11", "guerrero": "12",
       "hidalgo": "13", "jalisco": "14", "mexico": "15", "michoacan": "16",
       "michoacan de ocampo": "16", "morelos": "17", "nayarit": "18", "nuevo leon": "19",
       "oaxaca": "20", "puebla": "21", "queretaro": "22", "quintana roo": "23",
       "san luis potosi": "24", "sinaloa": "25", "sonora": "26", "tabasco": "27",
       "tamaulipas": "28", "tlaxcala": "29", "veracruz": "30",
       "veracruz de ignacio de la llave": "30", "yucatan": "31", "zacatecas": "32"}


def norm(s):
    s = unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode().lower()
    return s.replace("state of ", "").strip()


def main():
    d = pd.read_excel(SRC)
    mx = d[d.COUNTRY == "Mexico"].copy()
    mx["cve_ent"] = mx.ADMIN1.map(lambda s: EST.get(norm(s)))
    assert mx.cve_ent.notna().all(), f"sin mapear: {mx[mx.cve_ent.isna()].ADMIN1.unique()}"
    mx["anio"] = pd.to_datetime(mx.WEEK).dt.year
    pol = mx[mx.DISORDER_TYPE.str.contains("Political violence", na=False)]
    agg = (pol.groupby(["cve_ent", "anio"])
              .agg(eventos=("EVENTS", "sum"), fatalidades=("FATALITIES", "sum")).reset_index())
    bat = (mx[mx.EVENT_TYPE == "Battles"].groupby(["cve_ent", "anio"])["EVENTS"].sum()
             .rename("batallas").reset_index())
    agg = agg.merge(bat, on=["cve_ent", "anio"], how="left").fillna({"batallas": 0})
    out = os.path.join(HERE, "data", "processed", "vistaG_crimen_estatal.parquet")
    agg.to_parquet(out, index=False)
    print(f"vistaG_crimen_estatal.parquet: {agg.shape} | {mx.WEEK.min().date()} → {mx.WEEK.max().date()}")
    print(agg[agg.anio == 2020].nlargest(5, "eventos").to_string(index=False))


if __name__ == "__main__":
    main()
