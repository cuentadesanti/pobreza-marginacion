#!/usr/bin/env python
"""
DAG de medición v4 — objeto canónico: dict/dag_nodes.csv + dict/dag_edges.csv.

Antes de renderizar, VALIDA formalmente:
  1. aciclicidad (networkx.is_directed_acyclic_graph) — el lazo FAIS está temporalizado
     (t-1, t, t+1, t+2), así que el grafo debe ser acíclico SIN notas externas;
  2. consistencia nodos↔aristas (ids, kinds);
  3. matriz permitida de tipos (relation_type × (source_kind, target_kind));
  4. reporta nodos con rol dual.

La pobreza multidimensional NO se deriva de prevalencias marginales: pasa por la
distribución conjunta persona-hogar (dist_conjunta) y la regla de identificación
(op_identif). SAE y calibración son secuenciales: op_sae → preliminares → op_calib →
publicados.
"""
import os, sys
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG, DICT = os.path.join(HERE, "figures"), os.path.join(HERE, "dict")
SURF, INK, INK2, MUT = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"

STYLE = {
    "causal_sustantivo":          ("#0b0b0b", "-", 1.3, 0.85),
    "carga_latente":              ("#0b0b0b", "-", 1.0, 0.42),
    "efecto_directo":             ("#1baf7a", "-", 1.2, 0.85),
    "relacion_definicional":      ("#8a6d3b", ":", 1.4, 0.95),
    "medicion":                   ("#2a78d6", "-", 0.9, 0.5),
    "estimacion_estadistica":     ("#4a3aa7", "-", 1.2, 0.8),
    "derivacion_determinista":    ("#898781", "-", 0.8, 0.45),
    "retroalimentacion_politica": ("#e34948", "--", 1.5, 0.95),
}
ALLOWED = {
    "causal_sustantivo": {("estructural", "latente"), ("estructural", "indicador"),
                          ("satelital", "latente"), ("latente", "latente")},
    "efecto_directo": {("estructural", "indicador")},
    "relacion_definicional": {("estructural", "indicador")},
    "carga_latente": {("latente", "indicador")},
    "medicion": {("instrumento", "indicador"), ("instrumento", "estructural"),
                 ("instrumento", "microdato"), ("latente", "satelital")},
    "estimacion_estadistica": {("instrumento", "operador"), ("operador", "preliminar"),
                               ("preliminar", "operador"), ("operador", "indicador"),
                               ("operador", "microdato"), ("operador", "indice")},
    "derivacion_determinista": {("indicador", "indice"), ("estructural", "indice"),
                                ("microdato", "operador"), ("operador", "indice")},
    "retroalimentacion_politica": {("indice", "politica"), ("politica", "politica"),
                                   ("politica", "latente")},
}

IND_ORDER = ["analf", "sin_basica", "rezago_educ",
             "sin_drenaje", "sin_electr", "sin_agua", "piso_tierra", "hacinam",
             "car_vivienda", "car_servbas", "car_salud", "car_segsoc",
             "ing_2sm", "car_alim", "lp_ingreso", "lp_ingreso_ext"]
