import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF
from sklearn.preprocessing import MinMaxScaler
import os

# Clean and Simple Professional Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles - Clean and Simple */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Fix anchor link positioning for centered text */
    h1, h2, h3, h4, h5, h6 {
        position: relative;
    }
    
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        position: absolute;
        left: -1.5rem;
        opacity: 0;
        transition: opacity 0.2s ease;
        text-decoration: none;
        color: #6b7280;
    }
    
    h1:hover a, h2:hover a, h3:hover a, h4:hover a, h5:hover a, h6:hover a {
        opacity: 1;
    }
    
    /* Hide anchor links in player cards to prevent centering issues */
    .player-card h4 a,
    .player-card p a {
        display: none !important;
    }
    
    /* Main container - Clean white background */
    .main {
        background: #ffffff;
    }
    
    /* Sidebar styling - Simple blue theme */
    [data-testid="stSidebar"] {
        background: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    
    [data-testid="stSidebar"] * {
        color: #495057 !important;
    }
    
    /* Clean metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2563eb;
    }
    
    /* Simple buttons */
    .stButton > button {
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #1d4ed8;
        transform: none;
    }
    
    /* Clean expanders */
    [data-testid="stExpander"] {
        margin: 0.5rem 0 !important;
        background: #2563eb !important;
        border-radius: 8px !important;
        border: 1px solid #e9ecef !important;
    }
    
    .streamlit-expanderHeader {
        background: #2563eb !important;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        font-weight: 500;
        padding: 0.75rem 1rem !important;
        color: #ffffff !important;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #1d4ed8 !important;
        border-color: #2563eb;
    }
    
    .streamlit-expanderHeader svg {
        stroke: #ffffff !important;
    }
    
    .streamlit-expanderHeader p {
        color: #ffffff !important;
    }
    
    .streamlit-expanderHeader span {
        color: #ffffff !important;
    }
    
    .streamlit-expanderHeader div {
        color: #ffffff !important;
    }
    
    .streamlit-expanderHeader * {
        color: #ffffff !important;
    }
    
    /* Force white text for all expander content */
    [data-testid="stExpander"] .streamlit-expanderHeader,
    [data-testid="stExpander"] .streamlit-expanderHeader *,
    [data-testid="stExpander"] .streamlit-expanderHeader p,
    [data-testid="stExpander"] .streamlit-expanderHeader span,
    [data-testid="stExpander"] .streamlit-expanderHeader div {
        color: #ffffff !important;
    }
    
    /* Additional specific selectors for expander text */
    .streamlit-expanderHeader .streamlit-expanderHeaderContent,
    .streamlit-expanderHeader .streamlit-expanderHeaderContent *,
    .streamlit-expanderHeader button,
    .streamlit-expanderHeader button * {
        color: #ffffff !important;
    }
    
    /* Override any existing text colors in expanders */
    [data-testid="stExpander"] * {
        color: #ffffff !important;
    }
    
    /* Specific for expander header text */
    [data-testid="stExpander"] .streamlit-expanderHeader {
        color: #ffffff !important;
    }
    
    [data-testid="stExpander"] .streamlit-expanderHeader * {
        color: #ffffff !important;
    }
    
    [data-testid="stExpanderDetails"] {
        border: 1px solid #e9ecef;
        border-top: none;
        border-radius: 0 0 8px 8px;
        background: #ffffff;
        padding: 1rem;
        margin-top: -1px;
    }
    
    /* Column Descriptions content should have black text */
    [data-testid="stExpanderDetails"] * {
        color: #000000 !important;
    }
    
    [data-testid="stExpanderDetails"] p {
        color: #000000 !important;
    }
    
    [data-testid="stExpanderDetails"] strong {
        color: #000000 !important;
    }
    
    /* Clean dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e9ecef;
    }
    
    /* Simple tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: 1px solid #e9ecef;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e9ecef;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2563eb;
        color: white !important;
        border-color: #2563eb;
    }
    
    /* Clean info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #2563eb;
        background-color: #f8f9fa !important;
        border: 1px solid #e9ecef !important;
    }
    
    .stAlert [data-testid="stMarkdownContainer"] p {
        color: #495057 !important;
    }
    
    .stAlert [data-testid="stMarkdownContainer"] strong {
        color: #2563eb !important;
    }
    
    /* Simple divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: #e9ecef;
    }
    
    /* Clean multiselect */
    [data-baseweb="tag"] {
        background-color: #2563eb !important;
        border-color: #1d4ed8 !important;
    }
    
    [data-baseweb="tag"] span {
        color: white !important;
    }
    
    /* Clean slider */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #2563eb !important;
    }
    
    /* Success boxes */
    div[data-baseweb="notification"] {
        background-color: #f8f9fa !important;
        border-left-color: #2563eb !important;
    }
    
    div[data-baseweb="notification"] p {
        color: #495057 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# STEP 0: FIXED DATA FILE
# ---------------------------

# Dosya yolu düzeltmesi - hem local hem de cloud için çalışır
if os.path.exists('data/eredivisie_midfielders_scored.csv'):
    df = pd.read_csv('data/eredivisie_midfielders_scored.csv')
elif os.path.exists('notebooks/../data/eredivisie_midfielders_scored.csv'):
    df = pd.read_csv('notebooks/../data/eredivisie_midfielders_scored.csv')
else:
    st.error("CSV file not found!")
    st.stop()
df = df.dropna(how='all')  # Clean empty rows

# ---------------------------
# GLOBAL HELPER FUNCTIONS
# ---------------------------

# Color coding function for rating scores
def get_rating_color(score):
    if score < 20:
        return '#dc2626'  # Red for low scores
    elif score < 40:
        return '#ea580c'  # Orange-red
    elif score < 60:
        return '#d97706'  # Orange
    elif score < 80:
        return '#ca8a04'  # Yellow
    else:
        return '#16a34a'  # Green for high scores

# Color coding function for archetype names
def get_archetype_color(archetype):
    archetype_colors = {
        'Anchor': '#dc2626',      # Red
        'DLP': '#ea580c',        # Orange
        'BallWinner': '#d97706',  # Yellow
        'BoxToBox': '#16a34a',   # Green
        'APM': '#059669',        # Teal
        'CAM': '#2563eb',        # Blue
        'BoxCrasher': '#7c3aed'  # Purple
    }
    return archetype_colors.get(archetype, '#6b7280')  # Default gray

def get_team_color(team_name):
    """Get primary color for each Eredivisie team"""
    team_colors = {
        'Ajax': '#d2122e',           # Ajax Red
        'PSV Eindhoven': '#ff6600',   # PSV Orange
        'Feyenoord': '#ff6600',      # Feyenoord Orange
        'AZ Alkmaar': '#ff0000',     # AZ Red
        'Twente': '#ff0000',         # Twente Red
        'Utrecht': '#ff6600',        # Utrecht Orange
        'NEC Nijmegen': '#ff0000',   # NEC Red
        'Heerenveen': '#0066cc',     # Heerenveen Blue
        'Groningen': '#0066cc',       # Groningen Blue
        'Sparta R\'dam': '#ff0000',  # Sparta Red
        'Willem II': '#ff6600',      # Willem II Orange
        'NAC Breda': '#ff6600',      # NAC Orange
        'Go Ahead Eag': '#0066cc',   # Go Ahead Blue
        'Heracles Almelo': '#ff0000', # Heracles Red
        'RKC Waalwijk': '#ff0000',   # RKC Red
        'Fortuna Sittard': '#ff6600', # Fortuna Orange
        'Almere City': '#0066cc'     # Almere Blue
    }
    return team_colors.get(team_name, '#6b7280')

# Profile color function
def get_profile_color(profile_id):
    profile_colors = {
        0: '#1E88E5',  # Blue for Elite Creative
        1: '#43A047',  # Green for Developing
        2: '#FB8C00'   # Orange for Defensive Engines
    }
    return profile_colors.get(profile_id, '#6b7280')  # Default gray

# Color coding function for scores based on archetype
def get_score_color(score, archetype):
    # Define color palettes for each archetype
    color_palettes = {
        'Anchor': {
            'low': '#dc2626',      # Red
            'medium_low': '#ea580c', # Orange-red
            'medium': '#d97706',    # Orange
            'medium_high': '#ca8a04', # Yellow
            'high': '#16a34a'       # Green
        },
        'DLP': {
            'low': '#7c2d12',       # Dark red
            'medium_low': '#ea580c', # Orange
            'medium': '#d97706',    # Orange
            'medium_high': '#65a30d', # Light green
            'high': '#059669'      # Emerald
        },
        'BallWinner': {
            'low': '#991b1b',       # Dark red
            'medium_low': '#dc2626', # Red
            'medium': '#ea580c',    # Orange
            'medium_high': '#d97706', # Orange
            'high': '#16a34a'       # Green
        },
        'BoxToBox': {
            'low': '#7c2d12',       # Dark red
            'medium_low': '#ea580c', # Orange
            'medium': '#d97706',    # Orange
            'medium_high': '#65a30d', # Light green
            'high': '#059669'      # Emerald
        },
        'APM': {
            'low': '#7c2d12',       # Dark red
            'medium_low': '#ea580c', # Orange
            'medium': '#d97706',    # Orange
            'medium_high': '#65a30d', # Light green
            'high': '#059669'      # Emerald
        },
        'CAM': {
            'low': '#7c2d12',       # Dark red
            'medium_low': '#ea580c', # Orange
            'medium': '#d97706',    # Orange
            'medium_high': '#65a30d', # Light green
            'high': '#059669'      # Emerald
        },
        'BoxCrasher': {
            'low': '#7c2d12',       # Dark red
            'medium_low': '#ea580c', # Orange
            'medium': '#d97706',    # Orange
            'medium_high': '#65a30d', # Light green
            'high': '#059669'      # Emerald
        }
    }
    
    # Get palette for archetype or use default
    palette = color_palettes.get(archetype, color_palettes['Anchor'])
    
    if score < 20:
        return palette['low']
    elif score < 40:
        return palette['medium_low']
    elif score < 60:
        return palette['medium']
    elif score < 80:
        return palette['medium_high']
    else:
        return palette['high']

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
st.set_page_config(
    page_title=" Eredivisie U24 Midfielders Analytics", 
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Eredivisie U24 Midfielders Analytics Dashboard\nProfessional scouting and player analysis tool powered by data science.\n Emin Eren Sağlam"
    }
)


# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
with st.sidebar:
    st.markdown("## Filter Options")
    st.markdown("---")
    
    # Age Filter
    st.markdown("<h3 style='margin: 0; font-size: 1.2rem;'>Age Range</h3>", unsafe_allow_html=True)
    age_filter = st.slider(
        "Select age range", 
        int(df["Age"].min()), 
        int(df["Age"].max()), 
        (18, 24),
        help="Filter players by age",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Position Filter
    st.markdown("<h3 style='margin: 0; font-size: 1.2rem;'>Position</h3>", unsafe_allow_html=True)
    pos_filter = st.multiselect(
        "Select positions", 
        sorted(df["Pos"].unique()), 
        default=df["Pos"].unique(),
        help="Filter by player positions"
    )
    
    st.markdown("---")
    
    # Team Filter
    st.markdown("<h3 style='margin: 0; font-size: 1.2rem;'>Team</h3>", unsafe_allow_html=True)
    squad_filter = st.multiselect(
        "Select teams", 
        sorted(df["Squad"].unique()), 
        default=df["Squad"].unique(),
        help="Filter by team"
    )
    
    st.markdown("---")
    
    # Player Profile Filter
    st.markdown("<h3 style='margin: 0; font-size: 1.2rem;'>Player Profile</h3>", unsafe_allow_html=True)
    cluster_filter = st.multiselect(
        "Select profiles", 
        sorted(df["Cluster"].unique()), 
        default=df["Cluster"].unique(),
        format_func=lambda x: f"Profile {x}",
        help="Filter by player profile type"
    )
    
    st.markdown("---")
    
    # Player Search
    st.markdown("<h3 style='margin: 0; font-size: 1.2rem;'>Player Search</h3>", unsafe_allow_html=True)
    player_search = st.text_input(
        "Enter player name", 
        placeholder="e.g. Kenneth Taylor",
        help="Search for specific players"
    )
    
    # Reset button
    if st.button("Reset All Filters", type="primary", use_container_width=True):
        st.rerun()

# Apply filters
df_filtered = df[
    (df["Age"] >= age_filter[0]) &
    (df["Age"] <= age_filter[1]) &
    (df["Pos"].isin(pos_filter)) &
    (df["Squad"].isin(squad_filter)) &
    (df["Cluster"].isin(cluster_filter))
]

if player_search:
    df_filtered = df_filtered[df_filtered["Player"].str.contains(player_search, case=False, na=False)]

# Create 7 main navigation tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Overview", 
    "Player Profiles", 
    "Top Players", 
    "Player Analysis", 
    "Scatter Analysis", 
    "Trend Analysis", 
    "Distribution Analysis"
])

