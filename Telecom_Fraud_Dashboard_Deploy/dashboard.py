import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import warnings
import time

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="FRAUD ACTIVITY | AMANTEL",
    page_icon="💀",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;600;800&display=swap');

* {
    font-family: 'Share Tech Mono', 'Orbitron', monospace;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    background: #000000 !important;
}

[data-testid="stAppViewContainer"] {
    background: #000000 !important;
    position: relative;
}

/* شبكة اختراق */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        linear-gradient(rgba(0, 255, 100, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 100, 0.1) 1px, transparent 1px);
    background-size: 35px 35px;
    pointer-events: none;
    z-index: 0;
}

/* بقع نيون */
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 30%, rgba(0, 255, 100, 0.12) 0%, transparent 45%),
        radial-gradient(circle at 85% 70%, rgba(0, 255, 200, 0.08) 0%, transparent 45%),
        radial-gradient(circle at 50% 20%, rgba(0, 255, 100, 0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

.block-container {
    position: relative;
    z-index: 2;
    background: transparent !important;
}

/* عنوان glitch */
.glitch-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00ff88 0%, #00ffaa 40%, #00ffcc 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff8844;
    letter-spacing: 4px;
    animation: glitchText 2.5s infinite;
}

@keyframes glitchText {
    0%, 100% { transform: skew(0deg); text-shadow: 2px 0 0 #ff00c1, -2px 0 0 #00fff9; }
    20% { transform: skew(-0.8deg); text-shadow: -2px 0 0 #ff00c1, 2px 0 0 #00fff9; }
    40% { transform: skew(0.5deg); text-shadow: 1px 0 0 #ff00c1, -1px 0 0 #00fff9; }
    60% { transform: skew(-0.3deg); text-shadow: -1px 0 0 #ff00c1, 2px 0 0 #00fff9; }
    80% { transform: skew(0.2deg); text-shadow: 1px 0 0 #ff00c1, -2px 0 0 #00fff9; }
}

.cyber-card {
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 255, 100, 0.4);
    border-radius: 16px;
    padding: 18px;
    margin: 10px 0;
    box-shadow: 0 0 30px rgba(0, 255, 100, 0.08);
    transition: 0.25s ease;
    position: relative;
    z-index: 2;
}

.cyber-card:hover {
    border-color: #00ff88;
    box-shadow: 0 0 40px rgba(0, 255, 100, 0.2);
    transform: translateY(-3px);
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 900;
    color: #00ffaa;
    text-shadow: 0 0 12px #00ff88;
    letter-spacing: 2px;
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
    font-size: 0.85rem;
    letter-spacing: 2px;
    animation: pulseRed 1.2s infinite;
}

@keyframes pulseRed {
    0%, 100% { opacity: 0.8; box-shadow: 0 0 0 0 #ff330044; }
    50% { opacity: 1; box-shadow: 0 0 0 8px #ff330022; }
}

.risk-high {
    background: #220000cc;
    border: 1px solid #ff0000;
    color: #ff5555;
    padding: 5px 14px;
    border-radius: 25px;
    font-weight: bold;
    animation: blinkRed 1s infinite;
}

@keyframes blinkRed {
    0%, 100% { opacity: 0.9; }
    50% { opacity: 1; background: #ff000030; }
}

.status-approved {
    background: #003300cc;
    border: 1px solid #00ff00;
    color: #00ff88;
    padding: 4px 12px;
    border-radius: 20px;
}

.status-rejected {
    background: #330000cc;
    border: 1px solid #ff0000;
    color: #ff5555;
    padding: 4px 12px;
    border-radius: 20px;
}

.status-pending {
    background: #332200cc;
    border: 1px solid #ffaa00;
    color: #ffaa44;
    padding: 4px 12px;
    border-radius: 20px;
    animation: pulseYellow 1.5s infinite;
}

@keyframes pulseYellow {
    0%, 100% { opacity: 0.8; }
    50% { opacity: 1; background: #ffaa0030; }
}

section[data-testid="stSidebar"] {
    background: rgba(0, 5, 10, 0.95);
    border-right: 2px solid #00ff8833;
    backdrop-filter: blur(8px);
}

.stButton > button {
    background: #0a1518;
    border: 1px solid #00ff88;
    color: #00ffaa;
    font-weight: 800;
    letter-spacing: 1px;
    transition: 0.2s;
    border-radius: 8px;
}
.stButton > button:hover {
    background: #00ff8822;
    border-color: #00ffcc;
    box-shadow: 0 0 15px #00ff88;
    transform: scale(1.02);
}

div[data-testid="stDataFrame"] {
    border: 1px solid #00ff8844;
    border-radius: 12px;
    background: rgba(0, 0, 0, 0.5);
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

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0a0f0f;
}
::-webkit-scrollbar-thumb {
    background: #00ff88;
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

COUNTRY_MAP_FULL = {
    'EG': "Egypt", 'SA': "Saudi Arabia", 'AE': "UAE", 'QA': "Qatar", 'BH': "Bahrain",
    'KW': "Kuwait", 'OM': "Oman", 'JO': "Jordan", 'LB': "Lebanon", 'IQ': "Iraq",
    'YE': "Yemen", 'MA': "Morocco", 'TN': "Tunisia", 'DZ': "Algeria", 'LY': "Libya",
    'IN': "India", 'RU': "Russia", 'US': "United States", 'GB': "United Kingdom",
    'DE': "Germany", 'FR': "France", 'IT': "Italy", 'ES': "Spain", 'CN': "China",
    'KR': "South Korea", 'JP': "Japan", 'TR': "Turkey", 'PK': "Pakistan", 'LK': "Sri Lanka",
    'SG': "Singapore", 'MY': "Malaysia", 'PH': "Philippines", 'ZA': "South Africa",
    'NG': "Nigeria", 'KE': "Kenya", 'MX': "Mexico", 'BR': "Brazil", 'AR': "Argentina",
    'CL': "Chile", 'CA': "Canada", 'AU': "Australia", 'ID': "Indonesia", 'TH': "Thailand",
    'VN': "Vietnam", 'PL': "Poland", 'NL': "Netherlands", 'BE': "Belgium", 'CH': "Switzerland"
}


def severity_from_score(score):
    if score <= 30:
        return "Normal"
    if score <= 50:
        return "Low"
    if score <= 75:
        return "Medium"
    return "High"


def get_fraud_type(row):
    if row["risk_score"] < 40:
        return "Normal"
    if row["call_out"] > row["call_in"] * 3 and row["call_out"] > 5:
        return "IRSF"
    if row["sms_out"] > row["sms_in"] * 3 and row["sms_out"] > 10:
        return "SMS Spam"
    if row["risk_score"] > 70:
        return "Premium Rate Fraud"
    if row["call_in"] > 0 and row["call_out"] == 0:
        return "Wangiri Fraud"
    return "General Fraud"


def calculate_risk_adaptive(df):
    df = df.copy()
    call_threshold = max(df["call_out"].quantile(0.85), 5)
    sms_threshold = max(df["sms_out"].quantile(0.85), 10)
    internet_threshold = max(df["internet_traffic"].quantile(0.85), 100)

    df["call_risk"] = np.clip(df["call_out"] / call_threshold, 0, 1)
    df["sms_risk"] = np.clip(df["sms_out"] / sms_threshold, 0, 1)
    df["internet_risk"] = np.clip(df["internet_traffic"] / internet_threshold, 0, 1)

    df["risk_score"] = (df["call_risk"] * 0.50 + df["sms_risk"] * 0.30 + df["internet_risk"] * 0.20) * 100

    unusual_call = (df["call_out"] > df["call_in"] * 2) & (df["call_out"] > 3)
    unusual_sms = (df["sms_out"] > df["sms_in"] * 2) & (df["sms_out"] > 5)

    df["risk_score"] = np.where(unusual_call, df["risk_score"] * 1.3, df["risk_score"])
    df["risk_score"] = np.where(unusual_sms, df["risk_score"] * 1.2, df["risk_score"])
    df["risk_score"] = np.clip(df["risk_score"], 0, 100)

    df["severity"] = df["risk_score"].apply(severity_from_score)
    df["pred_label"] = (df["risk_score"] >= 40).astype(int)

    if "event_id" not in df.columns:
        df["event_id"] = [f"EVT_{i + 1000}" for i in range(len(df))]
    if "phone_number" not in df.columns:
        df["phone_number"] = [f"+20{100000000 + i}" for i in range(len(df))]

    if "country_name" not in df.columns:
        df["country_name"] = df["country_code"].astype(str).str.upper().map(COUNTRY_MAP_FULL).fillna(df["country_code"].astype(str))

    df["fraud_type"] = df.apply(get_fraud_type, axis=1)

    if "user_action" not in df.columns:
        df["user_action"] = "pending"
    if "user_note" not in df.columns:
        df["user_note"] = ""
    if "reviewed_at" not in df.columns:
        df["reviewed_at"] = None

    df["system_action"] = df["severity"].apply(
        lambda x: "Allow" if x == "Normal" else ("Block by Operator" if x == "High" else "Notify User"))
    df["override_allowed"] = df["severity"].apply(lambda x: "No" if x == "Normal" else "Yes")
    df["user_decision_required"] = df["severity"].apply(lambda x: "No" if x == "Normal" else "Yes")
    df["auto_action_if_no_response"] = df["severity"].apply(
        lambda x: "None" if x == "Normal" else ("Keep Blocked" if x == "High" else ("Flag + Temporary Restriction" if x == "Medium" else "Monitor / Flag"))
    )

    return df.sort_values("risk_score", ascending=False).reset_index(drop=True)


def save_data(df):
    with open("../fraud_data.json", "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, default=str)


def load_data():
    if os.path.exists("../fraud_data.json"):
        try:
            with open("../fraud_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error reading fraud_data.json: {e}")
    return pd.DataFrame()


def normalize_dashboard_df(df):
    df = df.copy()

    if df.empty:
        return df

    # numeric safety
    for col in ["sms_in", "sms_out", "call_in", "call_out", "internet_traffic", "risk_score", "fraud_probability"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "pred_label" in df.columns:
        df["pred_label"] = pd.to_numeric(df["pred_label"], errors="coerce").fillna(0).astype(int)
    else:
        df["pred_label"] = 0

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    if "severity" not in df.columns:
        if "risk_score" in df.columns:
            df["severity"] = df["risk_score"].apply(severity_from_score)
        else:
            df["severity"] = "Normal"

    df["severity"] = df["severity"].astype(str).str.strip().str.title()

    if "country_name" not in df.columns:
        if "country_code" in df.columns:
            df["country_name"] = df["country_code"].astype(str).str.upper().map(COUNTRY_MAP_FULL).fillna(df["country_code"].astype(str))
        else:
            df["country_name"] = "Unknown"

    if "event_id" not in df.columns:
        df["event_id"] = [f"EVT_{i + 1000}" for i in range(len(df))]
    if "phone_number" not in df.columns:
        df["phone_number"] = [f"+20{100000000 + i}" for i in range(len(df))]
    if "fraud_type" not in df.columns:
        df["fraud_type"] = df.apply(get_fraud_type, axis=1)

    if "user_action" not in df.columns:
        df["user_action"] = "pending"
    if "user_note" not in df.columns:
        df["user_note"] = ""
    if "reviewed_at" not in df.columns:
        df["reviewed_at"] = None
    if "system_action" not in df.columns:
        df["system_action"] = "Notify User"
    if "override_allowed" not in df.columns:
        df["override_allowed"] = "Yes"
    if "user_decision_required" not in df.columns:
        df["user_decision_required"] = "Yes"
    if "auto_action_if_no_response" not in df.columns:
        df["auto_action_if_no_response"] = "Monitor / Flag"

    return df


def explain_risk_factors(row):
    factors = []
    if row.get("call_out", 0) > 10:
        factors.append(f"📞 High outgoing calls: {row['call_out']} calls")
    if row.get("call_out", 0) > row.get("call_in", 0) * 2:
        factors.append(f"📊 Call ratio imbalance: {row['call_out']:.0f} out vs {row['call_in']:.0f} in")
    if row.get("sms_out", 0) > 15:
        factors.append(f"💬 High SMS volume: {row['sms_out']} messages")
    if row.get("internet_traffic", 0) > 500:
        factors.append(f"🌐 Abnormal data usage: {row['internet_traffic']:.0f} MB")
    if row.get("risk_score", 0) > 70:
        factors.append(f"⚠️ Risk score: {row['risk_score']:.0f}% (Critical)")
    elif row.get("risk_score", 0) > 40:
        factors.append(f"⚠️ Risk score: {row['risk_score']:.0f}% (Elevated)")
    return factors


def generate_lime_explanation(row):
    explanations = []
    if row.get("call_out", 0) > row.get("call_in", 0) * 2:
        explanations.append("Outgoing calls significantly exceed incoming calls")
    if row.get("call_out", 0) > 10:
        explanations.append("High volume of outgoing calls detected")
    if row.get("risk_score", 0) > 70:
        explanations.append("**VERDICT:** High-risk fraud pattern - Immediate action required")
    elif row.get("risk_score", 0) > 40:
        explanations.append("**VERDICT:** Medium-risk anomaly - User verification needed")
    else:
        explanations.append("**VERDICT:** Normal behavior pattern")
    return explanations

def monitoring_page(df, filtered_df, top_n, time_bucket):
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-label">⚡ TOTAL EVENTS</div><div class="metric-value">{len(df)}</div>',
                    unsafe_allow_html=True)
    with col2:
        fraud_count = (df["pred_label"] == 1).sum()
        st.markdown(f'<div class="metric-label">🚨 FRAUD ALERTS</div><div class="metric-value">{fraud_count}</div>',
                    unsafe_allow_html=True)
    with col3:
        st.markdown(
            f'<div class="metric-label">🎯 AVG RISK</div><div class="metric-value">{df["risk_score"].mean():.1f}</div>',
            unsafe_allow_html=True)
    with col4:
        pending_count = (df["user_action"] == "pending").sum()
        st.markdown(
            f'<div class="metric-label">⏳ PENDING</div><div class="metric-value" style="color:#ffaa44">{pending_count}</div>',
            unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    left_col, center_col, right_col = st.columns([1, 1.6, 1])

    with left_col:
        st.markdown('<div class="cyber-card"><div class="panel-title">📡 LIVE THREAT FEED</div>', unsafe_allow_html=True)
        feed_df = filtered_df[["event_id", "phone_number", "country_name", "fraud_type", "risk_score"]].head(top_n).copy()
        feed_df["risk_score"] = feed_df["risk_score"].round(1)
        feed_df.rename(columns={"country_name": "country"}, inplace=True)
        st.dataframe(feed_df, use_container_width=True, hide_index=True, height=350)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">🎯 FRAUD SCENARIOS</div>', unsafe_allow_html=True)
        fraud_counts = filtered_df[filtered_df["fraud_type"] != "Normal"]["fraud_type"].value_counts().reset_index()
        fraud_counts.columns = ["fraud_type", "count"]
        if fraud_counts.empty:
            fraud_counts = pd.DataFrame({"fraud_type": ["Normal"], "count": [1]})
        fig_pie = px.pie(fraud_counts, names="fraud_type", values="count", hole=0.5,
                         color_discrete_sequence=px.colors.sequential.Tealgrn)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#00ffaa"), margin=dict(l=0, r=0, t=0, b=0), height=280)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with center_col:
        st.markdown('<div class="cyber-card"><div class="panel-title">🚨 FRAUD ALERTS</div>', unsafe_allow_html=True)
        alerts_df = filtered_df[["event_id", "phone_number", "country_name", "risk_score", "fraud_type", "severity"]].head(top_n).copy()
        alerts_df["risk_score"] = alerts_df["risk_score"].round(1)
        alerts_df.rename(columns={"country_name": "country"}, inplace=True)
        st.dataframe(alerts_df, use_container_width=True, hide_index=True, height=250)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">🌍 GLOBAL THREAT INTELLIGENCE MAP</div>',
                    unsafe_allow_html=True)

        map_df = filtered_df.groupby("country_name", as_index=False).agg(
            alerts=("pred_label", "sum"),
            avg_risk=("risk_score", "mean"),
            total=("event_id", "count")
        ).dropna(subset=["country_name"]).rename(columns={"country_name": "country"})

        if not map_df.empty:
            fig_map = px.choropleth(
                map_df,
                locations="country",
                locationmode="country names",
                color="avg_risk",
                hover_name="country",
                hover_data={"alerts": True, "avg_risk": ':.1f', "total": True},
                color_continuous_scale=[
                    [0.0, "#00ff88"],
                    [0.25, "#aaff00"],
                    [0.5, "#ffcc00"],
                    [0.75, "#ff6600"],
                    [1.0, "#ff0033"]
                ],
                template="plotly_dark"
            )

            fig_map.update_geos(
                showcountries=True,
                countrycolor="#ffffff",
                coastlinecolor="#00ff88",
                coastlinewidth=1.2,
                showland=True,
                landcolor="#0d1117",
                showocean=True,
                oceancolor="#0a0a1a",
                showcoastlines=True,
                showframe=False,
                bgcolor="rgba(0,0,0,0)",
                projection_type="natural earth",
                projection_scale=1.1
            )

            fig_map.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=0, b=0),
                height=500,
                font=dict(color="#00ffaa", family="Share Tech Mono", size=12),
                coloraxis_colorbar=dict(
                    title="RISK SCORE",
                    title_font=dict(color="#00ffaa", size=14),
                    tickfont=dict(color="#00ffaa", size=11),
                    thickness=15,
                    len=0.65,
                    bgcolor="rgba(0,0,0,0.6)",
                    bordercolor="#00ff88",
                    borderwidth=2
                ),
            )
            fig_map.update_traces(marker_line_width=0.8, marker_line_color="#00ff88")
            st.plotly_chart(fig_map, use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("🌍 COUNTRIES", len(map_df))
            with c2:
                st.metric("🚨 TOTAL ALERTS", int(map_df["alerts"].sum()))
            with c3:
                st.metric("📊 AVG RISK", f"{map_df['avg_risk'].mean():.1f}")
            with c4:
                high_risk = len(map_df[map_df["avg_risk"] > 50])
                st.metric("⚠️ HIGH RISK", high_risk)
        else:
            st.warning("⚠️ No map data available - check your country codes")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">📈 FRAUD TRENDS</div>', unsafe_allow_html=True)
        trend_df = filtered_df.copy()
        trend_df["timestamp"] = pd.to_datetime(trend_df["timestamp"], errors="coerce")
        trend_df = trend_df.dropna(subset=["timestamp"])

        if not trend_df.empty:
            trend_df["bucket"] = trend_df["timestamp"].dt.floor(time_bucket)
            trend_agg = trend_df.groupby("bucket", as_index=False).agg(
                avg_risk=("risk_score", "mean"),
                alerts=("pred_label", "sum")
            )

            fig_timeline = go.Figure()
            fig_timeline.add_trace(
                go.Scatter(
                    x=trend_agg["bucket"],
                    y=trend_agg["avg_risk"],
                    mode="lines+markers",
                    name="Avg Risk",
                    line=dict(width=3, color="#00ff88"),
                    marker=dict(size=8, color="#00ff88")
                )
            )
            fig_timeline.add_trace(
                go.Bar(
                    x=trend_agg["bucket"],
                    y=trend_agg["alerts"],
                    name="Alerts",
                    opacity=0.35,
                    yaxis="y2",
                    marker_color="#ff6644"
                )
            )
            fig_timeline.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#00ffaa", family="Share Tech Mono"),
                margin=dict(l=10, r=10, t=10, b=10),
                height=280,
                yaxis=dict(title="Risk Score", gridcolor="rgba(0,255,136,0.15)"),
                yaxis2=dict(title="Alerts", overlaying="y", side="right", showgrid=False),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No valid timestamps available for trend chart.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="cyber-card"><div class="panel-title">🌍 TOP RISK COUNTRIES</div>',
                    unsafe_allow_html=True)
        country_risk = filtered_df.groupby("country_name")["risk_score"].mean().sort_values(ascending=False).head(8).reset_index()
        country_risk.rename(columns={"country_name": "country"}, inplace=True)
        fig_bar = px.bar(
            country_risk,
            x="country",
            y="risk_score",
            color="risk_score",
            color_continuous_scale="reds",
            text_auto=".0f"
        )
        fig_bar.update_traces(textposition="outside", textfont=dict(color="#00ffaa", size=11))
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#00ffaa", family="Share Tech Mono"),
            height=320,
            xaxis_title="",
            yaxis_title="Risk Score",
            xaxis=dict(gridcolor="rgba(0,255,136,0.1)", tickangle=-15),
            yaxis=dict(gridcolor="rgba(0,255,136,0.1)")
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cyber-card"><div class="panel-title">⚠️ SEVERITY DISTRIBUTION</div>',
                    unsafe_allow_html=True)
        sev_counts = filtered_df["severity"].value_counts().reset_index()
        sev_counts.columns = ["severity", "count"]
        fig_sev = px.bar(
            sev_counts,
            x="severity",
            y="count",
            color="severity",
            color_discrete_map={"High": "#ff5555", "Medium": "#ffaa44", "Low": "#ffdd88", "Normal": "#44ff88"},
            text_auto=True
        )
        fig_sev.update_traces(textposition="outside", textfont=dict(color="#00ffaa", size=12))
        fig_sev.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#00ffaa", family="Share Tech Mono"),
            height=250,
            xaxis_title="",
            yaxis_title="Count",
            xaxis=dict(gridcolor="rgba(0,255,136,0.1)"),
            yaxis=dict(gridcolor="rgba(0,255,136,0.1)")
        )
        st.plotly_chart(fig_sev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def user_actions_page(df):
    st.markdown(
        '<div class="cyber-card"><div class="glitch-title" style="font-size:1.5rem">👤 USER ACTION REQUIRED</div></div>',
        unsafe_allow_html=True)

    pending_df = df[df["user_decision_required"] == "Yes"].copy()
    pending_df = pending_df[pending_df["user_action"] == "pending"].copy()

    if len(pending_df) == 0:
        st.markdown(
            '<div class="cyber-card" style="text-align:center">✅ No pending actions! All fraud alerts have been reviewed.</div>',
            unsafe_allow_html=True)
        return df

    st.markdown(f'<div class="cyber-card"><div class="metric-label">⏳ PENDING REVIEWS: {len(pending_df)}</div></div>',
                unsafe_allow_html=True)

    event_options = pending_df.apply(
        lambda r: f"{r['event_id']} | {r['fraud_type'][:35]} | Risk: {r['risk_score']:.0f}", axis=1).tolist()
    selected_event_label = st.selectbox("🔎 Select event to analyze", event_options)
    selected_event_id = selected_event_label.split(" | ")[0]
    selected_row = pending_df[pending_df["event_id"] == selected_event_id].iloc[0]

    st.markdown(f"""
    <div class="cyber-card">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap">
            <div>
                <span class="risk-high">🚨 {selected_row['fraud_type']}</span>
                <span style="margin-left:12px">📞 {selected_row['phone_number']}</span>
                <span style="margin-left:12px">📍 {selected_row['country_name']}</span>
            </div>
            <div>
                <span style="color:#ffaa44; font-weight:bold">Risk: {selected_row['risk_score']:.0f}</span>
                <span style="margin-left:12px; background:#330000aa; padding:5px 14px; border-radius:25px; font-weight:bold">{selected_row['severity']}</span>
            </div>
        </div>
        <div style="margin-top:12px; background:rgba(0,255,100,0.05); padding:10px; border-radius:10px">
            <small>⚡ System Action: {selected_row['system_action']} | Override: {selected_row['override_allowed']} | Auto-response: {selected_row['auto_action_if_no_response']}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="cyber-card"><div class="panel-title">🔬 SHAP ANALYSIS - Risk Factors</div>',
                unsafe_allow_html=True)
    risk_factors = explain_risk_factors(selected_row)
    if risk_factors:
        for factor in risk_factors:
            st.markdown(f'<div class="explain-box">📊 {factor}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="explain-box">✅ No significant risk factors detected. Activity appears normal.</div>',
                    unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.4); padding:12px; border-radius:10px; margin-top:12px">
        <small style="color:#88aabb">
        📞 Call Out: <span style="color:#00ffaa">{selected_row['call_out']}</span> | 
        📞 Call In: <span style="color:#00ffaa">{selected_row['call_in']}</span> |
        💬 SMS Out: <span style="color:#00ffaa">{selected_row['sms_out']}</span> | 
        📨 SMS In: <span style="color:#00ffaa">{selected_row['sms_in']}</span> |
        🌐 Data: <span style="color:#00ffaa">{selected_row['internet_traffic']:.1f} MB</span>
        </small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="cyber-card"><div class="panel-title">🔍 LIME ANALYSIS - Local Explanation</div>',
                unsafe_allow_html=True)
    lime_explanations = generate_lime_explanation(selected_row)
    for exp in lime_explanations:
        if "VERDICT" in exp:
            st.markdown(f'<div class="explain-box" style="border-left-color:#ff5555">⚖️ {exp}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="explain-box">🔹 {exp}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="cyber-card"><div class="panel-title">✍️ YOUR DECISION</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button(f"✓ APPROVE", key=f"approve_{selected_row['event_id']}"):
            df.loc[df["event_id"] == selected_row["event_id"], "user_action"] = "approved"
            df.loc[df["event_id"] == selected_row["event_id"], "reviewed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(df)
            st.success("✅ Approved! Refreshing...")
            st.rerun()
    with col2:
        if st.button(f"✗ REJECT", key=f"reject_{selected_row['event_id']}"):
            df.loc[df["event_id"] == selected_row["event_id"], "user_action"] = "rejected"
            df.loc[df["event_id"] == selected_row["event_id"], "reviewed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(df)
            st.warning("❌ Rejected! Refreshing...")
            st.rerun()
    with col3:
        note = st.text_input("📝 Investigation note (optional)", key=f"note_{selected_row['event_id']}",
                             placeholder="Write your findings here...")
        if note:
            df.loc[df["event_id"] == selected_row["event_id"], "user_note"] = note
            save_data(df)
            st.info("📌 Note saved")
    st.markdown('</div>', unsafe_allow_html=True)

    return df

def main():
    col1, col2 = st.columns([2.5, 1])
    with col1:
        st.markdown(
            '<div class="cyber-card"><div class="glitch-title">💀 FRAUD ACTIVITY 💀</div><div style="color:#00ffaa88; margin-top:5px">⚡ AI-POWERED FRAUD DETECTION SYSTEM ⚡</div></div>',
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<div class="cyber-card" style="text-align:center"><span class="live-badge">🔴 SYSTEM ACTIVE</span></div>',
            unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## 🔓 NAVIGATION")
        page = st.radio("", ["📊 MONITORING", "👤 USER ACTIONS"], label_visibility="collapsed")

        st.divider()
        st.markdown("## 📁 DATA SOURCE")
        use_streaming = st.checkbox("Use live streaming data", value=True)

        uploaded_file = None
        if not use_streaming:
            uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

        st.divider()
        st.markdown("## ⚙️ SETTINGS")
        top_n = st.slider("Alerts Limit", 5, 50, 15)
        time_bucket = st.selectbox("Timeline", ["15min", "30min", "1H", "2H"], index=1)
        severity_filter = st.multiselect(
            "Severity",
            ["High", "Medium", "Low", "Normal"],
            default=["High", "Medium", "Low"]
        )

    required_cols = [
        "square_id", "timestamp", "country_code",
        "sms_in", "sms_out", "call_in", "call_out", "internet_traffic"
    ]

    if use_streaming:
        df = load_data()

        if df.empty:
            st.warning("⚠️ Waiting for streaming data from kafka_consumer.py ...")
            st.info("Run first: python kafka_consumer.py")
            st.stop()
    else:
        if uploaded_file is None:
            st.warning("⚠️ Please upload a CSV file or enable live streaming mode.")
            st.markdown("""
            **Required columns:**
            - square_id, timestamp, country_code
            - sms_in, sms_out, call_in, call_out, internet_traffic
            """)
            st.stop()

        df = pd.read_csv(uploaded_file)
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            st.error(f"❌ Missing columns: {missing_cols}")
            st.stop()

        df = calculate_risk_adaptive(df)
        save_data(df)

    df = normalize_dashboard_df(df)

    st.success(
        f"✅ Loaded {len(df)} records | Fraud Alerts: {(df['pred_label'] == 1).sum()} | Avg Risk: {df['risk_score'].mean():.1f}"
    )

    filtered_df = df[df["severity"].isin(severity_filter)].copy()
    if filtered_df.empty:
        filtered_df = df.head(1).copy()

    if page == "📊 MONITORING":
        monitoring_page(df, filtered_df, top_n, time_bucket)

        st.markdown('<div class="cyber-card"><div class="panel-title">💾 EXPORT RESULTS</div>', unsafe_allow_html=True)
        csv_data = df.to_csv(index=False).encode()
        st.download_button(
            "⬇️ DOWNLOAD CSV",
            csv_data,
            f"fraud_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        df = user_actions_page(df)

    st.caption(f"⚡ FRAUD ACTIVITY • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • SYSTEM ONLINE ⚡")

    if use_streaming:
        time.sleep(1)
        st.rerun()


if __name__ == "__main__":
    main()