POS = {"loc_peq": (1.15, 11.35), "pct_60mas": (1.15, 9.85), "dep_ratio": (1.15, 8.85),
       "pct_prim": (1.15, 7.95), "empleo_prec": (1.15, 6.95), "remesas": (1.15, 5.95),
       "fiscal": (1.15, 5.05), "pol_salud": (1.15, 3.9),
       "z_edu": (3.85, 10.6), "z_infra": (3.85, 8.3), "z_lab": (3.85, 5.4), "z_mon": (3.5, 3.1),
       "censo_basico": (4.9, 12.15), "muestra_censal": (4.9, 1.15), "mec_enigh": (1.15, 1.15),
       "op_sae": (3.1, 2.3), "op_calib": (5.55, 5.3),
       "segsoc_raw": (5.1, 4.55), "alim_raw": (5.1, 3.9), "lpi_raw": (5.1, 3.25),
       "lpe_raw": (5.1, 2.6),
       "dist_conjunta": (7.0, 1.05), "op_identif": (8.5, 1.75),
       "im_conapo": (9.7, 9.6), "pobreza_coneval": (9.7, 3.4), "pobreza_2015": (2.75, 0.95),
       "masa_carencial_pre2013": (0.9, 0.05), "piso_2013": (2.75, 0.05),
       "formula_fais_t0": (4.9, 0.4), "fism_t0": (6.7, 0.05), "inversion_t0": (8.5, 0.4),
       "formula_fais_t1": (11.0, 0.9), "fism_t1": (12.45, 2.6),
       "inversion_t1": (12.45, 4.6), "z_infra_t2": (12.45, 8.8),
       "actividad_economica": (2.4, 12.15), "viirs_ntl": (0.9, 12.15),
       "elevacion": (1.05, 2.6), "rugosidad": (2.45, 2.2), "acc_ciudad": (1.05, 3.25)}
for i, nid in enumerate(IND_ORDER):
    POS[nid] = (6.9, 11.7 - i * 0.62)
KIND_FC = {"estructural": "#f2fbf7", "latente": "#eef4fd", "indicador": "#ffffff",
           "instrumento": "#f6f5f1", "operador": "#f6f3ff", "indice": "#fdf2e6",
           "politica": "#fdeeee", "preliminar": "#faf8ff", "microdato": "#fffbe8", "satelital": "#eafaf2"}
KIND_EC = {"estructural": "#1baf7a", "latente": "#2a78d6", "indicador": "#898781",
           "instrumento": "#52514e", "operador": "#4a3aa7", "indice": "#eda100",
           "politica": "#e34948", "preliminar": "#9085e9", "microdato": "#c98500", "satelital": "#0e7a52"}


# estilo homogéneo del repo + figuras por capítulo (ver scripts/plotstyle.py)
import plotstyle as ps
ps.use()
FIG = ps.figdir("05_dag")

def validate(N, E):
    ok = True
    ids = set(N["node_id"])
    used = set(E["source"]) | set(E["target"])
    if used - ids: print("✗ aristas con nodos no declarados:", used - ids); ok = False
    if ids - used: print("· nodos declarados sin aristas:", ids - used)
    if set(N["node_id"]) - set(POS): print("✗ nodos sin posición:", ids - set(POS)); ok = False
    kind = dict(zip(N["node_id"], N["kind"]))
    bad_kind = [(r.source, r.target) for r in E.itertuples()
                if (kind[r.source], kind[r.target]) != (r.source_kind, r.target_kind)]
    if bad_kind: print("✗ kinds inconsistentes nodos↔aristas:", bad_kind); ok = False
    viol = [(r.source, r.target, r.relation_type) for r in E.itertuples()
            if (r.source_kind, r.target_kind) not in ALLOWED[r.relation_type]]
    if viol: print("✗ aristas fuera de la matriz de tipos permitidos:", viol); ok = False
    else: print("✓ matriz de tipos: 0 violaciones")
    G = nx.DiGraph(list(zip(E["source"], E["target"])))
    if nx.is_directed_acyclic_graph(G):
        print(f"✓ ACÍCLICO (networkx): {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")
    else:
        print("✗ CICLOS:", list(nx.find_cycle(G))); ok = False
    dual = N[N["dual_role"] != "no"]
    print("· nodos con rol dual:", dual["node_id"].tolist())
    print("· aristas por tipo:\n" + E.groupby("relation_type").size().to_string())
    import check_dag_conteos
    if check_dag_conteos.main() != 0:
        ok = False
    return ok


