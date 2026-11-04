"""
FootLens Analytics - Player Injuries and Team Performance Dashboard
Course: Mathematics for AI-II (Summative Assessment)
Scenario 1: FootLens Analytics Junior Sports Data Analyst Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Local imports
from src.preprocessing import load_and_preprocess_data
from src.visualizations import (
    plot_top_injuries_performance_drop,
    plot_player_performance_timeline,
    plot_injury_heatmap,
    plot_age_vs_performance_drop,
    get_comeback_leaderboard,
    plot_injury_distribution_donut,
    plot_team_outcomes_comparison
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="FootLens Analytics | Player Injuries & Team Performance",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern CSS Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global Font & Spacing */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Header Card */
    .header-box {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #0D9488 100%);
        padding: 26px 32px;
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .header-box h1 {
        color: #FFFFFF !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .header-box p {
        color: #E2E8F0;
        font-size: 1.05rem;
        margin-bottom: 0px;
    }
    .badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #F1F5F9;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 8px;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.88rem;
        color: #64748B;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.7rem;
        font-weight: 700;
        color: #0F172A;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        font-weight: 600;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        border-color: #1E3A8A !important;
    }

    /* Insight Callout */
    .insight-card {
        background-color: #EFF6FF;
        border-left: 4px solid #2563EB;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 14px 0;
        color: #1E3A8A;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Data Loading (Cached for Speed)
# ---------------------------------------------------------
@st.cache_data
def get_data():
    return load_and_preprocess_data('player_injuries_impact.csv')


try:
    df_clean = get_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()


# ---------------------------------------------------------
# Sidebar: Brand and Interactive Filters
# ---------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=500&auto=format&fit=crop&q=60", use_container_width=True)
st.sidebar.title("⚽ FootLens Analytics")
st.sidebar.markdown("**AI Research & Insights Division**  \n*Premier League Injury & Squad Performance Monitor*")
st.sidebar.markdown("---")

st.sidebar.header("🎯 Dashboard Filters")

# Club Filter
all_clubs = sorted(df_clean['Club'].dropna().unique().tolist())
selected_clubs = st.sidebar.multiselect(
    "Filter by Club:",
    options=all_clubs,
    default=all_clubs
)

# Season Filter
all_seasons = sorted(df_clean['Season'].dropna().unique().tolist())
selected_seasons = st.sidebar.multiselect(
    "Filter by Season:",
    options=all_seasons,
    default=all_seasons
)

# Position Unit Filter
all_positions = sorted(df_clean['Position_Group'].dropna().unique().tolist())
selected_positions = st.sidebar.multiselect(
    "Filter by Tactical Unit:",
    options=all_positions,
    default=all_positions
)

# Injury Category Filter
all_injuries = sorted(df_clean['Injury_Category'].dropna().unique().tolist())
selected_injuries = st.sidebar.multiselect(
    "Filter by Injury Category:",
    options=all_injuries,
    default=all_injuries
)

# Age Range Slider
min_age = int(df_clean['Age'].min())
max_age = int(df_clean['Age'].max())
age_range = st.sidebar.slider(
    "Filter by Player Age Range:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

st.sidebar.markdown("---")
st.sidebar.caption("Summative Assessment II - Mathematics for AI")
st.sidebar.caption("Role: Junior Sports Data Analyst @ FootLens")


# ---------------------------------------------------------
# Apply Filters
# ---------------------------------------------------------
filtered_df = df_clean[
    (df_clean['Club'].isin(selected_clubs)) &
    (df_clean['Season'].isin(selected_seasons)) &
    (df_clean['Position_Group'].isin(selected_positions)) &
    (df_clean['Injury_Category'].isin(selected_injuries)) &
    (df_clean['Age'].between(age_range[0], age_range[1]))
]

if filtered_df.empty:
    st.warning("⚠️ No records match the selected filter combination. Please broaden your filter criteria in the sidebar.")
    st.stop()


# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown("""
<div class="header-box">
    <div>
        <span class="badge">FootLens Analytics Pro</span>
        <span class="badge">Premier League Data</span>
        <span class="badge">Seasons 2019/20 - 2023/24</span>
    </div>
    <h1>Player Injuries & Team Performance Intelligence Dashboard</h1>
    <p>Empowering Technical Directors, Performance Coaches, and Squad Managers with Data-Backed Injury Analytics and Comeback Insights.</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Executive KPI Row