with tab1:
    # Clean Header Section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem; background: #f8f9fa; 
                    border-radius: 8px; margin-bottom: 2rem; border: 1px solid #e9ecef;'>
            <h1 style='color: #2563eb; font-size: 2rem; margin: 0; font-weight: 700;'>
                Eredivisie U24 Midfielders Analytics - Season 24/25
            </h1>
            <p style='color: #6c757d; font-size: 1rem; margin: 0.5rem 0 0.3rem 0; font-weight: 500;'>
                Professional Scouting & Analytics Dashboard
            </p>
            <p style='color: #6c757d; font-size: 0.9rem; margin: 0;'>
                Advanced player analysis powered by data science
            </p>
            <p style='color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
                <a href='https://www.linkedin.com/in/erensglm' target='_blank' 
                   style='color: #2563eb; text-decoration: none; font-weight: 500;'>
                    Created by Emin Eren Sağlam
                </a>
                <a href='https://x.com/blindsiderdata' target='_blank' 
                   style='color: #2563eb; text-decoration: none; font-weight: 500;'>
                    , \n Blindsiderdata
                </a>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Project Overview & Scoring System - Side by Side Cards
    col_info1, col_info2 = st.columns(2, gap="large")

    with col_info1:
        st.markdown("""
            <div style='background: #ffffff; border-radius: 8px; padding: 1.5rem; height: 100%;
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h3 style='color: #2563eb; margin: 0 0 1rem 0; font-size: 1.1rem; font-weight: 600;'>
                    About This Dashboard
                </h3>
                <p style='color: #495057; font-size: 0.9rem; line-height: 1.6; margin: 0;'>
                    This analytics platform provides data-driven insights into <strong style='color: #2563eb;'>Eredivisie's most promising young midfielders</strong> (under 24). 
                    Using advanced clustering algorithms and statistical analysis, we identify three distinct player profiles to help scouts, 
                    analysts, and teams make informed decisions.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_info2:
        st.markdown("""
            <div style='background: #ffffff; border-radius: 8px; padding: 1.5rem; height: 100%;
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h3 style='color: #2563eb; margin: 0 0 1rem 0; font-size: 1.1rem; font-weight: 600;'>
                    Scoring System
                </h3>
                <p style='color: #495057; font-size: 0.9rem; line-height: 1.6; margin: 0;'>
                    All performance metrics are scored on a <strong style='color: #2563eb;'>0-100 scale</strong>. 
                    A score of <strong style='color: #dc2626;'>0</strong> represents the <em>lowest</em> performance, 
                    while <strong style='color: #16a34a;'>100</strong> represents the <em>highest</em>. 
                    For example, a player with 85 in passing demonstrates superior passing ability compared to others in the dataset.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

    # Clean Stats Cards
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        st.markdown("""
            <div style='background: #ffffff; padding: 1.5rem 1rem; border-radius: 8px; text-align: center; 
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2 style='color: #2563eb; margin: 0; font-size: 2rem; font-weight: 700;'>49</h2>
                <p style='color: #6c757d; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;'>TOTAL PLAYERS</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style='background: #ffffff; padding: 1.5rem 1rem; border-radius: 8px; text-align: center; 
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2 style='color: #2563eb; margin: 0; font-size: 2rem; font-weight: 700;'>3</h2>
                <p style='color: #6c757d; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;'>PLAYER PROFILES</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style='background: #ffffff; padding: 1.5rem 1rem; border-radius: 8px; text-align: center; 
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2 style='color: #2563eb; margin: 0; font-size: 2rem; font-weight: 700;'>18-24</h2>
                <p style='color: #6c757d; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;'>AGE RANGE</p>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div style='background: #ffffff; padding: 1.5rem 1rem; border-radius: 8px; text-align: center; 
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2 style='color: #2563eb; margin: 0; font-size: 2rem; font-weight: 700;'>18</h2>
                <p style='color: #6c757d; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;'>TEAMS</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # General Overview Info
    st.info("""
    **🔍 What's in Other Tabs:**
    - **👥 Player Profiles**: Detailed player archetype analysis and filtered player list (use filters in top-left corner for filtered players section)
    - **🏆 Top Players**: Best performers by each profile type
    - **🔍 Player Analysis**: Individual player comparison tools and radar charts
    - **📈 Scatter Analysis**: Performance correlation charts and distribution analyses
    - **📉 Trend Analysis**: Age and performance trends, team performance analyses
    - **📊 Distribution Analysis**: Statistical distribution charts and histogram analyses
    """)

with tab2:
    st.markdown("### Player Profile Types")
    st.markdown("Understand the three distinct player profiles in our analysis")
    
    # Profile Summary Info Cards
    st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; text-align: center; color: #2563eb;'>
                Player Profile Summary
            </h2>
            <p style='text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;'>
                Overview of the three main player profiles in our analysis
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Profile summary cards
    profile_summary_cols = st.columns(3, gap="medium")
    
    # Calculate most common archetype for each profile
    def get_most_common_archetype(cluster_id):
        cluster_data = df[df['Cluster'] == cluster_id]
        if len(cluster_data) > 0 and 'Primary_Archetype' in cluster_data.columns:
            archetype_counts = cluster_data['Primary_Archetype'].value_counts()
            if len(archetype_counts) > 0:
                return archetype_counts.index[0]
        return 'N/A'
    
    profile_summaries = [
        {
            'id': 0,
            'name': 'Elite Creative Attacking Players',
            'color': '#1E88E5',
            'description': 'Elite-level players with highest creativity and goal contribution. Young stars from big clubs with superior technical quality.',
            'key_traits': ['Goals & Assists', 'Creativity', 'Technical Quality'],
            'player_count': len(df[df['Cluster'] == 0]),
            'avg_age': df[df['Cluster'] == 0]['Age'].mean() if len(df[df['Cluster'] == 0]) > 0 else 0,
            'top_teams': ['Ajax', 'PSV', 'Go Ahead Eagle', 'NAC Breda', 'Twente'],
            'most_common_archetype': get_most_common_archetype(0)
        },
        {
            'id': 1,
            'name': 'Developing Players',
            'color': '#43A047',
            'description': 'Players in development phase with basic passing abilities. High growth potential for the future with young age.',
            'key_traits': ['Basic Passing', 'Young Age', 'Development Phase'],
            'player_count': len(df[df['Cluster'] == 1]),
            'avg_age': df[df['Cluster'] == 1]['Age'].mean() if len(df[df['Cluster'] == 1]) > 0 else 0,
            'top_teams': ['Groningen', 'Utrecht', 'Sparta R\'dam', 'Feyenoord', 'Ajax'],
            'most_common_archetype': get_most_common_archetype(1)
        },
        {
            'id': 2,
            'name': 'Defensive Engines',
            'color': '#FB8C00',
            'description': 'Defensively-minded players who prioritize defensive duties. Strong in physical battles with high endurance.',
            'key_traits': ['Defense', 'Ball Recovery', 'Endurance'],
            'player_count': len(df[df['Cluster'] == 2]),
            'avg_age': df[df['Cluster'] == 2]['Age'].mean() if len(df[df['Cluster'] == 2]) > 0 else 0,
            'top_teams': ['Go Ahead Eagle', 'NEC Nijmegen', 'Zwolle', 'Utrecht', 'Heerenveen'],
            'most_common_archetype': get_most_common_archetype(2)
        }
    ]
    
    for idx, profile in enumerate(profile_summaries):
        with profile_summary_cols[idx]:
            st.markdown(f"""
                <div style='background: #ffffff; border-radius: 8px; padding: 1.5rem; margin: 0.5rem 0;
                            border: 2px solid {profile['color']}; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                        <h3 style='color: {profile['color']}; margin: 0; font-size: 1.1rem; font-weight: 600;'>
                            Profile {profile['id']}: {profile['name']}
                        </h3>
                    </div>
                    <p style='color: #495057; font-size: 0.85rem; line-height: 1.5; margin: 0 0 1rem 0;'>
                        {profile['description']}
                    </p>
                    <div style='margin-bottom: 1rem;'>
                        <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem;'>Key Traits:</div>
                        <div style='display: flex; flex-wrap: wrap; gap: 0.3rem;'>
                            {''.join([f'<span style="background: {profile["color"]}15; color: {profile["color"]}; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 500;">{trait}</span>' for trait in profile['key_traits']])}
                        </div>
                    </div>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-bottom: 1rem;'>
                        <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                            <div style='color: #888; font-size: 0.65rem;'>Players</div>
                            <div style='font-weight: 600; color: {profile["color"]};'>{profile['player_count']}</div>
                        </div>
                        <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                            <div style='color: #888; font-size: 0.65rem;'>Avg Age</div>
                            <div style='font-weight: 600; color: {profile["color"]};'>{profile['avg_age']:.1f}</div>
                        </div>
                    </div>
                    <div style='margin-bottom: 1rem;'>
                        <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem;'>Most Common Archetype:</div>
                        <div style='background: {get_archetype_color(profile["most_common_archetype"])}15; color: {get_archetype_color(profile["most_common_archetype"])}; padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; display: inline-block;'>
                            {profile['most_common_archetype']}
                        </div>
                    </div>
                    <div>
                        <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem;'>Top Teams:</div>
                        <div style='font-size: 0.75rem; color: #495057; line-height: 1.4;'>
                            {', '.join(profile['top_teams'][:3])}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Archetype Info Cards Section
    st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; text-align: center; color: #2563eb;'>
                Player Archetypes Overview
            </h2>
            <p style='text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;'>
                Detailed breakdown of each player archetype with examples
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Archetype definitions and examples
    archetype_info = {
        'Anchor': {
            'name': 'Anchor (Defensive Midfielder)',
            'description': 'Plays in front of the defensive line, maintains team defensive balance. Physical player who wins the ball, makes simple passes, avoids risk.',
            'key_metrics': ['Tkl+Int', 'Blocks', 'Recoveries'],
            'example_players': ['Max Balard (<span style="color: #ff6600;">NAC Breda</span>)', 'Alonzo Engwanda (<span style="color: #ff6600;">Utrecht</span>)', 'Amine Lachkar (<span style="color: #ff6600;">Willem II</span>)']
        },
        'DLP': {
            'name': 'Deep Lying Playmaker (DLP)',
            'description': 'Initiates play from defensive areas, builds attacks with long passes. Technical player with high pass success rate, wide vision, progressive passing.',
            'key_metrics': ['Pass Success', 'Prog Distance', 'Prog Passes'],
            'example_players': ['Ringo Meerveld (<span style="color: #ff6600;">Willem II</span>)', 'Dirk Proper (<span style="color: #ff0000;">NEC Nijmegen</span>)', 'Ryan Fosso (<span style="color: #ff6600;">Fortuna Sittard</span>)']
        },
        'BallWinner': {
            'name': 'Ball Winner (Ball Winner)',
            'description': 'Expert in winning the ball in midfield, high physical strength, aggressive player. High tackle and interception numbers, effective in ball recovery.',
            'key_metrics': ['Tkl+Int', 'Tkl Won', 'Recoveries'],
            'example_players': ['Enric Llansana (<span style="color: #0066cc;">Go Ahead Eagle</span>)', 'Paxten Aaronson (<span style="color: #ff6600;">Utrecht</span>)', 'Espen van Ee (<span style="color: #0066cc;">Heerenveen</span>)']
        },
        'BoxToBox': {
            'name': 'Box to Box (Box to Box)',
            'description': 'Performs both defensive and offensive duties, effective everywhere on the pitch, high endurance player.',
            'key_metrics': ['Prog Runs', 'Recoveries', 'Prog Distance'],
            'example_players': ['Antoni Milambo (<span style="color: #ff6600;">Feyenoord</span>)', 'Jorg Schreuders (<span style="color: #0066cc;">Groningen</span>)', 'Malik Tillman (<span style="color: #ff6600;">PSV</span>)']
        },
        'APM': {
            'name': 'Advanced Playmaker (APM)',
            'description': 'High creativity and technical abilities, expert in creating goals, effective in final passes and key passes.',
            'key_metrics': ['Key Passes', 'xAG', 'GCA Pass'],
            'example_players': ['Kenneth Taylor (<span style="color: #d2122e;">Ajax</span>)', 'Levi Smans (<span style="color: #0066cc;">Heerenveen</span>)', 'Luciano Valente (<span style="color: #0066cc;">Groningen</span>)']
        },
        'CAM': {
            'name': 'Central Attacking Midfielder (CAM)',
            'description': 'Effective in attacking areas, shows creativity in final third, enters penalty area, effective in goals and assists.',
            'key_metrics': ['Final 3rd', 'Pen Area', 'xAG'],
            'example_players': ['Ismael Saibari (<span style="color: #ff6600;">PSV</span>)', 'Jorg Schreuders (<span style="color: #0066cc;">Groningen</span>)', 'Mohammed Ihattaren (<span style="color: #ff0000;">RKC Waalwijk</span>)']
        },
        'BoxCrasher': {
            'name': 'Box Crasher (Shadow Striker)',
            'description': 'Enters penalty area, takes shots, effective in scoring goals, shows striker-like characteristics as a midfielder.',
            'key_metrics': ['xG', 'Shots', 'Goals'],
            'example_players': ['Ismael Saibari (<span style="color: #ff6600;">PSV</span>)', 'Leo Sauer (<span style="color: #ff6600;">NAC Breda</span>)', 'Sem Steijn (<span style="color: #ff0000;">Twente</span>)']
        }
    }
    
    # Create archetype cards in a grid layout
    archetype_cols = st.columns(2, gap="medium")
    
    for idx, (archetype_key, archetype_data) in enumerate(archetype_info.items()):
        col_idx = idx % 2
        with archetype_cols[col_idx]:
            st.markdown(f"""
                <div style='background: #ffffff; border-radius: 8px; padding: 1.5rem; margin: 0.5rem 0;
                            border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                        <h3 style='color: {get_archetype_color(archetype_key)}; margin: 0; font-size: 1.1rem; font-weight: 600;'>
                            {archetype_data['name']}
                        </h3>
                    </div>
                    <p style='color: #495057; font-size: 0.85rem; line-height: 1.5; margin: 0 0 1rem 0;'>
                        {archetype_data['description']}
                    </p>
                    <div style='margin-bottom: 1rem;'>
                        <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem;'>Key Metrics:</div>
                        <div style='display: flex; flex-wrap: wrap; gap: 0.3rem;'>
                            {''.join([f'<span style="background: {get_archetype_color(archetype_key)}15; color: {get_archetype_color(archetype_key)}; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 500;">{metric}</span>' for metric in archetype_data['key_metrics']])}
                        </div>
                    </div>
                    <div>
                        <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem;'>Example Players:</div>
                        <div style='font-size: 0.75rem; color: #495057; line-height: 1.4;'>
                            {', '.join(archetype_data['example_players'])}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    
    # Filtered Results Section with Modern Cards
    st.markdown("""
        <div style='text-align: center; margin: 2rem 0 1rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; margin: 0; color: #2563eb;'>
                Filtered Players
            </h2>
            <p style='color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
                Current filter results and player statistics (use filters in top-left corner)
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(f"""
            <div style='background: #ffffff; padding: 1.5rem 1rem; border-radius: 8px; text-align: center; 
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2 style='color: #2563eb; margin: 0; font-size: 2rem; font-weight: 700;'>{len(df_filtered)}</h2>
                <p style='color: #6c757d; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;'>TOTAL PLAYERS</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style='background: #ffffff; padding: 1.5rem 1rem; border-radius: 8px; text-align: center; 
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2 style='color: #2563eb; margin: 0; font-size: 2rem; font-weight: 700;'>{df_filtered['Age'].mean():.1f}</h2>
                <p style='color: #6c757d; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;'>AVERAGE AGE</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div style='background: #ffffff; padding: 1.5rem 1rem; border-radius: 8px; text-align: center; 
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2 style='color: #2563eb; margin: 0; font-size: 2rem; font-weight: 700;'>{df_filtered['std_Min'].mean():.0f}</h2>
                <p style='color: #6c757d; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;'>AVERAGE MINUTES</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; margin: 2rem 0 1rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; margin: 0; color: #2563eb;'>
                View Detailed Player Data
            </h2>
            <p style='color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
                Complete player statistics and performance metrics
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.dataframe(df_filtered, use_container_width=True, height=400)

    st.markdown("---")
    
    # Column Descriptions Section
    with st.expander("Column Descriptions (Click to expand)", expanded=False):
        # Create columns for better layout
        col1, col2, col3 = st.columns(3, gap="medium")
        
        # Split column_info into 3 parts
        items = list(column_info.items())
        chunk_size = len(items) // 3
        remainder = len(items) % 3
        
        # Distribute items across columns
        start = 0
        for i, col in enumerate([col1, col2, col3]):
            if i < remainder:
                end = start + chunk_size + 1
            else:
                end = start + chunk_size
            
            with col:
                for col_name, desc in items[start:end]:
                    st.markdown(f"**{col_name}**: {desc}", unsafe_allow_html=True)
            
            start = end

with tab3:
    st.markdown("### Top 5 Players by Profile")
    st.markdown("Discover the best performers in each player profile category")
    
    # Metric sets suitable for cluster profiles (New 3 Clusters)
    cluster_metrics_map = {
        0: ['std_Gls','std_Ast','std_xG','std_xAG','pass_KP','shoot_Sh','gca_PassLive'],      # Super Stars: goals + assists + creativity + shots
        1: ['std_Min','pass_Cmp%','pt_Min%','misc_Won','std_MP'],                           # Developing: playing time + basic passing + duels
        2: ['def_Tkl','def_TklW','def_Int','def_Blocks','misc_Recov','misc_TklW','poss_PrgDist'] # Hard Workers: defense + ball recovery + physical power
    }

    # Calculate according to current filters
    df_rank = df_filtered.copy()

    for cid, metrics in cluster_metrics_map.items():
        # Modern Profile Cards with Gradients
        profile_gradients = {
            0: 'linear-gradient(135deg, #FF6600 0%, #FF8533 100%)',
            1: 'linear-gradient(135deg, #FFA500 0%, #FFB84D 100%)',
            2: 'linear-gradient(135deg, #FF8533 0%, #FFA64D 100%)'
        }
        profile_icons = {0: '', 1: '', 2: ''}
        
        st.markdown(f"""
            <div style='background: #ffffff; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0;
                        border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h2 style='color: #2563eb; margin: 0; font-size: 1.3rem; font-weight: 600;'>
                    Profile {cid}: {cluster_profiles[cid]['name']}
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate cluster statistics from real data
        cluster_data = df[df['Cluster'] == cid]
        
        st.info(f"**Playing Style**: {cluster_profiles[cid]['detailed_stats'].get('playing_style', 'General midfield players')}")

        # Is this player profile available in selected filter?
        if cid not in df_rank["Cluster"].unique():
            st.info("No players found in this player profile matching filtering criteria.")
            continue

        # Only available metrics
        available_metrics = [m for m in metrics if m in df_rank.columns]
        if not available_metrics:
            st.warning("No valid metrics found for this player profile.")
            continue

        # Normalization
        scaler_rank = MinMaxScaler()
        scaled_vals = scaler_rank.fit_transform(df_rank[available_metrics])
        score = scaled_vals.mean(axis=1)  # Equal weight: you can add weighting if desired

        # Score series
        df_rank[f"Cluster{cid}_Score"] = score

        # Top 5 in this cluster
        top_players = df_rank[df_rank["Cluster"] == cid].nlargest(5, f"Cluster{cid}_Score")

        # Player Report Cards - Minimal Design
        st.markdown("### Player Report")
        st.markdown("---")
        
        # Create player cards in rows (3 cards per row for compact view)
        for idx in range(0, len(top_players), 3):
            cols = st.columns(3, gap="medium")
            
            for col_idx, col in enumerate(cols):
                player_idx = idx + col_idx
                if player_idx < len(top_players):
                    player = top_players.iloc[player_idx]
                    
                    # Get archetype info
                    primary_archetype = player.get('Primary_Archetype', 'N/A')
                    archetype_score = player.get('Archetype_Score', 0)
                    
                    # Border colors based on cluster
                    border_colors = {0: '#1E88E5', 1: '#43A047', 2: '#FB8C00'}
                    score_value = player[f"Cluster{cid}_Score"] * 100
                    
                    with col:
                        
                        # Minimal card with border
                        st.markdown(f"""
                            <div class='player-card' style='border: 2px solid {border_colors.get(cid, border_colors[0])};
                                        border-radius: 10px; padding: 1rem; 
                                        background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                                <div style='text-align: center;'>
                                    <div style='color: {border_colors.get(cid, border_colors[0])}; 
                                                font-size: 0.8rem; font-weight: 600;'>
                                        #{player_idx + 1}
                                    </div>
                                    <h4 style='margin: 0.3rem 0; color: #333; font-size: 1.1rem; background: linear-gradient(135deg, {get_profile_color(cid)}15, {get_profile_color(cid)}08); padding: 0.3rem 0.5rem; border-radius: 4px;'>
                                        {player['Player']}
                                    </h4>
                                    <p style='margin: 0; color: {get_team_color(player['Squad'])}; font-size: 0.85rem; background: linear-gradient(135deg, {get_profile_color(cid)}12, {get_profile_color(cid)}05); padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600;'>
                                        {player['Squad']}
                                    </p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Compact info grid
                        st.markdown(f"""
                            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; 
                                        margin-top: 0.8rem; font-size: 0.85rem;'>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Nation</div>
                                    <div style='font-weight: 600; color: #333;'>{player.get('Nation', 'N/A')}</div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Age</div>
                                    <div style='font-weight: 600; color: #333;'>{player['Age']:.0f}</div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px; grid-column: span 2;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Profile</div>
                                    <div style='font-weight: 600; color: {border_colors.get(cid, border_colors[0])}; font-size: 0.75rem;'>
                                        {cid}: {cluster_profiles[cid]['name']}
                                    </div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px; grid-column: span 2;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Overall Rating</div>
                                    <div style='font-weight: 600; color: {get_rating_color(score_value)};'>
                                        {score_value:.1f}
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        
                        # Archetype section
                        st.markdown(f"""
                            <div style='margin-top: 0.8rem; padding: 0.6rem; 
                                        background: linear-gradient(135deg, {get_archetype_color(primary_archetype)}15, {get_archetype_color(primary_archetype)}05);
                                        border-radius: 5px; text-align: center;'>
                                <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.4rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.2rem; display: inline-block;'>
                                    Archetype
                                </div>
                                <div style='font-weight: 700; color: {get_archetype_color(primary_archetype)}; 
                                            font-size: 0.95rem;'>
                                    {primary_archetype}
                                </div>
                                <div style='color: #666; font-size: 0.75rem; margin-top: 0.2rem;'>
                                   Archetype Score: {archetype_score:.1f}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Performance stats - Dynamic based on archetype
                        archetype = str(primary_archetype).strip()
                        if archetype == 'Anchor':
                            metric1_label, metric1_value = "Tkl+Int", player['def_Tkl+Int']
                            metric2_label, metric2_value = "Blocks", player['def_Blocks']
                            metric3_label, metric3_value = "Recoveries", player['misc_Recov']
                        elif archetype == 'DLP':
                            metric1_label, metric1_value = "Pass Success", player['pass_Cmp%']
                            metric2_label, metric2_value = "Prog Distance", player['pass_PrgDist']
                            metric3_label, metric3_value = "Prog Passes", player['pass_PrgP']
                        elif archetype == 'BallWinner':
                            metric1_label, metric1_value = "Tkl+Int", player['def_Tkl+Int']
                            metric2_label, metric2_value = "Tkl Won", player['def_TklW']
                            metric3_label, metric3_value = "Recoveries", player['misc_Recov']
                        elif archetype == 'BoxToBox':
                            metric1_label, metric1_value = "Prog Runs", player['std_PrgR']
                            metric2_label, metric2_value = "Recoveries", player['misc_Recov']
                            metric3_label, metric3_value = "Prog Distance", player['poss_PrgDist']
                        elif archetype == 'APM':
                            metric1_label, metric1_value = "Key Passes", player['pass_KP']
                            metric2_label, metric2_value = "xAG", player['std_xAG']
                            metric3_label, metric3_value = "GCA Pass", player['gca_PassLive']
                        elif archetype == 'CAM':
                            metric1_label, metric1_value = "Final 3rd", player['poss_1/3']
                            metric2_label, metric2_value = "Pen Area", player['poss_CPA']
                            metric3_label, metric3_value = "xAG", player['std_xAG']
                        elif archetype == 'BoxCrasher':
                            metric1_label, metric1_value = "xG", player['std_xG']
                            metric2_label, metric2_value = "Shots", player['shoot_Sh']
                            metric3_label, metric3_value = "Goals", player['std_Gls']
                        else:  # Default/fallback metrics
                            metric1_label, metric1_value = "Minutes", player['std_Min']
                            metric2_label, metric2_value = "Pass Success", player['pass_Cmp%']
                            metric3_label, metric3_value = "Matches", player['std_MP']
                        
                        
                        
                        st.markdown(f"""
                            <div style='margin-top: 0.8rem; padding: 0.6rem; background: #f9f9f9; border-radius: 5px;'>
                                <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.3rem; font-size: 0.75rem; text-align: center;'>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric1_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric1_value, archetype)};'>{metric1_value:.1f}</div>
                                    </div>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric2_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric2_value, archetype)};'>{metric2_value:.1f}</div>
                                    </div>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric3_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric3_value, archetype)};'>{metric3_value:.1f}</div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
        
        st.divider()

with tab4:
    st.markdown("### Player Analysis & Comparison")
    st.markdown("Deep dive into individual player performance with radar charts and similarity analysis")
    
    # Instructions box
    with st.expander("How to use this section (Click to expand)", expanded=False):
        st.markdown("""
        **Steps:**
        1. Select one or more players from the dropdown below
        2. View their performance radar charts across multiple categories
        3. See similar players based on statistical similarity
        4. Compare selected players against profile averages
        5. Download detailed reports in Excel or PDF format
        
        **Tips:**
        - Select multiple players to compare them directly
        - Click on legend items in charts to show/hide specific data
        - Use sidebar filters to narrow down player selection
        """)

    st.markdown("---")

    # Initial radar metrics
    radar_metrics = ['std_MP','std_Min','std_90s','std_Gls','std_Ast','std_xG','std_xAG','misc_Fls','std_CrdY','std_CrdR']

    st.markdown("<h3 style='margin: 0 0 1rem 0; font-size: 1.3rem;'>Select Players for Analysis</h3>", unsafe_allow_html=True)
    player_select = st.multiselect(
        "Choose one or more players", 
        df["Player"].unique(), 
        default=[], 
        key="player_select",
        help="You can select multiple players for comparison"
    )

    def update_player_view(selected_players):
        if not selected_players:
            st.info("Please select the player(s) you want to analyze.")
            return
            
        # Get data of selected players
        selected_rows = df[df["Player"].isin(selected_players)]
        if selected_rows.empty:
            st.warning("Selected players are outside filtering criteria.")
            return

        # Player Profile information of selected players
        unique_clusters = selected_rows["Cluster"].unique()
        
        # ---------------------------
        # Selected Players Profile Cards
        # ---------------------------
        st.markdown("### 🎯 Selected Player Cards")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Calculate overall ratings for selected players
        cluster_metrics_map_analysis = {
            0: ['std_Gls','std_Ast','std_xG','std_xAG','pass_KP','shoot_Sh','gca_PassLive'],
            1: ['std_Min','pass_Cmp%','pt_Min%','misc_Won','std_MP'],
            2: ['def_Tkl','def_TklW','def_Int','def_Blocks','misc_Recov','misc_TklW','poss_PrgDist']
        }
        
        # Create player cards in rows (3 cards per row for compact view)
        for idx in range(0, len(selected_players), 3):
            cols = st.columns(3, gap="medium")
            
            for col_idx, col in enumerate(cols):
                player_idx = idx + col_idx
                if player_idx < len(selected_players):
                    player_name = selected_players[player_idx]
                    player = selected_rows[selected_rows["Player"] == player_name].iloc[0]
                    
                    # Get archetype info
                    primary_archetype = player.get('Primary_Archetype', 'N/A')
                    archetype_score = player.get('Archetype_Score', 0)
                    
                    # Border colors based on cluster
                    border_colors = {0: '#1E88E5', 1: '#43A047', 2: '#FB8C00'}
                    cluster_id = player['Cluster']
                    
                    # Calculate overall rating for this player
                    metrics_for_cluster = cluster_metrics_map_analysis.get(cluster_id, [])
                    available_metrics = [m for m in metrics_for_cluster if m in df.columns]
                    if available_metrics:
                        scaler_rating = MinMaxScaler()
                        scaled_vals = scaler_rating.fit_transform(df[available_metrics])
                        player_idx_in_df = df[df['Player'] == player_name].index[0]
                        player_position_in_filtered = df.index.get_loc(player_idx_in_df)
                        overall_rating = scaled_vals[player_position_in_filtered].mean() * 100
                    else:
                        overall_rating = 0
                    
                    with col:
                        
                        # Minimal card with border
                        st.markdown(f"""
                            <div class='player-card' style='border: 2px solid {border_colors.get(cluster_id, border_colors[0])};
                                        border-radius: 10px; padding: 1rem; 
                                        background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                                <div style='text-align: center;'>
                                    <div style='color: {border_colors.get(cluster_id, border_colors[0])}; 
                                                font-size: 0.8rem; font-weight: 600;'>
                                        SELECTED #{player_idx + 1}
                                    </div>
                                    <h4 style='margin: 0.3rem 0; color: #333; font-size: 1.1rem; background: linear-gradient(135deg, {get_profile_color(cluster_id)}15, {get_profile_color(cluster_id)}08); padding: 0.3rem 0.5rem; border-radius: 4px;'>
                                        {player['Player']}
                                    </h4>
                                    <p style='margin: 0; color: {get_team_color(player['Squad'])}; font-size: 0.85rem; background: linear-gradient(135deg, {get_profile_color(cluster_id)}12, {get_profile_color(cluster_id)}05); padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600;'>
                                        {player['Squad']}
                                    </p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Compact info grid
                        st.markdown(f"""
                            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; 
                                        margin-top: 0.8rem; font-size: 0.85rem;'>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Nation</div>
                                    <div style='font-weight: 600; color: #333;'>{player.get('Nation', 'N/A')}</div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Age</div>
                                    <div style='font-weight: 600; color: #333;'>{player['Age']:.0f}</div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px; grid-column: span 2;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Profile</div>
                                    <div style='font-weight: 600; color: {border_colors.get(cluster_id, border_colors[0])}; font-size: 0.75rem;'>
                                        {cluster_id}: {cluster_profiles[cluster_id]['name']}
                                    </div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px; grid-column: span 2;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Overall Rating</div>
                                    <div style='font-weight: 600; color: {get_rating_color(overall_rating)};'>
                                        {overall_rating:.1f}
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        
                        # Archetype section
                        st.markdown(f"""
                            <div style='margin-top: 0.8rem; padding: 0.6rem; 
                                        background: linear-gradient(135deg, {get_archetype_color(primary_archetype)}15, {get_archetype_color(primary_archetype)}05);
                                        border-radius: 5px; text-align: center;'>
                                <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.4rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.2rem; display: inline-block;'>
                                    Archetype
                                </div>
                                <div style='font-weight: 700; color: {get_archetype_color(primary_archetype)}; 
                                            font-size: 0.95rem;'>
                                    {primary_archetype}
                                </div>
                                <div style='color: #666; font-size: 0.75rem; margin-top: 0.2rem;'>
                                   Archetype Score: {archetype_score:.1f}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Performance stats - Dynamic based on archetype
                        archetype = str(primary_archetype).strip()
                        if archetype == 'Anchor':
                            metric1_label, metric1_value = "Tkl+Int", player['def_Tkl+Int']
                            metric2_label, metric2_value = "Blocks", player['def_Blocks']
                            metric3_label, metric3_value = "Recoveries", player['misc_Recov']
                        elif archetype == 'DLP':
                            metric1_label, metric1_value = "Pass Success", player['pass_Cmp%']
                            metric2_label, metric2_value = "Prog Distance", player['pass_PrgDist']
                            metric3_label, metric3_value = "Prog Passes", player['pass_PrgP']
                        elif archetype == 'BallWinner':
                            metric1_label, metric1_value = "Tkl+Int", player['def_Tkl+Int']
                            metric2_label, metric2_value = "Tkl Won", player['def_TklW']
                            metric3_label, metric3_value = "Recoveries", player['misc_Recov']
                        elif archetype == 'BoxToBox':
                            metric1_label, metric1_value = "Prog Runs", player['std_PrgR']
                            metric2_label, metric2_value = "Recoveries", player['misc_Recov']
                            metric3_label, metric3_value = "Prog Distance", player['poss_PrgDist']
                        elif archetype == 'APM':
                            metric1_label, metric1_value = "Key Passes", player['pass_KP']
                            metric2_label, metric2_value = "xAG", player['std_xAG']
                            metric3_label, metric3_value = "GCA Pass", player['gca_PassLive']
                        elif archetype == 'CAM':
                            metric1_label, metric1_value = "Final 3rd", player['poss_1/3']
                            metric2_label, metric2_value = "Pen Area", player['poss_CPA']
                            metric3_label, metric3_value = "xAG", player['std_xAG']
                        elif archetype == 'BoxCrasher':
                            metric1_label, metric1_value = "xG", player['std_xG']
                            metric2_label, metric2_value = "Shots", player['shoot_Sh']
                            metric3_label, metric3_value = "Goals", player['std_Gls']
                        else:  # Default/fallback metrics
                            metric1_label, metric1_value = "Minutes", player['std_Min']
                            metric2_label, metric2_value = "Pass Success", player['pass_Cmp%']
                            metric3_label, metric3_value = "Matches", player['std_MP']
                        
                        
                        
                        st.markdown(f"""
                            <div style='margin-top: 0.8rem; padding: 0.6rem; background: #f9f9f9; border-radius: 5px;'>
                                <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.3rem; font-size: 0.75rem; text-align: center;'>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric1_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric1_value, archetype)};'>{metric1_value:.1f}</div>
                                    </div>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric2_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric2_value, archetype)};'>{metric2_value:.1f}</div>
                                    </div>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric3_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric3_value, archetype)};'>{metric3_value:.1f}</div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("---")

        # ---------------------------
        # Multi-Player vs Cluster Radar
        # ---------------------------
        scaler = MinMaxScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df[radar_metrics]), columns=radar_metrics, index=df.index)

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
        
        # Add player profile averages
        # Chart renkler - birbirinden ayırt edilebilir
        cluster_colors = ['#1E88E5', '#43A047', '#FB8C00']  # Profile 0: Mavi, Profile 1: Yeşil, Profile 2: Turuncu
        for idx, cluster_id in enumerate(unique_clusters):
            cluster_mean_scaled = df_scaled[df["Cluster"] == cluster_id].mean()
            cluster_color = cluster_colors[cluster_id % len(cluster_colors)]
            # Create closed polygon by adding first value to the end
            r_cluster_values = list(cluster_mean_scaled.values) + [cluster_mean_scaled.values[0]]
            theta_cluster_values = metrics_tr + [metrics_tr[0]]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=r_cluster_values, 
                theta=theta_cluster_values, 
                fill='toself', 
                name=f"Player Profile {cluster_id} Average", 
                line=dict(color=cluster_color, width=3, dash='dot'), 
                opacity=0.6,
                visible='legendonly'
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,1])),
            showlegend=True, 
            title="Selected Players vs Player Profile Averages",
            template='plotly_dark', 
            title_font=dict(size=20), 
            legend=dict(font=dict(size=12))
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # ---------------------------
        # Category-Based Radars
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
            cat_metrics_available = [m for m in cat_metrics if m in df.columns]
            cat_metrics_tr = [column_info[m] for m in cat_metrics_available]
            
            if not cat_metrics_tr:
                continue
                
            # Scaling for category
            cat_scaler = MinMaxScaler()
            df_cat_scaled = pd.DataFrame(
                cat_scaler.fit_transform(df[cat_metrics_available]),
                columns=cat_metrics_tr, 
                index=df.index
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
            
            # Add player profile averages
            for idx, cluster_id in enumerate(unique_clusters):
                cluster_mean_cat = df_cat_scaled[df["Cluster"] == cluster_id].mean()
                cluster_color = cluster_colors[cluster_id % len(cluster_colors)]
                # Create closed polygon by adding first value to the end
                r_cat_cluster_values = list(cluster_mean_cat.values) + [cluster_mean_cat.values[0]]
                theta_cat_cluster_values = cat_metrics_tr + [cat_metrics_tr[0]]
                
                fig_cat.add_trace(go.Scatterpolar(
                    r=r_cat_cluster_values, 
                    theta=theta_cat_cluster_values, 
                    fill='toself', 
                    name=f"Player Profile {cluster_id} Average", 
                    line=dict(color=cluster_color, width=3, dash='dot'), 
                    opacity=0.6,
                    visible='legendonly'
                ))

            fig_cat.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0,1])),
                showlegend=True,
                template='plotly_dark',
                title=f"{category} - Selected Players vs Player Profile Averages",
                title_font=dict(size=20),
                legend=dict(font=dict(size=12))
            )
            st.plotly_chart(fig_cat, use_container_width=True)

            

        # ---------------------------
        # Similar Players
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.5rem 0;'>
                <h2 style='font-size: 2rem; font-weight: 800;
                           background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    Similar Players
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Find similar players for each selected player
        for player_name in selected_players:
            player_row = selected_rows[selected_rows["Player"] == player_name]
            if not player_row.empty:
                df_metrics = df[radar_metrics].copy()
                selected_vector = player_row[radar_metrics].values.flatten()
                df_temp = df.copy()
                df_temp["Similarity"] = np.linalg.norm(df_metrics.values - selected_vector, axis=1)
                similar_players = df_temp[df_temp["Player"] != player_name].nsmallest(5, "Similarity")
                
                st.write(f"5 most similar players to **{player_name}**:")
                st.dataframe(similar_players[["Player","Pos","Squad","Age","Cluster"] + radar_metrics])

        # ---------------------------
        # Compare All Player Profiles
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.5rem 0;'>
                <h2 style='font-size: 2rem; font-weight: 800;
                           background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    Compare All Player Profiles
                </h2>
            </div>
        """, unsafe_allow_html=True)
        df_scaled_all = pd.DataFrame(MinMaxScaler().fit_transform(df[radar_metrics]),
                                     columns=radar_metrics, index=df.index)
        cluster_means_scaled = df_scaled_all.groupby(df["Cluster"]).mean()
        fig_all = go.Figure()
        # Chart renkler - birbirinden ayırt edilebilir
        colors = ['#1E88E5', '#43A047', '#FB8C00']  # Profile 0: Mavi, Profile 1: Yeşil, Profile 2: Turuncu
        for idx, (cid,row) in enumerate(cluster_means_scaled.iterrows()):
            # Create closed polygon by adding first value to the end
            r_all_values = list(row.values) + [row.values[0]]
            theta_all_values = [column_info[m] for m in radar_metrics] + [column_info[radar_metrics[0]]]
            
            fig_all.add_trace(go.Scatterpolar(
                r=r_all_values,
                theta=theta_all_values,
                fill='toself',
                name=f"Player Profile {cid}",
                line=dict(width=2,color=colors[idx%len(colors)]),
                opacity=0.7
            ))
        fig_all.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,1])),
            showlegend=True,
            title="Comparison of All Player Profiles",
            template='plotly_dark'
        )
        st.plotly_chart(fig_all, use_container_width=True, key="all_clusters_radar")

        # ---------------------------
        # PDF / Excel Report
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.5rem 0;'>
                <h2 style='font-size: 2rem; font-weight: 800;
                           background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    Download Report
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        if len(selected_players) == 1:
            # Current format for single player
            player_name = selected_players[0]
            player_row = selected_rows[selected_rows["Player"] == player_name]
            df_metrics = df[radar_metrics].copy()
            selected_vector = player_row[radar_metrics].values.flatten()
            df_temp = df.copy()
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
                line = f"{row['Player']} | {row['Pos']} | {row['Squad']} | Profile {row['Cluster']}"
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
                line = f"{row['Player']} | {row['Pos']} | {row['Squad']} | Age: {row['Age']} | Profile: {row['Cluster']}"
                pdf.cell(200, 10, txt=line, ln=True)
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(label="Selected Players Comparison - Download PDF",
                               data=pdf_output,
                               file_name=f"player_comparison_{len(selected_players)}_players.pdf",
                               mime="application/pdf")

    # Call the analysis function
    update_player_view(player_select)

with tab5:
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0 1.5rem 0;'>
        <h1 style='font-size: 1.8rem; font-weight: 600; margin: 0; color: #2563eb;'>
            Advanced Scatter Plot Analyses
        </h1>
        <p style='color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
            Explore correlations and relationships between different player metrics
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Understanding Scatter Plots (Click to expand)", expanded=False):
        st.markdown("""
        **What are scatter plots?**
        - Each point represents one player
        - Colors indicate player profiles
        - Hover over points to see detailed information
        
        **How to interpret:**
        - Points in top-right indicate high performance in both metrics
        - Clusters show groups of similar players
        - Outliers indicate unique player characteristics
        """)

    st.markdown("---")

    # Create tabs for different scatter plot analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "Age vs Performance", 
        "Minutes vs Effectiveness",
        "Passing vs Creativity", 
        "Defense vs Attack"
    ])

    with tab1:
        st.markdown("### Age vs Performance Analysis")
        st.markdown("Analyze how player age correlates with goal and assist performance.")
        
        # Age vs Performance Scatter Plot
        fig_age = go.Figure()
        
        # Color by player profile - chart renkler
        cluster_colors_scatter = {0: '#1E88E5', 1: '#43A047', 2: '#FB8C00'}  # Mavi, Yeşil, Turuncu
        cluster_names = {0: 'Elite Creative', 1: 'Developing', 2: 'Defensive Engines'}
        
        for cluster_id in df['Cluster'].unique():
            cluster_data = df[df['Cluster'] == cluster_id]
            
            fig_age.add_trace(go.Scatter(
                x=cluster_data['Age'],
                y=cluster_data['std_Gls'] + cluster_data['std_Ast'],
                mode='markers',
                name=f'Profile {cluster_id}: {cluster_names[cluster_id]}',
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
            youngest_top_performer = df.loc[df['std_Gls'] + df['std_Ast'] > 1.5, 'Age'].min()
            st.metric("Youngest High Performer Age", f"{youngest_top_performer:.0f}" if not pd.isna(youngest_top_performer) else "N/A")
        with col2:
            avg_age_top_performers = df[df['std_Gls'] + df['std_Ast'] > 1.0]['Age'].mean()
            st.metric("Avg Age of Top Contributors", f"{avg_age_top_performers:.1f}" if not pd.isna(avg_age_top_performers) else "N/A")

    with tab2:
        st.markdown("### Playing Time vs Effectiveness")
        st.markdown("Examine the relationship between minutes played and expected goal contributions.")
        
        # Minutes vs Effectiveness Scatter Plot
        fig_minutes = go.Figure()
        
        for cluster_id in df['Cluster'].unique():
            cluster_data = df[df['Cluster'] == cluster_id]
            
            fig_minutes.add_trace(go.Scatter(
                x=cluster_data['std_Min'],
                y=cluster_data['std_xG'] + cluster_data['std_xAG'],
                mode='markers',
                name=f'Profile {cluster_id}: {cluster_names[cluster_id]}',
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
            eligible_players = df[df['std_Min'] > 1000].copy()
            if not eligible_players.empty:
                eligible_players['efficiency'] = (eligible_players['std_xG'] + eligible_players['std_xAG']) / eligible_players['std_Min'] * 1000
                efficiency_leader_idx = eligible_players['efficiency'].idxmax()
                efficiency_leader = df.loc[efficiency_leader_idx]
                st.metric("Most Efficient Player", efficiency_leader['Player'])
            else:
                st.metric("Most Efficient Player", "N/A")
        with col2:
            avg_minutes = df['std_Min'].mean()
            st.metric("Average Minutes Played", f"{avg_minutes:.0f}")

    with tab3:
        st.markdown("### Passing Accuracy vs Creativity")
        st.markdown("Discover the balance between safe passing and creative playmaking.")
        
        # Passing vs Creativity Scatter Plot
        fig_passing = go.Figure()
        
        for cluster_id in df['Cluster'].unique():
            cluster_data = df[df['Cluster'] == cluster_id]
            
            fig_passing.add_trace(go.Scatter(
                x=cluster_data['pass_Cmp%'],
                y=cluster_data['pass_KP'],
                mode='markers',
                name=f'Profile {cluster_id}: {cluster_names[cluster_id]}',
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
            if not df.empty and 'pass_Cmp%' in df.columns:
                best_passer_idx = df['pass_Cmp%'].idxmax()
                best_passer = df.loc[best_passer_idx]
                st.metric("Most Accurate Passer", f"{best_passer['Player']} ({best_passer['pass_Cmp%']:.1%})")
            else:
                st.metric("Most Accurate Passer", "N/A")
        with col2:
            if not df.empty and 'pass_KP' in df.columns:
                most_creative_idx = df['pass_KP'].idxmax()
                most_creative = df.loc[most_creative_idx]
                st.metric("Most Creative Player", f"{most_creative['Player']} ({most_creative['pass_KP']:.1f} KP)")
            else:
                st.metric("Most Creative Player", "N/A")

    with tab4:
        st.markdown("### Defensive vs Offensive Contributions")
        st.markdown("Compare players' defensive work rate with their attacking output.")
        
        # Defense vs Attack Scatter Plot
        fig_def_att = go.Figure()
        
        for cluster_id in df['Cluster'].unique():
            cluster_data = df[df['Cluster'] == cluster_id]
            
            fig_def_att.add_trace(go.Scatter(
                x=cluster_data['def_Tkl'] + cluster_data['def_Int'],
                y=cluster_data['std_Gls'] + cluster_data['std_Ast'],
                mode='markers',
                name=f'Profile {cluster_id}: {cluster_names[cluster_id]}',
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
            if not df.empty:
                defensive_actions = df['def_Tkl'] + df['def_Int']
                best_defender_idx = defensive_actions.idxmax()
                best_defender = df.loc[best_defender_idx]
                st.metric("Best Defender", f"{best_defender['Player']} ({defensive_actions.loc[best_defender_idx]:.1f})")
            else:
                st.metric("Best Defender", "N/A")
        with col2:
            if not df.empty:
                balance_score = ((df['def_Tkl'] + df['def_Int']) * 
                               (df['std_Gls'] + df['std_Ast']))
                most_balanced_idx = balance_score.idxmax()
                most_balanced = df.loc[most_balanced_idx]
                st.metric("Most Balanced Player", most_balanced['Player'])
            else:
                st.metric("Most Balanced Player", "N/A")

    st.divider()

    # Summary insights section - Clean
    st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; text-align: center; color: #2563eb;'>
                💡 Key Insights from Scatter Analysis
            </h2>
            <p style='text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;'>
                Statistical correlations and standout performers
            </p>
        </div>
    """, unsafe_allow_html=True)

    insights_col1, insights_col2 = st.columns(2)

    with insights_col1:
        st.markdown("### Performance Trends")
        
        # Calculate correlations
        age_performance_corr = df['Age'].corr(df['std_Gls'] + df['std_Ast'])
        minutes_effectiveness_corr = df['std_Min'].corr(df['std_xG'] + df['std_xAG'])
        
        st.write(f"• **Age-Performance Correlation**: {age_performance_corr:.3f}")
        st.write(f"• **Minutes-Effectiveness Correlation**: {minutes_effectiveness_corr:.3f}")
        
        if age_performance_corr > 0.1:
            st.success("Older players tend to be more productive")
        elif age_performance_corr < -0.1:
            st.info("Younger players show higher goal contributions")
        else:
            st.info("Age has minimal impact on performance")

    with insights_col2:
        st.markdown("### Standout Players")
        
        # Find standout players in different categories
        young_players = df[df['Age'] <= 20]
        if not young_players.empty:
            top_young_talent = young_players.nlargest(1, 'std_Gls')
            if not top_young_talent.empty:
                st.write(f"• **Top Young Talent**: {top_young_talent.iloc[0]['Player']} (Age {top_young_talent.iloc[0]['Age']})")
            else:
                st.write("• **Top Young Talent**: No players ≤20 years old")
        else:
            st.write("• **Top Young Talent**: No players ≤20 years old")
        
        experienced_players = df[df['std_Min'] > 1000]
        if not experienced_players.empty:
            most_efficient = experienced_players.nlargest(1, 'std_xG')
            if not most_efficient.empty:
                st.write(f"• **Most Efficient**: {most_efficient.iloc[0]['Player']} ({most_efficient.iloc[0]['std_xG']:.2f} xG)")
            else:
                st.write("• **Most Efficient**: No experienced players found")
        else:
            st.write("• **Most Efficient**: No experienced players found")
        
        # Best two-way player
        if not df.empty:
            df_copy = df.copy()
            df_copy['two_way_score'] = (df_copy['std_Gls'] + df_copy['std_Ast']) * (df_copy['def_Tkl'] + df_copy['def_Int'])
            best_two_way = df_copy.nlargest(1, 'two_way_score')
            
            if not best_two_way.empty:
                st.write(f"• **Best Two-Way Player**: {best_two_way.iloc[0]['Player']}")
            else:
                st.write("• **Best Two-Way Player**: No data available")
        else:
            st.write("• **Best Two-Way Player**: No data available")

