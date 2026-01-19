# logic/current_state.py
def get_current_state_from_sessions(df):
    latest_date = df["session_date"].max()
    today_df = df[df["session_date"] == latest_date].sort_values("session")

    completed_dirs = today_df["session_direction"].tolist()
    last_session = f"S{int(today_df['session'].iloc[-1])}"
    range_regime = today_df["range_regime"].iloc[0]

    return {
        "date": latest_date,
        "range_regime": range_regime,
        "completed_dirs": completed_dirs,
        "last_session": last_session
    }


def build_state_string(directions):
    return " → ".join(directions)


def infer_target_session(last_session):
    if last_session in ["S1", "S2"]:
        return "S3"
    elif last_session == "S3":
        return "S4"
    else:
        return None
