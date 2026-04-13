"""
FinRaksha AI — Bank Customer Churn Analysis Dashboard
Author : A. Reddy Prakash | Founder, FinRaksha AI
Run    : streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib, json, os

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bank Churn Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    h1 { font-size: 1.8rem !important; font-weight: 700 !important; }
    h2 { font-size: 1.3rem !important; font-weight: 600 !important; }
    .metric-card {
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        border: 1px solid #e0e4f0;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .metric-value { font-size: 2rem; font-weight: 700; }
    .metric-label { font-size: 0.78rem; color: #666; text-transform: uppercase;
                    letter-spacing: 0.05em; margin-top: 4px; }
    .metric-sub   { font-size: 0.75rem; color: #999; margin-top: 2px; }
    .danger  { color: #E53935; }
    .warning { color: #F57C00; }
    .success { color: #2E7D32; }
    .info    { color: #1565C0; }
    .purple  { color: #6A1B9A; }
    .insight-box {
        background: #EFF6FF; border-left: 4px solid #1565C0;
        border-radius: 0 8px 8px 0; padding: 12px 16px;
        margin: 8px 0; font-size: 0.88rem; color: #1a1a2e;
    }
    .stSelectbox label, .stMultiSelect label { font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    if os.path.exists("European_Bank.csv"):
        df = pd.read_csv("European_Bank.csv")
    else:
        # Generate synthetic demo data if CSV not present
        np.random.seed(42)
        n = 10000
        geo = np.random.choice(['France','Germany','Spain'],
                               n, p=[0.50, 0.25, 0.25])
        age = np.random.normal(38, 12, n).clip(18, 92).astype(int)
        balance = np.random.choice(
            [0, np.random.uniform(10000,200000)], n,
            p=[0.35, 0.65]).astype(float)
        balance = np.where(balance == 0, 0,
                           np.random.uniform(10000, 200000, n))
        tenure  = np.random.randint(0, 11, n)
        products= np.random.choice([1,2,3,4], n, p=[0.46,0.46,0.05,0.03])
        active  = np.random.randint(0, 2, n)
        gender  = np.random.choice(['Male','Female'], n)
        credit  = np.random.randint(350, 850, n)
        salary  = np.random.uniform(10000, 200000, n)
        # Churn probability driven by features
        churn_prob = (
            0.10
            + 0.15 * (geo == 'Germany')
            + 0.06 * (age > 45)
            + 0.08 * (active == 0)
            + 0.10 * (products >= 3)
            + 0.04 * (balance > 100000)
        )
        exited = (np.random.rand(n) < churn_prob).astype(int)
        df = pd.DataFrame({
            'RowNumber': range(1, n+1), 'CustomerId': range(15600000, 15600000+n),
            'Surname': ['Customer']*n, 'CreditScore': credit,
            'Geography': geo, 'Gender': gender, 'Age': age, 'Tenure': tenure,
            'Balance': balance, 'NumOfProducts': products,
            'HasCrCard': np.random.randint(0,2,n),
            'IsActiveMember': active, 'EstimatedSalary': salary, 'Exited': exited
        })
    # Feature engineering
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0,30,40,50,60,100],
                            labels=['<30','30-40','40-50','50-60','60+'])
    df['BalanceTier'] = pd.cut(df['Balance'],
                               bins=[-1,0,50000,100000,300000],
                               labels=['Zero','Low','Mid','High'])
    return df

df = load_data()

# ── SIDEBAR FILTERS ───────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/48/bank-building.png", width=48)
    st.title("🔍 Filters")
    st.caption("Churn Analytics")
    st.divider()

    geo_sel = st.multiselect("🌍 Geography",
                             df['Geography'].unique().tolist(),
                             default=df['Geography'].unique().tolist())
    gender_sel = st.multiselect("👤 Gender",
                                df['Gender'].unique().tolist(),
                                default=df['Gender'].unique().tolist())
    age_range = st.slider("🎂 Age Range", 18, 92, (18, 92))
    balance_thresh = st.number_input("💶 High-Value Threshold (€)",
                                     min_value=0, max_value=300000,
                                     value=100000, step=10000)
    show_churned = st.radio("Show customers",
                            ["All", "Churned Only", "Retained Only"])
    st.divider()
    st.caption("Bank Churn Analysis · European Banking\nRampuram Ganesh")

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
mask = (
    df['Geography'].isin(geo_sel) &
    df['Gender'].isin(gender_sel) &
    df['Age'].between(*age_range)
)
if show_churned == "Churned Only":
    mask &= df['Exited'] == 1
elif show_churned == "Retained Only":
    mask &= df['Exited'] == 0

fdf = df[mask]

st.title("🏦 Bank Customer Churn Analysis")
st.caption(f"European Banking Dataset · **{len(fdf):,}** customers selected · "
           f"Filters: {', '.join(geo_sel)} | Age {age_range[0]}–{age_range[1]}")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Churn Summary",
    "🌍 Geography Analysis",
    "👥 Age & Tenure",
    "💎 High-Value Explorer"
])

with tab1:
    st.subheader("Key Performance Indicators")

    # KPI Cards
    total      = len(fdf)
    churned    = fdf['Exited'].sum()
    churn_pct  = churned / total * 100 if total else 0
    retained   = total - churned
    hv         = fdf[fdf['Balance'] > balance_thresh]
    hv_churn   = hv['Exited'].mean()*100 if len(hv) else 0
    inactive_c = fdf[fdf['IsActiveMember']==0]['Exited'].mean()*100 if len(fdf) else 0
    active_c   = fdf[fdf['IsActiveMember']==1]['Exited'].mean()*100 if len(fdf) else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(f"""<div class='metric-card'>
        <div class='metric-value danger'>{churn_pct:.1f}%</div>
        <div class='metric-label'>Overall Churn Rate</div>
        <div class='metric-sub'>{churned:,} of {total:,} customers</div>
    </div>""", unsafe_allow_html=True)

    geo_churn = fdf.groupby('Geography')['Exited'].mean()*100
    max_geo   = geo_churn.idxmax() if len(geo_churn) else 'N/A'
    max_pct   = geo_churn.max() if len(geo_churn) else 0
    c2.markdown(f"""<div class='metric-card'>
        <div class='metric-value warning'>{max_pct:.1f}%</div>
        <div class='metric-label'>Segment Churn (Peak)</div>
        <div class='metric-sub'>Highest: {max_geo}</div>
    </div>""", unsafe_allow_html=True)

    c3.markdown(f"""<div class='metric-card'>
        <div class='metric-value info'>{hv_churn:.1f}%</div>
        <div class='metric-label'>High-Value Churn</div>
        <div class='metric-sub'>Balance &gt; €{balance_thresh:,.0f}</div>
    </div>""", unsafe_allow_html=True)

    geo_risk  = geo_churn.max() / geo_churn.max() if len(geo_churn) else 0
    c4.markdown(f"""<div class='metric-card'>
        <div class='metric-value purple'>{max_geo}</div>
        <div class='metric-label'>Geographic Risk Index</div>
        <div class='metric-sub'>Highest churn region</div>
    </div>""", unsafe_allow_html=True)

    ratio = inactive_c / active_c if active_c else 0
    c5.markdown(f"""<div class='metric-card'>
        <div class='metric-value danger'>{ratio:.1f}×</div>
        <div class='metric-label'>Engagement Drop</div>
        <div class='metric-sub'>Inactive vs active churn</div>
    </div>""", unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(values=[churned, retained],
                     names=['Churned','Retained'],
                     color_discrete_sequence=['#E53935','#43A047'],
                     hole=0.45, title="Overall Churn Distribution")
        fig.update_traces(textinfo='percent+label', textfont_size=13)
        fig.update_layout(showlegend=False, height=320,
                          margin=dict(t=40,b=10,l=10,r=10))
        st.plotly_chart(fig, width='stretch')

    with col2:
        gender_churn = fdf.groupby(['Gender','Exited']).size().reset_index(name='Count')
        fig2 = px.bar(gender_churn, x='Gender', y='Count', color='Exited',
                      barmode='group',
                      color_discrete_map={0:'#43A047',1:'#E53935'},
                      title="Churn by Gender",
                      labels={'Exited':'Churn Status'})
        fig2.update_layout(height=320, margin=dict(t=40,b=10,l=10,r=10))
        st.plotly_chart(fig2, width='stretch')

    st.markdown("""<div class='insight-box'>
    💡 <b>Key Insight:</b> Female customers show a higher churn propensity despite
    comprising a smaller share. Combine this with geographic risk for targeted outreach.
    </div>""", unsafe_allow_html=True)

with tab2:
    st.subheader("Geography-wise Churn Analysis")

    geo_df = fdf.groupby('Geography').agg(
        Total    =('Exited','count'),
        Churned  =('Exited','sum'),
        ChurnRate=('Exited','mean')
    ).reset_index()
    geo_df['ChurnPct'] = (geo_df['ChurnRate'] * 100).round(2)
    geo_df['RetainedPct'] = (100 - geo_df['ChurnPct']).round(2)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(geo_df, x='Geography', y='ChurnPct',
                     color='ChurnPct',
                     color_continuous_scale='RdYlGn_r',
                     text='ChurnPct', title="Churn Rate by Country (%)")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(coloraxis_showscale=False, height=370,
                          margin=dict(t=50,b=20,l=20,r=20),
                          yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, width='stretch')

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name='Churned', x=geo_df['Geography'],
                              y=geo_df['Churned'], marker_color='#E53935'))
        fig2.add_trace(go.Bar(name='Retained', x=geo_df['Geography'],
                              y=geo_df['Total']-geo_df['Churned'],
                              marker_color='#43A047'))
        fig2.update_layout(barmode='stack', title="Customer Volume by Country",
                           height=370, margin=dict(t=50,b=20,l=20,r=20))
        st.plotly_chart(fig2, width='stretch')


    # Geographic Risk Table
    st.subheader("Geographic Risk Index")
    min_rate = geo_df['ChurnRate'].min()
    max_rate = geo_df['ChurnRate'].max()
    geo_df['Risk Index'] = ((geo_df['ChurnRate'] - min_rate) /
                            (max_rate - min_rate + 1e-9)).round(3)
    geo_df['Risk Level'] = geo_df['Risk Index'].apply(
        lambda x: '🔴 High' if x > 0.66 else ('🟡 Medium' if x > 0.33 else '🟢 Low'))
    show_cols = ['Geography','Total','Churned','ChurnPct','Risk Index','Risk Level']
    st.dataframe(geo_df[show_cols].sort_values('Risk Index', ascending=False),
                 width='stretch', hide_index=True)

    st.markdown("""<div class='insight-box'>
    💡 <b>Key Insight:</b> Germany's churn rate is ~2× that of France and Spain.
    A dedicated Germany retention programme could recover €2M+ in annual revenue
    from high-balance customers alone.
    </div>""", unsafe_allow_html=True)


with tab3:
    st.subheader("Age & Tenure Churn Comparison")

    col1, col2 = st.columns(2)
    with col1:
        age_churn = fdf.groupby('AgeGroup')['Exited'].mean().reset_index()
        age_churn['ChurnPct'] = (age_churn['Exited'] * 100).round(2)
        colors = ['#E53935' if v == age_churn['ChurnPct'].max()
                  else '#42A5F5' for v in age_churn['ChurnPct']]
        fig = px.bar(age_churn, x='AgeGroup', y='ChurnPct',
                     color='ChurnPct', color_continuous_scale='RdBu_r',
                     text='ChurnPct', title="Churn Rate by Age Group")
        fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        fig.update_layout(coloraxis_showscale=False, height=350,
                          margin=dict(t=50,b=20), yaxis_title="Churn Rate (%)")
        st.plotly_chart(fig, width='stretch')

    with col2:
        tenure_churn = fdf.groupby('Tenure')['Exited'].mean().reset_index()
        tenure_churn['ChurnPct'] = (tenure_churn['Exited'] * 100).round(2)
        fig2 = px.line(tenure_churn, x='Tenure', y='ChurnPct',
                       markers=True, title="Churn Rate by Tenure (Years)",
                       color_discrete_sequence=['#1565C0'])
        fig2.update_traces(line_width=2.5, marker_size=7)
        fig2.add_hrect(y0=0, y1=tenure_churn['ChurnPct'].mean(),
                       fillcolor='green', opacity=0.05)
        fig2.update_layout(height=350, margin=dict(t=50,b=20),
                           yaxis_title="Churn Rate (%)", xaxis_title="Tenure (Years)")
        st.plotly_chart(fig2, width='stretch')

    # Engagement Drop Indicator
    st.subheader("Engagement Drop Indicator")
    eng_df = fdf.groupby(['AgeGroup','IsActiveMember'])['Exited'].mean().reset_index()
    eng_df['IsActiveMember'] = eng_df['IsActiveMember'].map({0:'Inactive', 1:'Active'})
    eng_df['ChurnPct'] = (eng_df['Exited'] * 100).round(2)
    fig3 = px.bar(eng_df, x='AgeGroup', y='ChurnPct', color='IsActiveMember',
                  barmode='group', title="Churn by Age Group × Engagement Status",
                  color_discrete_map={'Inactive':'#E53935','Active':'#43A047'})
    fig3.update_layout(height=350, margin=dict(t=50,b=20),
                       yaxis_title="Churn Rate (%)")
    st.plotly_chart(fig3, width='stretch')

    st.markdown("""<div class='insight-box'>
    💡 <b>Key Insight:</b> Customers aged 40–50 with inactive status are the single
    highest-risk group. Early re-engagement (email campaigns, loyalty rewards) in
    the 35–40 age window could prevent churn before it occurs.
    </div>""", unsafe_allow_html=True)


with tab4:
    st.subheader("High-Value Customer Churn Explorer")
    st.caption(f"Threshold: Balance > €{balance_thresh:,.0f}")

    hv_df   = fdf[fdf['Balance'] > balance_thresh]
    non_hv  = fdf[fdf['Balance'] <= balance_thresh]

    m1, m2, m3 = st.columns(3)
    m1.metric("High-Value Customers", f"{len(hv_df):,}",
              f"{len(hv_df)/len(fdf)*100:.1f}% of total")
    m2.metric("High-Value Churn Rate",
              f"{hv_df['Exited'].mean()*100:.1f}%",
              f"{hv_df['Exited'].mean()*100 - fdf['Exited'].mean()*100:+.1f}% vs average",
              delta_color="inverse")
    m3.metric("Avg Balance (Churned HV)",
              f"€{hv_df[hv_df['Exited']==1]['Balance'].mean():,.0f}")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(fdf, x='Balance', color='Exited',
                           nbins=50, barmode='overlay',
                           color_discrete_map={0:'#43A047',1:'#E53935'},
                           title="Balance Distribution: Churned vs Retained",
                           labels={'Exited':'Churned'})
        fig.add_vline(x=balance_thresh, line_dash='dash', line_color='navy',
                      annotation_text="High-Value Threshold",
                      annotation_position="top right")
        fig.update_layout(height=350, margin=dict(t=50,b=20))
        st.plotly_chart(fig, width='stretch')

    with col2:
        prod_df = fdf.groupby('NumOfProducts')['Exited'].mean().reset_index()
        prod_df['ChurnPct'] = (prod_df['Exited'] * 100).round(2)
        fig2 = px.bar(prod_df, x='NumOfProducts', y='ChurnPct',
                      color='ChurnPct', color_continuous_scale='RdYlGn_r',
                      text='ChurnPct', title="Churn Rate by No. of Products",
                      labels={'NumOfProducts':'Number of Products'})
        fig2.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        fig2.update_layout(coloraxis_showscale=False, height=350,
                           margin=dict(t=50,b=20))
        st.plotly_chart(fig2, width='stretch')

    # Drill-down table
    st.subheader("Drill-down: High-Value Churned Customers")
    drill = hv_df[hv_df['Exited']==1][
        ['CustomerId','Geography','Gender','Age','Balance',
         'NumOfProducts','IsActiveMember','Tenure']
    ].sort_values('Balance', ascending=False).head(50)
    drill['IsActiveMember'] = drill['IsActiveMember'].map({0:'❌ Inactive', 1:'✅ Active'})
    drill['Balance'] = drill['Balance'].apply(lambda x: f"€{x:,.0f}")
    st.dataframe(drill, width='stretch', hide_index=True)

    st.markdown("""<div class='insight-box'>
    💡 <b>Key Insight:</b> Customers with 3–4 products churn at >80% — possibly due to
    product complexity or mis-selling. High-balance inactive customers are the top
    priority for a white-glove retention programme.
    </div>""", unsafe_allow_html=True)

st.divider()
st.caption("🏦 Customer Segmentation and Churn Pattern Analytics · European Banking Dataset · "
           "Built by **Rampuram Ganesh** |· "
           "Tech: Python · Streamlit · Plotly · XGBoost · SHAP")