import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Blocklight",
    layout="wide"
)

st.title("Blocklight")
st.caption("Market State Discovery · Historical Context")

@st.cache_data
def load_data():
    return pd.read_parquet("/Users/rahulbarai/Desktop/blocklight Beta/real_distribution_sheet2.csv")

df = load_data()

latest = df.sort_values("timestamp").iloc[-1]

current_date = latest["date"]
current_session = int(latest["session"])
current_regime = latest["range_regime"]

today = df[df["date"] == current_date].sort_values("session")
session_dirs = today[["session", "direction"]].values.tolist()

st.subheader("Current Market State")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Date", str(current_date))

with col2:
    st.metric("Last Completed Session", f"S{current_session}")

with col3:
    st.metric("Range Regime", current_regime)

st.write("Session Path:")
st.write(" → ".join([f"S{s}:{d}" for s, d in session_dirs]))
