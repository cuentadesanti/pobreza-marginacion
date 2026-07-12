"""
Estilo compartido de TODAS las figuras del repo (homogeneización 2026-07-12).

Uso en cada script:
    import plotstyle as ps
    ps.use()                              # rcParams comunes
    FIG = ps.figdir("07_satelital")       # crea figures/<capitulo>/ y devuelve la ruta

Paleta de referencia validada (modo claro): categóricos en orden fijo; divergente azul-rojo
con neutro gris; secuencial azul. No inventar hex nuevos en los scripts: importar de aquí.
"""
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# superficies y tinta
SURF, PAGE = "#fcfcfb", "#f9f9f7"
INK, INK2, MUT = "#0b0b0b", "#52514e", "#898781"
GRID, BASE = "#e1e0d9", "#c3c2b7"
# categóricos (orden fijo, nunca ciclar)
C = ["#2a78d6", "#1baf7a", "#eda100", "#008300", "#4a3aa7", "#e34948", "#e87ba4", "#eb6834"]
BLUE, AQUA, YELLOW, GREEN, VIOLET, RED = C[:6]
GRAY = "#d5d4cd"
# mapas
DIV = LinearSegmentedColormap.from_list("div", ["#104281", "#3987e5", "#f0efec", "#e34948", "#8f1f1f"])
SEQ = LinearSegmentedColormap.from_list("seq", ["#cde2fb", "#3987e5", "#0d366b"])


def use():
    matplotlib.use("Agg", force=False)
    plt.rcParams.update({
        "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
        "font.family": "sans-serif", "font.size": 9,
        "axes.edgecolor": BASE, "axes.labelcolor": INK2, "text.color": INK,
        "xtick.color": MUT, "ytick.color": MUT,
        "grid.color": GRID, "grid.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False,
        "figure.dpi": 100, "savefig.dpi": 160,
    })


def figdir(capitulo):
    p = os.path.join(REPO, "figures", capitulo)
    os.makedirs(p, exist_ok=True)
    return p
