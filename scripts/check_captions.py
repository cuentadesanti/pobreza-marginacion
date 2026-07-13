#!/usr/bin/env python
"""
Guarda de sincronía prosa/captions/tablas ↔ CSVs fuente (capa C2 del handoff; hermano de
check_dag_conteos.py — tercer episodio de riesgo de desincronización, automatizado).

Cada binding computa un valor DESDE su CSV en outputs/ y exige que su representación
(normalizada: signo unicode → '-', sin separador de miles) aparezca en el paper. Si el CSV
cambia y la prosa se queda con el número viejo, el valor nuevo no aparece y el check FALLA.

Uso: python scripts/check_captions.py   (exit 1 si hay desincronía)
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")
P1 = os.path.join(HERE, "paper", "paper1_metodo.md")
P2 = os.path.join(HERE, "paper", "paper2_desigualdad.md")


def norm_text(path):
    t = open(path, encoding="utf-8").read()
    t = t.replace("−", "-").replace(" ", " ")
    # quitar separador de miles SOLO entre dígitos (24,106.1 -> 24106.1)
    import re
    while re.search(r"(\d),(\d)", t):
        t = re.sub(r"(\d),(\d)", r"\1\2", t)
    return t


def bindings():
    """[(paper_path, etiqueta, valor, formato)] — valor computado del CSV, nunca a mano."""
    B = []

    cert = pd.read_csv(os.path.join(OUT, "certeza_canonica.csv"))
    for _, r in cert.iterrows():
        B.append((P1, f"certeza {r.eje} % sustantivo", r.pct_sustantivo, "{:.1f}"))

    t1 = pd.read_csv(os.path.join(OUT, "tabla1_escalera.csv"))
    for _, r in t1[t1.bloque == "marginalizado_MvN"].iterrows():
        B.append((P1, f"tabla1 rhat {r.modelo}", r.rhat, "{:.3f}"))
        B.append((P1, f"tabla1 elpd {r.modelo}", r.elpd, "{:.1f}"))

    t2 = pd.read_csv(os.path.join(OUT, "desacuerdo_familias.csv"))
    fam = t2.set_index("familia")
    B += [(P1, "mload educación", fam.loc["educacion", "mload_p2"], "{:.3f}"),
          (P1, "mload líneas p2", fam.loc["lineas_sae", "mload_p2"], "{:.3f}"),
          (P1, "mload viv p2", fam.loc["viv_servicios", "mload_p2"], "{:.3f}"),
          (P1, "mload viv p3", fam.loc["viv_servicios", "mload_p3"], "{:.3f}"),
          (P1, "% sustantivo líneas", fam.loc["lineas_sae", "pct_sustantivo"], "{:.1f}"),
          (P1, "firma media AA", fam.loc["lineas_sae", "media_AA"], "{:.3f}"),
          (P1, "firma media BB", fam.loc["lineas_sae", "media_BB"], "{:.3f}")]

    eig = pd.read_csv(os.path.join(OUT, "eigen_marginal_2v3.csv"))
    for _, r in eig.iterrows():
        for k in (1, 2, 3):
            B.append((P1, f"eigen{k} {r.modelo}", r[f"eigen{k}"], "{:.3f}"))
    # M5: la nulidad firma↔composición — el máximo |r| citado como cota debe estar en prosa
    t2m5 = pd.read_csv(os.path.join(OUT, "desacuerdo_familias.csv")).set_index("familia")
    maxr = max(abs(t2m5.loc["lineas_sae", c])
               for c in ["corr_loc_peq_pct", "corr_pct_60mas", "corr_log_pob"])
    B.append((P1, "cota |r| firma-composición", max(maxr, 0.001), "{:.3f}"))

    t3 = pd.read_csv(os.path.join(OUT, "tabla3_gamma.csv")).set_index("medida")
    B += [(P1, "gamma share PC1", t3.loc["share_varianza_PC1_pct", "valor"], "{:.1f}"),
          (P1, "gamma share sectorial", t3.loc["share_sectorial_pct", "valor"], "{:.1f}"),
          (P1, "corr PC1 pibe", t3.loc["corr_PC1_log_pibe_pc", "valor"], "{:.2f}"),
          (P1, "corr PC1 gasto", t3.loc["corr_PC1_gasto_pibe_pct", "valor"], "{:.2f}")]

    ig = pd.read_csv(os.path.join(OUT, "veta_ignorancia.csv")).set_index("eje")
    B += [(P1, "ignorancia corr log_pob eje1", ig.loc["eje1", "log_pob"], "{:.3f}"),
          (P1, "ignorancia corr ruralidad eje1", ig.loc["eje1", "loc_peq_pct"], "{:.3f}")]

    th = pd.read_csv(os.path.join(OUT, "desigualdad_theil.csv")).set_index("medida")
    for med, lab in [("z_material_bruto", "material bruto"), ("lp_ingreso_pct", "líneas"),
                     ("analf_pct", "analf"), ("piso_tierra_pct", "piso"),
                     ("sin_agua_pct", "agua"), ("eje1", "eje1"), ("eje2", "eje2"),
                     ("eje3", "eje3")]:
        B.append((P2, f"theil % entre {lab}", th.loc[med, "pct_entre"], "{:.1f}"))

    rob = pd.read_csv(os.path.join(OUT, "desigualdad_robustez.csv"))
    ac = rob[(rob.bloque == "C_acumulacion")].set_index("esquema")
    for q in ["q70", "q75", "q80", "q90"]:
        B.append((P2, f"acumulación obs/esp {q}", ac.loc[q, "valor"], "{:.2f}"))
    cap = rob[rob.bloque == "capa3_incremental"].set_index("esquema")
    for esq in cap.index:
        B.append((P2, f"escalera R² '{esq}'", cap.loc[esq, "valor"], "{:.3f}"))

    g5 = pd.read_csv(os.path.join(OUT, "g5_coercion.csv"))
    g5b = g5[(g5.linea == "G5b") & (g5["var"] == "coercion_any")].iloc[0]
    B += [(P2, "G5b beta coerción→homicidio", g5b.beta, "{:.2f}"),
          (P2, "G5b t coerción→homicidio", g5b.t, "{:.1f}")]

    gap = pd.read_csv(os.path.join(OUT, "gap_aportaciones_regimen.csv")).set_index("coef")
    B += [(P2, "gap fiscal AA", gap.loc["AA", "gap_pct_vs_ns"], "{:.1f}"),
          (P2, "gap fiscal BB", gap.loc["BB", "gap_pct_vs_ns"], "{:.1f}")]
    return B


def main():
    textos = {p: norm_text(p) for p in (P1, P2)}
    errores = []
    n = 0
    for paper, etiqueta, valor, fmt in bindings():
        n += 1
        v = float(valor)
        rep = fmt.format(abs(v))
        if rep not in textos[paper]:
            errores.append(f"{os.path.basename(paper)}: '{etiqueta}' — el CSV dice "
                           f"{fmt.format(v)} y la prosa no lo contiene")
    print(f"check_captions: {n} bindings verificados contra outputs/")
    if errores:
        print("✗ DESINCRONÍA prosa↔CSV:")
        for e in errores:
            print("  " + e)
        return 1
    print("✓ toda cifra vinculada aparece en su paper (papers sincronizados con outputs/)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
