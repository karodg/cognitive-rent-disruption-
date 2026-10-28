"""Data preparation and validation for occupational and county panels.

Loads administrative BLS OEWS and QCEW panels matched to Felten et al. (2021, 2023)
exposure indices, constructs log wage transformations, quantiles, and standardizes variables.
"""

from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


def prepare_occupational_panel() -> pd.DataFrame:
    """Prepares the 2018-2025 BLS OEWS occupational panel."""
    csv_path = DATA_DIR / "oews_ai_occupational_panel.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Occupational panel not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Impute top-coded percentiles ($208,000 threshold in BLS OEWS) and drop missing
    df["a_pct90"] = df["a_pct90"].fillna(208000.0)
    df = df.dropna(subset=["a_mean", "a_median", "a_pct10", "lm_aioe_score"]).copy()

    # Core log wage transformations
    df["ln_mean"] = np.log(df["a_mean"])
    df["ln_p90"] = np.log(df["a_pct90"])
    df["ln_p50"] = np.log(df["a_median"])
    df["ln_p10"] = np.log(df["a_pct10"])

    # Intra-occupational wage spreads
    df["spread_p90_p50"] = df["ln_p90"] - df["ln_p50"]
    df["spread_p50_p10"] = df["ln_p50"] - df["ln_p10"]
    df["spread_p90_p10"] = df["ln_p90"] - df["ln_p10"]

    # Exposure normalization (standardized z-scores)
    df["lme"] = (df["lm_aioe_score"] - df["lm_aioe_score"].mean()) / df["lm_aioe_score"].std()
    df["img_exp"] = (df["img_aioe_score"] - df["img_aioe_score"].mean()) / df["img_aioe_score"].std()
    df["aioe"] = (df["aioe_score"] - df["aioe_score"].mean()) / df["aioe_score"].std()

    # Treatment timing and interaction terms
    df["post_2023"] = (df["year"] >= 2023).astype(int)
    df["post_x_lme"] = df["post_2023"] * df["lme"]
    df["post_x_col"] = df["post_2023"] * df["is_college_plus"]
    df["post_x_lme_x_col"] = df["post_2023"] * df["lme"] * df["is_college_plus"]

    return df


def prepare_county_panel() -> pd.DataFrame:
    """Prepares the 2018-2025 BLS QCEW county-level panel."""
    csv_path = DATA_DIR / "qcew_aige_county_panel.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"County panel not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Filter non-positive earnings and missing exposure
    df = df[df["avg_annual_pay"] > 0].dropna(subset=["avg_annual_pay", "aige_score"]).copy()

    # Wage and exposure transformations
    df["ln_annual_pay"] = np.log(df["avg_annual_pay"])
    df["aige"] = (df["aige_score"] - df["aige_score"].mean()) / df["aige_score"].std()

    # Timing indicators
    df["post_2023"] = (df["year"] >= 2023).astype(int)
    df["post_x_aige"] = df["post_2023"] * df["aige"]

    return df


def main():
    print("[1/2] Loading and verifying occupational panel...")
    df_occ = prepare_occupational_panel()
    print(f"      Occupational panel: {len(df_occ):,} rows, {df_occ['soc_code'].nunique()} SOCs.")

    print("[2/2] Loading and verifying county panel...")
    df_county = prepare_county_panel()
    print(f"      County panel: {len(df_county):,} rows, {df_county['fips'].nunique()} counties.")


if __name__ == "__main__":
    main()
