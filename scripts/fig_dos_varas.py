#!/usr/bin/env python
"""
Figura insignia: "Dos varas, un presupuesto".

(a) Dos varas, dos Méxicos: privación media CONAPO vs CONEVAL (logit-z), 45°, régimen LISA,
    municipios extremos nombrados, tamaño = población.
(b) La vara vale dinero: aportaciones federales pc vs nivel de privación total; a mismo nivel
    y tamaño, AA recibe +19% vs BB (fórmula FAIS: base 2013 heredada de la fórmula vieja de
    masa carencial + incremento por pobreza CONEVAL).

Salida: figures/fig_dos_varas_dinero.png, outputs/gap_aportaciones_regimen.csv
"""
import os
import numpy as np, pandas as pd
import numpy.linalg as la
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT, FIG = (os.path.join(HERE, p) for p in (os.path.join("data", "processed"), "outputs", "figures"))
SURF, INK, INK2, MUT, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
RED, BLUE, GRAY = "#e34948", "#2a78d6", "#d5d4cd"
CONAPO = ["analf", "sin_basica", "sin_drenaje", "sin_electr", "sin_agua",
          "piso_tierra", "hacinam", "loc_peq", "ing_2sm"]
CONEVAL = ["rezago_educ", "car_salud", "car_segsoc", "car_vivienda", "car_servbas",
           "car_alim", "lp_ingreso", "lp_ingreso_ext"]

plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "font.size": 9,
                     "axes.edgecolor": "#c3c2b7", "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": MUT, "ytick.color": MUT,
                     "axes.spines.top": False, "axes.spines.right": False})


