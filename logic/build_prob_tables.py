# logic/build_prob_tables.py
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
PARQUET_PATH = DATA_DIR / "prob_tables.parquet"


def build_prob_tables(daily_path=DATA_DIR / "daily_outcomes.csv"):
    """
    OFFLINE ONLY.
    Run manually to rebuild probability tables.
    """
    df = pd.read_csv(daily_path)

    rows = []

    # ---------- S3 ----------
    for _, r in df.iterrows():
        state = f"{r['S1_direction']} → {r['S2_direction']}"
        rows.append({
            "target_session": "S3",
            "range_regime": r["range_regime"],
            "state": state,
            "return": r["S3_pct_change"]
        })

    # ---------- S4 ----------
    for _, r in df.iterrows():
        state = f"{r['S1_direction']} → {r['S2_direction']} → {r['S3_direction']}"
        rows.append({
            "target_session": "S4",
            "range_regime": r["range_regime"],
            "state": state,
            "return": r["S4_pct_change"]
        })

    long_df = pd.DataFrame(rows)

    prob_table = (
        long_df
        .groupby(["target_session", "range_regime", "state"])
        .agg(
            p_up=("return", lambda x: (x > 0).mean()),
            EV=("return", "mean"),
            avg_win=("return", lambda x: x[x > 0].mean()),
            avg_loss=("return", lambda x: x[x < 0].mean()),
            sample_size=("return", "count")
        )
        .reset_index()
    )

    prob_table.to_parquet(PARQUET_PATH, index=False)
    return prob_table


def load_prob_tables():
    """
    ONLINE SAFE.
    Used by Streamlit app.
    """
    return pd.read_parquet(PARQUET_PATH)
