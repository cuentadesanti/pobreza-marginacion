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

    # Revisión mayor P1 — Bloque 2.1: Moran residual de los marginalizados (Tabla 1)
    mm = pd.read_csv(os.path.join(OUT, "moran_marginal.csv")).set_index("modelo")
    B += [(P1, "moran marginal M-γ", mm.loc["marginal_rung2", "moran_I_mean"], "{:.3f}"),
          (P1, "moran marginal M+γ", mm.loc["marginal_rung3", "moran_I_mean"], "{:.3f}")]

    # Bloque 2.3: selección formal de K (§4.6)
    sk = pd.read_csv(os.path.join(OUT, "seleccion_k.csv")).set_index("modelo")
    B += [(P1, "K2 delta elpd", sk.loc["K=2", "elpd_diff"], "{:.0f}"),
          (P1, "K2 dse", sk.loc["K=2", "dse"], "{:.0f}"),
          (P1, "K4 delta elpd", sk.loc["K=3", "elpd_diff"], "{:.0f}"),
          (P1, "K4 dse", sk.loc["K=3", "dse"], "{:.0f}"),
          (P1, "K rhat subespacio K2", sk.loc["rhat_subespacio_K2", "elpd_loo"], "{:.3f}"),
          (P1, "K eje4 share", sk.loc["eigen4_share_pct", "elpd_loo"], "{:.1f}"),
          (P1, "K ángulo 1", sk.loc["angulo_principal_1_grados", "elpd_loo"], "{:.1f}"),
          (P1, "K ángulo 2", sk.loc["angulo_principal_2_grados", "elpd_loo"], "{:.1f}"),
          (P1, "K ángulo 3", sk.loc["angulo_principal_3_grados", "elpd_loo"], "{:.1f}"),
          (P1, "K eje4 lp", sk.loc["eje4_carga_lp_ingreso", "elpd_loo"], "{:.2f}"),
          (P1, "K eje4 lp_ext", sk.loc["eje4_carga_lp_ingreso_ext", "elpd_loo"], "{:.2f}"),
          (P1, "K eje4 ing2sm", sk.loc["eje4_carga_ing_2sm", "elpd_loo"], "{:.2f}"),
          (P1, "K eje4 alim", sk.loc["eje4_carga_car_alim", "elpd_loo"], "{:.2f}"),
          (P1, "K eje4 viv", sk.loc["eje4_carga_car_vivienda", "elpd_loo"], "{:.2f}")]

    # Bloque 1: el hecho mecánico de las dos líneas (§5.2)
    cl = pd.read_csv(os.path.join(OUT, "corr_lineas.csv")).set_index("medida")
    B += [(P1, "corr líneas logit-z", cl.loc["corr_logitz_lineas", "valor"], "{:.3f}"),
          (P1, "corr líneas parcial", cl.loc["corr_parcial_dado_resto", "valor"], "{:.3f}")]

    # Bloque 2.2 + 4.2: sensibilidad v_b (apéndice E) e hiperprior sigma_gamma
    vb = pd.read_csv(os.path.join(OUT, "sensibilidad_vb.csv"))
    vb = vb[vb.bloque == "líneas (SAE)"].set_index("escenario")
    B += [(P1, "vb base líneas", vb.loc["base {+pesos originales}", "mload_mean"], "{:.2f}"),
          (P1, "vb educ+20 líneas", vb.loc["educ +20% censal", "mload_mean"], "{:.2f}"),
          (P1, "vb asim 0.8:1", vb.loc["líneas asimétrica 0.8:1", "mload_mean"], "{:.2f}"),
          (P1, "vb asim 1:0.8", vb.loc["líneas asimétrica 1:0.8", "mload_mean"], "{:.2f}"),
          (P1, "vb asim 1:0.8 lo", vb.loc["líneas asimétrica 1:0.8", "mload_lo"], "{:.2f}"),
          (P1, "vb asim 1:0.8 hi", vb.loc["líneas asimétrica 1:0.8", "mload_hi"], "{:.2f}")]
    hy = pd.read_csv(os.path.join(OUT, "hyper_sigma_gamma.csv")).set_index("medida")
    B += [(P1, "hyper sigma_gamma", hy.loc["sigma_gamma_post_media", "valor"], "{:.2f}"),
          (P1, "hyper share PC1", hy.loc["share_PC1_hyper_pct", "valor"], "{:.1f}"),
          (P1, "hyper corr gamma", hy.loc["corr_gamma_hyper_base", "valor"], "{:.3f}"),
          (P1, "hyper rhat", hy.loc["rhat_LamLamT_hyper", "valor"], "{:.2f}")]

    # Nivel 1: capa de error de medición heteroscedástica (§5.3)
    h1 = pd.read_csv(os.path.join(OUT, "nivel1_hetero_resumen.csv")).set_index("métrica")
    B += [(P1, "hetero mload líneas", h1.loc["mload_lineas_sae", "hetero"], "{:.3f}"),
          (P1, "hetero mload líneas homo", h1.loc["mload_lineas_sae", "homo"], "{:.3f}"),
          (P1, "hetero corr logpob eje1 homo", h1.loc["corr_sd_logpob_eje1", "homo"], "{:.2f}"),
          (P1, "hetero corr logpob eje1", h1.loc["corr_sd_logpob_eje1", "hetero"], "{:.2f}"),
          (P1, "hetero corr logpob eje3 homo", h1.loc["corr_sd_logpob_eje3", "homo"], "{:.2f}"),
          (P1, "hetero corr logpob eje3", h1.loc["corr_sd_logpob_eje3", "hetero"], "{:.2f}"),
          (P1, "hetero rhat", h1.loc["rhat_max_monitoreado", "hetero"], "{:.3f}")]

    # Nivel 2: simulación de identificación (apéndice F)
    sim = pd.read_csv(os.path.join(OUT, "sim_identificacion_resumen.csv"))
    simi = sim.set_index(["escenario", "variante"])
    B += [(P1, "sim d_referee libre", simi.loc[("d_referee", "libre"), "lambda_hat"], "{:.3f}"),
          (P1, "sim c_gen3_fit2 λ", simi.loc[("c_gen3_fit2", "libre"), "lambda_hat"], "{:.2f}"),
          (P1, "sim c_gen3_fit2 frob", simi.loc[("c_gen3_fit2", "libre"), "frob"], "{:.2f}"),
          (P1, "sim a_lam03 λ", simi.loc[("a_lam03", "libre"), "lambda_hat"], "{:.3f}"),
          (P1, "sim a_lam06 λ", simi.loc[("a_lam06", "libre"), "lambda_hat"], "{:.3f}")]
    d_lib = sim[(sim.escenario == "d_referee") & (sim.variante == "libre")]

    # Bloque 4.1: IC de Fisher en correlaciones estatales (§7)
    fi = pd.read_csv(os.path.join(OUT, "ic_fisher_estatales.csv")).set_index("correlacion")
    for nombre, key in [("pibe", "PC1_log_pibe_pc"), ("gasto", "PC1_gasto_pibe"),
                        ("salud", "salud_dependencia_sp")]:
        B += [(P1, f"IC fisher {nombre} lo", fi.loc[key, "ci_lo"], "{:.2f}"),
              (P1, f"IC fisher {nombre} hi", fi.loc[key, "ci_hi"], "{:.2f}")]

    th = pd.read_csv(os.path.join(OUT, "desigualdad_theil.csv")).set_index("medida")
    for med, lab in [("z_material_bruto", "material bruto"), ("lp_ingreso_pct", "líneas"),
                     ("analf_pct", "analf"), ("piso_tierra_pct", "piso"),
                     ("sin_agua_pct", "agua"), ("sin_electr_pct", "electricidad"),
                     ("eje1", "eje1"), ("eje2", "eje2"), ("eje3", "eje3")]:
        B.append((P2, f"theil % entre {lab}", th.loc[med, "pct_entre"], "{:.1f}"))
    # F1: los extremos del rango citado en prosa deben ser los del CSV
    ind = pd.read_csv(os.path.join(OUT, "desigualdad_theil.csv"))
    ind = ind[ind.tipo == "theil_indicador"]
    B.append((P2, "theil rango min", ind.pct_entre.min(), "{:.1f}"))
    B.append((P2, "theil rango max", ind.pct_entre.max(), "{:.1f}"))

    # F2: el conteo de combinaciones residuales negativas, computado del CSV
    sm = pd.read_csv(os.path.join(OUT, "satelital_modelos.csv"))
    r3 = sm[sm.outcome == "rung3"]
    B.append((P2, "combinaciones residuales negativas", float((r3.r2cv_media < 0).sum()),
              "{:.0f} de 30"))

    # R2 (revisión v2): solapamiento con solo las dos dimensiones firmes
    s2 = pd.read_csv(os.path.join(OUT, "solapamiento_2dim.csv")).set_index("dimensiones")
    B.append((P2, "obs/esp dos dimensiones firmes", s2.loc["dos_firmes", "razon"], "{:.2f}"))
    B.append((P2, "IC lo dos firmes", s2.loc["dos_firmes", "ic_lo"], "{:.2f}"))
    B.append((P2, "IC hi dos firmes", s2.loc["dos_firmes", "ic_hi"], "{:.2f}"))

    # F3: monopolio vs competencia desde su CSV (ventana principal + variantes ap. D)
    mc = pd.read_csv(os.path.join(OUT, "g_monopolio_competencia.csv")).set_index(
        ["ventana", "var"])
    for vent in ["reciente_1518", "calderon_0611", "w2018"]:
        for var in ["monopolio_N1", "competencia_N2plus"]:
            B.append((P2, f"{var} {vent}", mc.loc[(vent, var), "beta"], "{:.3f}"))

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

    # Tarea B — descomposición piso/incremento del FISM (§7.3, Figuras 5 y 6)
    bf = pd.read_csv(os.path.join(OUT, "b_fism_descomposicion.csv"))
    res = bf[bf.spec == "resumen"].set_index("term")["coef"]
    t_inc_BB = bf[(bf.spec == "niveles_inc_pc") & (bf.term == "BB")]["t"].iloc[0]
    t_sub_AA = bf[(bf.spec == "log_aportaciones_efipem_submuestra")
                  & (bf.term == "AA")]["t"].iloc[0]
    B += [(P2, "B piso share fondo", res["share_piso_fondo_oficial_pct"], "{:.1f}"),
          (P2, "B ic dif efipem lo", res["brecha_AABB_efipem_full_pct_ci_lo"], "{:.1f}"),
          (P2, "B ic dif efipem hi", res["brecha_AABB_efipem_full_pct_ci_hi"], "{:.1f}"),
          (P2, "B n intersección", res["n_interseccion"], "{:.0f}"),
          (P2, "B cobertura modelo", res["cobertura_modelo_pct"], "{:.1f}"),
          (P2, "B brecha submuestra AA", res["ols_efipem_submuestra_AA_pct"], "{:.1f}"),
          (P2, "B t submuestra AA", t_sub_AA, "{:.1f}"),
          (P2, "B brecha piso", res["ols_brecha_AABB_piso"], "{:.0f}"),
          (P2, "B brecha incremento", res["ols_brecha_AABB_inc"], "{:.0f}"),
          (P2, "B ic dif brecha lo", res["dif_brecha_piso_menos_inc_ci_lo"], "{:.0f}"),
          (P2, "B ic dif brecha hi", res["dif_brecha_piso_menos_inc_ci_hi"], "{:.0f}"),
          (P2, "B piso BB pct", res["ols_piso_BB_pct"], "{:.1f}"),
          (P2, "B piso BB ci lo", 100 * (np.exp(res["log_piso_BB_ci_lo"]) - 1), "{:.1f}"),
          (P2, "B piso BB ci hi", 100 * (np.exp(res["log_piso_BB_ci_hi"]) - 1), "{:.1f}"),
          (P2, "B incremento BB pc", res["ols_inc_BB_pc"], "{:.0f}"),
          (P2, "B t incremento BB", t_inc_BB, "{:.1f}"),
          (P2, "B deflactor INPC", res["deflactor_inpc_2013_2020"], "{:.3f}"),
          (P2, "B n spec extendida", res["n_spec_extendida"], "{:.0f}")]
    cob = pd.read_csv(os.path.join(OUT, "b_fism_cobertura.csv")).set_index("variable")
    B += [(P2, "B SMD población", cob.loc["log_pob", "smd"], "{:.2f}"),
          (P2, "B SMD ruralidad", cob.loc["loc_peq_pct", "smd"], "{:.2f}"),
          (P2, "B SMD privación", cob.loc["nivel", "smd"], "{:.2f}")]
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
