#!/usr/bin/env python
"""
Figura de las dos escalas (pulido editorial §3): barras apiladas entre/dentro de estados.

Dos paneles con funcionales DISTINTOS y no comparables entre sí (corrección 4a):
  (a) indicadores observados — descomposición aditiva de Theil (tipo=theil_indicador)
  (b) factor bruto y ejes condicionales — descomposición de varianza (var_eje*)
Fuente: outputs/desigualdad_theil.csv (existente; cero cómputo nuevo).

Salida: figures/09_desigualdad/fig_theil_escalas.png
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

import plotstyle as ps
ps.use()
FIG = ps.figdir("09_desigualdad")
HERE = ps.REPO

NOMBRES = {"analf_pct": "analfabetismo", "sin_basica_pct": "sin educación básica",
           "sin_drenaje_pct": "sin drenaje", "sin_electr_pct": "sin electricidad",
           "sin_agua_pct": "sin agua entubada", "piso_tierra_pct": "piso de tierra",
           "hacinam_pct": "hacinamiento", "loc_peq_pct": "localidades pequeñas",
           "ing_2sm_pct": "ingreso ≤ 2 SM", "rezago_educ_pct": "rezago educativo",
           "car_salud_pct": "carencia salud", "car_segsoc_pct": "carencia seg. social",
           "car_vivienda_pct": "carencia vivienda", "car_servbas_pct": "carencia serv. básicos",
           "car_alim_pct": "carencia alimentación", "lp_ingreso_pct": "línea de pobreza",
           "lp_ingreso_ext_pct": "línea de pobreza extrema",
           "z_material_bruto": "factor material (sin condicionar)",
           "eje1": "dimensión material (residual)", "eje2": "dimensión educativa (residual)",
           "eje3": "dim. vivienda-ingreso vs redes (residual)"}
AZUL, ARENA = ps.C[0], "#d9d4c5"


def barras(ax, df, titulo, xlabel):
    df = df.sort_values("pct_entre")
    y = range(len(df))
    ax.barh(y, df.pct_entre, color=AZUL, label="entre estados")
    ax.barh(y, 100 - df.pct_entre, left=df.pct_entre, color=ARENA, label="dentro de estados")
    ax.set_yticks(list(y), [NOMBRES.get(m, m) for m in df.medida], fontsize=8.2)
    for yi, v in zip(y, df.pct_entre):
        ax.text(v + 1.2, yi, f"{v:.1f}", va="center", fontsize=7.4, color=ps.INK2)
    ax.axvline(50, color=ps.INK2, lw=0.7, ls=":")
    ax.set_xlim(0, 100)
    ax.set_xlabel(xlabel, fontsize=8.5)
    ax.set_title(titulo, fontsize=9.5, loc="left", color=ps.INK)
    ax.spines[["top", "right"]].set_visible(False)


def main():
    th = pd.read_csv(os.path.join(HERE, "outputs", "desigualdad_theil.csv"))
    ind = th[th.tipo == "theil_indicador"]
    ejes = th[th.tipo.isin(["var_eje_canonico", "var_eje"])]
    fig, (a, b) = plt.subplots(1, 2, figsize=(11.8, 5.4), facecolor=ps.SURF,
                               gridspec_kw={"width_ratios": [1.45, 1]})
    barras(a, ind, "(a) Desigualdad observada (indicadores publicados)",
           "fracción del índice de Theil atribuible a diferencias entre estados (%)")
    barras(b, ejes, "(b) Heterogeneidad residual",
           "fracción de la varianza atribuible a diferencias entre estados (%)")
    b.legend(frameon=False, fontsize=8, loc="lower right")
    fig.suptitle("Buena parte de la desigualdad observada coincide con fronteras estatales;\n"
                 "la heterogeneidad residual vive dentro de los estados (métodos distintos por panel; niveles no comparables entre paneles)",
                 fontsize=10.5, color=ps.INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(os.path.join(FIG, "fig_theil_escalas.png"), dpi=150)
    print("figures/09_desigualdad/fig_theil_escalas.png")


if __name__ == "__main__":
    main()
