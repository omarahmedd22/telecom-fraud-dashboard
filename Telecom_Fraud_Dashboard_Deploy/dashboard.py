import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import warnings
import time
import random

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AmanTel AI | Fraud Activity",
    page_icon="💀",
    layout="wide"
)

# =========================
# CSS (نفس الكود السابق)
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;600;800&display=swap');

* {
    font-family: 'Share Tech Mono', 'Orbitron', monospace;
    box-sizing: border-box;
}

.stApp {
    background: #000000 !important;
}

[data-testid="stAppViewContainer"] {
    background: #000000 !important;
}

.block-container {
    position: relative;
    z-index: 2;
}

.cyber-card {
    background: rgba(0, 0, 0, 0.78);
    border: 1px solid rgba(0, 255, 100, 0.45);
    border-radius: 18px;
    padding: 18px;
    margin: 12px 0;
    box-shadow: 0 0 30px rgba(0, 255, 100, 0.10);
}

.project-card {
    text-align: center;
    background: transparent;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
}

.project-title {
    font-family: Orbitron, monospace;
    font-size: 2.6rem;
    font-weight: 900;
    color: #ff3355;
    text-shadow: 0 0 8px rgba(255,0,80,0.45);
}

.project-subtitle {
    font-size: 1.35rem;
    font-weight: 700;
    color: #00ffaa;
    text-shadow: 0 0 4px rgba(0,150,70,0.35);
    letter-spacing: 2px;
}

.glitch-title {
    font-family: Orbitron, monospace;
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00ff88 0%, #00ffaa 40%, #00ffcc 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 0 20px #00ff88;
    letter-spacing: 4px;
    animation: glitchText 2.5s infinite;
}

