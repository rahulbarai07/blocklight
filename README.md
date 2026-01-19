Perfect. Here’s a **clean, professional README** tailored exactly to what **Blocklight v1.1** is today — not overhyped, not vague, and aligned with how you actually built it.

You can copy-paste this directly into `README.md` in your GitHub repo.

---

# Blocklight

**Blocklight** is an intraday crypto market state discovery platform that analyzes how early-session behavior and daily range regimes influence later-session outcomes.

Instead of predicting prices directly, Blocklight focuses on **probability, expected value, and historical context**, helping traders understand *what tends to happen next* given the current market structure.

---

## Core Concept

Blocklight divides a 24-hour trading day into **four 6-hour sessions**:

* **Session 1 (S1)**
* **Session 2 (S2)**
* **Session 3 (S3)**
* **Session 4 (S4)**

For each day, the platform:

* Classifies the **daily range regime** (`Low / Normal / High`)
* Tracks the **direction and return** of each session
* Builds historical probability tables to answer:

  * *Given what happened in S1 & S2, how often is S3 positive?*
  * *Given S1–S3 behavior, what is the expected outcome for S4?*

---

## What Blocklight Shows (v1.1)

### 1. Current Market State

* Latest trading date
* Active daily range regime
* Last completed session
* Intraday path (e.g. `Up → Down → Up`)

### 2. Historical Context Heatmap

* Target session: **Session 3 or Session 4**
* Metrics:

  * **Probability (p_up)**
  * **Expected Value (EV)**
* Heatmap indexed by:

  * Session state (`S1 → S2` or `S1 → S2 → S3`)
  * Range regime (`Low / Normal / High`)

### 3. Research Table (Full Transparency)

A complete probability & expectancy table showing:

* Target session
* Range regime
* Session state
* Probability of upside
* Expected value
* Average win
* Average loss
* Sample size

This table is precomputed offline and displayed read-only in the app.

---

## Architecture Overview

### Offline (Research Layer)

* Raw intraday session data
* Daily outcomes dataset
* Probability & EV tables computed once
* Stored as a Parquet artifact

### Online (Application Layer)

* Streamlit app
* No recomputation of probabilities
* Cached data loading
* Deterministic, reproducible outputs

This separation ensures:

* Fast load times
* Stable results
* Clean research → production workflow

---

## Tech Stack

* **Python**
* **Streamlit**
* **Pandas**
* **Plotly**
* **PyArrow (Parquet storage)**

---

## Project Structure

```
blocklight/
├── app.py
├── requirements.txt
├── data/
│   ├── daily_outcomes.csv
│   ├── real_distribution_sessions.csv
│   └── prob_tables.parquet
└── logic/
    ├── load.py
    ├── current_state.py
    ├── build_prob_tables.py
    ├── s3.py
    └── s4.py
```

---

## How to Run Locally

```bash
git clone https://github.com/rahulbarai07/blocklight.git
cd blocklight
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Live App

The app is deployed on **Streamlit Cloud** and runs directly from the `main` branch.

> Live URL: *(add your Streamlit Cloud link here)*

---

## What Blocklight Is (and Isn’t)

**Blocklight is:**

* A market structure & probability exploration tool
* Designed for discretionary and quantitative traders
* Focused on understanding distributions, not signals

**Blocklight is not:**

* An automated trading system
* A price prediction engine
* Financial advice

---

## Roadmap (High Level)

* Highlight current live state in tables & heatmaps
* Confidence masking based on sample size
* Historical analog day explorer
* Versioned probability tables (v1.2+)
* Expansion to multiple assets

---

## Disclaimer

This project is for **educational and research purposes only**.
All data is historical. No guarantees of future performance are implied.

---

If you want, next we can:

* Tighten this README for public launch
* Add a short “How to read the heatmap” section
* Prepare a v1.2 roadmap doc
* Or write documentation directly inside the app

Just tell me what you want to do next.
