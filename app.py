
# app.py
import streamlit as st
import plotly.express as px

from logic.load import load_sessions
from logic.s3 import compute_s3_table
from logic.s4 import compute_s4_table
from logic.build_prob_tables import load_prob_tables

st.set_page_config(layout="wide")
st.title("Blocklight")
st.caption("Intraday Market State & Historical Context")

# ===================== CACHED LOADERS =====================
@st.cache_data
def get_sessions():
    return load_sessions()

@st.cache_data
def get_prob_tables():
    return load_prob_tables()

df = get_sessions()
prob_df = get_prob_tables()

# ===================== CURRENT STATE =====================
latest_date = df["session_date"].max()
today = df[df["session_date"] == latest_date].sort_values("session")

st.subheader("Current Market State")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Date", latest_date.strftime("%Y-%m-%d"))
c2.metric("Range Regime", today["range_regime"].iloc[0])
c3.metric("Last Session", f"S{today['session'].max()}")
c4.metric("Path", " → ".join(today["session_direction"].values))

st.divider()

# ===================== ANALYSIS =====================
target = st.radio("Target Session", ["Session 3", "Session 4"], horizontal=True)

if target == "Session 3":
    table = compute_s3_table(df)
    index_col = "S1_S2_state"
else:
    table = compute_s4_table(df)
    index_col = "S1_S2_S3_state"

metric = st.radio("Metric", ["Probability", "Expected Value"], horizontal=True)
value_col = "p_up" if metric == "Probability" else "EV"

matrix = table.pivot(
    index=index_col,
    columns="range_regime",
    values=value_col
)

fig = px.imshow(
    matrix,
    text_auto=".2f",
    color_continuous_scale="RdYlGn",
    labels=dict(color=value_col)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================== RESEARCH TABLE =====================
st.subheader("Probability & Expectancy Table")

display_cols = [
    "target_session",
    "range_regime",
    "state",
    "p_up",
    "EV",
    "avg_win",
    "avg_loss",
    "sample_size"
]

st.dataframe(
    prob_df[display_cols]
        .sort_values(["target_session", "range_regime", "state"]),
    use_container_width=True
)

