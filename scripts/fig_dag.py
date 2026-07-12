#!/usr/bin/env python
"""
El DAG de medición, renderizado (figures/fig_dag_dgp.png).
Layout manual: latente -> instrumentos -> indicadores; cofactores arriba; lazo FAIS abajo.
Aristas rojas numeradas = las 5 dependencias mecánicas de reports/reporte_dgp_dag.md.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(HERE, "figures")
SURF, INK, INK2, MUT = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
BLUE, AQUA, YELLOW, RED, VIOLET = "#2a78d6", "#1baf7a", "#eda100", "#e34948", "#4a3aa7"

fig, ax = plt.subplots(figsize=(14, 9.6), facecolor=SURF)
ax.set_xlim(0, 14); ax.set_ylim(0, 9.6); ax.set_axis_off()


def box(x, y, w, h, text, fc, ec, fs=8.5, tc=INK, style="round,pad=0.08", lw=1.4):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle=style,
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=4)


def arrow(x1, y1, x2, y2, color=MUT, lw=1.4, ls="-", rad=0.0, z=2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13,
                                 color=color, lw=lw, linestyle=ls, zorder=z,
                                 connectionstyle=f"arc3,rad={rad}"))


def tag(x, y, n):
    ax.add_patch(Ellipse((x, y), 0.34, 0.34, facecolor=RED, zorder=6))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=8, color="white",
            zorder=7, fontweight="bold")


# ---- capa latente y cofactores ----
ax.add_patch(Ellipse((1.8, 4.5), 2.4, 1.5, facecolor="#eef4fd", edgecolor=BLUE, lw=2, zorder=3))
ax.text(1.8, 4.5, "PRIVACIÓN LATENTE\n$z_i$ material · educativo\n· monetario", ha="center",
        va="center", fontsize=9, color=INK, zorder=4)
box(1.8, 7.3, 3.0, 1.1, "COFACTORES (Vista D/E)\nruralidad · remesas · demografía\nsectores · fiscal", "#f2fbf7", AQUA)
arrow(1.8, 6.7, 1.8, 5.35, AQUA, 1.8)
ax.text(1.45, 6.0, "composición\n→ privación", ha="right", fontsize=7.2, color=INK2)
# efectos DIRECTOS beta_D,j de los cofactores sobre los indicadores (NO pasan por z):
# infraestructura por dispersión, cohortes, estructura ocupacional, transferencias
arrow(3.35, 7.62, 11.0, 7.85, AQUA, 2.2, rad=-0.14)
ax.text(7.2, 8.62, "efectos DIRECTOS $\\beta_{D,j}$ por indicador — canales que NO son privación:\n"
        "dispersión→costo de red (agua/drenaje) · cohortes viejas→rezago_educ · pensiones→car_segsoc\n"
        "· sector primario→ing_2sm · remesas→lp_ingreso/vivienda", ha="center",
        fontsize=7.2, color=INK2)
# identidad definicional: ruralidad ES loc_peq (el cofactor es uno de los 9 indicadores)
arrow(2.9, 6.72, 10.5, 6.6, "#0e7a52", 1.6, ls="--", rad=0.22)
ax.text(5.4, 5.45, "identidad: ruralidad ≡ loc_peq (mismo dato)", fontsize=7.2,
        color="#0e7a52", ha="center")

# ---- instrumentos ----
box(5.4, 6.6, 2.5, 1.0, "CENSO 2020\ncuestionario básico\n(conteo completo)", "#fff", INK2)
box(5.4, 4.5, 2.5, 1.0, "MUESTRA CENSAL\ncuestionario ampliado\n(municipal)", "#fff", INK2)
box(5.4, 2.4, 2.5, 1.0, "MEC MCS-ENIGH\n(solo nacional/estatal)", "#fff", INK2)
for y in (6.6, 4.5, 2.4):
    arrow(2.95, 4.5 + (y - 4.5) * 0.35, 4.1, y, BLUE, 1.8)

# ---- procesos CONEVAL ----
box(8.3, 3.5, 2.1, 1.0, "12 MODELOS SAE\nlogístico + EBPH\n(grupos de estados)", "#f6f3ff", VIOLET)
box(8.3, 1.6, 2.1, 0.8, "CALIBRACIÓN\na totales estatales", "#f6f3ff", VIOLET)
arrow(6.65, 4.3, 7.2, 3.7, VIOLET, 1.6)          # covariables censales -> SAE
arrow(6.65, 2.4, 7.2, 3.2, VIOLET, 1.6)          # parámetros ENIGH -> SAE
arrow(6.65, 2.2, 7.22, 1.7, VIOLET, 1.2)         # ENIGH -> calibración

# ---- indicadores ----
box(11.9, 6.9, 3.4, 1.5, "9 INDICADORES CONAPO\nanalf · sin_basica · drenaje · electr\nagua · piso · hacinam · loc_peq\n· ing_2sm (muestra)", "#eef4fd", BLUE, fs=8)
box(11.9, 4.6, 3.4, 1.1, "4 CONEVAL DIRECTOS\nrezago_educ · car_salud\ncar_vivienda · car_servbas", "#fdf2e6", YELLOW, fs=8)
box(11.9, 2.6, 3.4, 1.1, "4 CONEVAL MODELADOS\ncar_segsoc · car_alim\nlp_ingreso · lp_ingreso_ext", "#fdeeee", RED, fs=8)
arrow(6.65, 6.75, 10.15, 6.95, BLUE, 1.8)        # censo -> CONAPO
arrow(6.65, 4.75, 10.15, 6.55, BLUE, 1.4, rad=-0.12)  # muestra -> ing_2sm
arrow(6.65, 4.55, 10.15, 4.6, YELLOW, 1.8)       # muestra -> directos
arrow(9.38, 3.4, 10.15, 2.9, RED, 1.8)           # SAE -> modelados
arrow(9.38, 1.62, 10.15, 2.3, RED, 1.4)          # calibración -> modelados

# ---- dependencias mecánicas (rojas numeradas) ----
tag(8.6, 5.9, 1); ax.text(8.6, 5.52, "mismo instrumento →\nbloques de método $m_{ij}$",
                          ha="center", fontsize=7.2, color=INK2)
tag(7.6, 4.05, 2); ax.text(7.55, 4.42, "correlación inducida\n(covariables compartidas)",
                           ha="center", fontsize=7.2, color=INK2)
tag(9.05, 1.15, 3); ax.text(9.15, 0.78, "umbral + calibración estatal → γ_s con doble lectura",
                            ha="center", fontsize=7.2, color=INK2)
tag(8.45, 6.62, 4); ax.text(8.45, 6.28, "ing_2sm: puente\nmuestra ↔ ingreso", ha="center",
                            fontsize=7.2, color=INK2)

# ---- lazo FAIS ----
box(6.4, 0.55, 3.6, 0.75, "FAIS 2016–2020  ←  fórmula art. 34 LCF  ←  pobreza medida 2015",
    "#fdeeee", RED, fs=8)
arrow(11.9, 2.02, 8.25, 0.72, RED, 1.5, ls=":", rad=0.25)
arrow(4.55, 0.62, 1.75, 3.7, RED, 1.5, ls=":", rad=0.25)
tag(3.3, 1.35, 5); ax.text(3.95, 1.06, "circularidad de política:\nel dinero sigue a la medida",
                           ha="center", fontsize=7.2, color=INK2)

ax.text(0.15, 9.35, "El proceso generador de datos como DAG de medición — México 2020",
        fontsize=13, color=INK, fontweight="bold")
ax.text(0.15, 9.02, "flechas sólidas: flujo de medición · punteadas rojas: retroalimentación de política · "
        "círculos rojos: las 5 dependencias mecánicas (reporte_dgp_dag.md)", fontsize=8.5, color=INK2)

fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig_dag_dgp.png"), dpi=160)
print("figures/fig_dag_dgp.png lista")