with tab6:
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0 1.5rem 0;'>
        <h1 style='font-size: 1.8rem; font-weight: 600; margin: 0; color: #2563eb;'>
            Trend & Line Chart Analyses
        </h1>
        <p style='color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
            Discover performance trends across different dimensions
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("How to read trend charts (Click to expand)", expanded=False):
        st.markdown("""
        **Understanding trends:**
        - Line charts show average performance at different levels
        - Multiple lines allow comparison across metrics
        - Peaks indicate optimal performance ranges
        
        **Use cases:**
        - Identify age peaks for different skills
        - Compare team performance levels
        - Understand playing time impact on performance
        """)

    st.markdown("---")

    # Create tabs for different trend analyses
    trend_tab1, trend_tab2, trend_tab3= st.tabs([
        "Age Trends", 
        "Playing Time Trends",
        "Team Performance Trends", 
    ])

    with trend_tab1:
        st.markdown("### Performance Trends by Age")
        st.markdown("Analyze how different performance metrics change with player age.")
        
        # Age trend analysis
        age_groups = df.groupby('Age').agg({
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
            
            st.plotly_chart(fig_age_trend, use_container_width=True, key="age_trend_offensive")
            
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
            
            st.plotly_chart(fig_age_def, use_container_width=True, key="age_trend_defensive")
            
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
        st.markdown("### Performance vs Playing Time")
        st.markdown("Examine how performance metrics correlate with minutes played.")
        
        # Create minutes bins for trend analysis
        df['Minutes_Bin'] = pd.cut(df['std_Min'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        minutes_trend = df.groupby('Minutes_Bin').agg({
            'std_Gls': 'mean',
            'std_Ast': 'mean',
            'std_xG': 'mean',
            'std_xAG': 'mean',
            'pass_KP': 'mean',
            'def_Tkl': 'mean',
            'Player': 'count'
        }).reset_index()
        minutes_trend.rename(columns={'Player': 'Player_Count'}, inplace=True)
        
        if not minutes_trend.empty:
            # Minutes vs Performance chart
            fig_minutes_trend = go.Figure()
            
            fig_minutes_trend.add_trace(go.Scatter(
                x=minutes_trend['Minutes_Bin'],
                y=minutes_trend['std_Gls'],
                mode='lines+markers',
                name='Goals per Game',
                line=dict(color='#FF6B6B', width=3),
                marker=dict(size=8)
            ))
# Trend analysis moved to Tab6

    
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
    st.markdown("### Performance vs Playing Time")
    st.markdown("Examine how performance metrics correlate with minutes played.")
    
    # Create minutes bins for trend analysis
    df_minutes = df.copy()
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
        
        st.plotly_chart(fig_minutes_trend, use_container_width=True, key="minutes_trend")
        
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
    st.markdown("### Team Performance Comparison")
    st.markdown("Compare average performance metrics across different teams.")
    
    # Team performance analysis
    team_performance = df.groupby('Squad').agg({
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
        
        st.plotly_chart(fig_team_off, use_container_width=True, key="team_offensive_trend")
        
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
        
        st.plotly_chart(fig_team_def, use_container_width=True, key="team_defensive_trend")
        
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



# Key Trend Insights moved to Tab6

with tab7:
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0 1.5rem 0;'>
        <h1 style='font-size: 1.8rem; font-weight: 600; margin: 0; color: #2563eb;'>
            Distribution Analysis (Histograms)
        </h1>
        <p style='color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
            Understand how player metrics are distributed across the dataset
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Reading histograms (Click to expand)", expanded=False):
        st.markdown("""
        **What are histograms?**
        - Show the distribution of values for a specific metric
        - Height indicates how many players fall into each range
        - Help identify patterns and outliers in the data
        
        **How to interpret:**
        - Normal distribution: Bell-shaped curve
        - Skewed distribution: Most values on one side
        - Bimodal: Two distinct peaks
        """)

    st.markdown("---")

    # Create tabs for different histogram analyses
    hist_tab1, hist_tab2, hist_tab3, hist_tab4 = st.tabs([
        "Performance Metrics", 
        "Playing Time & Participation",
        "Passing & Creativity", 
        "Defensive & Discipline"
    ])

    with hist_tab1:
        st.markdown("### Performance Metrics Distribution")
        st.markdown("Analyze the distribution of goals, assists, and expected performance metrics.")
        
        # Goals distribution
        fig_goals_hist = go.Figure()
        fig_goals_hist.add_trace(go.Histogram(
            x=df['std_Gls'],
            nbinsx=20,
            name='Goals per Game',
            marker_color='#FF6B6B',
            opacity=0.7
        ))
        
        fig_goals_hist.update_layout(
            title="Distribution of Goals per Game",
            xaxis_title="Goals per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_goals_hist, use_container_width=True, key="goals_histogram")
        
        # Assists distribution
        fig_assists_hist = go.Figure()
        fig_assists_hist.add_trace(go.Histogram(
            x=df['std_Ast'],
            nbinsx=20,
            name='Assists per Game',
            marker_color='#4ECDC4',
            opacity=0.7
        ))
        
        fig_assists_hist.update_layout(
            title="Distribution of Assists per Game",
            xaxis_title="Assists per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_assists_hist, use_container_width=True, key="assists_histogram")
        
        # Combined Goals + Assists
        df['Goals_Assists'] = df['std_Gls'] + df['std_Ast']
        fig_ga_hist = go.Figure()
        fig_ga_hist.add_trace(go.Histogram(
            x=df['Goals_Assists'],
            nbinsx=20,
            name='Goals + Assists',
            marker_color='#45B7D1',
            opacity=0.7
        ))
        
        fig_ga_hist.update_layout(
            title="Distribution of Goals + Assists per Game",
            xaxis_title="Goals + Assists per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_ga_hist, use_container_width=True, key="goals_assists_histogram")

    with hist_tab2:
        st.markdown("### Playing Time & Participation Distribution")
        st.markdown("Examine how playing time and match participation are distributed.")
        
        # Minutes distribution
        fig_minutes_hist = go.Figure()
        fig_minutes_hist.add_trace(go.Histogram(
            x=df['std_Min'],
            nbinsx=20,
            name='Minutes Played',
            marker_color='#96CEB4',
            opacity=0.7
        ))
        
        fig_minutes_hist.update_layout(
            title="Distribution of Minutes Played",
            xaxis_title="Minutes Played",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_minutes_hist, use_container_width=True, key="minutes_histogram")
        
        # Matches distribution
        fig_matches_hist = go.Figure()
        fig_matches_hist.add_trace(go.Histogram(
            x=df['std_MP'],
            nbinsx=20,
            name='Matches Played',
            marker_color='#FFEAA7',
            opacity=0.7
        ))
        
        fig_matches_hist.update_layout(
            title="Distribution of Matches Played",
            xaxis_title="Matches Played",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_matches_hist, use_container_width=True, key="matches_histogram")
        
        # Age distribution
        fig_age_hist = go.Figure()
        fig_age_hist.add_trace(go.Histogram(
            x=df['Age'],
            nbinsx=10,
            name='Age',
            marker_color='#DDA0DD',
            opacity=0.7
        ))
        
        fig_age_hist.update_layout(
            title="Distribution of Player Ages",
            xaxis_title="Age",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_age_hist, use_container_width=True, key="age_histogram")

    with hist_tab3:
        st.markdown("### Passing & Creativity Distribution")
        st.markdown("Analyze the distribution of passing accuracy and creative metrics.")
        
        # Passing accuracy distribution
        fig_pass_hist = go.Figure()
        fig_pass_hist.add_trace(go.Histogram(
            x=df['pass_Cmp%'],
            nbinsx=20,
            name='Pass Completion %',
            marker_color='#98D8C8',
            opacity=0.7
        ))
        
        fig_pass_hist.update_layout(
            title="Distribution of Pass Completion Rate",
            xaxis_title="Pass Completion %",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_pass_hist, use_container_width=True, key="pass_completion_histogram")
        
        # Key passes distribution
        fig_kp_hist = go.Figure()
        fig_kp_hist.add_trace(go.Histogram(
            x=df['pass_KP'],
            nbinsx=20,
            name='Key Passes per Game',
            marker_color='#F7DC6F',
            opacity=0.7
        ))
        
        fig_kp_hist.update_layout(
            title="Distribution of Key Passes per Game",
            xaxis_title="Key Passes per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_kp_hist, use_container_width=True, key="key_passes_histogram")
        
        # Progressive passing distribution
        fig_prog_pass = go.Figure()
        fig_prog_pass.add_trace(go.Histogram(
            x=df['pass_PrgDist'],
            nbinsx=20,
            name='Progressive Pass Distance',
            marker_color='#BB8FCE',
            opacity=0.7
        ))
        
        fig_prog_pass.update_layout(
            title="Distribution of Progressive Pass Distance",
            xaxis_title="Progressive Pass Distance",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_prog_pass, use_container_width=True, key="progressive_passing_histogram")
        
        # Progressive carrying distribution
        fig_prog_carry = go.Figure()
        fig_prog_carry.add_trace(go.Histogram(
            x=df['poss_PrgDist'],
            nbinsx=20,
            name='Progressive Carry Distance',
            marker_color='#85C1E9',
            opacity=0.7
        ))
        
        fig_prog_carry.update_layout(
            title="Distribution of Progressive Carry Distance",
            xaxis_title="Progressive Carry Distance",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_prog_carry, use_container_width=True, key="progressive_carrying_histogram")

    with hist_tab4:
        st.markdown("### Defensive & Discipline Distribution")
        st.markdown("Examine the distribution of defensive actions and disciplinary metrics.")
        
        # Tackles distribution
        fig_tackles_hist = go.Figure()
        fig_tackles_hist.add_trace(go.Histogram(
            x=df['def_Tkl'],
            nbinsx=20,
            name='Tackles per Game',
            marker_color='#F8C471',
            opacity=0.7
        ))
        
        fig_tackles_hist.update_layout(
            title="Distribution of Tackles per Game",
            xaxis_title="Tackles per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_tackles_hist, use_container_width=True, key="tackles_histogram")
        
        # Interceptions distribution
        fig_int_hist = go.Figure()
        fig_int_hist.add_trace(go.Histogram(
            x=df['def_Int'],
            nbinsx=20,
            name='Interceptions per Game',
            marker_color='#82E0AA',
            opacity=0.7
        ))
        
        fig_int_hist.update_layout(
            title="Distribution of Interceptions per Game",
            xaxis_title="Interceptions per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_int_hist, use_container_width=True, key="interceptions_histogram")
        
        # Ball recoveries distribution
        fig_recov_hist = go.Figure()
        fig_recov_hist.add_trace(go.Histogram(
            x=df['misc_Recov'],
            nbinsx=20,
            name='Ball Recoveries per Game',
            marker_color='#F1948A',
            opacity=0.7
        ))
        
        fig_recov_hist.update_layout(
            title="Distribution of Ball Recoveries per Game",
            xaxis_title="Ball Recoveries per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_recov_hist, use_container_width=True, key="recoveries_histogram")
        
        # Yellow cards distribution
        fig_yellow_hist = go.Figure()
        fig_yellow_hist.add_trace(go.Histogram(
            x=df['std_CrdY'],
            nbinsx=20,
            name='Yellow Cards per Game',
            marker_color='#F7DC6F',
            opacity=0.7
        ))
        
        fig_yellow_hist.update_layout(
            title="Distribution of Yellow Cards per Game",
            xaxis_title="Yellow Cards per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_yellow_hist, use_container_width=True, key="yellow_cards_histogram")
        
        # Fouls distribution
        fig_fouls_hist = go.Figure()
        fig_fouls_hist.add_trace(go.Histogram(
            x=df['misc_Fls'],
            nbinsx=20,
            name='Fouls per Game',
            marker_color='#D7BDE2',
            opacity=0.7
        ))
        
        fig_fouls_hist.update_layout(
            title="Distribution of Fouls per Game",
            xaxis_title="Fouls per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig_fouls_hist, use_container_width=True, key="fouls_histogram")

    st.divider()

    # Summary insights
    st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; text-align: center; color: #2563eb;'>
                💡 Key Insights from Distribution Analysis
            </h2>
            <p style='text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;'>
                Statistical patterns and data distribution characteristics
            </p>
        </div>
    """, unsafe_allow_html=True)

    insights_col1, insights_col2 = st.columns(2)

    with insights_col1:
        st.markdown("### Performance Distribution Patterns")
        
        # Goals distribution insights
        goals_mean = df['std_Gls'].mean()
        goals_std = df['std_Gls'].std()
        st.write(f"• **Goals per Game**: Mean = {goals_mean:.2f}, Std = {goals_std:.2f}")
        
        if goals_std > goals_mean:
            st.info("High variability in goal scoring")
        else:
            st.success("Consistent goal scoring patterns")
        
        # Assists distribution insights
        assists_mean = df['std_Ast'].mean()
        assists_std = df['std_Ast'].std()
        st.write(f"• **Assists per Game**: Mean = {assists_mean:.2f}, Std = {assists_std:.2f}")
        
        if assists_std > assists_mean:
            st.info("High variability in assist creation")
        else:
            st.success("Consistent assist patterns")

    with insights_col2:
        st.markdown("### Playing Time Distribution")
        
        # Minutes distribution insights
        minutes_mean = df['std_Min'].mean()
        minutes_std = df['std_Min'].std()
        st.write(f"• **Minutes Played**: Mean = {minutes_mean:.0f}, Std = {minutes_std:.0f}")
        
        if minutes_std > minutes_mean * 0.5:
            st.info("High variability in playing time")
        else:
            st.success("Consistent playing time allocation")
        
        # Age distribution insights
        age_mean = df['Age'].mean()
        age_std = df['Age'].std()
        st.write(f"• **Player Age**: Mean = {age_mean:.1f}, Std = {age_std:.1f}")
        
        if age_std > 2:
            st.info("Wide age range in the dataset")
        else:
            st.success("Focused age group")

# ---------------------------
# COMMON FOOTER FOR ALL TABS
# ---------------------------
st.markdown("""
    <div style='text-align: center; margin: 3rem 0 1rem 0; padding: 1rem; 
                background: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef;'>
        <p style='color: #6c757d; font-size: 0.8rem; margin: 0;'>
            Created by 
            <a href='https://www.linkedin.com/in/erensglm' target='_blank' 
               style='color: #2563eb; text-decoration: none; font-weight: 500;'>
                Emin Eren Sağlam
            </a>
            , 
            <a href='https://x.com/blindsiderdata' target='_blank' 
               style='color: #2563eb; text-decoration: none; font-weight: 500;'>
                Blindsiderdata
            </a>
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# STEP 8: HISTOGRAM ANALYSES - Moved to Tab7
# ---------------------------
# Distribution analysis moved to Tab7