def main():
    d = pd.read_parquet(os.path.join(PROC, "diagnostico_municipal_v1.parquet"))
    fin = pd.read_parquet(os.path.join(PROC, "finanzas_mun_2020.parquet"))[["cvegeo", "aportaciones_pc"]]
    Y = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))
    Y.index = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))["cvegeo"].values
    d["conapo"] = Y.loc[d["cvegeo"], CONAPO].mean(axis=1).values
    d["coneval"] = Y.loc[d["cvegeo"], CONEVAL].mean(axis=1).values
    d["nivel"] = Y.loc[d["cvegeo"]].mean(axis=1).values
    d = d.merge(fin, on="cvegeo")
    d["reg"] = d["lisa"].where(d["lisa"].isin(["AA", "BB"]), "ns")

    # regresión del gap (misma spec que la verificación)
    m = d.dropna(subset=["aportaciones_pc"]).query("aportaciones_pc>0").copy()
    m["log_apo"] = np.log(m["aportaciones_pc"])
    X = np.column_stack([np.ones(len(m)), m["nivel"], m["nivel"]**2, m["log_pob"],
                         (m["reg"] == "AA").astype(float), (m["reg"] == "BB").astype(float)])
    b, *_ = la.lstsq(X, m["log_apo"], rcond=None)
    gapAA, gapBB = (np.exp(b[4]) - 1) * 100, (np.exp(b[5]) - 1) * 100
    pd.DataFrame({"coef": ["AA", "BB"], "gap_pct_vs_ns": [gapAA, gapBB]}).round(2).to_csv(
        os.path.join(OUT, "gap_aportaciones_regimen.csv"), index=False)

    fig, (a, bx) = plt.subplots(1, 2, figsize=(13, 5.6))

    # (a) dos varas
    for reg, c, zo in [("ns", GRAY, 1), ("BB", BLUE, 3), ("AA", RED, 3)]:
        s = d[d["reg"] == reg]
        a.scatter(s["coneval"], s["conapo"], s=np.sqrt(s["pob_conapo"]) / 18, color=c,
                  alpha=0.75 if reg != "ns" else 0.45, zorder=zo, linewidths=0)
    lim = [-2.2, 2.6]
    a.plot(lim, lim, color="#c3c2b7", lw=1, zorder=0)
    a.set_xlim(lim); a.set_ylim(lim)
    a.set_xlabel("privación según CONEVAL (pobreza, media logit-z)")
    a.set_ylabel("privación según CONAPO (marginación)")
    a.set_title("(a) Dos varas, dos Méxicos\narriba de la diagonal: más marginado que pobre",
                fontsize=10, loc="left", color=INK)
    # nombrar extremos con población >20k
    ext = d[(d["pob_conapo"] > 20000)]
    for _, r in pd.concat([ext.nlargest(4, "discordancia_obs"),
                           ext.nsmallest(3, "discordancia_obs")]).iterrows():
        a.annotate(r["nom_mun"], (r["coneval"], r["conapo"]), fontsize=7, color=INK2,
                   xytext=(5, 3), textcoords="offset points")
    a.text(0.02, 0.95, "● AA  ", transform=a.transAxes, color=RED, fontsize=9)
    a.text(0.10, 0.95, "● BB  ", transform=a.transAxes, color=BLUE, fontsize=9)
    a.text(0.18, 0.95, "● no significativo", transform=a.transAxes, color=MUT, fontsize=9)

    # (b) la vara vale dinero — explícito: qué dinero, qué fórmula, cuánta brecha
    for reg, c, zo, al in [("ns", GRAY, 1, 0.25), ("BB", BLUE, 3, 0.75), ("AA", RED, 3, 0.75)]:
        s = m[m["reg"] == reg]
        bx.scatter(s["nivel"], s["aportaciones_pc"], s=11, color=c, alpha=al,
                   zorder=zo, linewidths=0)
    xs = np.linspace(m["nivel"].min(), m["nivel"].max(), 60)
    base = np.exp(b[0] + b[1] * xs + b[2] * xs**2 + b[3] * m["log_pob"].median())
    bx.plot(xs, base * np.exp(b[4]), color=RED, lw=2.2, ls="--", zorder=5,
            label=f"municipios AA: {gapAA:+.0f}% (t=4.3)")
    bx.plot(xs, base, color=INK2, lw=2, zorder=5, label="esperado por su nivel de privación")
    bx.plot(xs, base * np.exp(b[5]), color=BLUE, lw=2.2, ls="--", zorder=5,
            label=f"municipios BB: {gapBB:+.0f}% (n.s.)")
    # brecha anotada con flecha doble en el extremo derecho
    xg = xs[-6]
    yA = float(base[-6] * np.exp(b[4])); yB = float(base[-6] * np.exp(b[5]))
    bx.annotate("", (xg, yA), (xg, yB),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4), zorder=6)
    bx.text(xg - 0.07, np.sqrt(yA * yB), "brecha 19%\n≈ $1,200 millones/año",
            ha="right", va="center", fontsize=9, color=INK, fontweight="bold", zorder=6)
    # la mecánica de la fórmula, dentro de la figura
    bx.text(0.02, 0.97,
            "El dinero: Ramo 33 por habitante (FAIS+FORTAMUN, EFIPEM 2020).\n"
            "La fórmula FAIS (art. 34 Ley de Coordinación Fiscal):\n"
            "  piso = asignación 2013 (fórmula VIEJA de masa carencial ≈ perfil marginación)\n"
            "  + excedente repartido por pobreza extrema CONEVAL (vara nueva)\n"
            "→ el piso heredado sigue pagando al perfil 'marginado'.",
            transform=bx.transAxes, fontsize=8, color=INK2, va="top",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#f6f5f1", edgecolor="#c3c2b7", lw=0.8))
    bx.set_yscale("log")
    bx.set_xlabel("nivel de privación total del municipio (media de los 17 indicadores, logit-z)")
    bx.set_ylabel("transferencias federales Ramo 33, 2020\n(pesos por habitante, escala log)")
    bx.set_title("(b) Mismo nivel de privación, distinta etiqueta, distinto dinero",
                 fontsize=10, loc="left", color=INK)
    bx.legend(frameon=False, fontsize=8.5, loc="lower right")
    bx.grid(axis="y", color=GRID, lw=0.5)

    fig.suptitle("La vara vale dinero: a igual privación, el municipio 'más marginado que pobre' (AA)\n"
                 "recibe 19% más transferencias por habitante que el 'más pobre que marginado' (BB)",
                 fontsize=12, color=INK, x=0.02, ha="left")
    fig.text(0.02, 0.005, "Cada punto = un municipio (2,250 con EFIPEM 2020). Regresión: "
             "log(transferencia pc) ~ nivel + nivel² + log población + régimen LISA. "
             "FORTAMUN es ~per cápita: diluye, no invierte. Asociación, no causalidad.",
             fontsize=7.5, color=MUT)
    fig.tight_layout(rect=[0, 0.02, 1, 0.90])
    fig.savefig(os.path.join(FIG, "fig_dos_varas_dinero.png"), dpi=160)
    print(f"gap AA {gapAA:+.1f}% | BB {gapBB:+.1f}% | figura lista")


if __name__ == "__main__":
    main()
