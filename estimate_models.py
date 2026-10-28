"""Econometric estimation of TWFE, DDD, and quantile wage regressions.

Replicates Tables 2 through 5:
- Table 2: Occupational wage deceleration & DDD by college requirement
- Table 3: Intra-occupational quantile dispersion (P90/P50 vs P50/P10)
- Table 4: County-level spatial wage convergence (QCEW)
- Table 5: Multi-modal horse-race (Language vs Image vs General AI)
"""

from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

from .data_prep import prepare_occupational_panel, prepare_county_panel


def twfe_cluster_ols(y, X, group_ids, time_ids, cluster_ids):
    """Two-way fixed effects estimator with cluster-robust standard errors.
    
    Absorbs entity and time fixed effects via iterative demeaning, then computes
    OLS coefficients with cluster-robust sandwich covariance matrix.
    """
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X[:, None]

    n, k = X.shape

    # Two-way demeaning
    y_tilde = y.copy()
    X_tilde = X.copy()
    for _ in range(5):
        df_y = pd.DataFrame(y_tilde)
        y_tilde = y_tilde - df_y.groupby(group_ids).transform("mean").values.ravel()
        df_y2 = pd.DataFrame(y_tilde)
        y_tilde = y_tilde - df_y2.groupby(time_ids).transform("mean").values.ravel()

        df_X = pd.DataFrame(X_tilde)
        X_tilde = X_tilde - df_X.groupby(group_ids).transform("mean").values
        df_X2 = pd.DataFrame(X_tilde)
        X_tilde = X_tilde - df_X2.groupby(time_ids).transform("mean").values

    # OLS
    XtX = X_tilde.T @ X_tilde
    XtX_inv = np.linalg.pinv(XtX)
    beta = XtX_inv @ (X_tilde.T @ y_tilde)

    # Residuals
    resid = y_tilde - X_tilde @ beta

    # Clustered covariance
    clusters = np.unique(cluster_ids)
    g = len(clusters)
    u_score = np.zeros((g, k))
    for idx, c in enumerate(clusters):
        mask = (cluster_ids == c)
        u_score[idx, :] = np.sum(X_tilde[mask, :] * resid[mask, None], axis=0)

    meat = u_score.T @ u_score
    df_c = (g / (g - 1)) * ((n - 1) / (n - k))
    vcov = df_c * (XtX_inv @ meat @ XtX_inv)
    se = np.sqrt(np.diag(vcov))
    t_stat = beta / se
    p_val = 2 * (1 - stats.norm.cdf(np.abs(t_stat)))

    return beta, se, t_stat, p_val


def run_table2(df_occ):
    """Table 2: Generative AI Exposure and Occupational Mean Wage Growth."""
    print("\n" + "=" * 76)
    print("TABLE 2: Generative AI Exposure & Occupational Wage Growth (2018-2025)")
    print("=" * 76)

    g_id = df_occ["soc_code"].values
    t_id = df_occ["year"].values
    c_id = df_occ["soc_code"].values

    # Col 1: Baseline TWFE
    X1 = df_occ[["post_x_lme"]].values
    b1, se1, t1, p1 = twfe_cluster_ols(df_occ["ln_mean"].values, X1, g_id, t_id, c_id)
    print(f"Col (1) Post-2023 x LME:           beta = {b1[0]:.4f} (SE: {se1[0]:.4f}, t = {t1[0]:.2f}, p < {max(p1[0], 0.001):.3f})")

    # Col 4: Triple Difference (DDD)
    X4 = df_occ[["post_x_lme", "post_x_col", "post_x_lme_x_col"]].values
    b4, se4, t4, p4 = twfe_cluster_ols(df_occ["ln_mean"].values, X4, g_id, t_id, c_id)
    print(f"Col (4) Post-2023 x LME:           beta = {b4[0]:.4f} (SE: {se4[0]:.4f}, p = {p4[0]:.3f})")
    print(f"        Post-2023 x College:       beta = {b4[1]:.4f} (SE: {se4[1]:.4f}, p = {p4[1]:.3f})")
    print(f"        Post-2023 x LME x College: beta = {b4[2]:.4f} (SE: {se4[2]:.4f}, t = {t4[2]:.2f}, p < {max(p4[2], 0.001):.3f})")


