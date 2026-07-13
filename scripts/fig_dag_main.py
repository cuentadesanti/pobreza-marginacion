#!/usr/bin/env python
"""
Vista principal del DAG (figures/05_dag/fig_dag_main.png): ≤25 nodos visibles.

NO cambia la edge-list: las familias de indicadores se dibujan como PLACAS (notación de
repetición ×N con un nodo unitario ejemplar adentro), no como cajas agregadas causales.
Cada arista dibujada se VERIFICA contra dict/dag_edges.csv (expandiendo el ejemplar a su
familia); si una arista dibujada no existe en el canónico, el script aborta.

Tres historias enfatizadas:
  (a) privaciones latentes → indicadores
  (b) SAE → preliminares → calibración → publicados (+ distribución conjunta → regla → pobreza)
  (c) masa carencial pre-2013 → piso 2013 → fórmula FAIS → FISM → inversión → infraestructura
"""
import os, sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG, DICT = os.path.join(HERE, "figures"), os.path.join(HERE, "dict")
SURF, INK, INK2, MUT = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
STYLE = {
    "causal_sustantivo": ("#0b0b0b", "-", 1.6), "carga_latente": ("#0b0b0b", "-", 1.2),
    "efecto_directo": ("#1baf7a", "-", 1.5), "relacion_definicional": ("#8a6d3b", ":", 1.5),
    "medicion": ("#2a78d6", "-", 1.2), "estimacion_estadistica": ("#4a3aa7", "-", 1.5),
    "derivacion_determinista": ("#898781", "-", 1.1),
    "retroalimentacion_politica": ("#e34948", "--", 1.8),
}
KIND_FC = {"estructural": "#f2fbf7", "latente": "#eef4fd", "indicador": "#ffffff",
           "instrumento": "#f6f5f1", "operador": "#f6f3ff", "indice": "#fdf2e6",
           "politica": "#fdeeee", "preliminar": "#faf8ff", "microdato": "#fffbe8"}
KIND_EC = {"estructural": "#1baf7a", "latente": "#2a78d6", "indicador": "#898781",
           "instrumento": "#52514e", "operador": "#4a3aa7", "indice": "#eda100",
           "politica": "#e34948", "preliminar": "#9085e9", "microdato": "#c98500"}