def main():
    N = pd.read_csv(os.path.join(DICT, "dag_nodes.csv"))
    E = pd.read_csv(os.path.join(DICT, "dag_edges.csv"))
    if not validate(N, E):
        sys.exit("VALIDACIÓN FALLÓ — no se renderiza")

    fig, ax = plt.subplots(figsize=(15.5, 12.6), facecolor=SURF)
    ax.set_xlim(0, 14.6); ax.set_ylim(-0.3, 13.4); ax.set_axis_off()
    rad_cycle = [0.0, 0.07, -0.07, 0.12, -0.12]
    special_rad = {("inversion_t0", "z_infra"): 0.28, ("loc_peq", "im_conapo"): -0.24,
                   ("pobreza_coneval", "formula_fais_t1"): 0.12,
                   ("mec_enigh", "op_calib"): 0.30, ("piso_2013", "formula_fais_t1"): -0.12}
    for i, r in E.iterrows():
        (x1, y1), (x2, y2) = POS[r["source"]], POS[r["target"]]
        col, ls, lw, al = STYLE[r["relation_type"]]
        rad = special_rad.get((r["source"], r["target"]), rad_cycle[i % 5])
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=8,
                                     shrinkA=15, shrinkB=15, color=col, lw=lw, alpha=al,
                                     linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2))
    lbl = dict(zip(N["node_id"], N["label"]))
    knd = dict(zip(N["node_id"], N["kind"]))
    tix = dict(zip(N["node_id"], N["time_index"].fillna("t")))
    for nid, (x, y) in POS.items():
        text = lbl[nid] + ("" if tix[nid] in ("t", "") else f"  [{tix[nid]}]")
        text = "\n".join(__import__("textwrap").wrap(text, 24))
        w = 0.052 * max(len(l) for l in text.split("\n")) + 0.25
        h = 0.30 + 0.21 * text.count("\n")
        k = knd[nid]
        if k == "latente":
            ax.add_patch(Ellipse((x, y), w * 1.3, h * 2.0, facecolor=KIND_FC[k],
                                 edgecolor=KIND_EC[k], lw=1.6, zorder=3))
        else:
            ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.06",
                                        facecolor=KIND_FC[k], edgecolor=KIND_EC[k],
                                        lw=1.6 if nid == "loc_peq" else 1.2, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=6.4, color=INK, zorder=4)
    for x, t in [(1.15, "CONDICIONES\nESTRUCTURALES"), (3.85, "PRIVACIONES\nLATENTES [t]"),
                 (6.9, "INDICADORES\nPUBLICADOS [t]"), (9.7, "ÍNDICES\n[t-1 · t]"),
                 (12.45, "POLÍTICA\n[t-1 → t+2]")]:
        ax.text(x, 12.62, t, ha="center", fontsize=8.5, color=MUT, fontweight="bold")
    leyenda = [Line2D([0], [0], color=c, ls=ls, lw=max(lw, 1.4),
                      label={"causal_sustantivo": "causal sustantivo",
                             "carga_latente": "carga latente",
                             "efecto_directo": "efecto directo de cofactor (no vía z)",
                             "relacion_definicional": "relación definicional (denominador)",
                             "medicion": "observación por instrumento",
                             "estimacion_estadistica": "estimación estadística",
                             "derivacion_determinista": "derivación determinista",
                             "retroalimentacion_politica": "política (temporalizada t-1…t+2)"}[k])
               for k, (c, ls, lw, al) in STYLE.items()]
    ax.legend(handles=leyenda, loc="center right", bbox_to_anchor=(0.998, 0.83),
              frameon=False, fontsize=7.5)
    ax.text(0.1, 13.25, "DAG de medición y política a nivel de variable — México 2020 (vista completa)",
            fontsize=12.5, color=INK, fontweight="bold")
    ax.text(0.1, 12.95, f"canónico: dict/dag_nodes.csv ({len(N)}) + dict/dag_edges.csv ({len(E)}) · "
            "verificado acíclico (networkx) · pobreza vía distribución conjunta persona + regla de "
            "identificación · SAE→preliminares→calibración→publicados · borde grueso = rol dual",
            fontsize=7.3, color=INK2)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_dag_full.png"), dpi=150)
    print("\nfigures/05_dag/fig_dag_full.png regenerada (vista suplementaria auditable)")


if __name__ == "__main__":
    main()