def run_table3(df_occ):
    """Table 3: Intra-Occupational Quantile Dispersion."""
    print("\n" + "=" * 76)
    print("TABLE 3: Cognitive Rent Dissipation: Quantile Dispersion Ratios")
    print("=" * 76)

    sub = df_occ[df_occ["is_college_plus"] == 1].copy()
    g_id = sub["soc_code"].values
    t_id = sub["year"].values
    c_id = sub["soc_code"].values
    X = sub[["post_x_lme"]].values

    # Upper tail: ln(P90/P50)
    b_up, se_up, t_up, p_up = twfe_cluster_ols(sub["spread_p90_p50"].values, X, g_id, t_id, c_id)
    print(f"Upper-Tail [ln(P90/P50)]: beta = {b_up[0]:.4f} (SE: {se_up[0]:.4f}, t = {t_up[0]:.2f}, p < {max(p_up[0], 0.001):.3f})")

    # Lower tail: ln(P50/P10)
    b_dn, se_dn, t_dn, p_dn = twfe_cluster_ols(sub["spread_p50_p10"].values, X, g_id, t_id, c_id)
    print(f"Lower-Tail [ln(P50/P10)]: beta = {b_dn[0]:.4f} (SE: {se_dn[0]:.4f}, t = {t_dn[0]:.2f}, p = {p_dn[0]:.3f})")


def run_table4(df_county):
    """Table 4: County-Level Wage Growth Panel."""
    print("\n" + "=" * 76)
    print("TABLE 4: Regional Wage Growth: U.S. County Panel (2018-2025)")
    print("=" * 76)

    g_id = df_county["fips"].values
    t_id = df_county["year"].values
    c_id = df_county["fips"].values
    X = df_county[["post_x_aige"]].values

    b, se, t, p = twfe_cluster_ols(df_county["ln_annual_pay"].values, X, g_id, t_id, c_id)
    print(f"County Pay Growth: Post-2023 x AIGE: beta = {b[0]:.4f} (SE: {se[0]:.4f}, t = {t[0]:.2f}, p < {max(p[0], 0.001):.3f})")


def run_table5(df_occ):
    """Table 5: Multi-Modal Horse-Race."""
    print("\n" + "=" * 76)
    print("TABLE 5: Multi-Modal Horse-Race (Language vs Image vs General AI)")
    print("=" * 76)

    g_id = df_occ["soc_code"].values
    t_id = df_occ["year"].values
    c_id = df_occ["soc_code"].values

    df_occ["post_x_img"] = df_occ["post_2023"] * df_occ["img_exp"]
    df_occ["post_x_aioe"] = df_occ["post_2023"] * df_occ["aioe"]

    X = df_occ[["post_x_lme", "post_x_img", "post_x_aioe"]].values
    b, se, t, p = twfe_cluster_ols(df_occ["ln_mean"].values, X, g_id, t_id, c_id)

    print(f"Post-2023 x LME:          beta = {b[0]:.4f} (SE: {se[0]:.4f}, p < {max(p[0], 0.001):.3f})")
    print(f"Post-2023 x Image AI:     beta = {b[1]:.4f} (SE: {se[1]:.4f}, p = {p[1]:.3f})")
    print(f"Post-2023 x General AIOE: beta = {b[2]:.4f} (SE: {se[2]:.4f}, p = {p[2]:.3f})")


def main():
    df_occ = prepare_occupational_panel()
    df_county = prepare_county_panel()

    run_table2(df_occ)
    run_table3(df_occ)
    run_table4(df_county)
    run_table5(df_occ)


if __name__ == "__main__":
    main()