# placas: ejemplar -> (etiqueta de familia, miembros en la edge-list)
PLATES = {
    "rezago_educ": ("educativos ×3", ["analf", "sin_basica", "rezago_educ"]),
    "sin_agua": ("infraestructura y vivienda ×7",
                 ["sin_drenaje", "sin_electr", "sin_agua", "piso_tierra", "hacinam",
                  "car_vivienda", "car_servbas"]),
    "lp_ingreso": ("monetarios y alimentación ×4",
                   ["ing_2sm", "car_alim", "lp_ingreso", "lp_ingreso_ext"]),
    "lpi_raw": ("preliminares SAE ×4", ["segsoc_raw", "alim_raw", "lpi_raw", "lpe_raw"]),
}
POS = {  # 25 nodos visibles
    "loc_peq": (1.1, 7.5), "pct_60mas": (1.1, 5.7), "pol_salud": (1.1, 4.1),
    "z_edu": (3.6, 8.15), "z_infra": (3.6, 6.4), "z_mon": (3.6, 4.4),
    "rezago_educ": (6.6, 8.35), "sin_agua": (6.6, 6.6), "car_salud": (6.6, 5.15),
    "lp_ingreso": (6.6, 3.95),
    "censo_basico": (6.6, 9.35), "muestra_censal": (4.6, 2.35), "mec_enigh": (1.1, 2.35),
    "op_sae": (3.15, 2.95), "lpi_raw": (4.85, 3.4), "op_calib": (6.35, 2.55),
    "dist_conjunta": (6.75, 1.55), "op_identif": (8.35, 2.05),
    "im_conapo": (9.6, 7.3), "pobreza_coneval": (9.6, 3.2),
    "masa_carencial_pre2013": (1.3, 0.5), "piso_2013": (3.3, 0.5),
    "formula_fais_t0": (5.3, 0.5), "fism_t0": (7.3, 0.5), "inversion_t0": (9.4, 0.5),
}
# aristas visibles: (source_ejemplar, target_ejemplar, relation_type, rad)
DRAW = [
    ("loc_peq", "z_infra", "causal_sustantivo", 0.0), ("loc_peq", "z_edu", "causal_sustantivo", 0.0),
    ("pol_salud", "car_salud", "causal_sustantivo", 0.06),
    ("loc_peq", "sin_agua", "efecto_directo", -0.14),
    ("pct_60mas", "rezago_educ", "efecto_directo", -0.18),
    ("z_edu", "rezago_educ", "carga_latente", 0.0), ("z_infra", "sin_agua", "carga_latente", 0.0),
    ("z_mon", "lp_ingreso", "carga_latente", 0.0),
    ("censo_basico", "sin_agua", "medicion", -0.12),
    ("muestra_censal", "rezago_educ", "medicion", -0.30),
    ("muestra_censal", "dist_conjunta", "medicion", 0.10),
    ("muestra_censal", "op_sae", "estimacion_estadistica", 0.08),
    ("mec_enigh", "op_sae", "estimacion_estadistica", 0.0),
    ("mec_enigh", "op_calib", "estimacion_estadistica", 0.28),
    ("op_sae", "lpi_raw", "estimacion_estadistica", 0.0),
    ("lpi_raw", "op_calib", "estimacion_estadistica", 0.0),
    ("op_calib", "lp_ingreso", "estimacion_estadistica", 0.0),
    ("op_sae", "dist_conjunta", "estimacion_estadistica", -0.22),
    ("dist_conjunta", "op_identif", "derivacion_determinista", 0.0),
    ("op_identif", "pobreza_coneval", "derivacion_determinista", 0.0),
    ("op_calib", "pobreza_coneval", "estimacion_estadistica", 0.14),
    ("sin_agua", "im_conapo", "derivacion_determinista", 0.0),
    ("masa_carencial_pre2013", "piso_2013", "retroalimentacion_politica", 0.0),
    ("piso_2013", "formula_fais_t0", "retroalimentacion_politica", 0.0),
    ("formula_fais_t0", "fism_t0", "retroalimentacion_politica", 0.0),
    ("fism_t0", "inversion_t0", "retroalimentacion_politica", 0.0),
    ("inversion_t0", "z_infra", "retroalimentacion_politica", 0.62),
]


# estilo homogéneo del repo + figuras por capítulo (ver scripts/plotstyle.py)
import plotstyle as ps
ps.use()
FIG = ps.figdir("05_dag")

def verify(E):
    """cada arista dibujada debe existir en el canónico para ALGÚN miembro de la placa."""
    fam = {ex: set(m) | {ex} for ex, (_, m) in PLATES.items()}
    pairs = set(zip(E["source"], E["target"]))
    faltan = []
    for s, t, rt, _ in DRAW:
        S, T = fam.get(s, {s}), fam.get(t, {t})
        if not any((a, b) in pairs for a in S for b in T):
            faltan.append((s, t, rt))
    if faltan:
        sys.exit(f"✗ aristas dibujadas SIN respaldo en dag_edges.csv: {faltan}")
    print(f"✓ vista principal: {len(POS)} nodos visibles, {len(DRAW)} aristas, "
          f"todas respaldadas por el canónico")


