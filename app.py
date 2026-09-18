"""
Mental Health in Tech — Streamlit EDA Dashboard
Run locally:  streamlit run app.py
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mental Health in Tech — EDA Dashboard",
    page_icon="🧠",
    layout="wide",
)

PRIMARY = "#3d5a80"
ACCENT = "#e07a5f"
PALETTE = ["#3d5a80", "#e07a5f", "#81b29a", "#f2cc8f", "#98c1d9", "#ee6c4d"]


# ----------------------------------------------------------------------------
# Data loading & cleaning (cached)
# ----------------------------------------------------------------------------
@st.cache_data
   def load_data(path: str = "survey.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # Clean Age: clip implausible values to NaN
    df.loc[(df["Age"] < 18) | (df["Age"] > 75), "Age"] = np.nan

    # Normalize Gender into 3 buckets
    def normalize_gender(g):
        g = str(g).strip().lower()
        male_terms = {"male", "m", "man", "cis male", "cis man", "make", "malr", "maile",
                      "mal", "male (cis)", "male-ish", "msle", "mail", "guy (-ish) ^_^",
                      "male leaning androgynous", "ostensibly male, unsure what that really means"}
        female_terms = {"female", "f", "woman", "cis female", "cis-female/femme", "femake",
                         "femail", "female (cis)", "female (trans)", "trans woman", "trans-female"}
        if g in male_terms:
            return "Male"
        if g in female_terms:
            return "Female"
        return "Other/Non-binary"

    df["Gender_clean"] = df["Gender"].apply(normalize_gender)
    return df


df_raw = load_data()

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
st.sidebar.title("🧠 Filters")
st.sidebar.caption("OSMI Mental Health in Tech Survey")

genders = st.sidebar.multiselect(
    "Gender",
    options=sorted(df_raw["Gender_clean"].unique()),
    default=sorted(df_raw["Gender_clean"].unique()),
)

top_countries_all = df_raw["Country"].value_counts().index.tolist()
countries = st.sidebar.multiselect(
    "Country (top 15 shown, empty = all)",
    options=top_countries_all,
    default=[],
)

age_min, age_max = int(df_raw["Age"].min(skipna=True)), int(df_raw["Age"].max(skipna=True))
age_range = st.sidebar.slider("Age range", min_value=age_min, max_value=age_max,
                               value=(age_min, age_max))

treatment_filter = st.sidebar.radio(
    "Sought treatment?",
    options=["All", "Yes", "No"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit + Plotly")

# ----------------------------------------------------------------------------
# Apply filters
# ----------------------------------------------------------------------------
df = df_raw[df_raw["Gender_clean"].isin(genders)]
if countries:
    df = df[df["Country"].isin(countries)]
df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1]) | df["Age"].isna()]
if treatment_filter != "All":
    df = df[df["treatment"] == treatment_filter]

# ----------------------------------------------------------------------------
# Header + KPIs
# ----------------------------------------------------------------------------
st.title("🧠 Mental Health in Tech — Survey Dashboard")
st.caption(
    "Interactive exploration of the OSMI Mental Health in Tech Survey "
    f"({len(df_raw):,} responses, filtered to {len(df):,})."
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Respondents (filtered)", f"{len(df):,}")
k2.metric("Median Age", f"{df['Age'].median():.0f}" if len(df) else "—")
k3.metric(
    "Sought Treatment",
    f"{(df['treatment'] == 'Yes').mean() * 100:.1f}%" if len(df) else "—",
)
k4.metric(
    "Family History",
    f"{(df['family_history'] == 'Yes').mean() * 100:.1f}%" if len(df) else "—",
)

st.markdown("---")

if len(df) == 0:
    st.warning("No rows match the current filters. Try widening your selection in the sidebar.")
    st.stop()

# ----------------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------------
tab_overview, tab_demo, tab_workplace, tab_treatment, tab_data = st.tabs(
    ["📊 Overview", "👥 Demographics", "🏢 Workplace", "💊 Treatment Analysis", "🗂️ Raw Data"]
)

# ---- Overview tab -----------------------------------------------------------
with tab_overview:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Age Distribution")
        fig = px.histogram(df, x="Age", nbins=30, color_discrete_sequence=[PRIMARY])
        fig.add_vline(x=df["Age"].median(), line_dash="dash", line_color=ACCENT,
                      annotation_text=f"Median: {df['Age'].median():.0f}")
        fig.update_layout(bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Treatment-Seeking")
        counts = df["treatment"].value_counts()
        fig = px.pie(values=counts.values, names=counts.index, hole=0.45,
                     color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Gender Breakdown")
        counts = df["Gender_clean"].value_counts()
        fig = px.bar(x=counts.values, y=counts.index, orientation="h",
                     color=counts.index, color_discrete_sequence=PALETTE,
                     labels={"x": "Count", "y": ""})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.subheader("Top 10 Countries")
        counts = df["Country"].value_counts().head(10)
        fig = px.bar(x=counts.values, y=counts.index, orientation="h",
                     color_discrete_sequence=[PRIMARY],
                     labels={"x": "Count", "y": ""})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

# ---- Demographics tab -------------------------------------------------------
with tab_demo:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Age by Gender")
        fig = px.box(df, x="Gender_clean", y="Age", color="Gender_clean",
                     color_discrete_sequence=PALETTE, points="outliers")
        fig.update_layout(showlegend=False, xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Gender vs Treatment-Seeking (%)")
        ct = pd.crosstab(df["Gender_clean"], df["treatment"], normalize="index") * 100
        fig = px.bar(ct, barmode="stack", color_discrete_sequence=[PRIMARY, ACCENT],
                     labels={"value": "% of Group", "Gender_clean": ""})
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Age Distribution by Country (Top 8)")
    top8 = df["Country"].value_counts().head(8).index
    fig = px.violin(df[df["Country"].isin(top8)], x="Country", y="Age",
                     color="Country", box=True, color_discrete_sequence=PALETTE * 2)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---- Workplace tab ----------------------------------------------------------
with tab_workplace:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Company Size")
        order_size = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
        counts = df["no_employees"].value_counts().reindex(order_size).dropna()
        fig = px.bar(x=counts.index, y=counts.values, color_discrete_sequence=[PRIMARY],
                     labels={"x": "", "y": "Count"})
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Remote Work")
        counts = df["remote_work"].value_counts()
        fig = px.pie(values=counts.values, names=counts.index, hole=0.45,
                     color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Workplace Support Indicators")
    support_cols = ["benefits", "care_options", "wellness_program", "seek_help", "anonymity"]
    chosen = st.multiselect("Choose indicators to compare", support_cols, default=support_cols)

    if chosen:
        melted = df[chosen].melt(var_name="Indicator", value_name="Response")
        fig = px.histogram(melted, x="Indicator", color="Response", barmode="group",
                            color_discrete_sequence=PALETTE)
        fig.update_layout(xaxis_title="", legend_title="Response")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Comfort Discussing Mental Health")
    c3, c4 = st.columns(2)
    with c3:
        counts = df["coworkers"].value_counts()
        fig = px.pie(values=counts.values, names=counts.index, title="With Coworkers",
                     color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        counts = df["supervisor"].value_counts()
        fig = px.pie(values=counts.values, names=counts.index, title="With Supervisor",
                     color_discrete_sequence=PALETTE)
        st.plotly_chart(fig, use_container_width=True)

# ---- Treatment analysis tab --------------------------------------------------
with tab_treatment:
    st.subheader("Work Interference vs Treatment-Seeking")
    order_wi = ["Never", "Rarely", "Sometimes", "Often"]
    ct = pd.crosstab(df["work_interfere"], df["treatment"]).reindex(order_wi).dropna(how="all")
    fig = px.bar(ct, barmode="group", color_discrete_sequence=[PRIMARY, ACCENT],
                 labels={"value": "Count", "work_interfere": ""})
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Family History vs Treatment")
        ct = pd.crosstab(df["family_history"], df["treatment"])
        fig = px.bar(ct, barmode="group", color_discrete_sequence=[PRIMARY, ACCENT],
                     labels={"value": "Count", "family_history": ""})
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Perceived Consequence: Mental vs Physical")
        mh = df["mental_health_consequence"].value_counts()
        ph = df["phys_health_consequence"].value_counts()
        cats = mh.index.tolist()
        fig = go.Figure()
        fig.add_bar(name="Mental Health", x=cats, y=[mh.get(c, 0) for c in cats], marker_color=PRIMARY)
        fig.add_bar(name="Physical Health", x=cats, y=[ph.get(c, 0) for c in cats], marker_color=ACCENT)
        fig.update_layout(barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Correlation Heatmap")
    st.caption("Label-encoded categorical variables — values near ±1 indicate stronger association.")
    from sklearn.preprocessing import LabelEncoder
    corr_cols = ["treatment", "family_history", "work_interfere", "benefits", "care_options",
                 "wellness_program", "seek_help", "anonymity", "mental_health_consequence",
                 "phys_health_consequence", "coworkers", "supervisor", "obs_consequence", "remote_work"]
    df_enc = df[corr_cols].copy()
    for c in corr_cols:
        df_enc[c] = LabelEncoder().fit_transform(df_enc[c].astype(str))
    corr = df_enc.corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                     aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

# ---- Raw data tab -------------------------------------------------------------
with tab_data:
    st.subheader("Filtered Data")
    st.dataframe(df, use_container_width=True, height=500)
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="survey_filtered.csv",
        mime="text/csv",
    )
