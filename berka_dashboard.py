
# Import the libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# Must be the first Streamlit command called
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Berka Bank SQL Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# COLOR PALETTE
# ─────────────────────────────────────────────────────────────
NAVY   = "#1F3864"
TEAL   = "#2E75B6"
RED    = "#C00000"
GREEN  = "#375623"
ORANGE = "#E97132"

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #FAFAFA; }

    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-left: 4px solid #2E75B6;
        border-radius: 6px;
        padding: 12px 16px;
    }

    .section-header {
        background: linear-gradient(90deg, #1F3864, #2E75B6);
        color: white;
        padding: 10px 18px;
        border-radius: 6px;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    .insight-box {
        background-color: #EBF3FB;
        border-left: 4px solid #2E75B6;
        border-radius: 4px;
        padding: 12px 16px;
        margin: 10px 0;
        font-size: 14px;
        color: #1F3864;
    }

    .warning-box {
        background-color: #FFF3E0;
        border-left: 4px solid #E97132;
        border-radius: 4px;
        padding: 12px 16px;
        margin: 10px 0;
        font-size: 14px;
        color: #7B3F00;
    }

    .risk-box {
        background-color: #FFE5E5;
        border-left: 4px solid #C00000;
        border-radius: 4px;
        padding: 12px 16px;
        margin: 10px 0;
        font-size: 14px;
        color: #C00000;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DATA LOADING
# CSV files live in a /data subfolder in the repository
# @st.cache_data means files are only read once per session
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_dir = os.path.join(os.path.dirname(__file__), "data")

    def read(filename):
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            st.error(
                f"Missing file: data/{filename}\n\n"
                "Make sure your repository contains a /data folder "
                "with all four CSV files."
            )
            st.stop()
        return pd.read_csv(path)

    q1 = read("query1_balance_vs_default.csv")
    q2 = read("query2_velocity_drop.csv")
    q3 = read("query3_cashout_risk_50%.csv")
    q4 = read("query4_cashout_risk_80%.csv")

    return q1, q2, q3, q4


q1, q2, q3, q4 = load_data()


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='color:white; font-size:20px; font-weight:700;
                padding-bottom:6px; border-bottom:1px solid #2E75B6;
                margin-bottom:16px;'>
        🏦 Berka Bank Analytics
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#90CAF9; font-size:12px;'>Urbanus Kathitu | Kat.Codes</p>",
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border-color:#2E75B6;'>", unsafe_allow_html=True)

    page = st.radio(
        label="Navigate",
        options=[
            "Overview",
            "Query 1: Balance vs Default",
            "Query 2: Velocity Drop",
            "Query 3: Cash-Out Risk",
        ]
    )

    st.markdown("<hr style='border-color:#2E75B6;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='color:#90CAF9; font-size:11px; line-height:1.7;'>
        <b style='color:white;'>Dataset</b><br>
        Czech Bank 1993-1998<br>
        1,056,320 transactions<br>
        682 loans | 4,500 accounts<br><br>
        <b style='color:white;'>SQL Techniques</b><br>
        CTEs | Window Functions<br>
        NTILE | LAG | ROW_NUMBER<br>
        Subqueries | Aggregations<br><br>
        <b style='color:white;'>Stack</b><br>
        PostgreSQL | DBeaver<br>
        Python | Streamlit | Plotly
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────────────────────
if page == "Overview":

    # Hero banner
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1F3864,#2E75B6);
                padding:30px 24px; border-radius:10px; margin-bottom:24px;'>
        <h1 style='color:white; margin:0; font-size:28px;'>
            Berka Bank — Transaction-Level SQL Analytics
        </h1>
        <p style='color:#BBDEFB; margin:8px 0 0 0; font-size:15px;'>
            Credit risk insights extracted from 1,056,320 real bank transactions
            using advanced PostgreSQL: CTEs, Window Functions, and Subqueries.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Transactions", "1,056,320")
    c2.metric("Total Accounts",     "4,500")
    c3.metric("Total Loans",        "682")
    c4.metric("Bad Loans (B+D)",    "76",
              delta="-11.1% of total", delta_color="inverse")
    c5.metric("Good Loans (A+C)",   "606",
              delta="88.9% of total")

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    # Loan status bar chart
    with col_l:
        st.markdown(
            '<div class="section-header">Loan Status Distribution</div>',
            unsafe_allow_html=True
        )
        status_df = pd.DataFrame({
            "Status": [
                "C: Running, Good",
                "A: Finished, Paid",
                "D: Running, In Trouble",
                "B: Finished, Unpaid"
            ],
            "Count": [403, 203, 45, 31]
        })
        fig = go.Figure(go.Bar(
            x=status_df["Status"],
            y=status_df["Count"],
            marker_color=[GREEN, TEAL, ORANGE, RED],
            text=status_df["Count"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
        ))
        fig.update_layout(
            height=340,
            margin=dict(t=20, b=20, l=10, r=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(gridcolor="#F0F0F0", title="Number of Loans"),
            xaxis=dict(tickangle=-15),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Good vs bad donut
    with col_r:
        st.markdown(
            '<div class="section-header">Good vs Bad Loan Split</div>',
            unsafe_allow_html=True
        )
        fig2 = go.Figure(go.Pie(
            labels=["Good (A+C)", "Bad (B+D)"],
            values=[606, 76],
            marker_colors=[TEAL, RED],
            hole=0.55,
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
        ))
        fig2.update_layout(
            height=340,
            margin=dict(t=20, b=20, l=10, r=10),
            paper_bgcolor="white",
            annotations=[dict(
                text="682<br>Loans", x=0.5, y=0.5,
                font_size=16, font_color=NAVY, showarrow=False
            )]
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <b>Core Credit Risk Question:</b> Out of 682 loans, 76 are bad or in trouble.
        How do you identify these 76 before disbursing the money?
        The three queries below explore different behavioural signals that predict this outcome.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Query summary cards
    st.markdown(
        '<div class="section-header">Project Queries at a Glance</div>',
        unsafe_allow_html=True
    )

    ca, cb, cc = st.columns(3)

    with ca:
        st.markdown(f"""
        <div style='border:1px solid #E0E0E0; border-top:4px solid {TEAL};
                    border-radius:6px; padding:16px; background:white; min-height:150px;'>
            <b style='color:{NAVY}; font-size:15px;'>Query 1: Balance vs Default</b><br><br>
            <span style='color:#444; font-size:13px;'>
                Bottom 20% accounts default at <b>37.5%</b> vs <b>2.85%</b> for the top 20%.
                A <b>13x</b> difference in risk driven by average balance behaviour.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with cb:
        st.markdown(f"""
        <div style='border:1px solid #E0E0E0; border-top:4px solid {ORANGE};
                    border-radius:6px; padding:16px; background:white; min-height:150px;'>
            <b style='color:{NAVY}; font-size:15px;'>Query 2: Velocity Drop</b><br><br>
            <span style='color:#444; font-size:13px;'>
                Flagged accounts whose monthly transaction count dropped more than
                <b>40%</b> in a single month. Worst case: <b>-90%</b> drop in one month.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with cc:
        st.markdown(f"""
        <div style='border:1px solid #E0E0E0; border-top:4px solid {RED};
                    border-radius:6px; padding:16px; background:white; min-height:150px;'>
            <b style='color:{NAVY}; font-size:15px;'>Query 3: Cash-Out Risk</b><br><br>
            <span style='color:#444; font-size:13px;'>
                Account <b>10857</b> flagged HIGH RISK: largest troubled loan (385,560)
                with a last transfer of <b>73.68%</b> of average monthly income.
            </span>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: QUERY 1
# ─────────────────────────────────────────────────────────────
elif page == "Query 1: Balance vs Default":

    st.markdown(
        f"<h2 style='color:{NAVY};'>Query 1: Does Account Balance Predict Default Risk?</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="insight-box">
        <b>Business Question:</b> If a customer maintains a consistently high average balance,
        are they less likely to default on a loan? I split all 4,500 accounts into quintiles
        by average balance across all 1,056,320 transactions and compared the default rate
        of the top 20% against the bottom 20%.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Extract values
    bottom_row = q1[q1["balance_tier"] == "BOTTOM 20%"].iloc[0]
    top_row    = q1[q1["balance_tier"] == "TOP 20%"].iloc[0]

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bottom 20% Default Rate",
              f"{bottom_row['default_rate_percent']}%",
              delta="High risk", delta_color="inverse")
    c2.metric("Top 20% Default Rate",
              f"{top_row['default_rate_percent']}%",
              delta="Low risk")
    c3.metric("Risk Multiplier", "13x",
              delta="Bottom defaults 13x more than top")
    c4.metric("Total Loans in Comparison",
              int(bottom_row["total_loans"] + top_row["total_loans"]))

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    # Default rate bar chart
    with col_l:
        st.markdown(
            '<div class="section-header">Default Rate by Balance Tier</div>',
            unsafe_allow_html=True
        )
        bar_colors = [
            RED if t == "BOTTOM 20%" else GREEN
            for t in q1["balance_tier"]
        ]
        fig = go.Figure(go.Bar(
            x=q1["balance_tier"],
            y=q1["default_rate_percent"],
            marker_color=bar_colors,
            text=[f"{v}%" for v in q1["default_rate_percent"]],
            textposition="outside",
            width=0.4,
            hovertemplate="<b>%{x}</b><br>Default Rate: %{y}%<extra></extra>"
        ))
        fig.update_layout(
            height=360,
            margin=dict(t=20, b=20, l=10, r=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(
                gridcolor="#F0F0F0",
                title="Default Rate (%)",
                range=[0, 45]
            ),
            xaxis=dict(title="Balance Tier"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Loan volume stacked bar
    with col_r:
        st.markdown(
            '<div class="section-header">Loan Volume: Good vs Bad by Tier</div>',
            unsafe_allow_html=True
        )
        q1["good_loans"] = q1["total_loans"] - q1["bad_loans"]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="Good Loans",
            x=q1["balance_tier"],
            y=q1["good_loans"],
            marker_color=TEAL,
            hovertemplate="<b>%{x}</b><br>Good Loans: %{y}<extra></extra>"
        ))
        fig2.add_trace(go.Bar(
            name="Bad Loans",
            x=q1["balance_tier"],
            y=q1["bad_loans"],
            marker_color=RED,
            hovertemplate="<b>%{x}</b><br>Bad Loans: %{y}<extra></extra>"
        ))
        fig2.update_layout(
            barmode="stack",
            height=360,
            margin=dict(t=20, b=20, l=10, r=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(gridcolor="#F0F0F0", title="Number of Loans"),
            xaxis=dict(title="Balance Tier"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Raw data table
    st.markdown(
        '<div class="section-header">Query Results</div>',
        unsafe_allow_html=True
    )
    st.dataframe(
        q1[["balance_tier", "total_loans", "bad_loans", "default_rate_percent"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    <div class="insight-box">
        <b>Key Insight:</b> Lending to someone in the bottom 20% by average balance carries a
        37.5% default rate compared to just 2.85% for the top 20%. That is a 13x difference
        in risk driven by a single behavioural signal. Average balance is a strong candidate
        feature in a credit scoring model. This is exactly the kind of insight that drives
        alternative credit scoring at companies like Pezesha and M-KOPA, where mobile money
        balance behaviour replaces formal credit bureau data.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box">
        <b>SQL Technique:</b> Three chained CTEs. CTE 1 calculates average balance per account
        across all transactions. CTE 2 uses NTILE(5) window function to split accounts into
        five equal groups by balance. CTE 3 filters to top and bottom groups only.
        Final SELECT joins to the loan table and computes default rates per group.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: QUERY 2
# ─────────────────────────────────────────────────────────────
elif page == "Query 2: Velocity Drop":

    st.markdown(
        f"<h2 style='color:{NAVY};'>Query 2: Month-Over-Month Transaction Velocity Drop</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="insight-box">
        <b>Business Question:</b> Can we detect early warning signs of default by monitoring
        sudden drops in transaction activity? A customer who goes from 10 transactions per month
        to 1 in a single month may be in financial trouble before they miss a payment.
        I flagged every account whose monthly transaction count dropped more than 40%
        compared to the previous month using the LAG() window function.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accounts Flagged",   len(q2))
    c2.metric("Worst Drop",         f"{q2['pct_change'].min()}%")
    c3.metric("Average Drop",       f"{q2['pct_change'].mean():.1f}%")
    c4.metric("All Flags",          "HIGH RISK > 40%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    # Drop bar chart
    with col_l:
        st.markdown(
            '<div class="section-header">Transaction Drop % per Flagged Account</div>',
            unsafe_allow_html=True
        )
        fig = go.Figure(go.Bar(
            x=q2["account_id"].astype(str),
            y=q2["pct_change"],
            marker_color=RED,
            text=[f"{v}%" for v in q2["pct_change"]],
            textposition="outside",
            hovertemplate="<b>Account %{x}</b><br>Drop: %{y}%<extra></extra>"
        ))
        fig.add_hline(
            y=-40, line_dash="dash", line_color=ORANGE,
            annotation_text="40% Threshold",
            annotation_position="top right"
        )
        fig.update_layout(
            height=360,
            margin=dict(t=30, b=20, l=10, r=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(
                gridcolor="#F0F0F0",
                title="% Change in Monthly Transactions",
                range=[-100, 0]
            ),
            xaxis=dict(title="Account ID", tickangle=-45),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Drops by year
    with col_r:
        st.markdown(
            '<div class="section-header">Flagged Accounts by Year</div>',
            unsafe_allow_html=True
        )
        year_counts = (
            q2.groupby("txn_year")
              .size()
              .reset_index(name="flagged_accounts")
        )
        fig2 = go.Figure(go.Bar(
            x=year_counts["txn_year"].astype(str),
            y=year_counts["flagged_accounts"],
            marker_color=TEAL,
            text=year_counts["flagged_accounts"],
            textposition="outside",
            hovertemplate="<b>Year %{x}</b><br>Flagged Accounts: %{y}<extra></extra>"
        ))
        fig2.update_layout(
            height=360,
            margin=dict(t=30, b=20, l=10, r=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(gridcolor="#F0F0F0", title="Number of Flagged Accounts"),
            xaxis=dict(title="Year"),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Before vs after line chart
    st.markdown(
        '<div class="section-header">Previous Month vs Current Month Transaction Count</div>',
        unsafe_allow_html=True
    )
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=q2["account_id"].astype(str),
        y=q2["previous_month_txns"],
        mode="markers+lines",
        name="Previous Month",
        marker=dict(color=GREEN, size=9),
        line=dict(color=GREEN, dash="dot")
    ))
    fig3.add_trace(go.Scatter(
        x=q2["account_id"].astype(str),
        y=q2["current_month_txns"],
        mode="markers+lines",
        name="Current Month (After Drop)",
        marker=dict(color=RED, size=9),
        line=dict(color=RED)
    ))
    fig3.update_layout(
        height=300,
        margin=dict(t=10, b=20, l=10, r=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(gridcolor="#F0F0F0", title="Transaction Count"),
        xaxis=dict(title="Account ID", tickangle=-45),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Raw data
    st.markdown(
        '<div class="section-header">Query Results</div>',
        unsafe_allow_html=True
    )
    st.dataframe(q2, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="warning-box">
        <b>Important Observation:</b> December 1998 appears repeatedly in the results.
        This is a data collection artefact, not a genuine risk signal. The dataset ends
        in late 1998, so many accounts have fewer transactions in their final recorded
        month because data collection stopped mid-month. In a production environment
        I would filter out the most recent month before flagging risk to eliminate this noise.
        Recognising artefacts like this is a critical part of responsible data analysis.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <b>SQL Technique:</b> LAG() window function partitioned by account_id and ordered
        chronologically. For each account and each month, LAG() reaches back to the previous
        row and retrieves the prior month's transaction count. This processed all 1,056,320
        rows in a single pass with no loops, enabling month-over-month comparison at scale.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: QUERY 3
# ─────────────────────────────────────────────────────────────
elif page == "Query 3: Cash-Out Risk":

    st.markdown(
        f"<h2 style='color:{NAVY};'>Query 3: Cash-Out Before Default Risk Detection</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="insight-box">
        <b>Business Question:</b> Can we detect accounts that are deliberately withdrawing
        funds before defaulting on a loan? I searched for accounts with a bad or troubled loan
        (status B or D) whose most recent transaction was a large outgoing payment relative
        to their average monthly income. I ran this query at two different thresholds to
        observe how sensitivity changes.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Threshold toggle
    st.markdown(
        '<div class="section-header">Select Risk Threshold</div>',
        unsafe_allow_html=True
    )
    threshold = st.radio(
        "Withdrawal threshold as % of average monthly inflow:",
        options=[
            "50% Threshold — catches HIGH RISK accounts",
            "80% Threshold — all accounts show as MONITOR"
        ],
        horizontal=True
    )

    active_df       = q3 if "50%" in threshold else q4
    threshold_val   = 50  if "50%" in threshold else 80
    threshold_label = "50%" if "50%" in threshold else "80%"

    high_risk_count = len(
        active_df[
            active_df["risk_flag"] == "HIGH RISK: Large withdrawal on bad loan account"
        ]
    )
    monitor_count = len(active_df[active_df["risk_flag"] == "MONITOR"])

    st.markdown("<br>", unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accounts Analysed",  len(active_df))
    c2.metric("HIGH RISK Flags",    high_risk_count,
              delta="Flagged for review" if high_risk_count > 0 else "None flagged",
              delta_color="inverse" if high_risk_count > 0 else "normal")
    c3.metric("MONITOR",            monitor_count)
    c4.metric("Active Threshold",   f"{threshold_label} of avg inflow")

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    # Withdrawal % bar chart
    with col_l:
        st.markdown(
            f'<div class="section-header">Withdrawal % of Avg Inflow (Threshold: {threshold_label})</div>',
            unsafe_allow_html=True
        )
        bar_colors = [
            RED if r == "HIGH RISK: Large withdrawal on bad loan account" else TEAL
            for r in active_df["risk_flag"]
        ]
        fig = go.Figure(go.Bar(
            x=active_df["account_id"].astype(str),
            y=active_df["withdrawal_as_pct_of_income"],
            marker_color=bar_colors,
            text=[f"{v}%" for v in active_df["withdrawal_as_pct_of_income"]],
            textposition="outside",
            hovertemplate=(
                "<b>Account %{x}</b><br>"
                "Withdrawal as % of Inflow: %{y}%<extra></extra>"
            )
        ))
        fig.add_hline(
            y=threshold_val,
            line_dash="dash",
            line_color=ORANGE,
            annotation_text=f"{threshold_label} Threshold",
            annotation_position="top right"
        )
        fig.update_layout(
            height=360,
            margin=dict(t=30, b=20, l=10, r=10),
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(
                gridcolor="#F0F0F0",
                title="Withdrawal as % of Avg Monthly Inflow",
                range=[0, 85]
            ),
            xaxis=dict(title="Account ID", tickangle=-30),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Risk flag pie
    with col_r:
        st.markdown(
            '<div class="section-header">Risk Flag Distribution</div>',
            unsafe_allow_html=True
        )
        flag_counts = active_df["risk_flag"].value_counts().reset_index()
        flag_counts.columns = ["Risk Flag", "Count"]

        pie_colors = [
            RED if "HIGH RISK" in f else GREEN
            for f in flag_counts["Risk Flag"]
        ]
        fig2 = go.Figure(go.Pie(
            labels=flag_counts["Risk Flag"],
            values=flag_counts["Count"],
            marker_colors=pie_colors,
            hole=0.5,
            textinfo="label+value",
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
        ))
        fig2.update_layout(
            height=360,
            margin=dict(t=20, b=20, l=10, r=10),
            paper_bgcolor="white",
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter: loan amount vs last withdrawal
    st.markdown(
        '<div class="section-header">Loan Amount vs Last Transaction Amount</div>',
        unsafe_allow_html=True
    )
    for status, symbol, label in [
        ("D", "diamond", "Status D: Running, In Trouble"),
        ("B", "circle",  "Status B: Finished, Unpaid")
    ]:
        subset = active_df[active_df["loan_status"] == status]
        if subset.empty:
            continue
        s_colors = [
            RED if r == "HIGH RISK: Large withdrawal on bad loan account" else TEAL
            for r in subset["risk_flag"]
        ]
        if "fig3" not in dir():
            fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=subset["loan_amount"],
            y=subset["last_txn_amount"],
            mode="markers",
            name=label,
            marker=dict(color=s_colors, size=14, symbol=symbol,
                        line=dict(width=1, color="white")),
            text=subset["account_id"].astype(str),
            hovertemplate=(
                "<b>Account %{text}</b><br>"
                "Loan Amount: %{x:,.0f}<br>"
                "Last Transaction: %{y:,.0f}<extra></extra>"
            )
        ))

    fig3 = go.Figure()
    for status, symbol, label in [
        ("D", "diamond", "Status D: Running, In Trouble"),
        ("B", "circle",  "Status B: Finished, Unpaid")
    ]:
        subset = active_df[active_df["loan_status"] == status]
        if subset.empty:
            continue
        s_colors = [
            RED if r == "HIGH RISK: Large withdrawal on bad loan account" else TEAL
            for r in subset["risk_flag"]
        ]
        fig3.add_trace(go.Scatter(
            x=subset["loan_amount"],
            y=subset["last_txn_amount"],
            mode="markers",
            name=label,
            marker=dict(color=s_colors, size=14, symbol=symbol,
                        line=dict(width=1, color="white")),
            text=subset["account_id"].astype(str),
            hovertemplate=(
                "<b>Account %{text}</b><br>"
                "Loan Amount: %{x:,.0f}<br>"
                "Last Transaction: %{y:,.0f}<extra></extra>"
            )
        ))
    fig3.update_layout(
        height=320,
        margin=dict(t=10, b=20, l=10, r=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(gridcolor="#F0F0F0", title="Loan Amount"),
        yaxis=dict(gridcolor="#F0F0F0", title="Last Transaction Amount"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Side by side threshold comparison table
    st.markdown(
        '<div class="section-header">Threshold Comparison: 50% vs 80%</div>',
        unsafe_allow_html=True
    )

    comparison = q3[[
        "account_id", "loan_amount", "loan_status",
        "withdrawal_as_pct_of_income"
    ]].copy()
    comparison["Risk @ 80% Threshold"] = q4["risk_flag"].apply(
        lambda x: "HIGH RISK" if "HIGH RISK" in str(x) else "MONITOR"
    )
    comparison["Risk @ 50% Threshold"] = q3["risk_flag"].apply(
        lambda x: "HIGH RISK" if "HIGH RISK" in str(x) else "MONITOR"
    )
    comparison = comparison.rename(columns={
        "account_id":                   "Account ID",
        "loan_amount":                  "Loan Amount",
        "loan_status":                  "Loan Status",
        "withdrawal_as_pct_of_income":  "Withdrawal % of Inflow"
    })

    def highlight_risk(val):
        if val == "HIGH RISK":
            return "background-color: #FFE5E5; color: #C00000; font-weight: bold;"
        elif val == "MONITOR":
            return "background-color: #E8F5E9; color: #375623;"
        return ""

    styled = comparison.style.applymap(
        highlight_risk,
        subset=["Risk @ 80% Threshold", "Risk @ 50% Threshold"]
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # Insight boxes
    st.markdown("""
    <div class="risk-box">
        <b>Key Finding:</b> At an 80% threshold zero accounts are flagged. Lowering to 50%
        surfaces account 10857 as HIGH RISK: the largest troubled loan in the dataset (385,560)
        with a last transfer of 6,426 representing 73.68% of average monthly income.
        The transfer went to another account (not a simple cash withdrawal), suggesting
        deliberate movement of funds before stopping repayments.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box">
        <b>Precision vs Recall Tradeoff:</b> A high threshold catches fewer accounts but misses
        real risks. A low threshold catches more but may flag good customers incorrectly.
        There is no mathematically correct threshold. A credit team sets it based on the
        relative cost of approving a bad loan versus the cost of rejecting a good customer.
        That is a business decision the data scientist informs but does not make alone.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <b>SQL Technique:</b> ROW_NUMBER() window function partitioned by account_id and
        ordered by date descending to find the most recent transaction per account in a
        single pass. The original correlated subquery version ran for over one hour on
        1,056,320 rows without completing. ROW_NUMBER() reduced runtime to under 5 seconds.
        This is a real production performance optimisation lesson.
    </div>
    """, unsafe_allow_html=True)
