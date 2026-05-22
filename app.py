import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Northwind BI Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: radial-gradient(ellipse at top left,#0d1b2a 0%,#050d1a 40%,#000814 100%);
    color: #e2e8f0;
}
[data-testid="stSidebar"] {
    background: rgba(10,20,40,0.95) !important;
    border-right: 1px solid rgba(0,200,255,0.18);
    backdrop-filter: blur(24px);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* ── Filter label row ── */
.filter-label-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 14px 0 4px 0;
}
.filter-icon {
    font-size: 1rem;
    line-height: 1;
}
.filter-label {
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .09em;
    text-transform: uppercase;
    color: #7dd3fc;
    flex: 1;
}
.filter-badge {
    font-size: .62rem;
    font-weight: 600;
    color: #00c8ff;
    background: rgba(0,200,255,.1);
    border: 1px solid rgba(0,200,255,.2);
    border-radius: 20px;
    padding: 1px 7px;
    white-space: nowrap;
}

/* ── Sidebar summary card ── */
.sb-summary {
    margin-top: 16px;
    padding: 12px 14px;
    background: linear-gradient(135deg,rgba(0,200,255,.06),rgba(0,100,200,.03));
    border: 1px solid rgba(0,200,255,.14);
    border-radius: 12px;
    font-size: .7rem;
    color: #475569;
    line-height: 2;
}
.sb-summary b { color: #38bdf8; }

/* Active filter dot */
.dot-active  { color: #34d399; }
.dot-partial { color: #fbbf24; }

.kpi-card {
    background: linear-gradient(135deg,rgba(0,200,255,0.08),rgba(0,100,200,0.04));
    border: 1px solid rgba(0,200,255,0.25);
    border-radius: 16px; padding: 22px 16px 16px;
    text-align: center;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 24px rgba(0,200,255,0.08),inset 0 1px 0 rgba(255,255,255,0.05);
    transition: box-shadow .3s, transform .3s;
}
.kpi-card:hover { box-shadow: 0 0 40px rgba(0,200,255,0.22); transform: translateY(-3px); }
.kpi-icon  { font-size:1.8rem; margin-bottom:5px; }
.kpi-label { font-size:.7rem; font-weight:700; letter-spacing:.1em;
             text-transform:uppercase; color:#7dd3fc; margin-bottom:7px; }
.kpi-value { font-size:1.7rem; font-weight:800; color:#f0f9ff;
             text-shadow:0 0 18px rgba(0,200,255,.5); }
.kpi-sub   { font-size:.74rem; margin-top:5px; color:#34d399; font-weight:600; }

.sec-head {
    font-size:.7rem; font-weight:700; letter-spacing:.13em;
    text-transform:uppercase; color:#38bdf8;
    border-bottom:1px solid rgba(56,189,248,.2);
    padding-bottom:7px; margin:26px 0 12px;
}
.insight-box {
    background: rgba(0,200,255,.04);
    border: 1px solid rgba(0,200,255,.18);
    border-radius:14px; padding:16px 18px; margin-bottom:12px;
    backdrop-filter: blur(10px);
}
.insight-title { font-size:.8rem; font-weight:700; color:#38bdf8; margin-bottom:5px; }
.insight-text  { font-size:.82rem; color:#94a3b8; line-height:1.65; }

::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#0a1628; }
::-webkit-scrollbar-thumb { background:rgba(0,200,255,.3); border-radius:4px; }

/* Select-All toggle row */
.sa-row {
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:3px;
}
.sa-label {
    font-size:.7rem; font-weight:700; letter-spacing:.07em;
    text-transform:uppercase; color:#7dd3fc;
}
.sa-count {
    font-size:.65rem; color:#475569; font-weight:600;
    background:rgba(0,200,255,.08); border-radius:6px;
    padding:1px 7px; border:1px solid rgba(0,200,255,.15);
}
</style>
""", unsafe_allow_html=True)

# ── Chart constants ───────────────────────────────────────────────────────────
NEON = ["#00c8ff","#0ea5e9","#38bdf8","#7dd3fc","#06b6d4",
        "#22d3ee","#a5f3fc","#67e8f9","#2dd4bf","#34d399"]
BG   = "rgba(5,13,26,0.0)"
GRID = "rgba(255,255,255,0.05)"
LINE = "rgba(255,255,255,0.08)"

def S(fig, title="", h=350):
    """Apply dark neon theme to a plotly figure in-place."""
    ax = dict(gridcolor=GRID, linecolor=LINE, zerolinecolor=GRID)
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, height=h,
        font=dict(family="Inter", color="#94a3b8", size=11),
        title=dict(text=title, font=dict(family="Inter", color="#e2e8f0", size=13)),
        xaxis=ax, yaxis=ax,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        margin=dict(l=10, r=10, t=40, b=10),
    )

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("northwind_cleaned.csv")
    df["orderDate"] = pd.to_datetime(df["orderDate"])
    df["order_year"]  = df["orderDate"].dt.year
    df["order_month"] = df["orderDate"].dt.month
    df["month_label"] = df["orderDate"].dt.to_period("M").astype(str)
    return df

RAW = load()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:

    # ── Logo / brand
    st.markdown("""
    <div style='text-align:center;padding:14px 0 20px'>
        <div style='font-size:2rem;filter:drop-shadow(0 0 10px #00c8ff)'>🌐</div>
        <div style='font-size:1rem;font-weight:800;color:#38bdf8;letter-spacing:.08em;margin-top:4px'>NORTHWIND BI</div>
        <div style='font-size:.62rem;color:#334155;letter-spacing:.14em;margin-top:2px'>ANALYTICS PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sec-head'>🎛️ &nbsp;Dashboard Filters</div>", unsafe_allow_html=True)

    # ── Build full option lists from raw data
    all_years    = sorted(RAW["order_year"].dropna().unique().astype(int))
    all_countries= sorted(RAW["customer_country"].dropna().unique())
    all_cats     = sorted(RAW["categoryName"].dropna().unique())
    all_emps     = sorted(RAW["employee_name"].dropna().unique())
    all_ships    = sorted(RAW["shipper_name"].dropna().unique())
    all_prods    = sorted(RAW["productName"].dropna().unique())

    # ── Reusable filter widget
    # Each filter:
    #   • Left  → ☑ Select All checkbox
    #   • Label → icon + name  (centre)
    #   • Badge → X / N count  (right)
    #   • Multiselect below (hidden label)
    def make_filter(key, label, icon, opts):
        n_all  = len(opts)
        sa_key = f"_sa_{key}"            # session-state key for checkbox
        ms_key = f"_ms_{key}"            # session-state key for multiselect

        # First-load: default all selected
        if sa_key not in st.session_state:
            st.session_state[sa_key] = True

        # ── Label row: [checkbox] [icon label] [count badge]
        cb_col, lbl_col, badge_col = st.columns([1, 4, 2])

        with cb_col:
            all_checked = st.checkbox(
                "All",
                value=st.session_state[sa_key],
                key=sa_key,
                label_visibility="collapsed",
                help=f"Select / deselect all {label}s",
            )

        with lbl_col:
            st.markdown(
                f"<div class='filter-label'><span class='filter-icon'>{icon}</span> {label}</div>",
                unsafe_allow_html=True,
            )

        # Decide default values for multiselect
        if all_checked:
            default_vals = opts          # all selected when checkbox ✓
        else:
            # keep whatever was previously chosen; if nothing, start empty
            prev = st.session_state.get(ms_key, [])
            default_vals = [v for v in prev if v in opts]

        sel = st.multiselect(
            label,
            options=opts,
            default=default_vals,
            key=ms_key,
            label_visibility="collapsed",
            placeholder=(
                f"All {n_all} {label}s ✓" if all_checked
                else f"Choose {label}s …"
            ),
        )

        # Badge: show count
        n_sel = len(sel) if sel else n_all
        dot   = "dot-active" if n_sel == n_all else "dot-partial"
        with badge_col:
            st.markdown(
                f"<div class='filter-badge'><span class='{dot}'>●</span> "
                f"{n_sel}/{n_all}</div>",
                unsafe_allow_html=True,
            )

        # Fail-safe: empty selection → treat as ALL
        return sel if sel else opts

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    sy = make_filter("year",    "Year",         "📅", all_years)
    sc = make_filter("country", "Country",      "🌍", all_countries)
    sk = make_filter("cat",     "Category",     "📦", all_cats)
    se = make_filter("emp",     "Employee",     "👤", all_emps)
    ss = make_filter("ship",    "Shipper",      "🚚", all_ships)
    sp = make_filter("prod",    "Product Name", "🏷️", all_prods)

    # ── Active-filter summary card
    st.markdown(f"""
    <div class='sb-summary'>
        📅 <b>{len(sy)}</b>/{len(all_years)} Year(s) &nbsp;·&nbsp;
        🌍 <b>{len(sc)}</b>/{len(all_countries)} Countr{'y' if len(sc)==1 else 'ies'}<br>
        📦 <b>{len(sk)}</b>/{len(all_cats)} Categor{'y' if len(sk)==1 else 'ies'} &nbsp;·&nbsp;
        👤 <b>{len(se)}</b>/{len(all_emps)} Employee(s)<br>
        🚚 <b>{len(ss)}</b>/{len(all_ships)} Shipper(s) &nbsp;·&nbsp;
        🏷️ <b>{len(sp)}</b>/{len(all_prods)} Product(s)
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<br><div style='font-size:.62rem;color:#1e293b;text-align:center'>"
        "Northwind Traders &nbsp;·&nbsp; BI v2.0</div>",
        unsafe_allow_html=True,
    )

# ── Apply filters ─────────────────────────────────────────────────────────────
df = RAW[
    RAW["order_year"].isin(sy) &
    RAW["customer_country"].isin(sc) &
    RAW["categoryName"].isin(sk) &
    RAW["employee_name"].isin(se) &
    RAW["shipper_name"].isin(ss) &
    RAW["productName"].isin(sp)
].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:16px 0 8px'>
  <div style='font-size:.7rem;font-weight:700;letter-spacing:.18em;color:#38bdf8;text-transform:uppercase;margin-bottom:5px'>
    ✦ Business Intelligence Platform ✦
  </div>
  <h1 style='font-size:2.1rem;font-weight:800;margin:0;
             background:linear-gradient(90deg,#00c8ff 0%,#38bdf8 40%,#7dd3fc 70%,#00c8ff 100%);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-.01em'>
    Northwind Business Performance Insights Dashboard
  </h1>
  <div style='font-size:.8rem;color:#475569;margin-top:6px;letter-spacing:.05em'>
    Real-time analytics &nbsp;·&nbsp; Sales &nbsp;·&nbsp; Customers &nbsp;·&nbsp; Logistics
  </div>
</div>
<hr style='border:none;border-top:1px solid rgba(0,200,255,0.12);margin:12px 0 4px'>
""", unsafe_allow_html=True)

# ── Guard: empty dataframe ────────────────────────────────────────────────────
if df.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust the sidebar selections.")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_rev   = df["line_total"].sum()
total_ord   = df["orderID"].nunique()
total_cust  = df["customerID"].nunique()
avg_ov      = df.groupby("orderID")["line_total"].sum().mean()
avg_delay   = df["ship_delay_days"].mean()

st.markdown("<div class='sec-head'>📊 &nbsp;Key Performance Indicators</div>", unsafe_allow_html=True)
k1,k2,k3,k4,k5 = st.columns(5)
kpis = [
    (k1,"💰","Total Revenue",   f"${total_rev:,.0f}",  "All-time gross sales"),
    (k2,"📦","Total Orders",    f"{total_ord:,}",        "Unique order count"),
    (k3,"👥","Total Customers", f"{total_cust:,}",       "Active accounts"),
    (k4,"🎯","Avg Order Value", f"${avg_ov:,.2f}",       "Revenue per order"),
    (k5,"🚚","Avg Ship Delay",  f"{avg_delay:.1f} days", "Days past schedule"),
]
for col,icon,label,val,sub in kpis:
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-icon'>{icon}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-value'>{val}</div>
          <div class='kpi-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Monthly trend | Top-10 Products ───────────────────────────────────
st.markdown("<div class='sec-head'>📈 &nbsp;Sales Analytics</div>", unsafe_allow_html=True)
r1a, r1b = st.columns([3,2])

with r1a:
    mn = (df.groupby("month_label")["line_total"].sum()
            .reset_index().rename(columns={"month_label":"Month","line_total":"Revenue"})
            .sort_values("Month"))
    fig = go.Figure(go.Scatter(
        x=mn["Month"], y=mn["Revenue"], mode="lines+markers",
        line=dict(color="#00c8ff",width=2.5),
        marker=dict(size=6,color="#00c8ff",line=dict(color="rgba(0,200,255,.3)",width=6)),
        fill="tozeroy", fillcolor="rgba(0,200,255,0.06)", name="Revenue",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    ))
    S(fig,"Monthly Sales Trend",330)
    fig.update_layout(xaxis_tickangle=-40)
    st.plotly_chart(fig, use_container_width=True)

with r1b:
    tp = (df.groupby("productName")["line_total"].sum()
            .nlargest(10).reset_index()
            .rename(columns={"line_total":"Revenue"}))
    fig = go.Figure(go.Bar(
        x=tp["Revenue"], y=tp["productName"], orientation="h",
        marker=dict(color=tp["Revenue"],colorscale=[[0,"#0369a1"],[1,"#00c8ff"]],
                    showscale=False,line=dict(color="rgba(0,200,255,.3)",width=.5)),
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
    ))
    S(fig,"Top 10 Products by Revenue",330)
    fig.update_layout(yaxis=dict(autorange="reversed",gridcolor=GRID,linecolor=LINE,zerolinecolor=GRID))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Category donut | Country bar | Employee bar ───────────────────────
st.markdown("<div class='sec-head'>🗂️ &nbsp;Category, Geography & Team Performance</div>", unsafe_allow_html=True)
r2a, r2b, r2c = st.columns(3)

with r2a:
    cr = (df.groupby("categoryName")["line_total"].sum()
            .reset_index().rename(columns={"line_total":"Revenue"}))
    fig = go.Figure(go.Pie(
        labels=cr["categoryName"], values=cr["Revenue"], hole=0.55,
        marker=dict(colors=NEON,line=dict(color="rgba(5,13,26,.8)",width=2)),
        textinfo="label+percent", textfont=dict(size=9,color="#94a3b8"),
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(text=f"<b>${total_rev/1e6:.1f}M</b>",x=.5,y=.5,
                       font=dict(size=15,color="#f0f9ff"),showarrow=False)
    S(fig,"Category-wise Revenue",340)
    fig.update_layout(showlegend=True,legend=dict(bgcolor="rgba(0,0,0,0)",orientation="v",font=dict(size=9)))
    st.plotly_chart(fig, use_container_width=True)

with r2b:
    cy = (df.groupby("customer_country")["line_total"].sum()
            .nlargest(12).reset_index()
            .rename(columns={"line_total":"Revenue"}))
    fig = go.Figure(go.Bar(
        x=cy["customer_country"], y=cy["Revenue"],
        marker=dict(color=cy["Revenue"],
                    colorscale=[[0,"#0c4a6e"],[.5,"#0ea5e9"],[1,"#00c8ff"]],
                    showscale=False,line=dict(color="rgba(0,200,255,.3)",width=.5)),
        hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
    ))
    S(fig,"Revenue by Country (Top 12)",340)
    fig.update_layout(xaxis_tickangle=-40)
    st.plotly_chart(fig, use_container_width=True)

with r2c:
    er = (df.groupby("employee_name")["line_total"].sum()
            .sort_values().reset_index()
            .rename(columns={"line_total":"Revenue"}))
    fig = go.Figure(go.Bar(
        x=er["Revenue"], y=er["employee_name"], orientation="h",
        marker=dict(color=er["Revenue"],colorscale=[[0,"#0369a1"],[1,"#22d3ee"]],
                    showscale=False,line=dict(color="rgba(34,211,238,.3)",width=.5)),
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
    ))
    S(fig,"Sales by Employee",340)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Quarterly grouped | Shipper delay ─────────────────────────────────
st.markdown("<div class='sec-head'>🚚 &nbsp;Logistics & Quarterly Performance</div>", unsafe_allow_html=True)
r3a, r3b = st.columns([3,2])

with r3a:
    qr = (df.groupby(["order_year","order_quarter"])["line_total"]
            .sum().reset_index().rename(columns={"line_total":"Revenue"}))
    qr["Quarter"] = "Q" + qr["order_quarter"].astype(str)
    fig = px.bar(qr, x="Quarter", y="Revenue", color="order_year",
                 barmode="group",
                 color_discrete_sequence=["#00c8ff","#0ea5e9","#38bdf8","#7dd3fc"],
                 labels={"order_year":"Year"})
    S(fig,"Quarterly Revenue by Year",320)
    fig.update_layout(legend_title="Year")
    st.plotly_chart(fig, use_container_width=True)

with r3b:
    sd = (df.groupby("shipper_name")["ship_delay_days"]
            .mean().reset_index()
            .rename(columns={"ship_delay_days":"AvgDelay"}))
    fig = go.Figure()
    for i,(_, row) in enumerate(sd.iterrows()):
        c = NEON[i % len(NEON)]
        fig.add_trace(go.Bar(
            x=[row["AvgDelay"]], y=[row["shipper_name"]], orientation="h",
            marker=dict(color=c,line=dict(color=c,width=.5)),
            name=row["shipper_name"],
            hovertemplate=f"<b>{row['shipper_name']}</b><br>Avg Delay: {row['AvgDelay']:.1f} days<extra></extra>",
        ))
    S(fig,"Avg Shipping Delay by Shipper",320)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 4: Customer scatter ───────────────────────────────────────────────────
st.markdown("<div class='sec-head'>🔍 &nbsp;Customer Intelligence</div>", unsafe_allow_html=True)
cdf = (df.groupby("customer_company")
       .agg(Revenue=("line_total","sum"),
            Orders=("orderID","nunique"),
            Country=("customer_country","first"))
       .reset_index())
fig = px.scatter(
    cdf, x="Orders", y="Revenue", size="Revenue",
    color="Country", hover_name="customer_company",
    size_max=40, color_discrete_sequence=NEON,
    labels={"Revenue":"Total Revenue ($)"},
)
fig.update_traces(marker=dict(opacity=.78,line=dict(color="rgba(255,255,255,.2)",width=.5)))
S(fig,"Customer Segmentation: Orders vs Revenue",390)
st.plotly_chart(fig, use_container_width=True)

# ── Insights ──────────────────────────────────────────────────────────────────
st.markdown("<div class='sec-head'>💡 &nbsp;Business Insights & Recommendations</div>", unsafe_allow_html=True)

top_prod   = df.groupby("productName")["line_total"].sum().idxmax()
top_cat    = df.groupby("categoryName")["line_total"].sum().idxmax()
top_cat_pct= df.groupby("categoryName")["line_total"].sum().max() / total_rev * 100
top_cntry  = df.groupby("customer_country")["line_total"].sum().idxmax()
top_emp    = df.groupby("employee_name")["line_total"].sum().idxmax()
worst_ship = df.groupby("shipper_name")["ship_delay_days"].mean().idxmax()
worst_dly  = df.groupby("shipper_name")["ship_delay_days"].mean().max()

items = [
    ("📦 Product Portfolio",
     f"<b>{top_prod}</b> is the top-grossing product. Bundle it with complementary items and expand availability to maximise cross-sell revenue."),
    ("🗂️ Category Concentration",
     f"<b>{top_cat}</b> drives <b>{top_cat_pct:.1f}%</b> of total revenue. Diversify marketing spend to grow under-performing categories."),
    ("🌍 Geographic Expansion",
     f"<b>{top_cntry}</b> is the highest-value market. Prioritise emerging markets with localised campaigns to unlock new revenue streams."),
    ("👤 Sales Team Excellence",
     f"<b>{top_emp}</b> leads overall sales. Deploy peer-mentoring and replicate top-performer strategies across the team."),
    ("🚚 Logistics Optimisation",
     f"<b>{worst_ship}</b> averages <b>{worst_dly:.1f} days</b> delay. Renegotiate SLAs or diversify carriers to improve customer satisfaction."),
    ("📈 Revenue Growth Strategy",
     f"Average Order Value is <b>${avg_ov:,.2f}</b>. Volume discounts and loyalty programmes can drive larger basket sizes and repeat purchases."),
]
ia, ib = st.columns(2)
for i,(title,text) in enumerate(items):
    with (ia if i%2==0 else ib):
        st.markdown(f"""
        <div class='insight-box'>
          <div class='insight-title'>{title}</div>
          <div class='insight-text'>{text}</div>
        </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border:none;border-top:1px solid rgba(0,200,255,0.1);margin:26px 0 14px'>
<div style='text-align:center;font-size:.68rem;color:#334155;letter-spacing:.06em'>
  Northwind Business Performance Insights Dashboard &nbsp;·&nbsp;
  Streamlit + Plotly &nbsp;·&nbsp; Dark BI Theme v2.0
</div>
""", unsafe_allow_html=True)