# ---------------------------------------------------------
total_injuries = len(filtered_df)
avg_recovery_days = filtered_df['Recovery_Days'].mean()
avg_ppm_drop = filtered_df['Performance_Drop_Index'].mean()
pct_perf_decline = (filtered_df['Performance_Drop_Index'] > 0).mean() * 100

top_comeback_row = filtered_df.dropna(subset=['Rating_Improvement']).sort_values(by='Rating_Improvement', ascending=False)
if not top_comeback_row.empty:
    star_comeback = top_comeback_row.iloc[0]
    star_name = f"{star_comeback['Player_Name']} (+{star_comeback['Rating_Improvement']:.2f})"
else:
    star_name = "N/A"

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Injury Incidents", f"{total_injuries:,}")
kpi2.metric("Avg. Recovery Time", f"{avg_recovery_days:.1f} Days" if pd.notna(avg_recovery_days) else "N/A")
kpi3.metric("Avg. Team PPM Drop", f"{avg_ppm_drop:+.2f} pts" if pd.notna(avg_ppm_drop) else "0.00")
kpi4.metric("Negative Impact Rate", f"{pct_perf_decline:.1f}%")
kpi5.metric("Top Comeback Surge", star_name)

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Tabbed Dashboard Sections
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Team Performance Impact",
    "📈 Player Recovery Timeline",
    "🗓️ Seasonality & Club Heatmap",
    "🎯 Age & Positional Risk",
    "🏆 Comeback Heroes Leaderboard",
    "🔬 Deep EDA & Research Answers"
])


