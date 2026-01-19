# logic/s4.py
def compute_s4_table(df):
    pivot = (
        df.pivot(
            index="session_date",
            columns="session",
            values="session_direction"
        )
        .rename(columns={1: "S1", 2: "S2", 3: "S3", 4: "S4"})
        .dropna()
    )

    pivot["S1_S2_S3_state"] = (
        pivot["S1"] + " → " + pivot["S2"] + " → " + pivot["S3"]
    )

    s4_ret = (
        df[df["session"] == 4][["session_date", "session_pct_change"]]
        .rename(columns={"session_pct_change": "S4_return"})
    )

    pivot = pivot.merge(s4_ret, on="session_date")

    regime_df = df[["session_date", "range_regime"]].drop_duplicates()
    pivot = pivot.merge(regime_df, on="session_date")

    table = (
        pivot
        .groupby(["range_regime", "S1_S2_S3_state"])
        .agg(
            p_up=("S4_return", lambda x: (x > 0).mean()),
            EV=("S4_return", "mean"),
            sample_size=("S4_return", "count")
        )
        .reset_index()
    )

    return table

