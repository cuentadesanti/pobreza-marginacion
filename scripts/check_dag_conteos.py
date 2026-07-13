#!/usr/bin/env python
"""
Guarda anti-deriva de conteos del DAG (tarea D2 del handoff).

La verdad son las tablas canónicas dict/dag_nodes.csv y dict/dag_edges.csv.
Este check barre la prosa (paper/*.md, reports/*.md, README.md) buscando
menciones "<n> nodos" / "<n> aristas" que se refieran al DAG completo y falla
si alguna difiere de los CSV. Umbrales: la vista principal tiene ≤25 nodos,
así que solo se auditan menciones con n ≥ 30 (nodos) / n ≥ 60 (aristas).

Se invoca solo (python scripts/check_dag_conteos.py) y desde fig_dag.py al
final de la validación, para que la prosa no pueda volver a desincronizarse
sin que la regeneración del DAG lo grite.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UMBRAL_NODOS, UMBRAL_ARISTAS = 30, 60


def conteos_canonicos():
    n = sum(1 for _ in open(os.path.join(HERE, "dict", "dag_nodes.csv"))) - 1
    e = sum(1 for _ in open(os.path.join(HERE, "dict", "dag_edges.csv"))) - 1
    return n, e


def main():
    n_true, e_true = conteos_canonicos()
    # ESTRATEGIA_AVANCE_Y_MANUSCRITOS.md queda fuera: cita "51 nodos" como
    # ejemplo del bug dentro de la instrucción D2, no como afirmación.
    archivos = (glob.glob(os.path.join(HERE, "paper", "*.md"))
                + glob.glob(os.path.join(HERE, "reports", "*.md"))
                + [os.path.join(HERE, "README.md")])
    errores = []
    for f in archivos:
        if not os.path.exists(f):
            continue
        for i, linea in enumerate(open(f, encoding="utf-8"), 1):
            for m in re.finditer(r"(\d+)\s+nodos", linea):
                v = int(m.group(1))
                if v >= UMBRAL_NODOS and v != n_true:
                    errores.append(f"{os.path.relpath(f, HERE)}:{i} dice {v} nodos (verdad: {n_true})")
            for m in re.finditer(r"(\d+)\s+aristas", linea):
                v = int(m.group(1))
                if v >= UMBRAL_ARISTAS and v != e_true:
                    errores.append(f"{os.path.relpath(f, HERE)}:{i} dice {v} aristas (verdad: {e_true})")
    print(f"conteos canónicos (CSV): {n_true} nodos, {e_true} aristas")
    if errores:
        print("✗ DERIVA DE CONTEOS EN LA PROSA:")
        for e in errores:
            print("  " + e)
        return 1
    print("✓ prosa sincronizada con los CSV (paper/, reports/, README, estrategia)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