def main():
    N = pd.read_csv(os.path.join(DICT, "dag_nodes.csv"))
    E = pd.read_csv(os.path.join(DICT, "dag_edges.csv"))
    verify(E)
    lbl = dict(zip(N["node_id"], N["label"]))
    knd = dict(zip(N["node_id"], N["kind"]))

    fig, ax = plt.subplots(figsize=(13.5, 9.2), facecolor=SURF)
    ax.set_xlim(0, 13.2); ax.set_ylim(-0.1, 10.15); ax.set_axis_off()

    for s, t, rt, rad in DRAW:
        col, ls, lw = STYLE[rt]
        ax.add_patch(FancyArrowPatch(POS[s], POS[t], arrowstyle="-|>", mutation_scale=11,
                                     shrinkA=20, shrinkB=20, color=col, lw=lw, linestyle=ls,
                                     connectionstyle=f"arc3,rad={rad}", zorder=2, alpha=0.9))
    # placas detrás de los ejemplares
    for ex, (fname, _) in PLATES.items():
        x, y = POS[ex]
        ax.add_patch(FancyBboxPatch((x - 1.05, y - 0.62), 2.1, 1.05, boxstyle="round,pad=0.05",
                                    facecolor="none", edgecolor=MUT, lw=1.0, ls=(0, (4, 3)),
                                    zorder=2.5))
        ax.text(x - 1.0, y - 0.52, fname, ha="left", fontsize=6.8, color=MUT, style="italic",
                zorder=4)
    for nid, (x, y) in POS.items():
        text = "\n".join(__import__("textwrap").wrap(lbl[nid], 20))
        w = 0.062 * max(len(l) for l in text.split("\n")) + 0.3
        h = 0.34 + 0.24 * text.count("\n")
        k = knd[nid]
        if k == "latente":
            ax.add_patch(Ellipse((x, y), w * 1.3, h * 2.0, facecolor=KIND_FC[k],
                                 edgecolor=KIND_EC[k], lw=1.8, zorder=3))
        else:
            ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.07",
                                        facecolor=KIND_FC[k], edgecolor=KIND_EC[k],
                                        lw=1.9 if nid == "loc_peq" else 1.3, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=7.6, color=INK, zorder=4)

    # anotaciones de contexto (no son aristas)
    ax.text(5.3, 0.06, "insumo adicional: pobreza municipal 2015 [t−1]", ha="center",
            fontsize=6.8, color=MUT, style="italic")
    ax.annotate("", (11.55, 1.85), (10.55, 2.85),
                arrowprops=dict(arrowstyle="-|>", color="#e34948", ls="--", lw=1.8))
    ax.text(11.65, 1.55, "fórmula FAIS 2021+ [t+1]\n→ infraestructura municipal\nfutura [t+2]",
            fontsize=7.2, color="#e34948", ha="left")
    ax.text(11.0, 4.9, "la inversión AUMENTA la\ninfraestructura (reduce la\nprivación futura)",
            ha="left", fontsize=6.8, color=MUT, style="italic")
    ax.text(0.15, 9.9, "El proceso generador en una página — medición y política de la privación municipal",
            fontsize=12.5, color=INK, fontweight="bold")
    ax.text(0.15, 9.55, "vista principal (25 nodos); placas ×N = repetición sobre la familia, no agregación · "
            "canónico completo: dict/dag_{nodes,edges}.csv y fig_dag_full.png "
            f"({len(N)} nodos, {len(E)} aristas, acíclico verificado)",
            fontsize=7.6, color=INK2)
    leyenda = [Line2D([0], [0], color=c, ls=ls, lw=max(lw, 1.6), label=n) for (c, ls, lw), n in
               [(STYLE["causal_sustantivo"], "causal sustantivo"),
                (STYLE["carga_latente"], "carga latente"),
                (STYLE["efecto_directo"], "efecto directo de cofactor"),
                (STYLE["medicion"], "observación por instrumento"),
                (STYLE["estimacion_estadistica"], "estimación estadística"),
                (STYLE["derivacion_determinista"], "derivación determinista"),
                (STYLE["retroalimentacion_politica"], "política (t−2 → t+2)")]]
    fig.legend(handles=leyenda, loc="lower center", ncol=4, frameon=False, fontsize=8)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(os.path.join(FIG, "fig_dag_main.png"), dpi=160)
    print("figures/05_dag/fig_dag_main.png lista")


if __name__ == "__main__":
    main()
