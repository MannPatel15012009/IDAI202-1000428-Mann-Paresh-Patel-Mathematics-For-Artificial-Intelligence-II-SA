"""
Interactive Visualizations Module using Plotly
FootLens Analytics - Player Injuries and Team Performance Dashboard
Course: Mathematics for AI-II (Summative Assessment)
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Premium modern sports analytics color palette
FOOTLENS_COLORS = {
    'primary': '#1E3A8A',     # Royal Navy
    'secondary': '#0D9488',   # Teal Accent
    'accent': '#E11D48',      # Rose / Danger
    'warning': '#F59E0B',     # Amber
    'neutral_light': '#F8FAFC',
    'neutral_dark': '#0F172A',
    'card_bg': '#FFFFFF'
}


def plot_top_injuries_performance_drop(df, min_incidents=2):
    """
    Visual 1: Bar Chart
    Top 10 injuries leading to the highest team performance drop (Points Per Match drop).
    """
    # Group by Injury type and aggregate mean drop and incident count
    injury_impact = df.groupby('Injury').agg(
        Avg_PPM_Drop=('Performance_Drop_Index', 'mean'),
        Avg_GD_Drop=('Team_GD_Drop', 'mean'),
        Incident_Count=('Injury', 'count')
    ).reset_index()

    # Filter by minimum sample size for statistical validity
    injury_impact = injury_impact[injury_impact['Incident_Count'] >= min_incidents]
    top_10 = injury_impact.sort_values(by='Avg_PPM_Drop', ascending=False).head(10)

    fig = px.bar(
        top_10,
        x='Avg_PPM_Drop',
        y='Injury',
        orientation='h',
        color='Avg_PPM_Drop',
        color_continuous_scale='Reds',
        hover_data={'Incident_Count': True, 'Avg_GD_Drop': ':.2f', 'Avg_PPM_Drop': ':.2f'},
        labels={
            'Avg_PPM_Drop': 'Average Team Points Per Match (PPM) Drop',
            'Injury': 'Injury Type',
            'Incident_Count': 'Number of Incidents',
            'Avg_GD_Drop': 'Avg Goal Diff Drop'
        },
        title='<b>Top 10 Injuries with Highest Team Performance Drop (PPM)</b>'
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title='Average Team Performance Drop Index (Points/Match Lost)',
        yaxis_title='Injury Diagnosis',
        font={'family': 'Segoe UI, sans-serif'},
        template='plotly_white',
        coloraxis_showscale=False,
        margin={'l': 10, 'r': 20, 't': 50, 'b': 40},
        height=450
    )
    fig.update_traces(
        texttemplate='%{x:.2f}',
        textposition='outside',
        marker_line_color='rgb(150,20,40)',
        marker_line_width=1
    )
    return fig


def plot_player_performance_timeline(df, selected_player='Callum Wilson'):
    """
    Visual 2: Line Chart
    Player performance timeline across 3 Pre-Injury and 3 Post-Injury matches.
    Displays match-by-match trajectory and average baseline.
    """
    player_records = df[df['Player_Name'] == selected_player]

    if player_records.empty:
        # Fallback to first available player
        selected_player = df['Player_Name'].iloc[0]
        player_records = df[df['Player_Name'] == selected_player]

    # Use the most severe or most recent injury of the player
    record = player_records.sort_values(by='Injury_Date', ascending=False).iloc[0]

    phases = ['Match 3 Before', 'Match 2 Before', 'Match 1 Before', 
              'Match 1 After', 'Match 2 After', 'Match 3 After']
    
    ratings = [
        record.get('Match3_before_injury_Player_rating_clean', np.nan),
        record.get('Match2_before_injury_Player_rating_clean', np.nan),
        record.get('Match1_before_injury_Player_rating_clean', np.nan),
        record.get('Match1_after_injury_Player_rating_clean', np.nan),
        record.get('Match2_after_injury_Player_rating_clean', np.nan),
        record.get('Match3_after_injury_Player_rating_clean', np.nan)
    ]

    opponents = [
        record.get('Match3_before_injury_Opposition', 'N/A'),
        record.get('Match2_before_injury_Opposition', 'N/A'),
        record.get('Match1_before_injury_Opposition', 'N/A'),
        record.get('Match1_after_injury_Opposition', 'N/A'),
        record.get('Match2_after_injury_Opposition', 'N/A'),
        record.get('Match3_after_injury_Opposition', 'N/A')
    ]

    results = [
        record.get('Match3_before_injury_Result', 'N/A'),
        record.get('Match2_before_injury_Result', 'N/A'),
        record.get('Match1_before_injury_Result', 'N/A'),
        record.get('Match1_after_injury_Result', 'N/A'),
        record.get('Match2_after_injury_Result', 'N/A'),
        record.get('Match3_after_injury_Result', 'N/A')
    ]

    timeline_df = pd.DataFrame({
        'Match_Phase': phases,
        'Rating': ratings,
        'Opposition': opponents,
        'Result': results
    })

    fig = go.Figure()

    # Pre-Injury Trace
    fig.add_trace(go.Scatter(
        x=phases[:3],
        y=ratings[:3],
        mode='lines+markers+text',
        name='Pre-Injury Matches',
        line={'color': '#2563EB', 'width': 3},
        marker={'size': 10, 'symbol': 'circle'},
        text=[f"{r:.1f}" if pd.notna(r) else "N/A" for r in ratings[:3]],
        textposition='top center',
        hovertemplate='<b>%{x}</b><br>Rating: %{y:.2f}<br>Opponent: %{customdata[0]}<br>Result: %{customdata[1]}<extra></extra>',
        customdata=np.stack((opponents[:3], results[:3]), axis=-1)
    ))

    # Post-Injury Trace
    fig.add_trace(go.Scatter(
        x=phases[3:],
        y=ratings[3:],
        mode='lines+markers+text',
        name='Post-Injury Return',
        line={'color': '#10B981', 'width': 3, 'dash': 'solid'},
        marker={'size': 10, 'symbol': 'square'},
        text=[f"{r:.1f}" if pd.notna(r) else "N/A" for r in ratings[3:]],
        textposition='top center',
        hovertemplate='<b>%{x}</b><br>Rating: %{y:.2f}<br>Opponent: %{customdata[0]}<br>Result: %{customdata[1]}<extra></extra>',
        customdata=np.stack((opponents[3:], results[3:]), axis=-1)
    ))

    # Pre-injury avg benchmark line
    if pd.notna(record['Pre_Injury_Avg_Rating']):
        fig.add_hline(
            y=record['Pre_Injury_Avg_Rating'], 
            line_dash='dot', 
            line_color='#64748B',
            annotation_text=f"Pre-Injury Avg: {record['Pre_Injury_Avg_Rating']:.2f}",
            annotation_position='bottom left'
        )

    # Post-injury avg benchmark line
    if pd.notna(record['Post_Injury_Avg_Rating']):
        fig.add_hline(
            y=record['Post_Injury_Avg_Rating'], 
            line_dash='dash', 
            line_color='#059669',
            annotation_text=f"Post-Injury Avg: {record['Post_Injury_Avg_Rating']:.2f}",
            annotation_position='top right'
        )

    # Injury event vertical separator
    fig.add_vline(x=2.5, line_width=2, line_dash='dash', line_color='#DC2626')
    fig.add_annotation(
        x=2.5, y=max([r for r in ratings if pd.notna(r)], default=8) + 0.3,
        text=f"<b>INJURY OCCURRED</b><br>({record['Injury']})",
        showarrow=False,
        font={'color': '#DC2626', 'size': 11}
    )

    fig.update_layout(
        title=f"<b>Performance Trajectory: {selected_player} ({record['Team Name']})</b><br>"
              f"<sup>Injury: {record['Injury']} | Season: {record['Season']} | Days Lost: {record.get('Recovery_Days', 'N/A')}</sup>",
        xaxis_title='Match Sequence',
        yaxis_title='Match Performance Rating (1 - 10)',
        font={'family': 'Segoe UI, sans-serif'},
        template='plotly_white',
        legend={'orientation': 'h', 'y': -0.2, 'x': 0.2},
        yaxis_range=[4.0, 10.0],
        height=450,
        margin={'l': 10, 'r': 20, 't': 70, 'b': 50}
    )
    return fig


def plot_injury_heatmap(df):
    """
    Visual 3: Heatmap
    Injury frequency across calendar months and Premier League clubs.
    Reveals fixture congestion spikes (e.g., December/January winter schedule).
    """
    month_order = [
        'August', 'September', 'October', 'November', 'December',
        'January', 'February', 'March', 'April', 'May', 'June', 'July'
    ]

    heatmap_df = df.dropna(subset=['Injury_Month', 'Club'])
    # Filter months that actually appear in football calendar
    heatmap_data = heatmap_df.groupby(['Club', 'Injury_Month']).size().unstack(fill_value=0)
    
    # Reindex columns to chronologically match football season (Aug -> May)
    existing_months = [m for m in month_order if m in heatmap_data.columns]
    heatmap_data = heatmap_data[existing_months]

    fig = px.imshow(
        heatmap_data,
        labels={'x': 'Calendar Month (Season Flow)', 'y': 'Club', 'color': 'Injuries'},
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale='YlOrRd',
        text_auto=True,
        title='<b>Injury Frequency Across Months and Clubs (Seasonality Heatmap)</b>'
    )

    fig.update_layout(
        xaxis_title='Calendar Month',
        yaxis_title='Premier League Club',
        font={'family': 'Segoe UI, sans-serif'},
        template='plotly_white',
        height=450,
        margin={'l': 10, 'r': 20, 't': 50, 'b': 40}
    )
    return fig


def plot_age_vs_performance_drop(df):
    """
    Visual 4: Scatter Plot
    Player Age vs. Team Performance Drop Index during player absence.
    Segmented by Position Group with an analytical trendline and detailed tooltips.
    """
    scatter_df = df.dropna(subset=['Age', 'Performance_Drop_Index', 'Position_Group']).copy()

    fig = px.scatter(
        scatter_df,
        x='Age',
        y='Performance_Drop_Index',
        color='Position_Group',
        size='FIFA rating',
        hover_name='Player_Name',
        hover_data={
            'Club': True,
            'Injury': True,
            'FIFA rating': True,
            'Performance_Drop_Index': ':.2f',
            'Age': True
        },
        labels={
            'Age': 'Player Age (Years)',
            'Performance_Drop_Index': 'Team Performance Drop Index (Points/Match Lost)',
            'Position_Group': 'Tactical Unit',
            'FIFA rating': 'FIFA Rating'
        },
        title='<b>Player Age vs. Team Performance Drop Index</b><br><sup>Bubble size represents FIFA Rating | Dash line shows overall linear trend</sup>'
    )

    # Add overall trendline using numpy polyfit (eliminating hard dependency on statsmodels)
    if len(scatter_df) > 2:
        x_vals = scatter_df['Age'].values.astype(float)
        y_vals = scatter_df['Performance_Drop_Index'].values.astype(float)
        valid = ~np.isnan(x_vals) & ~np.isnan(y_vals)
        if np.sum(valid) > 2:
            slope, intercept = np.polyfit(x_vals[valid], y_vals[valid], 1)
            x_line = np.linspace(x_vals[valid].min(), x_vals[valid].max(), 50)
            y_line = slope * x_line + intercept
            fig.add_trace(go.Scatter(
                x=x_line,
                y=y_line,
                mode='lines',
                name=f'Trendline (Slope: {slope:+.3f})',
                line={'color': '#1E293B', 'dash': 'dash', 'width': 2.5},
                hoverinfo='skip'
            ))

    fig.update_layout(
        font={'family': 'Segoe UI, sans-serif'},
        template='plotly_white',
        height=480,
        legend={'orientation': 'h', 'y': 1.14, 'x': 0.05},
        margin={'l': 10, 'r': 20, 't': 70, 'b': 40}
    )
    return fig


def get_comeback_leaderboard(df, min_matches=1):
    """
    Visual 5: Leaderboard Table Data
    Identifies players who demonstrated the strongest rating comeback after injury.
    """
    leaderboard = df.dropna(subset=['Rating_Improvement', 'Pre_Injury_Avg_Rating', 'Post_Injury_Avg_Rating']).copy()
    
    summary = leaderboard[[
        'Player_Name', 'Club', 'Position', 'Age', 'Injury', 'Season',
        'Pre_Injury_Avg_Rating', 'Post_Injury_Avg_Rating', 'Rating_Improvement',
        'Recovery_Days'
    ]].sort_values(by='Rating_Improvement', ascending=False)

    summary['Pre_Injury_Avg_Rating'] = summary['Pre_Injury_Avg_Rating'].round(2)
    summary['Post_Injury_Avg_Rating'] = summary['Post_Injury_Avg_Rating'].round(2)
    summary['Rating_Improvement'] = summary['Rating_Improvement'].round(2)

    return summary


def plot_injury_distribution_donut(df):
    """
    Bonus Visual: Donut Chart showing proportion of injuries by clinical category.
    """
    cat_counts = df['Injury_Category'].value_counts().reset_index()
    cat_counts.columns = ['Injury_Category', 'Count']

    fig = px.pie(
        cat_counts,
        values='Count',
        names='Injury_Category',
        hole=0.45,
        title='<b>Injury Breakdown by Anatomical Category</b>',
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        font={'family': 'Segoe UI, sans-serif'},
        template='plotly_white',
        showlegend=False,
        height=400,
        margin={'l': 10, 'r': 10, 't': 40, 'b': 20}
    )
    return fig


def plot_team_outcomes_comparison(df):
    """
    Bonus Visual: Match outcomes (Win%, Draw%, Loss%) across 3 phases:
    Pre-Injury vs. During Absence vs. Post-Injury.
    """
    # Count results before, during, after
    res_before = df[['Match1_before_injury_Result', 'Match2_before_injury_Result', 'Match3_before_injury_Result']].values.flatten()
    res_during = df[['Match1_missed_match_Result', 'Match2_missed_match_Result', 'Match3_missed_match_Result']].values.flatten()
    res_after = df[['Match1_after_injury_Result', 'Match2_after_injury_Result', 'Match3_after_injury_Result']].values.flatten()

    def get_pcts(arr):
        s = pd.Series([str(x).lower().strip() for x in arr if x not in ['N.A.', np.nan, None]])
        counts = s.value_counts(normalize=True) * 100
        return counts.get('win', 0), counts.get('draw', 0), counts.get('lose', 0)

    w_b, d_b, l_b = get_pcts(res_before)
    w_m, d_m, l_m = get_pcts(res_during)
    w_a, d_a, l_a = get_pcts(res_after)

    stages = ['Pre-Injury (With Player)', 'During Absence (Missed Matches)', 'Post-Recovery (Player Returned)']

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Win %', x=stages, y=[w_b, w_m, w_a], marker_color='#10B981'))
    fig.add_trace(go.Bar(name='Draw %', x=stages, y=[d_b, d_m, d_a], marker_color='#F59E0B'))
    fig.add_trace(go.Bar(name='Loss %', x=stages, y=[l_b, l_m, l_a], marker_color='#EF4444'))

    fig.update_layout(
        barmode='stack',
        title='<b>Team Match Outcome Distribution Across Injury Phases</b>',
        yaxis_title='Percentage of Matches (%)',
        font={'family': 'Segoe UI, sans-serif'},
        template='plotly_white',
        legend={'orientation': 'h', 'y': 1.15, 'x': 0.2},
        height=380,
        margin={'l': 10, 'r': 20, 't': 60, 'b': 40}
    )
    return fig
