# logic/load.py
import pandas as pd

def load_sessions(path="data/real_distribution_sessions.csv"):
    df = pd.read_csv(path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["session_date"] = pd.to_datetime(df["session_date"])

    # standardize text
    df["session_direction"] = (
        df["session_direction"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    return df