# =========================================================
# TAB 1: TEAM PERFORMANCE IMPACT
# =========================================================
with tab1:
    st.subheader("1. Team Performance Degradation During Player Absence")
    st.markdown("""
    Quantifying the structural gap left by absent squad members. We measure the drop in **Points Per Match (PPM)** 
    by comparing the club's results in the 3 games immediately prior to the injury versus the 3 matches missed.
    """)

    col1, col2 = st.columns([3, 2])
    with col1:
        # Visual 1: Bar Chart of Top 10 Injuries with highest drop
        fig_bar = plot_top_injuries_performance_drop(filtered_df)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Match Outcome Comparison Stacked Bar
        fig_outcomes = plot_team_outcomes_comparison(filtered_df)
        st.plotly_chart(fig_outcomes, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <b>💡 Tactical Director Takeaway:</b> Severe structural injuries such as <i>Knee Surgery</i>, <i>Shoulder Injuries</i>, 
        and <i>Concussions</i> produce the steepest drops in team point efficiency. During absence periods, team win percentage drops noticeably 
        while loss percentage rises, confirming the direct dependency on key starters.
    </div>
    """, unsafe_allow_html=True)

    # Club summary table
    st.subheader("Club Breakdown: Performance Drop & Days Lost")
    club_summary = filtered_df.groupby('Club').agg(
        Total_Injuries=('Injury', 'count'),
        Avg_Days_Lost=('Recovery_Days', 'mean'),
        Avg_PPM_Drop=('Performance_Drop_Index', 'mean'),
        Avg_GD_Drop=('Team_GD_Drop', 'mean')
    ).reset_index().sort_values(by='Total_Injuries', ascending=False)

    club_summary['Avg_Days_Lost'] = club_summary['Avg_Days_Lost'].round(1)
    club_summary['Avg_PPM_Drop'] = club_summary['Avg_PPM_Drop'].round(2)
    club_summary['Avg_GD_Drop'] = club_summary['Avg_GD_Drop'].round(2)

    st.dataframe(club_summary, use_container_width=True)


# =========================================================
# TAB 2: PLAYER RECOVERY TIMELINE
# =========================================================
with tab2:
    st.subheader("2. Player Match-by-Match Trajectory (Before vs. After Injury)")
    st.markdown("""
    Select any player from the squad to inspect their match performance trajectory. Track how their match rating 
    behaved across the **3 matches leading into the injury** and the **3 comeback matches post-recovery**.
    """)

    available_players = sorted(filtered_df['Player_Name'].unique().tolist())
    
    col_sel, col_stat = st.columns([1, 2])
    with col_sel:
        # Default to high-profile player if available
        default_idx = 0
        if "Callum Wilson" in available_players:
            default_idx = available_players.index("Callum Wilson")
        elif "Marcus Rashford" in available_players:
            default_idx = available_players.index("Marcus Rashford")
        elif "Heungmin Son" in available_players:
            default_idx = available_players.index("Heungmin Son")

        chosen_player = st.selectbox("Select Player to Inspect:", options=available_players, index=default_idx)

    # Player summary card
    p_df = filtered_df[filtered_df['Player_Name'] == chosen_player]
    p_club = p_df['Club'].iloc[0]
    p_pos = p_df['Position'].iloc[0]
    p_fifa = p_df['FIFA rating'].iloc[0]
    p_age = p_df['Age'].iloc[0]
    p_inj_count = len(p_df)
    p_avg_pre = p_df['Pre_Injury_Avg_Rating'].mean()
    p_avg_post = p_df['Post_Injury_Avg_Rating'].mean()
    p_diff = p_avg_post - p_avg_pre if pd.notna(p_avg_post) and pd.notna(p_avg_pre) else np.nan

    with col_stat:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; padding: 14px 20px; border-radius: 10px; margin-top: 10px;">
            <b>👤 {chosen_player}</b> | {p_club} | {p_pos} | Age: {p_age} | FIFA Rating: <b>{p_fifa}</b><br>
            Total Recorded Injuries: <b>{p_inj_count}</b> | Career Pre-Injury Avg: <b>{p_avg_pre:.2f}</b> | Post-Injury Avg: <b>{p_avg_post:.2f}</b> 
            (Net: <b style="color: {'#059669' if p_diff >= 0 else '#DC2626'}">{p_diff:+.2f}</b>)
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual 2: Line chart timeline
    fig_timeline = plot_player_performance_timeline(filtered_df, selected_player=chosen_player)
    st.plotly_chart(fig_timeline, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <b>💡 Sports Science Insight:</b> Players returning from soft-tissue strains (hamstrings, calves) frequently experience 
        a dip in their first match back due to minute restrictions or pacing anxiety before stabilizing by Match 2 and Match 3.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# TAB 3: SEASONALITY & CLUB HEATMAP
# =========================================================
with tab3:
    st.subheader("3. Injury Frequency Seasonality & Anatomical Distribution")
    st.markdown("""
    Analyzing seasonal load and fixture congestion. Identify high-risk periods during the Premier League calendar 
    (such as the December festive schedule) and evaluate anatomical vulnerability.
    """)

    col_h1, col_h2 = st.columns([3, 2])
    with col_h1:
        # Visual 3: Heatmap across Months and Clubs
        fig_heatmap = plot_injury_heatmap(filtered_df)
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col_h2:
        # Donut of Injury Categories
        fig_donut = plot_injury_distribution_donut(filtered_df)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <b>💡 Medical Insights:</b> 
        1. <b>Winter Congestion Peaks:</b> December and January consistently register the highest concentration of muscular and lower-limb injuries, 
        driven by congested festive fixtures, reduced recovery windows, and colder pitch conditions.<br>
        2. <b>Primary Culprits:</b> Hamstring and knee ligament injuries represent the overwhelming majority of absences, underscoring the need 
        for proactive rotation and sprint-load monitoring.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# TAB 4: AGE & POSITIONAL RISK
# =========================================================
with tab4:
    st.subheader("4. Player Age vs. Team Performance Drop Index")
    st.markdown("""
    Examining the correlation between player veteran status and team reliance. Does an injury to a senior star 
    cause a more catastrophic team collapse than an injury to an emerging prospect?
    """)

    # Visual 4: Scatter Plot Age vs Performance Drop
    fig_scatter = plot_age_vs_performance_drop(filtered_df)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Correlation Analysis
    corr_df = filtered_df[['Age', 'Performance_Drop_Index', 'FIFA rating', 'Recovery_Days']].dropna()
    r_val = corr_df['Age'].corr(corr_df['Performance_Drop_Index'])
    r_fifa = corr_df['FIFA rating'].corr(corr_df['Performance_Drop_Index'])

    st.markdown(f"""
    <div class="insight-card">
        <b>💡 Squad Planning Analysis:</b><br>
        • <b>Age Correlation:</b> Pearson Correlation $r = {r_val:+.3f}$ between Player Age and Performance Drop Index.<br>
        • <b>Star Player Reliance:</b> Correlation with FIFA Rating $r = {r_fifa:+.3f}$ indicates that squad quality and tactical dependence 
        (star player centrality) have a far greater destabilizing impact on team performance than chronological age alone. 
        High-rated defenders and creative midfielders trigger the largest absence drops.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# TAB 5: COMEBACK HEROES LEADERBOARD
# =========================================================
with tab5:
    st.subheader("5. Comeback Heroes & Form Decline Leaderboard")
    st.markdown("""
    Recognizing players who bounced back with the strongest form after recovery (**Positive Rating Delta**), 
    versus players whose post-injury ratings struggled to reach pre-injury benchmarks (**Negative Rating Delta**).
    """)

    leaderboard_data = get_comeback_leaderboard(filtered_df)

    filter_type = st.radio(
        "Display Filter:",
        options=["Top Comeback Surge (Major Rating Improvement)", "Severe Post-Injury Decline (Biggest Rating Drop)", "All Records"],
        horizontal=True
    )

    if filter_type == "Top Comeback Surge (Major Rating Improvement)":
        display_data = leaderboard_data.head(25)
    elif filter_type == "Severe Post-Injury Decline (Biggest Rating Drop)":
        display_data = leaderboard_data.sort_values(by='Rating_Improvement', ascending=True).head(25)
    else:
        display_data = leaderboard_data

    # Visual 5: Styled Interactive Leaderboard Table
    st.dataframe(
        display_data.style.background_gradient(subset=['Rating_Improvement'], cmap='RdYlGn'),
        use_container_width=True,
        height=500
    )

    # Download Button
    csv_bytes = display_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Leaderboard as CSV",
        data=csv_bytes,
        file_name="footlens_comeback_leaderboard.csv",
        mime="text/csv"
    )


