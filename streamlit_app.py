import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF
from sklearn.preprocessing import MinMaxScaler
import os

# Remixicon CSS import - ensure it loads properly
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/remixicon@4.0.0/fonts/remixicon.css" rel="stylesheet">
<style>
    .remix-icon {
        display: inline-block;
        vertical-align: middle;
        margin-right: 0.3em;
        line-height: 1;
    }
    /* Ensure icons load properly */
    [class^="ri-"], [class*=" ri-"] {
        font-family: 'remixicon' !important;
        font-style: normal;
        font-weight: normal;
        font-variant: normal;
        text-transform: none;
        line-height: 1;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
</style>
""", unsafe_allow_html=True)

# Helper function for Remixicon with better styling
def remix_icon(icon_name, size="1.2em", color="currentColor"):
    return f'<i class="ri-{icon_name} remix-icon" style="font-size: {size}; color: {color};"></i> '

# ---------------------------
# STEP 0: FIXED DATA FILE
# ---------------------------

# Dosya yolu düzeltmesi - hem local hem de cloud için çalışır
if os.path.exists('data/eredivisie_midfielders_clustered.csv'):
    df = pd.read_csv('data/eredivisie_midfielders_clustered.csv')
elif os.path.exists('notebooks/../data/eredivisie_midfielders_clustered.csv'):
    df = pd.read_csv('notebooks/../data/eredivisie_midfielders_clustered.csv')
else:
    st.error("CSV file not found!")
    st.stop()
df = df.dropna(how='all')  # Clean empty rows

# ---------------------------
# STEP 0.5: COLUMN DESCRIPTIONS (English)
# ---------------------------
column_info = {
    "Player": "Player Name",
    "Age": "Age",
    "Pos": "Position",
    "Squad": "Team",
    "Nation": "Nationality",
    "std_MP": "Matches Played",
    "std_Min": "Minutes Played",
    "pass_Cmp%": "Pass Success Rate",
    "pass_PrgDist": "Progressive Pass Distance",
    "pass_KP": "Key Passes",
    "pass_1/3": "Passes into Final Third",
    "pass_PPA": "Passes into Penalty Area",
    "pass_PrgP": "Progressive Passes",
    "passt_TB": "Through Balls",
    "passt_Sw": "Switches",
    "passt_Crs": "Crosses",
    "gca_PassLive": "Goal Creating Actions - Live Pass",
    "gca_PassDead": "Goal Creating Actions - Dead Ball",
    "poss_Carries": "Carries",
    "poss_PrgDist": "Progressive Carry Distance",
    "poss_PrgC": "Progressive Carries",
    "poss_1/3": "Carries into Final Third",
    "poss_CPA": "Carries into Penalty Area",
    "gca_TO": "Goal Creating Actions - Takeouts",
    "gca_Sh": "Goal Creating Actions - Shots",
    "gca_Fld": "Goal Creating Actions - Fouled",
    "def_Tkl": "Tackles",
    "def_TklW": "Tackles Won",
    "def_Int": "Interceptions",
    "def_Tkl+Int": "Tackles + Interceptions",
    "def_Blocks": "Blocks",
    "def_Pass": "Pass Blocks",
    "def_Def 3rd": "Defensive Actions - Def 3rd",
    "def_Mid 3rd": "Defensive Actions - Mid 3rd",
    "def_Att 3rd": "Defensive Actions - Att 3rd",
    "misc_TklW": "Tackles Won (Misc)",
    "misc_Recov": "Ball Recoveries",
    "misc_Won": "Aerial Duels Won",
    "misc_Lost": "Aerial Duels Lost",
    "misc_Fls": "Fouls Committed",
    "misc_Fld": "Fouls Drawn",
    "poss_Mis": "Miscontrols",
    "poss_Dis": "Dispossessed",
    "def_Lost": "Challenges Lost",
    "std_Gls": "Goals",
    "std_Ast": "Assists",
    "std_xG": "Expected Goals (xG)",
    "std_xAG": "Expected Assists (xAG)",
    "std_PrgR": "Progressive Receptions",
    "shoot_Sh": "Shots",
    "std_CrdY": "Yellow Cards",
    "std_CrdR": "Red Cards",
    "std_90s": "90s Played",
    "pt_Min%": "Minutes Played %",
    "pt_Mn/MP": "Minutes per Match",
    "Cluster": "Player Cluster"
}

with st.expander(f"COLUMN DESCRIPTIONS", expanded=False):
    for col, desc in column_info.items():
        st.markdown(f"**{col}**: {desc}", unsafe_allow_html=True)

# ---------------------------
# Cluster Profilleri (Gerçek Veri Analizine Dayalı)
# ---------------------------
cluster_profiles = {
    0: {
        "name": "Elite Creative Attacking Players", 
        "description": """**REAL DATA ANALYSIS:**  
This cluster contains elite-level players. Notable names include Kenneth Taylor (Ajax), Jakob Breum (Go Ahead Eagle), Leo Sauer (NAC Breda), Malik Tillman (PSV), Sem Steijn (Twente).

**STATISTICS:**  
Highest normalized scores for goals and assists are observed. Technical quality is at a superior level.

**CHARACTERISTICS:**  
Players providing the highest creativity and goal contribution. Young stars from big clubs are featured in this group.

**POSITIONS:**  
Offensive midfield, number 10 position, creative central roles are preferred.

**SCOUT NOTE:**  
Highest transfer value group. Players closely monitored by European clubs.""",
        "detailed_stats": {
            "avg_goals": None, "avg_assists": None, "avg_xG": None, "avg_shots": None,
            "avg_age": None, "avg_minutes": None, "top_teams": ["Ajax", "PSV", "Go Ahead Eagle", "NAC Breda", "Twente"],
            "key_strengths": ["Goals", "Assists", "Creativity", "Shots", "xG"], 
            "playing_style": "Attack-focused creative, ability to break opponent defense, effective in final pass"
        }
    },
    1: {
        "name": "Developing Players", 
        "description": """**REAL DATA ANALYSIS:**  
This cluster contains players in development phase (54% - largest group). Players like Antoni Milambo (Feyenoord), Kian Fitz-Jim (Ajax), Jorg Schreuders (Groningen), Johan Hove (Groningen), Joshua Kitolano (Sparta R'dam) are in development stage.

**STATISTICS:**  
Medium-level pass success rates are observed in normalized scores. Profiles still in development phase.

**CHARACTERISTICS:**  
Basic passing ability exists but not yet at creative level. Physical development continues, tactical understanding in learning phase.

**POSITIONS:**  
Central midfield, rotation roles, substitute starting positions are preferred.

**SCOUT NOTE:**  
Names that can show great development within 2-3 years. Potential stars that can be acquired at low cost.""",
        "detailed_stats": {
            "avg_pass_success": None, "avg_playing_time": None,             "avg_minutes": None, "avg_age": None,
            "top_teams": ["Groningen", "Utrecht", "Sparta R'dam", "Feyenoord", "Ajax"], "total_players": 26,
            "key_strengths": ["Rotation Adaptability", "Basic Passing Ability", "Young Age"],
            "playing_style": "Still in development phase, has basic abilities, high growth potential for the future"
        }
    },
    2: {
        "name": "Defensive Engines", 
        "description": """**REAL DATA ANALYSIS:**  
This cluster consists of defensively-minded players. Reliable profiles like Anouar El Azzouzi (Zwolle), Enric Llansana (Go Ahead Eagle), Paxten Aaronson (Utrecht), Dirk Proper (NEC Nijmegen), Espen van Ee (Heerenveen).

**STATISTICS:**  
Highest defensive values are observed in normalized scores. Stands out as the group playing the most minutes.

**CHARACTERISTICS:**  
Constantly running players who don't neglect defensive duties, strong in physical battles.

**POSITIONS:**  
Defensive midfield, number 6-8, holding midfielder positions are preferred.

**SCOUT NOTE:**  
Backbone players of the team. Leader-type, reliable names giving 100% performance every match.""",
        "detailed_stats": {
            "avg_tackles": None, "avg_interceptions": None, "avg_recoveries": None,
            "avg_minutes": None, "avg_age": None, "total_players": 12,
            "top_teams": ["Go Ahead Eagle", "NEC Nijmegen", "Zwolle", "Utrecht", "Heerenveen"],
            "key_strengths": ["Defense", "Ball Recovery", "Endurance"],
            "playing_style": "Destructive midfielder, cleanup specialist, team balance provider"
        }
    }
}

# ---------------------------
# STEP 1: PAGE HEADER INFO
# ---------------------------
st.set_page_config(page_title="Player Analysis", layout="wide")
st.markdown(f"# {remix_icon('football-line', '1.5em')} Eredivisie Under-24 Midfielders Scouting Dashboard", unsafe_allow_html=True)


# General statistics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"{remix_icon('group-line')}**Total Players: 48**", unsafe_allow_html=True)
with col2:
    st.markdown(f"{remix_icon('pie-chart-line')}**Number of Clusters: 3**", unsafe_allow_html=True)
st.markdown(f"### {remix_icon('target-line')}Detailed Cluster Profiles", unsafe_allow_html=True)

for cid, prof in cluster_profiles.items():
    # Calculate real cluster data
    cluster_data = df[df['Cluster'] == cid]
    real_player_count = len(cluster_data)
    
    with st.expander(f"**CLUSTER {cid}: {prof['name']}**"):
        st.markdown(prof['description'], unsafe_allow_html=True)
        
        # Dynamic statistics from real data
        if len(cluster_data) > 0:
            real_avg_age = cluster_data['Age'].mean()
            real_avg_minutes = cluster_data['std_Min'].mean()
            
            # Special performance metrics for each cluster
            if cid == 0:  # Elite Creative Attack
                perf_metric_1 = cluster_data['std_Gls'].mean()
                perf_metric_2 = cluster_data['std_Ast'].mean()
                perf_label_1 = "Average Goals"
                perf_label_2 = "Average Assists"
            elif cid == 1:  # Development Phase
                perf_metric_1 = cluster_data['pass_Cmp%'].mean()
                perf_metric_2 = cluster_data['pt_Min%'].mean()
                perf_label_1 = "Pass Success Score"
                perf_label_2 = "Playing Time Score"
            elif cid == 2:  # Defensive Engine
                perf_metric_1 = cluster_data['def_Tkl'].mean()
                perf_metric_2 = cluster_data['misc_Recov'].mean()
                perf_label_1 = "Average Tackles"
                perf_label_2 = "Ball Recovery"
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**{remix_icon('bar-chart-line')}Basic Statistics**", unsafe_allow_html=True)
                st.metric("Average Age", f"{real_avg_age:.1f}")
                st.metric("Average Minutes", f"{real_avg_minutes:.0f}")
                    
            with col2:
                st.markdown(f"**{remix_icon('football-line')}Performance Metrics**", unsafe_allow_html=True)
                st.caption("*(According to Z-score normalization)*")
                st.metric(perf_label_1, f"{perf_metric_1:.2f}")
                st.metric(perf_label_2, f"{perf_metric_2:.2f}")
                    
            with col3:
                st.markdown(f"**{remix_icon('trophy-line')}Top Teams by Player Count**", unsafe_allow_html=True)
                top_teams = cluster_data['Squad'].value_counts().head(3)
                for team, count in top_teams.items():
                    st.markdown(f"{remix_icon('team-line')}{team} ({count} players)", unsafe_allow_html=True)
        else:
            st.markdown(f":information_source: {remix_icon('information-line')} No players found in this cluster after filtering.", unsafe_allow_html=True)
                        
        st.markdown(f"**{remix_icon('gamepad-line')}Playing Style**: {prof['detailed_stats'].get('playing_style', 'General midfielder')}", unsafe_allow_html=True)
        
        if 'key_strengths' in prof['detailed_stats']:
            st.markdown(f"**{remix_icon('sword-line')}Key Strengths**: {', '.join(prof['detailed_stats']['key_strengths'])}", unsafe_allow_html=True)

# ---------------------------
# STEP 2: FILTERS & PLAYER SEARCH
# ---------------------------
st.markdown(f"## {remix_icon('filter-line')}Filtering and Player Search", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    age_filter = st.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (18, 24))
with col2:
    pos_filter = st.multiselect("Position", sorted(df["Pos"].unique()), default=df["Pos"].unique())
with col3:
    squad_filter = st.multiselect("Team", sorted(df["Squad"].unique()), default=df["Squad"].unique())
with col4:
    cluster_filter = st.multiselect("Select Cluster", sorted(df["Cluster"].unique()), default=df["Cluster"].unique())
with col5:
    player_search = st.text_input("Search Player (Name)")

df_filtered = df[
    (df["Age"] >= age_filter[0]) &
    (df["Age"] <= age_filter[1]) &
    (df["Pos"].isin(pos_filter)) &
    (df["Squad"].isin(squad_filter)) &
    (df["Cluster"].isin(cluster_filter))
]

if player_search:
    df_filtered = df_filtered[df_filtered["Player"].str.contains(player_search, case=False, na=False)]

st.dataframe(df_filtered)


# ---------------------------
# STEP 4: TOP 5 PLAYERS BY CLUSTER
# ---------------------------
st.markdown(f"# {remix_icon('medal-line')}Top 5 Players by Cluster", unsafe_allow_html=True)

# Metric sets suitable for cluster profiles (New 3 Clusters)
cluster_metrics_map = {
    0: ['std_Gls','std_Ast','std_xG','std_xAG','pass_KP','shoot_Sh','gca_PassLive'],      # Super Stars: goals + assists + creativity + shots
    1: ['std_Min','pass_Cmp%','pt_Min%','misc_Won','std_MP'],                           # Developing: playing time + basic passing + duels
    2: ['def_Tkl','def_TklW','def_Int','def_Blocks','misc_Recov','misc_TklW','poss_PrgDist'] # Hard Workers: defense + ball recovery + physical power
}

# Calculate according to current filters
df_rank = df_filtered.copy()

for cid, metrics in cluster_metrics_map.items():
    st.subheader(f"Cluster {cid}: {cluster_profiles[cid]['name']}")
    
    # Calculate cluster statistics from real data
    cluster_data = df_filtered[df_filtered['Cluster'] == cid]
    
    # Show individual standout features of top 5 players
    if len(cluster_data) > 0:
        st.markdown(f"**{remix_icon('star-line')}Outstanding Features of Top 5 Players:**", unsafe_allow_html=True)
        
        # Determine best players by cluster directly from CSV
        if cid == 0:  # Elite Creative Attack
            # Highest goal+assist combination
            cluster_data_sorted = cluster_data.copy()
            cluster_data_sorted['combined_score'] = cluster_data_sorted['std_Gls'] + cluster_data_sorted['std_Ast']
            top_5 = cluster_data_sorted.nlargest(5, 'combined_score')
            
            for idx, (_, player) in enumerate(top_5.iterrows(), 1):
                # Make specific comments for each player
                gol = player['std_Gls']
                asist = player['std_Ast']
                xg = player['std_xG']
                
                # Generate comments
                comment = ""
                if gol > 1.5 and asist > 1.0:
                    comment = f"{remix_icon('fire-line')}**Elite finisher and creator** - Both scores goals and provides assists"
                elif gol > 2.0:
                    comment = f"{remix_icon('football-line')}**Super goalscorer** - Team's most reliable goal machine"
                elif asist > 1.5:
                    comment = f"{remix_icon('crosshair-line')}**Playmaker** - Constantly sets up teammates for goals"
                elif xg > 2.0:
                    comment = f"{remix_icon('line-chart-line')}**High potential** - Statistically gets into very effective positions"
                else:
                    comment = f"{remix_icon('star-line')}**Balanced player** - Versatile profile contributing in many areas"
                    
                st.write(f"**{idx}. {player['Player']}**: {comment}", unsafe_allow_html=True)
                
        elif cid == 1:  # Development Phase
            # Highest pass success + playing time
            cluster_data_sorted = cluster_data.copy()
            cluster_data_sorted['combined_score'] = cluster_data_sorted['pass_Cmp%'] + (cluster_data_sorted['std_Min'] / 1000)  # Normalize minutes
            top_5 = cluster_data_sorted.nlargest(5, 'combined_score')
            
            for idx, (_, player) in enumerate(top_5.iterrows(), 1):
                # Make specific comments for each player
                pas_success = player['pass_Cmp%']
                minutes = player['std_Min']
                play_ratio = player['pt_Min%']
                
                # Generate comments
                comment = ""
                if minutes > 2000 and pas_success > 0.5:
                    comment = f"{remix_icon('star-line')}**Experienced reliable** - Plays a lot and has high pass quality"
                elif minutes > 2000:
                    comment = f"{remix_icon('heart-pulse-line')}**Hard-working engine** - Constantly plays in the team, gaining experience"
                elif pas_success > 0.8:
                    comment = f"{remix_icon('crosshair-line')}**Technical ability** - Very high pass quality, reliable"
                elif play_ratio > 0.5:
                    comment = f"{remix_icon('trending-up-line')}**Rising value** - Has gained coach's trust, potential"
                else:
                    comment = f"{remix_icon('seedling-line')}**Promising future** - Still raw but open to development profile"
                    
                st.write(f"**{idx}. {player['Player']}**: {comment}", unsafe_allow_html=True)
                
        elif cid == 2:  # Defensive Engine
            # Highest defensive contribution
            cluster_data_sorted = cluster_data.copy()
            cluster_data_sorted['combined_score'] = cluster_data_sorted['def_Tkl'] + cluster_data_sorted['misc_Recov']
            top_5 = cluster_data_sorted.nlargest(5, 'combined_score')
            
            for idx, (_, player) in enumerate(top_5.iterrows(), 1):
                # Make specific comments for each player
                tackles = player['def_Tkl']
                interceptions = player['def_Int']
                recoveries = player['misc_Recov']
                
                # Generate comments
                comment = ""
                if tackles > 2.5 and recoveries > 2.5:
                    comment = f"{remix_icon('shield-line')}**Defensive wall** - Both aggressive and intelligent defending"
                elif tackles > 3.0:
                    comment = f"{remix_icon('sword-line')}**Aggressive warrior** - Fighting style that doesn't let opponents breathe"
                elif recoveries > 3.0:
                    comment = f"{remix_icon('brain-line')}**Smart cleaner** - Master of ball recovery through positioning"
                elif interceptions > 2.0:
                    comment = f"{remix_icon('eye-line')}**Game reader** - Intelligent defender who intercepts opponent passes"
                else:
                    comment = f"{remix_icon('tools-line')}**Reliable worker** - Quiet but effective, team's indispensable"
                    
                st.write(f"**{idx}. {player['Player']}**: {comment}", unsafe_allow_html=True)
    
    st.caption(f"**Playing Style**: {cluster_profiles[cid]['detailed_stats'].get('playing_style', 'General midfield players')}")

    # Is this cluster available in selected filter?
    if cid not in df_rank["Cluster"].unique():
        st.markdown(f":information_source: {remix_icon('information-line')} No players found in this cluster matching filtering criteria.", unsafe_allow_html=True)
        continue

    # Only available metrics
    available_metrics = [m for m in metrics if m in df_rank.columns]
    if not available_metrics:
        st.markdown(f":warning: {remix_icon('alert-line')} No valid metrics found for this cluster.", unsafe_allow_html=True)
        continue

    # Normalization
    scaler_rank = MinMaxScaler()
    scaled_vals = scaler_rank.fit_transform(df_rank[available_metrics])
    score = scaled_vals.mean(axis=1)  # Equal weight: you can add weighting if desired

    # Score series
    df_rank[f"Cluster{cid}_Score"] = score

    # Top 5 in this cluster
    top_players = df_rank[df_rank["Cluster"] == cid].nlargest(5, f"Cluster{cid}_Score")

    # Columns to display
    show_cols = ["Player","Age","Pos","Squad",f"Cluster{cid}_Score"] + available_metrics
    renamed_cols = {col: column_info.get(col, col) for col in show_cols}

    st.dataframe(top_players[show_cols].rename(columns=renamed_cols))
# ---------------------------
# STEP 3: RADAR + SIMILAR PLAYERS + CLUSTER PROFILE
# ---------------------------
st.markdown(f"## {remix_icon('radar-line')}Professional Radar Chart, Similar Players and Cluster Profile", unsafe_allow_html=True)

# Initial radar metrics
radar_metrics = ['std_MP','std_Min','std_90s','std_Gls','std_Ast','std_xG','std_xAG','misc_Fls','std_CrdY','std_CrdR']

player_select = st.multiselect("Select Player (Multiple selection possible)", df_filtered["Player"].unique(), default=[], key="player_select")

def update_player_view(selected_players):
    if not selected_players:
        st.markdown(f":information_source: {remix_icon('information-line')} Please select the player(s) you want to analyze.", unsafe_allow_html=True)
        return
        
    # Get data of selected players
    selected_rows = df_filtered[df_filtered["Player"].isin(selected_players)]
    if selected_rows.empty:
        st.markdown(f":warning: {remix_icon('alert-line')} Selected players are outside filtering criteria.", unsafe_allow_html=True)
        return

    # Cluster information of selected players
    unique_clusters = selected_rows["Cluster"].unique()
    
    # Show cluster information
    for cluster_id in unique_clusters:
        players_in_cluster = selected_rows[selected_rows["Cluster"] == cluster_id]["Player"].tolist()
        st.write(f"**Cluster {cluster_id}: {cluster_profiles[cluster_id]['name']}** → {', '.join(players_in_cluster)}")
        st.caption(cluster_profiles[cluster_id]['description'])

    # ---------------------------
    # 1️⃣ Multi-Player vs Cluster Radar
    # ---------------------------
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_filtered[radar_metrics]), columns=radar_metrics, index=df_filtered.index)

    metrics_tr = [column_info[m] for m in radar_metrics]
    
    fig_radar = go.Figure()
    
    # Player colors
    player_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']
    
    # Add trace for each player
    for idx, player_name in enumerate(selected_players):
        player_row = selected_rows[selected_rows["Player"] == player_name]
        if not player_row.empty:
            player_scaled = df_scaled.loc[player_row.index[0]]
            color = player_colors[idx % len(player_colors)]
            # Create closed polygon by adding first value to the end
            r_values = list(player_scaled.values) + [player_scaled.values[0]]
            theta_values = metrics_tr + [metrics_tr[0]]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=r_values, 
                theta=theta_values, 
                fill='toself', 
                name=player_name, 
                line=dict(color=color, width=3)
            ))
    
    # Add cluster averages
    cluster_colors = ['#F97316', '#EC4899', '#06B6D4']  # For 3 clusters: Orange, Pink, Turquoise
    for idx, cluster_id in enumerate(unique_clusters):
        cluster_mean_scaled = df_scaled[df_filtered["Cluster"] == cluster_id].mean()
        cluster_color = cluster_colors[cluster_id % len(cluster_colors)]
        # Create closed polygon by adding first value to the end
        r_cluster_values = list(cluster_mean_scaled.values) + [cluster_mean_scaled.values[0]]
        theta_cluster_values = metrics_tr + [metrics_tr[0]]
        
        fig_radar.add_trace(go.Scatterpolar(
            r=r_cluster_values, 
            theta=theta_cluster_values, 
            fill='toself', 
            name=f"Cluster {cluster_id} Average", 
            line=dict(color=cluster_color, width=3, dash='dot'), 
            opacity=0.6,
            visible='legendonly'
        ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        showlegend=True, 
        title="Selected Players vs Cluster Averages",
        template='plotly_dark', 
        title_font=dict(size=20), 
        legend=dict(font=dict(size=12))
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # ---------------------------
    # 2️⃣ Category-Based Radars
    # ---------------------------
    categories = {
        "Playing Time / Participation": ['std_MP','std_Min','std_90s','pt_Min%','pt_Mn/MP'],
        "Passing / Playmaking": ['pass_Cmp%','pass_PrgDist','pass_KP','pass_1/3','pass_PPA','pass_PrgP','passt_TB','passt_Sw','passt_Crs','gca_PassLive','gca_PassDead','gca_TO'],
        "Ball Carrying / Progressive Play": ['poss_Carries','poss_PrgDist','poss_PrgC','poss_1/3','poss_CPA','gca_Sh','gca_Fld'],
        "Shooting / Goal Contribution": ['std_Gls','std_Ast','std_xG','std_xAG','shoot_Sh'],
        "Defensive Actions / Defense": ['def_Tkl','def_TklW','def_Int','def_Tkl+Int','def_Blocks','def_Pass','def_Def 3rd','def_Mid 3rd','def_Att 3rd','misc_TklW','misc_Recov','misc_Won','def_Lost'],
        "Mistakes / Discipline": ['misc_Lost','misc_Fls','misc_Fld','std_CrdY','std_CrdR','poss_Mis','poss_Dis']
    }

    for category, cat_metrics in categories.items():
        st.subheader(category)
        cat_metrics_available = [m for m in cat_metrics if m in df_filtered.columns]
        cat_metrics_tr = [column_info[m] for m in cat_metrics_available]
        
        if not cat_metrics_tr:
            continue
            
        # Scaling for category
        cat_scaler = MinMaxScaler()
        df_cat_scaled = pd.DataFrame(
            cat_scaler.fit_transform(df_filtered[cat_metrics_available]),
            columns=cat_metrics_tr, 
            index=df_filtered.index
        )

        fig_cat = go.Figure()
        
        # Add trace for each player
        for idx, player_name in enumerate(selected_players):
            player_row = selected_rows[selected_rows["Player"] == player_name]
            if not player_row.empty:
                player_scaled_cat = df_cat_scaled.loc[player_row.index[0]]
                color = player_colors[idx % len(player_colors)]
                # Create closed polygon by adding first value to the end
                r_cat_values = list(player_scaled_cat.values) + [player_scaled_cat.values[0]]
                theta_cat_values = cat_metrics_tr + [cat_metrics_tr[0]]
                
                fig_cat.add_trace(go.Scatterpolar(
                    r=r_cat_values, 
                    theta=theta_cat_values, 
                    fill='toself', 
                    name=player_name, 
                    line=dict(color=color, width=3)
                ))
        
        # Add cluster averages
        for idx, cluster_id in enumerate(unique_clusters):
            cluster_mean_cat = df_cat_scaled[df_filtered["Cluster"] == cluster_id].mean()
            cluster_color = cluster_colors[cluster_id % len(cluster_colors)]
            # Create closed polygon by adding first value to the end
            r_cat_cluster_values = list(cluster_mean_cat.values) + [cluster_mean_cat.values[0]]
            theta_cat_cluster_values = cat_metrics_tr + [cat_metrics_tr[0]]
            
            fig_cat.add_trace(go.Scatterpolar(
                r=r_cat_cluster_values, 
                theta=theta_cat_cluster_values, 
                fill='toself', 
                name=f"Cluster {cluster_id} Average", 
                line=dict(color=cluster_color, width=3, dash='dot'), 
                opacity=0.6,
                visible='legendonly'
            ))

        fig_cat.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,1])),
            showlegend=True,
            template='plotly_dark',
            title=f"{category} - Selected Players vs Cluster Averages",
            title_font=dict(size=20),
            legend=dict(font=dict(size=12))
        )
        st.plotly_chart(fig_cat, use_container_width=True)

        

    # ---------------------------
    # 3️⃣ Similar Players
    # ---------------------------
    st.markdown(f"## {remix_icon('user-search-line')}Similar Players", unsafe_allow_html=True)
    
    # Find similar players for each selected player
    for player_name in selected_players:
        player_row = selected_rows[selected_rows["Player"] == player_name]
        if not player_row.empty:
            df_metrics = df_filtered[radar_metrics].copy()
            selected_vector = player_row[radar_metrics].values.flatten()
            df_temp = df_filtered.copy()
            df_temp["Similarity"] = np.linalg.norm(df_metrics.values - selected_vector, axis=1)
            similar_players = df_temp[df_temp["Player"] != player_name].nsmallest(5, "Similarity")
            
            st.write(f"5 most similar players to **{player_name}**:")
            st.dataframe(similar_players[["Player","Pos","Squad","Age","Cluster"] + radar_metrics])

    # ---------------------------
    # 4️⃣ Compare All Clusters
    # ---------------------------
    st.markdown(f"## {remix_icon('pie-chart-line')}Compare All Clusters", unsafe_allow_html=True)
    df_scaled_all = pd.DataFrame(MinMaxScaler().fit_transform(df_filtered[radar_metrics]),
                                 columns=radar_metrics, index=df_filtered.index)
    cluster_means_scaled = df_scaled_all.groupby(df_filtered["Cluster"]).mean()
    fig_all = go.Figure()
    colors = ['#F97316','#EC4899','#06B6D4']  # For 3 clusters: Orange, Pink, Turquoise
    for idx, (cid,row) in enumerate(cluster_means_scaled.iterrows()):
        # Create closed polygon by adding first value to the end
        r_all_values = list(row.values) + [row.values[0]]
        theta_all_values = [column_info[m] for m in radar_metrics] + [column_info[radar_metrics[0]]]
        
        fig_all.add_trace(go.Scatterpolar(
            r=r_all_values,
            theta=theta_all_values,
            fill='toself',
            name=f"Cluster {cid}",
            line=dict(width=2,color=colors[idx%len(colors)]),
            opacity=0.7
        ))
    fig_all.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        showlegend=True,
        title="Comparison of All Clusters",
        template='plotly_dark'
    )
    st.plotly_chart(fig_all, use_container_width=True, key="all_clusters_radar")

    # ---------------------------
    # 5️⃣ PDF / Excel Report
    # ---------------------------
    st.markdown(f"## {remix_icon('download-line')}Download Report", unsafe_allow_html=True)
    
    if len(selected_players) == 1:
        # Current format for single player
        player_name = selected_players[0]
        player_row = selected_rows[selected_rows["Player"] == player_name]
        df_metrics = df_filtered[radar_metrics].copy()
        selected_vector = player_row[radar_metrics].values.flatten()
        df_temp = df_filtered.copy()
        df_temp["Similarity"] = np.linalg.norm(df_metrics.values - selected_vector, axis=1)
        similar_players = df_temp[df_temp["Player"] != player_name].nsmallest(5, "Similarity")
        
        # Excel
        excel_buffer = BytesIO()
        similar_players.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(label=f"{player_name} - Download Similar Players Excel",
                           data=excel_buffer,
                           file_name=f"{player_name}_similar_players.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{player_name} - Similar Players", ln=True)
        for idx, row in similar_players.iterrows():
            line = f"{row['Player']} | {row['Pos']} | {row['Squad']} | Cluster {row['Cluster']}"
            pdf.cell(200, 10, txt=line, ln=True)
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label=f"{player_name} - Download Similar Players PDF",
                           data=pdf_output,
                           file_name=f"{player_name}_similar_players.pdf",
                           mime="application/pdf")
    
    elif len(selected_players) > 1:
        # Comparison report for multiple players
        comparison_data = selected_rows[["Player","Pos","Squad","Age","Cluster"] + radar_metrics]
        
        # Excel
        excel_buffer = BytesIO()
        comparison_data.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(label="Selected Players Comparison - Download Excel",
                           data=excel_buffer,
                           file_name=f"player_comparison_{len(selected_players)}_players.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Player Comparison - {len(selected_players)} Players", ln=True)
        pdf.ln(5)
        for idx, row in comparison_data.iterrows():
            line = f"{row['Player']} | {row['Pos']} | {row['Squad']} | Age: {row['Age']} | Cluster: {row['Cluster']}"
            pdf.cell(200, 10, txt=line, ln=True)
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="Selected Players Comparison - Download PDF",
                           data=pdf_output,
                           file_name=f"player_comparison_{len(selected_players)}_players.pdf",
                           mime="application/pdf")

update_player_view(player_select)

# ---------------------------
# STEP 6: SCATTER PLOT ANALYSES
# ---------------------------
st.markdown(f"# {remix_icon('scatter-chart-line')}Advanced Scatter Plot Analyses", unsafe_allow_html=True)
st.markdown("Explore relationships between different player metrics through interactive scatter plots.")

# Create tabs for different scatter plot analyses
tab1, tab2, tab3, tab4 = st.tabs([
    f"Age vs Performance", 
    f"Minutes vs Effectiveness",
    f"Passing vs Creativity", 
    f"Defense vs Attack"
])

with tab1:
    st.markdown(f"### {remix_icon('user-line')}Age vs Performance Analysis", unsafe_allow_html=True)
    st.markdown("Analyze how player age correlates with goal and assist performance.")
    
    # Age vs Performance Scatter Plot
    fig_age = go.Figure()
    
    # Color by cluster
    cluster_colors_scatter = {0: '#F97316', 1: '#EC4899', 2: '#06B6D4'}
    cluster_names = {0: 'Elite Creative', 1: 'Developing', 2: 'Defensive Engines'}
    
    for cluster_id in df_filtered['Cluster'].unique():
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        
        fig_age.add_trace(go.Scatter(
            x=cluster_data['Age'],
            y=cluster_data['std_Gls'] + cluster_data['std_Ast'],
            mode='markers',
            name=f'Cluster {cluster_id}: {cluster_names[cluster_id]}',
            text=cluster_data['Player'] + '<br>' + cluster_data['Squad'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Age: %{x}<br>' +
                         'Goals + Assists: %{y:.2f}<br>' +
                         '<extra></extra>',
            marker=dict(
                size=10,
                color=cluster_colors_scatter[cluster_id],
                opacity=0.7,
                line=dict(width=1, color='white')
            )
        ))
    
    fig_age.update_layout(
        title="Age vs Total Goal Contributions (Goals + Assists)",
        xaxis_title="Age",
        yaxis_title="Goals + Assists",
        template='plotly_dark',
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig_age, use_container_width=True)
    
    # Age insights
    col1, col2 = st.columns(2)
    with col1:
        youngest_top_performer = df_filtered.loc[df_filtered['std_Gls'] + df_filtered['std_Ast'] > 1.5, 'Age'].min()
        st.metric("Youngest High Performer Age", f"{youngest_top_performer:.0f}" if not pd.isna(youngest_top_performer) else "N/A")
    with col2:
        avg_age_top_performers = df_filtered[df_filtered['std_Gls'] + df_filtered['std_Ast'] > 1.0]['Age'].mean()
        st.metric("Avg Age of Top Contributors", f"{avg_age_top_performers:.1f}" if not pd.isna(avg_age_top_performers) else "N/A")

with tab2:
    st.markdown(f"### {remix_icon('dashboard-line')}Playing Time vs Effectiveness", unsafe_allow_html=True)
    st.markdown("Examine the relationship between minutes played and expected goal contributions.")
    
    # Minutes vs Effectiveness Scatter Plot
    fig_minutes = go.Figure()
    
    for cluster_id in df_filtered['Cluster'].unique():
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        
        fig_minutes.add_trace(go.Scatter(
            x=cluster_data['std_Min'],
            y=cluster_data['std_xG'] + cluster_data['std_xAG'],
            mode='markers',
            name=f'Cluster {cluster_id}: {cluster_names[cluster_id]}',
            text=cluster_data['Player'] + '<br>' + cluster_data['Squad'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Minutes: %{x}<br>' +
                         'xG + xAG: %{y:.2f}<br>' +
                         '<extra></extra>',
            marker=dict(
                size=10,
                color=cluster_colors_scatter[cluster_id],
                opacity=0.7,
                line=dict(width=1, color='white')
            )
        ))
    
    fig_minutes.update_layout(
        title="Playing Time vs Expected Goal Contributions (xG + xAG)",
        xaxis_title="Minutes Played",
        yaxis_title="Expected Goals + Expected Assists",
        template='plotly_dark',
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig_minutes, use_container_width=True)
    
    # Minutes insights
    col1, col2 = st.columns(2)
    with col1:
        # Calculate efficiency and find the most efficient player
        eligible_players = df_filtered[df_filtered['std_Min'] > 1000].copy()
        if not eligible_players.empty:
            eligible_players['efficiency'] = (eligible_players['std_xG'] + eligible_players['std_xAG']) / eligible_players['std_Min'] * 1000
            efficiency_leader_idx = eligible_players['efficiency'].idxmax()
            efficiency_leader = df_filtered.loc[efficiency_leader_idx]
            st.metric("Most Efficient Player", efficiency_leader['Player'])
        else:
            st.metric("Most Efficient Player", "N/A")
    with col2:
        avg_minutes = df_filtered['std_Min'].mean()
        st.metric("Average Minutes Played", f"{avg_minutes:.0f}")

with tab3:
    st.markdown(f"### {remix_icon('route-line')}Passing Accuracy vs Creativity", unsafe_allow_html=True)
    st.markdown("Discover the balance between safe passing and creative playmaking.")
    
    # Passing vs Creativity Scatter Plot
    fig_passing = go.Figure()
    
    for cluster_id in df_filtered['Cluster'].unique():
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        
        fig_passing.add_trace(go.Scatter(
            x=cluster_data['pass_Cmp%'],
            y=cluster_data['pass_KP'],
            mode='markers',
            name=f'Cluster {cluster_id}: {cluster_names[cluster_id]}',
            text=cluster_data['Player'] + '<br>' + cluster_data['Squad'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Pass Success: %{x:.1%}<br>' +
                         'Key Passes: %{y:.2f}<br>' +
                         '<extra></extra>',
            marker=dict(
                size=10,
                color=cluster_colors_scatter[cluster_id],
                opacity=0.7,
                line=dict(width=1, color='white')
            )
        ))
    
    fig_passing.update_layout(
        title="Passing Accuracy vs Key Passes",
        xaxis_title="Pass Completion Rate",
        yaxis_title="Key Passes per Game",
        template='plotly_dark',
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig_passing, use_container_width=True)
    
    # Passing insights
    col1, col2 = st.columns(2)
    with col1:
        if not df_filtered.empty and 'pass_Cmp%' in df_filtered.columns:
            best_passer_idx = df_filtered['pass_Cmp%'].idxmax()
            best_passer = df_filtered.loc[best_passer_idx]
            st.metric("Most Accurate Passer", f"{best_passer['Player']} ({best_passer['pass_Cmp%']:.1%})")
        else:
            st.metric("Most Accurate Passer", "N/A")
    with col2:
        if not df_filtered.empty and 'pass_KP' in df_filtered.columns:
            most_creative_idx = df_filtered['pass_KP'].idxmax()
            most_creative = df_filtered.loc[most_creative_idx]
            st.metric("Most Creative Player", f"{most_creative['Player']} ({most_creative['pass_KP']:.1f} KP)")
        else:
            st.metric("Most Creative Player", "N/A")

with tab4:
    st.markdown(f"### {remix_icon('sword-line')}Defensive vs Offensive Contributions", unsafe_allow_html=True)
    st.markdown("Compare players' defensive work rate with their attacking output.")
    
    # Defense vs Attack Scatter Plot
    fig_def_att = go.Figure()
    
    for cluster_id in df_filtered['Cluster'].unique():
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        
        fig_def_att.add_trace(go.Scatter(
            x=cluster_data['def_Tkl'] + cluster_data['def_Int'],
            y=cluster_data['std_Gls'] + cluster_data['std_Ast'],
            mode='markers',
            name=f'Cluster {cluster_id}: {cluster_names[cluster_id]}',
            text=cluster_data['Player'] + '<br>' + cluster_data['Squad'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Tackles + Interceptions: %{x:.2f}<br>' +
                         'Goals + Assists: %{y:.2f}<br>' +
                         '<extra></extra>',
            marker=dict(
                size=10,
                color=cluster_colors_scatter[cluster_id],
                opacity=0.7,
                line=dict(width=1, color='white')
            )
        ))
    
    fig_def_att.update_layout(
        title="Defensive Actions vs Offensive Contributions",
        xaxis_title="Tackles + Interceptions per Game",
        yaxis_title="Goals + Assists per Game",
        template='plotly_dark',
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig_def_att, use_container_width=True)
    
    # Defense vs Attack insights
    col1, col2 = st.columns(2)
    with col1:
        if not df_filtered.empty:
            defensive_actions = df_filtered['def_Tkl'] + df_filtered['def_Int']
            best_defender_idx = defensive_actions.idxmax()
            best_defender = df_filtered.loc[best_defender_idx]
            st.metric("Best Defender", f"{best_defender['Player']} ({defensive_actions.loc[best_defender_idx]:.1f})")
        else:
            st.metric("Best Defender", "N/A")
    with col2:
        if not df_filtered.empty:
            balance_score = ((df_filtered['def_Tkl'] + df_filtered['def_Int']) * 
                           (df_filtered['std_Gls'] + df_filtered['std_Ast']))
            most_balanced_idx = balance_score.idxmax()
            most_balanced = df_filtered.loc[most_balanced_idx]
            st.metric("Most Balanced Player", most_balanced['Player'])
        else:
            st.metric("Most Balanced Player", "N/A")

# Summary insights section
st.markdown(f"## {remix_icon('lightbulb-line')}Key Insights from Scatter Analysis", unsafe_allow_html=True)

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown(f"### {remix_icon('trending-up-line')}Performance Trends", unsafe_allow_html=True)
    
    # Calculate correlations
    age_performance_corr = df_filtered['Age'].corr(df_filtered['std_Gls'] + df_filtered['std_Ast'])
    minutes_effectiveness_corr = df_filtered['std_Min'].corr(df_filtered['std_xG'] + df_filtered['std_xAG'])
    
    st.write(f"• **Age-Performance Correlation**: {age_performance_corr:.3f}")
    st.write(f"• **Minutes-Effectiveness Correlation**: {minutes_effectiveness_corr:.3f}")
    
    if age_performance_corr > 0.1:
        st.success("Older players tend to be more productive")
    elif age_performance_corr < -0.1:
        st.info("Younger players show higher goal contributions")
    else:
        st.info("Age has minimal impact on performance")

with insights_col2:
    st.markdown(f"### {remix_icon('award-line')}Standout Players", unsafe_allow_html=True)
    
    # Find standout players in different categories
    young_players = df_filtered[df_filtered['Age'] <= 20]
    if not young_players.empty:
        top_young_talent = young_players.nlargest(1, 'std_Gls')
        if not top_young_talent.empty:
            st.write(f"• **Top Young Talent**: {top_young_talent.iloc[0]['Player']} (Age {top_young_talent.iloc[0]['Age']:.0f})")
    else:
        st.write("• **Top Young Talent**: No players ≤20 years old")
    
    experienced_players = df_filtered[df_filtered['std_Min'] > 1000]
    if not experienced_players.empty:
        most_efficient = experienced_players.nlargest(1, 'std_xG')
        if not most_efficient.empty:
            st.write(f"• **Most Clinical Finisher**: {most_efficient.iloc[0]['Player']} ({most_efficient.iloc[0]['std_xG']:.2f} xG)")
    else:
        st.write("• **Most Clinical Finisher**: No players with >1000 minutes")
    
    # Best two-way player
    if not df_filtered.empty:
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy['two_way_score'] = (df_filtered_copy['std_Gls'] + df_filtered_copy['std_Ast']) * (df_filtered_copy['def_Tkl'] + df_filtered_copy['def_Int'])
        best_two_way = df_filtered_copy.nlargest(1, 'two_way_score')
        
        if not best_two_way.empty:
            st.write(f"• **Best Two-Way Player**: {best_two_way.iloc[0]['Player']}")
    else:
        st.write("• **Best Two-Way Player**: No data available")

# ---------------------------
# STEP 7: LINE CHART/TREND ANALYSES
# ---------------------------
st.markdown(f"# {remix_icon('line-chart-line')}Trend & Line Chart Analyses", unsafe_allow_html=True)
st.markdown("Discover performance trends across different dimensions with interactive line charts.")

# Create tabs for different trend analyses
trend_tab1, trend_tab2, trend_tab3= st.tabs([
    "Age Trends", 
    "Playing Time Trends",
    "Team Performance Trends", 
])

with trend_tab1:
    st.markdown(f"### {remix_icon('user-line')}Performance Trends by Age", unsafe_allow_html=True)
    st.markdown("Analyze how different performance metrics change with player age.")
    
    # Age trend analysis
    age_groups = df_filtered.groupby('Age').agg({
        'std_Gls': 'mean',
        'std_Ast': 'mean', 
        'std_xG': 'mean',
        'std_xAG': 'mean',
        'pass_KP': 'mean',
        'def_Tkl': 'mean',
        'def_Int': 'mean',
        'Player': 'count'
    }).reset_index()
    age_groups.rename(columns={'Player': 'Player_Count'}, inplace=True)
    
    # Filter out ages with very few players (less than 2)
    age_groups = age_groups[age_groups['Player_Count'] >= 2]
    
    if not age_groups.empty:
        # Create line chart for offensive metrics
        fig_age_trend = go.Figure()
        
        fig_age_trend.add_trace(go.Scatter(
            x=age_groups['Age'],
            y=age_groups['std_Gls'],
            mode='lines+markers',
            name='Goals per Game',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8)
        ))
        
        fig_age_trend.add_trace(go.Scatter(
            x=age_groups['Age'],
            y=age_groups['std_Ast'],
            mode='lines+markers',
            name='Assists per Game',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=8)
        ))
        
        fig_age_trend.add_trace(go.Scatter(
            x=age_groups['Age'],
            y=age_groups['pass_KP'],
            mode='lines+markers',
            name='Key Passes per Game',
            line=dict(color='#45B7D1', width=3),
            marker=dict(size=8)
        ))
        
        fig_age_trend.update_layout(
            title="Offensive Performance Trends by Age",
            xaxis_title="Age",
            yaxis_title="Average per Game",
            template='plotly_dark',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_age_trend, use_container_width=True)
        
        # Defensive trends by age
        fig_age_def = go.Figure()
        
        fig_age_def.add_trace(go.Scatter(
            x=age_groups['Age'],
            y=age_groups['def_Tkl'],
            mode='lines+markers',
            name='Tackles per Game',
            line=dict(color='#96CEB4', width=3),
            marker=dict(size=8)
        ))
        
        fig_age_def.add_trace(go.Scatter(
            x=age_groups['Age'],
            y=age_groups['def_Int'],
            mode='lines+markers',
            name='Interceptions per Game',
            line=dict(color='#FFEAA7', width=3),
            marker=dict(size=8)
        ))
        
        fig_age_def.update_layout(
            title="Defensive Performance Trends by Age",
            xaxis_title="Age",
            yaxis_title="Average per Game",
            template='plotly_dark',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_age_def, use_container_width=True)
        
        # Age insights
        col1, col2, col3 = st.columns(3)
        with col1:
            peak_goal_age = age_groups.loc[age_groups['std_Gls'].idxmax(), 'Age']
            st.metric("Peak Goal Scoring Age", f"{peak_goal_age:.0f}")
        with col2:
            peak_assist_age = age_groups.loc[age_groups['std_Ast'].idxmax(), 'Age']
            st.metric("Peak Assist Age", f"{peak_assist_age:.0f}")
        with col3:
            peak_defense_age = age_groups.loc[(age_groups['def_Tkl'] + age_groups['def_Int']).idxmax(), 'Age']
            st.metric("Peak Defensive Age", f"{peak_defense_age:.0f}")
    else:
        st.info("Not enough data for age trend analysis")

with trend_tab2:
    st.markdown(f"### {remix_icon('timer-line')}Performance vs Playing Time", unsafe_allow_html=True)
    st.markdown("Examine how performance metrics correlate with minutes played.")
    
    # Create minutes bins for trend analysis
    df_minutes = df_filtered.copy()
    df_minutes['Minutes_Bin'] = pd.cut(df_minutes['std_Min'], 
                                      bins=5, 
                                      labels=['0-500', '500-1000', '1000-1500', '1500-2000', '2000+'])
    
    minutes_trends = df_minutes.groupby('Minutes_Bin').agg({
        'std_Gls': 'mean',
        'std_Ast': 'mean',
        'std_xG': 'mean',
        'std_xAG': 'mean',
        'pass_Cmp%': 'mean',
        'def_Tkl': 'mean',
        'Player': 'count'
    }).reset_index()
    minutes_trends.rename(columns={'Player': 'Player_Count'}, inplace=True)
    
    if not minutes_trends.empty:
        # Performance vs Minutes line chart
        fig_minutes_trend = go.Figure()
        
        fig_minutes_trend.add_trace(go.Scatter(
            x=minutes_trends['Minutes_Bin'],
            y=minutes_trends['std_Gls'],
            mode='lines+markers',
            name='Goals per Game',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=10)
        ))
        
        fig_minutes_trend.add_trace(go.Scatter(
            x=minutes_trends['Minutes_Bin'],
            y=minutes_trends['std_Ast'],
            mode='lines+markers',
            name='Assists per Game',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=10)
        ))
        
        fig_minutes_trend.add_trace(go.Scatter(
            x=minutes_trends['Minutes_Bin'],
            y=minutes_trends['pass_Cmp%'],
            mode='lines+markers',
            name='Pass Success Rate',
            line=dict(color='#45B7D1', width=3),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig_minutes_trend.update_layout(
            title="Performance Trends by Playing Time",
            xaxis_title="Minutes Played (Bins)",
            yaxis_title="Goals/Assists per Game",
            yaxis2=dict(
                title="Pass Success Rate",
                overlaying='y',
                side='right'
            ),
            template='plotly_dark',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_minutes_trend, use_container_width=True)
        
        # Minutes insights
        col1, col2 = st.columns(2)
        with col1:
            highest_minutes_group = minutes_trends.loc[minutes_trends['std_Gls'].idxmax(), 'Minutes_Bin']
            st.metric("Most Productive Minutes Range", highest_minutes_group)
        with col2:
            most_accurate_group = minutes_trends.loc[minutes_trends['pass_Cmp%'].idxmax(), 'Minutes_Bin']
            st.metric("Most Accurate Passing Range", most_accurate_group)
    else:
        st.info("Not enough data for minutes trend analysis")

with trend_tab3:
    st.markdown(f"### {remix_icon('team-line')}Team Performance Comparison", unsafe_allow_html=True)
    st.markdown("Compare average performance metrics across different teams.")
    
    # Team performance analysis
    team_performance = df_filtered.groupby('Squad').agg({
        'std_Gls': 'mean',
        'std_Ast': 'mean',
        'std_xG': 'mean',
        'std_xAG': 'mean',
        'pass_Cmp%': 'mean',
        'def_Tkl': 'mean',
        'def_Int': 'mean',
        'Age': 'mean',
        'Player': 'count'
    }).reset_index()
    team_performance.rename(columns={'Player': 'Player_Count'}, inplace=True)
    
    # Filter teams with at least 2 players
    team_performance = team_performance[team_performance['Player_Count'] >= 2]
    team_performance = team_performance.sort_values('std_Gls', ascending=False)
    
    if not team_performance.empty:
        # Team offensive performance
        fig_team_off = go.Figure()
        
        fig_team_off.add_trace(go.Scatter(
            x=team_performance['Squad'],
            y=team_performance['std_Gls'],
            mode='lines+markers',
            name='Average Goals',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=10)
        ))
        
        fig_team_off.add_trace(go.Scatter(
            x=team_performance['Squad'],
            y=team_performance['std_Ast'],
            mode='lines+markers',
            name='Average Assists',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=10)
        ))
        
        fig_team_off.update_layout(
            title="Team Offensive Performance Comparison",
            xaxis_title="Team",
            yaxis_title="Average per Game",
            template='plotly_dark',
            height=500,
            xaxis_tickangle=-45,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_team_off, use_container_width=True)
        
        # Team defensive performance
        fig_team_def = go.Figure()
        
        fig_team_def.add_trace(go.Scatter(
            x=team_performance['Squad'],
            y=team_performance['def_Tkl'],
            mode='lines+markers',
            name='Average Tackles',
            line=dict(color='#96CEB4', width=3),
            marker=dict(size=10)
        ))
        
        fig_team_def.add_trace(go.Scatter(
            x=team_performance['Squad'],
            y=team_performance['def_Int'],
            mode='lines+markers',
            name='Average Interceptions',
            line=dict(color='#FFEAA7', width=3),
            marker=dict(size=10)
        ))
        
        fig_team_def.update_layout(
            title="Team Defensive Performance Comparison",
            xaxis_title="Team",
            yaxis_title="Average per Game",
            template='plotly_dark',
            height=500,
            xaxis_tickangle=-45,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_team_def, use_container_width=True)
        
        # Team insights
        col1, col2, col3 = st.columns(3)
        with col1:
            best_attacking_team = team_performance.loc[team_performance['std_Gls'].idxmax(), 'Squad']
            st.metric("Best Attacking Team", best_attacking_team)
        with col2:
            best_creative_team = team_performance.loc[team_performance['std_Ast'].idxmax(), 'Squad']
            st.metric("Most Creative Team", best_creative_team)
        with col3:
            best_defensive_team = team_performance.loc[(team_performance['def_Tkl'] + team_performance['def_Int']).idxmax(), 'Squad']
            st.metric("Best Defensive Team", best_defensive_team)
    else:
        st.info("Not enough data for team comparison")



# Trend Summary Section
st.markdown(f"## {remix_icon('trending-up-line')}Key Trend Insights", unsafe_allow_html=True)

trend_insights_col1, trend_insights_col2 = st.columns(2)

with trend_insights_col1:
    st.markdown(f"### {remix_icon('chart-line')}Performance Patterns", unsafe_allow_html=True)
    
    if not df_filtered.empty:
        # Age-performance correlation
        age_goal_corr = df_filtered['Age'].corr(df_filtered['std_Gls'])
        age_def_corr = df_filtered['Age'].corr(df_filtered['def_Tkl'] + df_filtered['def_Int'])
        
        st.write(f"• **Age-Goal Correlation**: {age_goal_corr:.3f}")
        st.write(f"• **Age-Defense Correlation**: {age_def_corr:.3f}")
        
        if age_goal_corr > 0.1:
            st.success("📈 Older players tend to score more")
        elif age_goal_corr < -0.1:
            st.info("📉 Younger players are more prolific")
        else:
            st.info("➡️ Age has minimal impact on scoring")
            
        if age_def_corr > 0.1:
            st.success("🛡️ Older players are more defensive")
        elif age_def_corr < -0.1:
            st.info("⚡ Younger players defend more actively")
        else:
            st.info("🔄 Age doesn't affect defensive work")

with trend_insights_col2:
    st.markdown(f"### {remix_icon('trophy-line')}Peak Performance Insights", unsafe_allow_html=True)
    
    if not df_filtered.empty:
        # Find peak performers in different age ranges
        young_stars = df_filtered[df_filtered['Age'] <= 20]
        prime_players = df_filtered[(df_filtered['Age'] > 20) & (df_filtered['Age'] <= 22)]
        experienced = df_filtered[df_filtered['Age'] > 22]
        
        if not young_stars.empty:
            best_young = young_stars.nlargest(1, 'std_Gls')['Player'].iloc[0]
            st.write(f"• **Best Young Star (≤20)**: {best_young}")
        
        if not prime_players.empty:
            best_prime = prime_players.nlargest(1, 'std_Gls')['Player'].iloc[0]
            st.write(f"• **Best Prime Player (21-22)**: {best_prime}")
            
        if not experienced.empty:
            best_experienced = experienced.nlargest(1, 'std_Gls')['Player'].iloc[0]
            st.write(f"• **Best Experienced (>22)**: {best_experienced}")
        
        # Overall trend summary
        avg_goals_by_age = df_filtered.groupby('Age')['std_Gls'].mean()
        if len(avg_goals_by_age) > 1:
            trend_direction = "increasing" if avg_goals_by_age.iloc[-1] > avg_goals_by_age.iloc[0] else "decreasing"
            st.write(f"• **Overall Goal Trend**: {trend_direction} with age")



#streamlit run streamlit_app.py