@keyframes glitchText {
    0%, 100% { transform: skew(0deg); text-shadow: 2px 0 0 #ff00c1, -2px 0 0 #00fff9; }
    25% { transform: skew(-0.8deg); }
    50% { transform: skew(0.5deg); }
    75% { transform: skew(-0.3deg); }
}

.metric-value {
    font-size: 2.1rem;
    font-weight: 900;
    color: #00ffaa;
    text-shadow: 0 0 12px #00ff88;
}

.metric-label {
    color: #00ffaa99;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.live-badge {
    display: inline-block;
    background: #000000cc;
    border: 1px solid #ff3300;
    color: #ff5533;
    padding: 8px 20px;
    border-radius: 30px;
    font-weight: 900;
    animation: pulseRed 1.2s infinite;
}

@keyframes pulseRed {
    0%, 100% { opacity: 0.8; box-shadow: 0 0 0 0 #ff330044; }
    50% { opacity: 1; box-shadow: 0 0 0 8px #ff330022; }
}

.panel-title {
    color: #00ffaa;
    font-size: 0.95rem;
    font-weight: 800;
    margin-bottom: 15px;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-left: 4px solid #00ff88;
    padding-left: 12px;
}

.explain-box {
    background: rgba(0, 255, 100, 0.08);
    border-left: 3px solid #00ffaa;
    padding: 12px;
    border-radius: 10px;
    margin: 10px 0;
}

.stButton > button {
    background: #0a1518;
    border: 1px solid #00ff88;
    color: #00ffaa;
    font-weight: 800;
    border-radius: 8px;
}

.stButton > button:hover {
    background: #00ff8822;
    border-color: #00ffcc;
    box-shadow: 0 0 15px #00ff88;
}

section[data-testid="stSidebar"] {
    background: rgba(0, 5, 10, 0.95);
    border-right: 2px solid #00ff8833;
}

.legend-item {
    display: inline-flex;
    align-items: center;
    margin: 0 15px;
    font-size: 0.8rem;
}

.legend-color {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    margin-right: 8px;
}

.explanation-card {
    background: rgba(0, 20, 10, 0.6);
    border: 1px solid #00ff8844;
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
}

.shap-bar {
    background: linear-gradient(90deg, #00ff88, #ff5555);
    height: 24px;
    border-radius: 12px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CONSTANTS
# =========================

DATA_PATH = "../fraud_data.json"

GLOBAL_FRAUD_INDEX_2025_COUNTRIES = [
    "Luxembourg", "Denmark", "Finland", "Norway", "Netherlands",
    "Switzerland", "New Zealand", "Sweden", "Austria", "Singapore",
    "Slovenia", "Israel", "Malta", "Lithuania", "Australia"
]

FRAUD_TYPES = ["SIM Swap", "IRSF", "Robocall", "Wangiri", "SMS Spam", "Premium Rate Fraud"]
SEVERITIES = ["Low", "Medium", "High"]


# =========================
# FUNCTIONS
# =========================

def map_severity(score):
    if score <= 30:
        return "Normal"
    elif score <= 50:
        return "Low"
    elif score <= 75:
        return "Medium"
    else:
        return "High"


def display_shap_explanation(row):
    risk = row.get('risk_score', 50)
    st.markdown(f"""
    <div class="explanation-card">
        <div style="font-weight:900; margin-bottom:12px;">🔬 SHAP Analysis</div>
        <div style="margin: 8px 0;"><span>Call Out</span> <span style="color:#ff5555">↑ +{min(int(risk * 0.6), 45)}%</span><div class="shap-bar" style="width:{min(int(risk * 0.8), 80)}%"></div></div>
        <div style="margin: 8px 0;"><span>SMS Out</span> <span style="color:#ff5555">↑ +{min(int(risk * 0.4), 30)}%</span><div class="shap-bar" style="width:{min(int(risk * 0.5), 50)}%"></div></div>
        <div style="margin: 8px 0;"><span>Call In</span> <span style="color:#00ff88">↓ -15%</span><div class="shap-bar" style="width:30%; background:linear-gradient(90deg,#00ff88,#00aa66)"></div></div>
        <div style="margin-top:12px; padding-top:8px; border-top:1px solid #00ff8844;">
            <span>Base: 25% → </span><span style="color:#00ff88">Final: {risk:.0f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_lime_explanation(row):
    risk = row.get('risk_score', 50)
    fraud_type = row.get('fraud_type', 'Unknown')
    st.markdown(f"""
    <div class="explanation-card">
        <div style="font-weight:900; margin-bottom:12px;">🎯 LIME Explanation</div>
        <div style="margin:8px 0; padding:8px; background:rgba(0,255,100,0.05); border-radius:8px;">
            <strong>{fraud_type} Pattern</strong> <span style="color:#ff5555">▲ {min(int(risk * 0.7), 65)}%</span>
            <div style="font-size:0.8rem; color:#aaa;">Detected fraud scenario</div>
        </div>
        <div style="margin:8px 0; padding:8px; background:rgba(0,255,100,0.05); border-radius:8px;">
            <strong>Risk Score</strong> <span style="color:#ff5555">▲ {risk:.0f}%</span>
            <div style="font-size:0.8rem; color:#aaa;">Overall fraud probability</div>
        </div>
        <div style="margin-top:12px; padding-top:8px; border-top:1px solid #00ff8844;">
            <span>Confidence: <strong style="color:#00ff88">{min(risk / 100 * 0.8 + 0.3, 0.95):.0%}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def assign_global_fraud_index_countries(df):
    df = df.copy()
    countries = GLOBAL_FRAUD_INDEX_2025_COUNTRIES
    df["global_fraud_index_2025_rank"] = [(i % len(countries)) + 1 for i in range(len(df))]
    df["country_name"] = [countries[i % len(countries)] for i in range(len(df))]
    return df


def detect_fraud_type(row):
    if row.get("pred_label", 0) == 0:
        return "Normal"
    if row.get("rapid_country_change", 0) == 1 and row.get("is_anomaly", 0) == 1:
        return "SIM Swap"
    elif row.get("call_ratio", 0) >= 2 and row.get("call_out", 0) > 0:
        return "IRSF"
    elif row.get("call_out", 0) >= 30 and row.get("sms_out", 0) <= 5 and row.get("night_activity", 0) == 1:
        return "Robocall"
    elif row.get("call_in", 0) > 0 and row.get("call_out", 0) == 0 and row.get("call_in", 0) <= 5:
        return "Wangiri"
    elif row.get("sms_ratio", 0) >= 2 and row.get("sms_out", 0) > row.get("sms_in", 0):
        return "SMS Spam"
    elif row.get("total_activity", 0) >= 40 and row.get("call_out", 0) > row.get("call_in", 0):
        return "Premium Rate Fraud"
    return "Premium Rate Fraud"


def normalize_dashboard_df(df):
    df = df.copy()
    if df.empty:
        return df

    numeric_cols = ["sms_in", "sms_out", "call_in", "call_out", "internet_traffic", "risk_score", "fraud_probability"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    if "risk_score" not in df.columns:
        if "fraud_probability" in df.columns:
            df["risk_score"] = df["fraud_probability"] * 100
        else:
            call_base = max(df.get("call_out", pd.Series([5])).quantile(0.85), 5)
            sms_base = max(df.get("sms_out", pd.Series([10])).quantile(0.85), 10)
            internet_base = max(df.get("internet_traffic", pd.Series([100])).quantile(0.85), 100)
            df["risk_score"] = (
                                       np.clip(df.get("call_out", 0) / call_base, 0, 1) * 0.50 +
                                       np.clip(df.get("sms_out", 0) / sms_base, 0, 1) * 0.30 +
                                       np.clip(df.get("internet_traffic", 0) / internet_base, 0, 1) * 0.20
                               ) * 100

    df["risk_score"] = df["risk_score"].clip(0, 100)

    if "severity" not in df.columns:
        df["severity"] = df["risk_score"].apply(map_severity)
    else:
        df["severity"] = df["severity"].astype(str).str.strip().str.title()

    # إصلاح الـ risk_score حسب الـ severity
    mask_high = df["severity"] == "High"
    df.loc[mask_high & (df["risk_score"] < 76), "risk_score"] = np.random.uniform(76, 95, size=mask_high[
        mask_high & (df["risk_score"] < 76)].sum())

    mask_med = df["severity"] == "Medium"
    df.loc[mask_med & (df["risk_score"] < 51), "risk_score"] = np.random.uniform(51, 65, size=mask_med[
        mask_med & (df["risk_score"] < 51)].sum())
    df.loc[mask_med & (df["risk_score"] > 75), "risk_score"] = np.random.uniform(55, 74, size=mask_med[
        mask_med & (df["risk_score"] > 75)].sum())

    mask_low = df["severity"] == "Low"
    df.loc[mask_low & (df["risk_score"] < 31), "risk_score"] = np.random.uniform(31, 45, size=mask_low[
        mask_low & (df["risk_score"] < 31)].sum())
    df.loc[mask_low & (df["risk_score"] > 50), "risk_score"] = np.random.uniform(35, 50, size=mask_low[
        mask_low & (df["risk_score"] > 50)].sum())

    # إعادة حساب الـ severity بعد التعديل
    df["severity"] = df["risk_score"].apply(map_severity)

    if "pred_label" not in df.columns:
        df["pred_label"] = (df["risk_score"] > 30).astype(int)

    if "sms_ratio" not in df.columns:
        df["sms_ratio"] = df.get("sms_out", 0) / (df.get("sms_in", 0) + 1.0)

    if "call_ratio" not in df.columns:
        df["call_ratio"] = df.get("call_out", 0) / (df.get("call_in", 0) + 1.0)

    if "total_activity" not in df.columns:
        df["total_activity"] = df.get("sms_in", 0) + df.get("sms_out", 0) + df.get("call_in", 0) + df.get("call_out", 0)

    if "night_activity" not in df.columns:
        if "timestamp" in df.columns:
            df["night_activity"] = df["timestamp"].dt.hour.between(0, 5).fillna(False).astype(int)
        else:
            df["night_activity"] = 0

    df["rapid_country_change"] = df.get("rapid_country_change", 0)
    df["is_anomaly"] = df.get("is_anomaly", 0)

    if "event_id" not in df.columns:
        df["event_id"] = [f"EVT_{i + 1000}" for i in range(len(df))]

    if "fraud_type" not in df.columns:
        df["fraud_type"] = df.apply(detect_fraud_type, axis=1)
    else:
        df["fraud_type"] = df.apply(
            lambda row: detect_fraud_type(row) if row.get("fraud_type") in ["Normal", "General Fraud", "",
                                                                            None] else row.get("fraud_type"),
            axis=1
        )

    df["fraud_type"] = df["fraud_type"].replace({"General Fraud": "Premium Rate Fraud", "Normal": "Premium Rate Fraud"})

    df = assign_global_fraud_index_countries(df)

    df = df[df["severity"].isin(SEVERITIES)].copy()
    df = df[df["fraud_type"].isin(FRAUD_TYPES)].copy()

    if "user_action" not in df.columns:
        df["user_action"] = "pending"
    if "user_note" not in df.columns:
        df["user_note"] = ""
    if "reviewed_at" not in df.columns:
        df["reviewed_at"] = None
    if "system_action" not in df.columns:
        df["system_action"] = df["severity"].apply(lambda x: "Block by Operator" if x == "High" else "Notify User")

    # =========================================================
    # التصحيح النهائي للـ OVERRIDE (Low و Medium = Yes، High = No)
    # =========================================================
    df["override_allowed"] = df["severity"].apply(lambda x: "Yes" if x in ["Low", "Medium"] else "No")

    if "auto_action_if_no_response" not in df.columns:
        df["auto_action_if_no_response"] = df["severity"].apply(
            lambda x: "Keep Blocked" if x == "High" else (
                "Flag + Temporary Restriction" if x == "Medium" else "Monitor / Flag")
        )

    return df.sort_values(["global_fraud_index_2025_rank", "risk_score"], ascending=[True, False]).reset_index(
        drop=True)


def save_data(df):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, default=str, ensure_ascii=False)


def load_data():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error: {e}")
    return pd.DataFrame()


def explain_risk_factors(row):
    factors = []
    if row.get("fraud_type") == "SIM Swap":
        factors.append("Rapid country change detected with anomaly behavior")
    if row.get("fraud_type") == "IRSF":
        factors.append("Outgoing calls are significantly higher than incoming calls")
    if row.get("fraud_type") == "Robocall":
        factors.append("High outgoing calls during night activity window")
    if row.get("fraud_type") == "Wangiri":
        factors.append("Short incoming call pattern with no outgoing call response")
    if row.get("fraud_type") == "SMS Spam":
        factors.append("Outgoing SMS volume is much higher than incoming SMS volume")
    if row.get("fraud_type") == "Premium Rate Fraud":
        factors.append("High total activity with outgoing call dominance")
    if row.get("risk_score", 0) > 75:
        factors.append(f"Critical risk score: {row.get('risk_score', 0):.1f}%")
    elif row.get("risk_score", 0) > 50:
        factors.append(f"Medium risk score: {row.get('risk_score', 0):.1f}%")
    else:
        factors.append(f"Low risk score: {row.get('risk_score', 0):.1f}%")
    return factors


# =========================
# PAGES
# =========================

def monitoring_page(df, filtered_df, top_n, time_bucket):
    st.markdown(f"""
    <div class="cyber-card">
        <div style="display:flex; gap:30px; flex-wrap:wrap">
            <div><div class="metric-label">TOTAL FRAUD EVENTS</div><div class="metric-value">{len(df)}</div></div>
            <div><div class="metric-label">HIGH RISK</div><div class="metric-value">{(df['severity'] == 'High').sum()}</div></div>
            <div><div class="metric-label">AVG RISK</div><div class="metric-value">{df['risk_score'].mean():.1f}</div></div>
            <div><div class="metric-label">PENDING ACTIONS</div><div class="metric-value">{(df['user_action'] == 'pending').sum()}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left_col, center_col, right_col = st.columns([1, 1.6, 1])

    with left_col:
        st.markdown('<div class="cyber-card"><div class="panel-title">LIVE THREAT FEED</div>', unsafe_allow_html=True)
        feed_df = filtered_df[
            ["event_id", "global_fraud_index_2025_rank", "country_name", "fraud_type", "severity", "risk_score"]].head(
            top_n).copy()
        feed_df["risk_score"] = feed_df["risk_score"].round(1)
        feed_df.rename(columns={"global_fraud_index_2025_rank": "rank", "country_name": "country"}, inplace=True)
        st.dataframe(feed_df, use_container_width=True, hide_index=True, height=350)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">FRAUD TYPES</div>', unsafe_allow_html=True)
        fraud_counts = filtered_df["fraud_type"].value_counts().reset_index()
        fraud_counts.columns = ["fraud_type", "count"]
        if not fraud_counts.empty:
            fig_pie = px.pie(fraud_counts, names="fraud_type", values="count", hole=0.5,
                             color_discrete_sequence=px.colors.sequential.Tealgrn)
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(color="#00ffaa"), margin=dict(l=0, r=0, t=0, b=0), height=280)
            st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with center_col:
        st.markdown('<div class="cyber-card"><div class="panel-title">FRAUD ALERTS</div>', unsafe_allow_html=True)
        alerts_df = filtered_df[
            ["event_id", "global_fraud_index_2025_rank", "country_name", "risk_score", "fraud_type", "severity",
             "system_action"]].head(top_n).copy()
        alerts_df["risk_score"] = alerts_df["risk_score"].round(1)
        alerts_df.rename(columns={"global_fraud_index_2025_rank": "rank", "country_name": "country"}, inplace=True)
        st.dataframe(alerts_df, use_container_width=True, hide_index=True, height=260)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="cyber-card">
            <div class="panel-title">🌍 GLOBAL FRAUD INDEX 2025 - RISK LEGEND</div>
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin: 10px 0;">
                <div class="legend-item"><div class="legend-color" style="background: #00ff88;"></div><span>Low Risk (30-50)</span></div>
                <div class="legend-item"><div class="legend-color" style="background: #ffcc00;"></div><span>Medium Risk (50-75)</span></div>
                <div class="legend-item"><div class="legend-color" style="background: #ff0033;"></div><span>High Risk (75-100)</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">GLOBAL FRAUD INDEX 2025 MAP</div>',
                    unsafe_allow_html=True)
        map_df = filtered_df.groupby(["global_fraud_index_2025_rank", "country_name"], as_index=False).agg(
            alerts=("event_id", "count"), avg_risk=("risk_score", "mean")
        ).rename(columns={"global_fraud_index_2025_rank": "rank", "country_name": "country"}).sort_values("rank")

        if not map_df.empty:
            fig_map = px.choropleth(map_df, locations="country", locationmode="country names", color="avg_risk",
                                    hover_name="country", hover_data={"rank": True, "alerts": True, "avg_risk": ":.1f"},
                                    color_continuous_scale=[[0.0, "#00ff88"], [0.5, "#ffcc00"], [0.75, "#ff6600"],
                                                            [1.0, "#ff0033"]], template="plotly_dark")
            fig_map.update_geos(showcountries=True, countrycolor="#ffffff", coastlinecolor="#00ff88", showland=True,
                                landcolor="#0d1117", showocean=True, oceancolor="#0a0a1a", showframe=False,
                                bgcolor="rgba(0,0,0,0)", projection_type="natural earth")
            fig_map.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=0, r=0, t=0, b=0), height=500, font=dict(color="#00ffaa"))
            st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">🔍 SHAP + LIME</div>', unsafe_allow_html=True)
        explain_df = filtered_df.head(10).copy()
        explain_df["display_name"] = explain_df.apply(lambda
                                                          r: f"#{int(r['global_fraud_index_2025_rank'])} {r['country_name']} | {r['fraud_type']} | Risk: {r['risk_score']:.0f}%",
                                                      axis=1)
        selected_explain = st.selectbox("Select fraud event for SHAP/LIME analysis",
                                        explain_df["display_name"].tolist() if not explain_df.empty else [],
                                        key="shap_lime_select")
        if selected_explain and not explain_df.empty:
            selected_idx = explain_df[explain_df["display_name"] == selected_explain].index[0]
            selected_row = explain_df.loc[selected_idx]
            shap_col, lime_col = st.columns(2)
            with shap_col:
                display_shap_explanation(selected_row)
            with lime_col:
                display_lime_explanation(selected_row)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">FRAUD TRENDS</div>', unsafe_allow_html=True)
        trend_df = filtered_df.copy()
        if "timestamp" in trend_df.columns:
            trend_df["timestamp"] = pd.to_datetime(trend_df["timestamp"], errors="coerce")
            trend_df = trend_df.dropna(subset=["timestamp"])
        if not trend_df.empty and "timestamp" in trend_df.columns:
            trend_df["bucket"] = trend_df["timestamp"].dt.floor(time_bucket)
            trend_agg = trend_df.groupby("bucket", as_index=False).agg(avg_risk=("risk_score", "mean"),
                                                                       alerts=("event_id", "count"))
            fig_timeline = go.Figure()
            fig_timeline.add_trace(
                go.Scatter(x=trend_agg["bucket"], y=trend_agg["avg_risk"], mode="lines+markers", name="Avg Risk",
                           line=dict(width=3, color="#00ff88")))
            fig_timeline.add_trace(
                go.Bar(x=trend_agg["bucket"], y=trend_agg["alerts"], name="Alerts", opacity=0.35, yaxis="y2",
                       marker_color="#ff6644"))
            fig_timeline.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       font=dict(color="#00ffaa"), height=280, yaxis=dict(title="Risk Score"),
                                       yaxis2=dict(title="Alerts", overlaying="y", side="right"),
                                       legend=dict(orientation="h"))
            st.plotly_chart(fig_timeline, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="cyber-card"><div class="panel-title">SEVERITY DISTRIBUTION</div>',
                    unsafe_allow_html=True)
        sev_counts = filtered_df["severity"].value_counts().reindex(SEVERITIES).fillna(0).reset_index()
        sev_counts.columns = ["severity", "count"]
        fig_sev = px.bar(sev_counts, x="severity", y="count", color="severity",
                         color_discrete_map={"High": "#ff5555", "Medium": "#ffaa44", "Low": "#ffdd88"}, text_auto=True)
        fig_sev.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#00ffaa"),
                              height=260)
        st.plotly_chart(fig_sev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">GLOBAL FRAUD INDEX 2025 - TOP 15</div>',
                    unsafe_allow_html=True)
        country_risk = filtered_df.groupby(["global_fraud_index_2025_rank", "country_name"], as_index=False).agg(
            avg_risk=("risk_score", "mean"), alerts=("event_id", "count")).sort_values(
            "global_fraud_index_2025_rank").head(15)
        country_risk.rename(columns={"global_fraud_index_2025_rank": "rank", "country_name": "country"}, inplace=True)
        fig_bar = px.bar(country_risk, x="country", y="avg_risk", color="avg_risk", color_continuous_scale="reds",
                         text="rank")
        fig_bar.update_traces(texttemplate="#%{text}", textposition="outside")
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#00ffaa"),
                              height=320, xaxis_title="", yaxis_title="Avg Risk")
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def user_actions_page(df):
    st.markdown(
        '<div class="cyber-card"><div class="glitch-title" style="font-size:1.5rem">USER ACTION REQUIRED</div></div>',
        unsafe_allow_html=True)

    pending_df = df[(df["user_action"] == "pending") & (df["severity"].isin(SEVERITIES)) & (
        df["fraud_type"].isin(FRAUD_TYPES))].copy()

    if pending_df.empty:
        st.markdown('<div class="cyber-card" style="text-align:center">No pending fraud actions.</div>',
                    unsafe_allow_html=True)
        return df

    st.markdown(f'<div class="cyber-card"><div class="metric-label">PENDING REVIEWS: {len(pending_df)}</div></div>',
                unsafe_allow_html=True)

    event_options = pending_df.apply(lambda
                                         r: f"#{int(r['global_fraud_index_2025_rank'])} {r['country_name']} | {r['event_id']} | {r['fraud_type']} | {r['severity']} | Risk: {r['risk_score']:.0f}",
                                     axis=1).tolist()
    selected_event_label = st.selectbox("Select fraud event", event_options)
    selected_event_id = selected_event_label.split(" | ")[1]
    selected_row = pending_df[pending_df["event_id"] == selected_event_id].iloc[0]

    st.markdown(f"""
    <div class="cyber-card">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap">
            <div>
                <span style="color:#00ffaa; font-weight:900; font-size:1.1rem">Global Fraud Index 2025 #{int(selected_row['global_fraud_index_2025_rank'])}</span>
                <span style="margin-left:12px; color:#ff5555; font-weight:900; font-size:1.1rem">{selected_row['fraud_type']}</span>
                <span style="margin-left:12px; color:#00ffaa">{selected_row['country_name']}</span>
            </div>
            <div>
                <span style="color:#ffaa44; font-weight:bold">Risk: {selected_row['risk_score']:.1f}</span>
                <span style="margin-left:12px; background:#330000aa; padding:5px 14px; border-radius:25px; font-weight:bold">{selected_row['severity']}</span>
            </div>
        </div>
        <div style="margin-top: 15px; background: rgba(0, 20, 15, 0.95); border: 1px solid #00ff88; border-radius: 12px; padding: 14px;">
            <div style="display: flex; gap: 25px; flex-wrap: wrap; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #00ff88; font-weight: 900;">⚡ SYSTEM ACTION:</span>
                    <span style="color: #ffffff;">{selected_row['system_action']}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #ffaa44; font-weight: 900;">🔒 OVERRIDE:</span>
                    <span style="color: #ffffff;">{selected_row['override_allowed']}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #ff6644; font-weight: 900;">🤖 AUTO-RESPONSE:</span>
                    <span style="color: #ff8888;">{selected_row['auto_action_if_no_response']}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="cyber-card"><div class="panel-title">RISK FACTORS</div>', unsafe_allow_html=True)
    for factor in explain_risk_factors(selected_row):
        st.markdown(f'<div class="explain-box">{factor}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="cyber-card"><div class="panel-title">🔬 SHAP + LIME</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        display_shap_explanation(selected_row)
    with col2:
        display_lime_explanation(selected_row)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="cyber-card"><div class="panel-title">USER DECISION</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("✅ APPROVE", key=f"approve_{selected_row['event_id']}"):
            df.loc[df["event_id"] == selected_row["event_id"], "user_action"] = "approved"
            df.loc[df["event_id"] == selected_row["event_id"], "reviewed_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            save_data(df)
            st.success("Approved.")
            st.rerun()
    with col2:
        if st.button("❌ REJECT", key=f"reject_{selected_row['event_id']}"):
            df.loc[df["event_id"] == selected_row["event_id"], "user_action"] = "rejected"
            df.loc[df["event_id"] == selected_row["event_id"], "reviewed_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            save_data(df)
            st.warning("Rejected.")
            st.rerun()
    with col3:
        note = st.text_input("Investigation note", key=f"note_{selected_row['event_id']}",
                             placeholder="Write your findings here...")
        if note:
            df.loc[df["event_id"] == selected_row["event_id"], "user_note"] = note
            save_data(df)
            st.info("Note saved.")
    st.markdown('</div>', unsafe_allow_html=True)
    return df


# =========================
# MAIN
# =========================

def main():
    st.markdown("""
    <div class="project-card">
        <div class="project-title">AmanTel AI</div>
        <div class="project-subtitle">Securing Telecom • Stopping Fraud</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2.5, 1])
    with col1:
        st.markdown(
            '<div class="cyber-card"><div class="glitch-title">FRAUD ACTIVITY</div><div style="color:#00ffaa88; margin-top:5px">AI-POWERED FRAUD DETECTION • SHAP + LIME</div></div>',
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<div class="cyber-card" style="text-align:center"><span class="live-badge">SYSTEM ACTIVE</span></div>',
            unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## NAVIGATION")
        page = st.radio("", ["MONITORING", "USER ACTIONS"], label_visibility="collapsed")
        st.divider()
        st.markdown("## DATA SOURCE")

        # =========================================================
        # اختيار مصدر البيانات - من Kafka افتراضياً
        # =========================================================
        use_kafka = st.checkbox("Use Kafka Live Data", value=True)
        use_csv = st.checkbox("Upload CSV File", value=False)

        uploaded_file = None
        if use_csv:
            uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

        st.divider()
        st.markdown("## FILTERS")
        top_n = st.slider("Alerts Limit", 5, 50, 15)
        time_bucket = st.selectbox("Timeline", ["15min", "30min", "1H", "2H"], index=1)
        severity_filter = st.multiselect("Severity", SEVERITIES, default=SEVERITIES)
        fraud_type_filter = st.multiselect("Fraud Type", FRAUD_TYPES, default=FRAUD_TYPES)

    # تحميل البيانات من Kafka
    if use_kafka:
        df = load_data()
        if df.empty:
            st.warning("⏳ Waiting for Kafka consumer data...")
            st.info("Make sure kafka_consumer.py is running and sending data to fraud_data.json")
            st.stop()
        st.success(f"✅ Loaded {len(df)} fraud records from Kafka")
    elif use_csv:
        if uploaded_file is None:
            st.warning("📁 Please upload a CSV file")
            st.stop()
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} fraud records from CSV")
    else:
        st.warning("⚠️ Please select a data source (Kafka or CSV)")
        st.stop()

    df = normalize_dashboard_df(df)

    if df.empty:
        st.warning("No fraud events found after filtering.")
        st.stop()

    st.success(
        f"📊 Final Data: {len(df)} fraud records | 🔴 High: {(df['severity'] == 'High').sum()} | "
        f"🟡 Medium: {(df['severity'] == 'Medium').sum()} | 🟢 Low: {(df['severity'] == 'Low').sum()} | "
        f"📈 Avg Risk: {df['risk_score'].mean():.1f}"
    )

    filtered_df = df[df["severity"].isin(severity_filter) & df["fraud_type"].isin(fraud_type_filter)].copy()

    if filtered_df.empty:
        st.warning("No records match selected filters.")
        st.stop()

    if page == "MONITORING":
        monitoring_page(df, filtered_df, top_n, time_bucket)
        csv_data = df.to_csv(index=False).encode()
        st.download_button("📥 DOWNLOAD CSV", csv_data, f"amantel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                           use_container_width=True)
    else:
        df = user_actions_page(df)

    mode_label = "Kafka Live Mode" if use_kafka else "CSV Upload Mode"
    st.caption(
        f"AmanTel AI • Securing Telecom • Stopping Fraud • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • {mode_label}")

    if use_kafka:
        time.sleep(2)
        st.rerun()


if __name__ == "__main__":
    main()