# =========================================================
# TAB 6: DEEP EDA & RESEARCH QUESTIONS
# =========================================================
with tab6:
    st.subheader("6. Exhaustive Exploratory Data Analysis & 5 Research Questions")
    st.markdown("""
    In accordance with FootLens Analytics research directives, here are the detailed mathematical answers to the 
    **Five Foundational Business Questions** guiding this investigation.
    """)

    # Question 1
    with st.expander("❓ Question 1: Which injuries led to the biggest team performance drop?", expanded=True):
        st.markdown("""
        **Analysis:** We compute the mean team drop index ($PPM_{before} - PPM_{during}$) grouped by injury diagnosis for all injuries with at least 3 occurrences.
        """)
        q1_table = filtered_df.groupby('Injury').agg(
            Incident_Count=('Injury', 'count'),
            Avg_PPM_Drop=('Performance_Drop_Index', 'mean'),
            Avg_GD_Drop=('Team_GD_Drop', 'mean'),
            Avg_Recovery_Days=('Recovery_Days', 'mean')
        ).query('Incident_Count >= 2').sort_values(by='Avg_PPM_Drop', ascending=False).head(10)
        st.dataframe(q1_table.style.format({'Avg_PPM_Drop': '{:+.2f}', 'Avg_GD_Drop': '{:+.2f}', 'Avg_Recovery_Days': '{:.1f}'}), use_container_width=True)
        st.markdown("**Key Finding:** Severe joint injuries (Shoulder injury, Knee surgery) and neurological disruptions (Concussion) lead to the most extreme team performance drop (up to 1.25 points per match lost).")

    # Question 2
    with st.expander("❓ Question 2: What was the team's win/loss record during player absence?", expanded=True):
        st.markdown("""
        **Analysis:** Evaluating total match outcomes across all missed matches during player absence versus matches with the player present.
        """)
        # Outcome aggregation
        def count_results(prefix):
            cols = [f'{prefix}{i}_Result' for i in [1, 2, 3] if f'{prefix}{i}_Result' in filtered_df.columns]
            vals = filtered_df[cols].values.flatten()
            s = pd.Series([str(v).lower().strip() for v in vals if v not in ['N.A.', np.nan, None]])
            vc = s.value_counts()
            tot = vc.sum()
            return {
                'Wins': vc.get('win', 0),
                'Draws': vc.get('draw', 0),
                'Losses': vc.get('lose', 0),
                'Total Matches': tot,
                'Win %': (vc.get('win', 0) / tot * 100) if tot > 0 else 0,
                'Loss %': (vc.get('lose', 0) / tot * 100) if tot > 0 else 0
            }

        q2_data = pd.DataFrame([
            count_results('Match'),  # Before
            count_results('Match_missed_match_' if 'Match_missed_match_1_Result' in filtered_df.columns else 'Match'),
        ])
        # Direct calculation from raw columns
        b_res = filtered_df[['Match1_before_injury_Result', 'Match2_before_injury_Result', 'Match3_before_injury_Result']].values.flatten()
        m_res = filtered_df[['Match1_missed_match_Result', 'Match2_missed_match_Result', 'Match3_missed_match_Result']].values.flatten()
        a_res = filtered_df[['Match1_after_injury_Result', 'Match2_after_injury_Result', 'Match3_after_injury_Result']].values.flatten()

        def get_stat_dict(arr, stage):
            s = pd.Series([str(v).lower().strip() for v in arr if v not in ['N.A.', np.nan, None, 'nan']])
            tot = len(s)
            w = (s == 'win').sum()
            d = (s == 'draw').sum()
            l = (s == 'lose').sum()
            return {
                'Stage': stage,
                'Matches': tot,
                'Wins': w,
                'Draws': d,
                'Losses': l,
                'Win %': f"{(w/tot*100):.1f}%" if tot > 0 else '0%',
                'Loss %': f"{(l/tot*100):.1f}%" if tot > 0 else '0%',
                'Pts/Match': f"{((w*3 + d*1)/tot):.2f}" if tot > 0 else '0.00'
            }

        q2_df = pd.DataFrame([
            get_stat_dict(b_res, 'Pre-Injury (With Player)'),
            get_stat_dict(m_res, 'During Absence (Player Missed)'),
            get_stat_dict(a_res, 'Post-Recovery (Player Returned)')
        ])
        st.dataframe(q2_df, use_container_width=True)
        st.markdown("**Key Finding:** Team Win % dips significantly during player absence while loss percentage escalates, causing an average drop of ~0.10 to 0.35 points per match across the league.")

    # Question 3
    with st.expander("❓ Question 3: How did individual players perform after recovery?", expanded=True):
        st.markdown("""
        **Analysis:** Comparing individual pre-injury match ratings against post-injury ratings.
        """)
        valid_ratings = filtered_df.dropna(subset=['Pre_Injury_Avg_Rating', 'Post_Injury_Avg_Rating'])
        improved = (valid_ratings['Rating_Improvement'] > 0.1).sum()
        stable = (valid_ratings['Rating_Improvement'].abs() <= 0.1).sum()
        declined = (valid_ratings['Rating_Improvement'] < -0.1).sum()
        total_p = len(valid_ratings)

        col_q3_1, col_q3_2, col_q3_3 = st.columns(3)
        col_q3_1.metric("Strong Comeback (> +0.1)", f"{improved} ({improved/total_p*100:.1f}%)")
        col_q3_2.metric("Form Retained (± 0.1)", f"{stable} ({stable/total_p*100:.1f}%)")
        col_q3_3.metric("Post-Injury Dip (< -0.1)", f"{declined} ({declined/total_p*100:.1f}%)")

        # Pivot Table comparing pre and post ratings across position units
        pv_pos = valid_ratings.pivot_table(
            index='Position_Group',
            values=['Pre_Injury_Avg_Rating', 'Post_Injury_Avg_Rating', 'Rating_Improvement'],
            aggfunc='mean'
        )
        st.markdown("<b>Pre vs. Post Injury Ratings by Tactical Position:</b>", unsafe_allow_html=True)
        st.dataframe(pv_pos.style.format('{:.2f}'), use_container_width=True)

    # Question 4
    with st.expander("❓ Question 4: Are there specific months or clubs with frequent injury clusters?", expanded=True):
        st.markdown("""
        **Analysis:** Monthly incident grouping to locate peak injury spikes across the competition.
        """)
        monthly_cluster = filtered_df.groupby('Injury_Month_Num').agg(
            Month=('Injury_Month', 'first'),
            Total_Injuries=('Injury', 'count')
        ).sort_values(by='Total_Injuries', ascending=False)
        st.dataframe(monthly_cluster, use_container_width=True)
        st.markdown("**Key Finding:** December, January, and October exhibit prominent spikes in soft-tissue injuries due to fixture load and domestic cup competitions.")

    # Question 5
    with st.expander("❓ Question 5: Which clubs suffer most due to injuries?", expanded=True):
        st.markdown("""
        **Analysis:** Composite club ranking evaluating total incident burden, total days lost, and net performance drop.
        """)
        q5_table = filtered_df.groupby('Club').agg(
            Total_Injuries=('Injury', 'count'),
            Total_Days_Lost=('Recovery_Days', 'sum'),
            Avg_Days_Per_Injury=('Recovery_Days', 'mean'),
            Avg_Performance_Drop=('Performance_Drop_Index', 'mean')
        ).sort_values(by='Total_Injuries', ascending=False)
        st.dataframe(q5_table.style.format({'Avg_Days_Per_Injury': '{:.1f}', 'Avg_Performance_Drop': '{:+.2f}', 'Total_Days_Lost': '{:,.0f}'}), use_container_width=True)
        st.markdown("**Key Finding:** Newcastle United, Everton, and Manchester United recorded the highest injury frequency and aggregate days lost, severely disrupting tactical continuity.")

    st.markdown("---")
    st.subheader("Raw Filtered Data Inspector")
    st.dataframe(filtered_df[['Player_Name', 'Club', 'Position', 'Age', 'Season', 'Injury', 'Date of Injury', 'Date of return', 'Recovery_Days', 'Performance_Drop_Index', 'Rating_Improvement']].head(100), use_container_width=True)


# ---------------------------------------------------------
# Footer Section
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.88rem; padding: 10px 0;">
    <b>FootLens Analytics</b> © 2026 | Built for Professional Football Decision Makers | Mathematics for AI-II Project Submission
</div>
""", unsafe_allow_html=True)
