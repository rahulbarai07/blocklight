# logic/s3.py
def compute_s3_table(df):
    s1 = (
        df[df["session"] == 1][["session_date", "session_direction"]]
        .rename(columns={"session_direction": "S1_dir"})
    )

    s2 = (
        df[df["session"] == 2][["session_date", "session_direction"]]
        .rename(columns={"session_direction": "S2_dir"})
    )

    state_df = s1.merge(s2, on="session_date")
    state_df["S1_S2_state"] = state_df["S1_dir"] + " → " + state_df["S2_dir"]

    regime_df = df[["session_date", "range_regime"]].drop_duplicates()
    state_df = state_df.merge(regime_df, on="session_date")

    s3 = (
        df[df["session"] == 3][
            ["session_date", "session_pct_change", "session_direction"]
        ]
        .rename(columns={
            "session_pct_change": "S3_return",
            "session_direction": "S3_dir"
        })
    )

    analysis_df = state_df.merge(s3, on="session_date")

    table = (
        analysis_df
        .groupby(["range_regime", "S1_S2_state"])
        .agg(
            p_up=("S3_dir", lambda x: (x == "Up").mean()),
            EV=("S3_return", "mean"),
            sample_size=("S3_return", "count")
        )
        .reset_index()
    )

    return table
