import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF
from sklearn.preprocessing import MinMaxScaler
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import matplotlib as mpl

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
if os.path.exists('data/eredivisie_midfielders_final_profiles.csv'):
    df = pd.read_csv('data/eredivisie_midfielders_final_profiles.csv')
elif os.path.exists('notebooks/../data/eredivisie_midfielders_final_profiles.csv'):
    df = pd.read_csv('notebooks/../data/eredivisie_midfielders_final_profiles.csv')
else:
    st.error("CSV file not found!")
    st.stop()
df = df.dropna(how='all')  # Clean empty rows

# Matplotlib default font (avoid missing 'Inter' warnings)
mpl.rcParams['font.family'] = 'DejaVu Sans'

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
        'BallWinner': '#1e3a8a',  # Navy (Lacivert)
        'BoxToBox': '#facc15',   # Lighter Yellow
        'APM': '#059669',        # Teal
        'Mezzala': '#2563eb',        # Blue (moved from CAM)
        'ShadowStriker': '#7c3aed'  # Purple (was BoxCrasher)
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
        1: '#ec4899',  # Pink for Developing
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
        'Mezzala': {
            'low': '#7c2d12',       # Dark red
            'medium_low': '#ea580c', # Orange
            'medium': '#d97706',    # Orange
            'medium_high': '#65a30d', # Light green
            'high': '#059669'      # Emerald
        },
        'ShadowStriker': {
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

# Similarity helpers
def get_0_100_metric_columns(df_input: pd.DataFrame) -> list:
    """Infer 0-100 scaled metric columns by value range, excluding id/meta fields."""
    exclude_cols = {
        'Player','Squad','Nation','Pos','Primary_Archetype','Secondary_Archetype',
        'Secondary_Archetype_Score','Archetype_Score','Cluster','Minutes_Bin'
    }
    # Age may be <= 100 but we don't want it as a score feature
    exclude_cols.add('Age')
    metric_cols = []
    for col in df_input.columns:
        if col in exclude_cols:
            continue
        s = df_input[col]
        if pd.api.types.is_numeric_dtype(s):
            vals = s.dropna().values
            if vals.size == 0:
                continue
            vmin = np.nanmin(vals)
            vmax = np.nanmax(vals)
            if vmin >= 0 and vmax <= 100:
                metric_cols.append(col)
    return metric_cols

def find_similar_players(df_all: pd.DataFrame, selected_player: str, top_k: int = 3) -> pd.DataFrame:
    """Return top_k most similar players to selected_player within the same Cluster.
    - Uses Euclidean distance over inferred 0-100 metric columns
    - Converts distance to 0-100 Similarity_Score: 100 - (d/max_d)*100
    """
    if selected_player not in set(df_all['Player']):
        return pd.DataFrame(columns=['Player','Squad','Age','Primary_Archetype','Similarity_Score'])

    metrics = get_0_100_metric_columns(df_all)
    if len(metrics) == 0:
        return pd.DataFrame(columns=['Player','Squad','Age','Primary_Archetype','Similarity_Score'])

    sel_row = df_all[df_all['Player'] == selected_player].iloc[0]
    sel_cluster = sel_row.get('Cluster', None)
    df_cluster = df_all[df_all['Cluster'] == sel_cluster].copy() if sel_cluster is not None else df_all.copy()

    # Drop rows without any metric values; fill remaining NaNs by cluster-wise column mean
    cluster_means = df_cluster[metrics].mean(numeric_only=True)
    df_cluster[metrics] = df_cluster[metrics].fillna(cluster_means).infer_objects(copy=False)

    sel_vec = sel_row[metrics].fillna(cluster_means).infer_objects(copy=False).values.astype(float)
    # Compute distances
    mat = df_cluster[metrics].values.astype(float)
    diffs = mat - sel_vec
    dists = np.linalg.norm(diffs, axis=1)
    df_cluster = df_cluster.assign(_dist=dists)
    # Exclude self
    df_cluster = df_cluster[df_cluster['Player'] != selected_player]
    if df_cluster.empty:
        return pd.DataFrame(columns=['Player','Squad','Age','Primary_Archetype','Similarity_Score'])

    max_d = float(df_cluster['_dist'].max())
    if max_d == 0.0:
        sim_scores = np.full(len(df_cluster), 100.0)
    else:
        sim_scores = 100.0 - (df_cluster['_dist'].values / max_d) * 100.0
    df_cluster = df_cluster.assign(Similarity_Score=sim_scores)
    df_sorted = df_cluster.sort_values('Similarity_Score', ascending=False)
    top = df_sorted.head(top_k)
    return top[['Player','Squad','Age','Primary_Archetype','Similarity_Score']]

def find_similar_players_with_all_metrics(df_all: pd.DataFrame, selected_player: str, top_k: int = 3) -> pd.DataFrame:
    """Return top_k most similar players with ALL metrics for detailed Excel export.
    - Uses Euclidean distance over inferred 0-100 metric columns
    - Returns complete player data including all statistics
    """
    if selected_player not in set(df_all['Player']):
        return pd.DataFrame()

    metrics = get_0_100_metric_columns(df_all)
    if len(metrics) == 0:
        return pd.DataFrame()

    sel_row = df_all[df_all['Player'] == selected_player].iloc[0]
    sel_cluster = sel_row.get('Cluster', None)
    df_cluster = df_all[df_all['Cluster'] == sel_cluster].copy() if sel_cluster is not None else df_all.copy()

    # Drop rows without any metric values; fill remaining NaNs by cluster-wise column mean
    cluster_means = df_cluster[metrics].mean(numeric_only=True)
    df_cluster[metrics] = df_cluster[metrics].fillna(cluster_means).infer_objects(copy=False)

    sel_vec = sel_row[metrics].fillna(cluster_means).infer_objects(copy=False).values.astype(float)
    # Compute distances
    mat = df_cluster[metrics].values.astype(float)
    diffs = mat - sel_vec
    dists = np.linalg.norm(diffs, axis=1)
    df_cluster = df_cluster.assign(_dist=dists)
    # Exclude self
    df_cluster = df_cluster[df_cluster['Player'] != selected_player]
    if df_cluster.empty:
        return pd.DataFrame()

    max_d = float(df_cluster['_dist'].max())
    if max_d == 0.0:
        sim_scores = np.full(len(df_cluster), 100.0)
    else:
        sim_scores = 100.0 - (df_cluster['_dist'].values / max_d) * 100.0
    df_cluster = df_cluster.assign(Similarity_Score=sim_scores)
    df_sorted = df_cluster.sort_values('Similarity_Score', ascending=False)
    top = df_sorted.head(top_k)
    
    # Return all columns with Similarity_Score added
    result = top.copy()
    result = result.drop(columns=['_dist'])  # Remove internal distance column
    return result

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
    "League Leaders", 
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
        'Mezzala': {
            'name': 'Mezzala (Half-space Playmaker)',
            'description': 'Creative midfielder occupying the half-spaces, links midfield to attack with progressive carries and final-third combinations; arrives late into the box.',
            'key_metrics': ['Passes into Final Third', 'Carries into Penalty Area', 'xAG'],
            'example_players': ['Ismael Saibari (<span style="color: #ff6600;">PSV</span>)', 'Jorg Schreuders (<span style="color: #0066cc;">Groningen</span>)', 'Mohammed Ihattaren (<span style="color: #ff0000;">RKC Waalwijk</span>)']
        },
        'ShadowStriker': {
            'name': 'Shadow Striker (Second Striker)',
            'description': 'Attacking-minded midfielder attacking the box aggressively; prioritizes shot volume and goal threat with striker-like instincts from deeper positions.',
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
                        
                        
                        # Archetype section + Secondary (if exists)
                        secondary_arch = player.get('Secondary_Archetype', None)
                        secondary_score_val = player.get('Secondary_Archetype_Score', None)
                        secondary_html = ""
                        if isinstance(secondary_arch, str) and len(secondary_arch.strip()) > 0 and secondary_arch != 'N/A':
                            secondary_color = get_archetype_color(secondary_arch)
                            # Güvenli sayı formatlama
                            try:
                                sec_score_txt = f", {float(secondary_score_val):.0f}" if secondary_score_val is not None and not pd.isna(secondary_score_val) else ""
                            except Exception:
                                sec_score_txt = ""
                            secondary_html = f"<div style='color: #6b7280; font-size: 0.72rem; font-weight: 500; margin-top: 0.4rem;'>Secondary: <span style='color: {secondary_color}; font-weight: 700;'>{secondary_arch}</span>{sec_score_txt}</div>"

                        st.markdown(
                            f"""
                            <div style='margin-top: 0.8rem; padding: 0.6rem; 
                                        background: linear-gradient(135deg, {get_archetype_color(primary_archetype)}15, {get_archetype_color(primary_archetype)}05);
                                        border-radius: 5px; text-align: center; min-height: 120px;'>
                                <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.4rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.2rem; display: inline-block;'>
                                    Archetype
                                </div>
                                <div style='font-weight: 700; color: {get_archetype_color(primary_archetype)}; 
                                            font-size: 0.95rem;'>
                                    {primary_archetype}
                                </div>
                                <div style='color: #666; font-size: 0.75rem; margin-top: 0.2rem;'>
                                   Archetype Score: {archetype_score:.0f}
                                </div>
                            """ + secondary_html + f"""
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
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
                        elif archetype == 'Mezzala':
                            metric1_label, metric1_value = "Final 3rd", player['poss_1/3']
                            metric2_label, metric2_value = "Pen Area", player['poss_CPA']
                            metric3_label, metric3_value = "xAG", player['std_xAG']
                        elif archetype == 'ShadowStriker':
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
                                        <div style='font-weight: 600; color: {get_score_color(metric1_value, archetype)};'>{metric1_value:.0f}</div>
                                    </div>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric2_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric2_value, archetype)};'>{metric2_value:.0f}</div>
                                    </div>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric3_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric3_value, archetype)};'>{metric3_value:.0f}</div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
        
        st.divider()

    # ---------------------------------
    # Top 3 Players by Archetype (New)
    # ---------------------------------
    st.markdown("### Top 3 Players by Archetype")
    st.markdown("Filtrelere göre her arketipin en iyi 3 oyuncusu")

    if 'Primary_Archetype' in df_filtered.columns:
        archetypes = [
            'Anchor','DLP','BallWinner','BoxToBox','APM','Mezzala','ShadowStriker'
        ]

        for arch in archetypes:
            arch_df = df_filtered[df_filtered['Primary_Archetype'] == arch]
            if arch_df.empty:
                continue

            score_col = 'Archetype_Score' if 'Archetype_Score' in arch_df.columns else None
            if score_col:
                arch_top = arch_df.sort_values(score_col, ascending=False).head(3)
            else:
                arch_top = arch_df.sort_values('std_Min', ascending=False).head(3)

            st.markdown(f"#### {arch} - Top 3")
            cols = st.columns(3, gap="medium")
            for i in range(3):
                if i < len(arch_top):
                    player = arch_top.iloc[i]
                    with cols[i]:
                        # Ensure cluster_id_int exists before using in card styles
                        cluster_id = player.get('Cluster', None)
                        try:
                            cluster_id_int = int(cluster_id) if cluster_id is not None and not pd.isna(cluster_id) else None
                        except Exception:
                            cluster_id_int = None
                        card_color = get_profile_color(cluster_id_int) if cluster_id_int is not None else '#6b7280'
                        archetype_color = get_archetype_color(arch)
                        player_name = player.get('Player','N/A')
                        squad = player.get('Squad','N/A')
                        age = player.get('Age', np.nan)
                        score_val = float(player.get(score_col, 0)) if score_col else float(player.get('std_Min', 0))

                        st.markdown(f"""
                            <div class='player-card' style='border: 2px solid {card_color};
                                        border-radius: 10px; padding: 1rem; 
                                        background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                                <div style='text-align: center;'>
                                    <div style='color: {card_color}; font-size: 0.8rem; font-weight: 600;'>
                                        #{i + 1}
                                    </div>
                                    <h4 style='margin: 0.3rem 0; color: #333; font-size: 1.1rem; background: linear-gradient(135deg, {card_color}15, {card_color}08); padding: 0.3rem 0.5rem; border-radius: 4px;'>
                                        {player_name}
                                    </h4>
                                    <p style='margin: 0; color: {get_team_color(squad)}; font-size: 0.85rem; background: linear-gradient(135deg, {card_color}12, {card_color}05); padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600;'>
                                        {squad}
                                    </p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        age_display = 'N/A' if pd.isna(age) else f"{age:.0f}"
                        cluster_id = player.get('Cluster', None)
                        try:
                            cluster_id_int = int(cluster_id) if cluster_id is not None and not pd.isna(cluster_id) else None
                        except Exception:
                            cluster_id_int = None
                        profile_name = cluster_profiles.get(cluster_id_int, {}).get('name', 'N/A') if cluster_id_int is not None else 'N/A'
                        profile_color = get_profile_color(cluster_id_int) if cluster_id_int is not None else '#6b7280'

                        st.markdown(f"""
                            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; 
                                        margin-top: 0.8rem; font-size: 0.85rem;'>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Archetype</div>
                                    <div style='font-weight: 600; color: {archetype_color};'>{arch}</div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Age</div>
                                    <div style='font-weight: 600; color: #333;'>{age_display}</div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px; grid-column: span 2;'>
                                    <div style='color: #888; font-size: 0.7rem;'>Profile</div>
                                    <div style='font-weight: 600; color: {profile_color};'>{'' if cluster_id_int is None else cluster_id_int}: {profile_name}</div>
                                </div>
                                <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px; grid-column: span 2;'>
                                    <div style='color: #888; font-size: 0.7rem;'>{'Archetype Score' if score_col else 'Minutes'}</div>
                                    <div style='font-weight: 600; color: {get_rating_color(score_val if score_col else min(score_val/20, 100))};'>
                                        {score_val:.1f}
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

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
        st.markdown("###  Selected Player Cards")
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
                        
                        
                        # Archetype section + Secondary (if exists)
                        secondary_arch_sel = player.get('Secondary_Archetype', None)
                        secondary_score_sel = player.get('Secondary_Archetype_Score', None)
                        secondary_html_sel = ""
                        if isinstance(secondary_arch_sel, str) and len(secondary_arch_sel.strip()) > 0 and secondary_arch_sel != 'N/A':
                            secondary_color_sel = get_archetype_color(secondary_arch_sel)
                            try:
                                sec_score_txt_sel = f", {float(secondary_score_sel):.0f}" if secondary_score_sel is not None and not pd.isna(secondary_score_sel) else ""
                            except Exception:
                                sec_score_txt_sel = ""
                            secondary_html_sel = f"<div style='color: #6b7280; font-size: 0.72rem; font-weight: 500; margin-top: 0.4rem;'>Secondary: <span style='color: {secondary_color_sel}; font-weight: 700;'>{secondary_arch_sel}</span>{sec_score_txt_sel}</div>"

                        st.markdown(
                            f"""
                            <div style='margin-top: 0.8rem; padding: 0.6rem; 
                                        background: linear-gradient(135deg, {get_archetype_color(primary_archetype)}15, {get_archetype_color(primary_archetype)}05);
                                        border-radius: 5px; text-align: center; min-height: 120px;'>
                                <div style='color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.4rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.2rem; display: inline-block;'>
                                    Archetype
                                </div>
                                <div style='font-weight: 700; color: {get_archetype_color(primary_archetype)}; 
                                            font-size: 0.95rem;'>
                                    {primary_archetype}
                                </div>
                                <div style='color: #666; font-size: 0.75rem; margin-top: 0.2rem;'>
                                   Archetype Score: {archetype_score:.0f}
                                </div>
                            """ + secondary_html_sel + f"""
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
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
                        elif archetype == 'Mezzala':
                            metric1_label, metric1_value = "Final 3rd", player['poss_1/3']
                            metric2_label, metric2_value = "Pen Area", player['poss_CPA']
                            metric3_label, metric3_value = "xAG", player['std_xAG']
                        elif archetype == 'ShadowStriker':
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
                                        <div style='font-weight: 600; color: {get_score_color(metric1_value, archetype)};'>{metric1_value:.0f}</div>
                                    </div>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric2_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric2_value, archetype)};'>{metric2_value:.0f}</div>
                                    </div>
                                    <div>
                                        <div style='color: #888; font-size: 0.65rem;'>{metric3_label}</div>
                                        <div style='font-weight: 600; color: {get_score_color(metric3_value, archetype)};'>{metric3_value:.0f}</div>
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
            title_font=dict(size=16, color='#000000'), 
            legend=dict(font=dict(size=12))
        )
        
        # Standart Stats başlığı
        st.markdown("""
            <h2 style='color: #2563eb; margin: 0 0 1rem 0; font-size: 1.8rem; font-weight: 700;'>
                Standart Stats
            </h2>
        """, unsafe_allow_html=True)
        
        # Radar ve tabloyu yan yana göster
        radar_col, table_col = st.columns([2, 1.5], gap="large")
        with radar_col:
            st.plotly_chart(fig_radar, use_container_width=True)

        with table_col:
            # Seçilen oyuncular için metrik info kartları (Player vs Profile Avg, 0-100)
            st.markdown("<h4 style='margin:0 0 0.5rem 0;'>Info Cards</h4>", unsafe_allow_html=True)

            def build_player_info_card(player_name_str):
                pr = selected_rows[selected_rows["Player"] == player_name_str]
                if pr.empty:
                    return None
                idx = pr.index[0]
                player_scaled = df_scaled.loc[idx]
                cluster_id = pr.iloc[0].get("Cluster", None)
                try:
                    cluster_int = int(cluster_id) if cluster_id is not None and not pd.isna(cluster_id) else None
                except Exception:
                    cluster_int = None
                if cluster_int is None:
                    cluster_avg = pd.Series([np.nan]*len(radar_metrics), index=radar_metrics)
                else:
                    cluster_avg = df_scaled[df["Cluster"] == cluster_int][radar_metrics].mean()
                # Archetype average (Primary_Archetype)
                primary_arch = pr.iloc[0].get('Primary_Archetype', None)
                if primary_arch is None or pd.isna(primary_arch):
                    archetype_avg = pd.Series([np.nan]*len(radar_metrics), index=radar_metrics)
                else:
                    archetype_avg = df_scaled[df['Primary_Archetype'] == primary_arch][radar_metrics].mean()
                # Archetype color (for bars and legend)
                arch_color = get_archetype_color(str(primary_arch)) if primary_arch is not None and not pd.isna(primary_arch) else '#6b7280'

                player_vals = (player_scaled.values * 100).astype(float)
                profile_vals = (cluster_avg.values * 100).astype(float)
                archetype_vals = (archetype_avg.values * 100).astype(float)

                # Kart üst bilgileri
                squad_name = pr.iloc[0].get("Squad", "N/A")
                age_val = pr.iloc[0].get("Age", None)
                profile_name = cluster_profiles.get(cluster_int, {}).get("name", "N/A") if cluster_int is not None else "N/A"
                border_color = get_profile_color(cluster_int) if cluster_int is not None else '#6b7280'

                # Metrik satırlarını HTML olarak kur (Player vs Profile Avg vs Archetype Avg)
                rows_html = []
                for i, metric in enumerate(radar_metrics):
                    metric_label = column_info.get(metric, metric)
                    pv = 0.0 if pd.isna(player_vals[i]) else float(player_vals[i])
                    av = 0.0 if pd.isna(profile_vals[i]) else float(profile_vals[i])
                    aav = 0.0 if pd.isna(archetype_vals[i]) else float(archetype_vals[i])
                    row = f"""
                    <div style='margin:0.35rem 0;'>
                        <div style='font-size:0.75rem;color:#6b7280;margin-bottom:0.2rem;'>{metric_label}</div>
                        <div style='display:flex;align-items:center;gap:0.5rem;'>
                            <div style='flex:1;'>
                                <div style='height:8px;background:#e9ecef;border-radius:999px;'>
                                    <div style='height:8px;width:{pv:.0f}%;background:#000000;border-radius:999px;'></div>
                                </div>
                            </div>
                            <div style='width:42px;text-align:right;font-size:0.75rem;color:#000000;font-weight:600;'>{pv:.0f}</div>
                        </div>
                        <div style='display:flex;align-items:center;gap:0.5rem;margin-top:0.2rem;'>
                            <div style='flex:1;'>
                                <div style='height:6px;background:#f1f5f9;border-radius:999px;'>
                                    <div style='height:6px;width:{av:.0f}%;background:{border_color};border-radius:999px;'></div>
                                </div>
                            </div>
                            <div style='width:42px;text-align:right;font-size:0.72rem;color:{border_color};'>{av:.0f}</div>
                        </div>
                        <div style='display:flex;align-items:center;gap:0.5rem;margin-top:0.15rem;'>
                            <div style='flex:1;'>
                                <div style='height:6px;background:#f1f5f9;border-radius:999px;'>
                                    <div style='height:6px;width:{aav:.0f}%;background:{arch_color};border-radius:999px;'></div>
                                </div>
                            </div>
                            <div style='width:42px;text-align:right;font-size:0.72rem;color:{arch_color};'>{aav:.0f}</div>
                        </div>
                    </div>
                    """
                    rows_html.append(row)

                age_text = "N/A" if age_val is None or pd.isna(age_val) else f"{float(age_val):.0f}"
                primary_arch = pr.iloc[0].get('Primary_Archetype', 'N/A')
                card_html = f"""
                <div class='player-card' style='border: 2px solid {border_color}; border-radius: 10px; padding: 1rem; background: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                    <div style='display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;justify-content:space-between;margin-bottom:0.4rem;'>
                        <div style='display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;'>
                            <h4 style='margin:0;color:#111827;font-size:1.0rem;'>{player_name_str}</h4>
                            <span style='color:{get_team_color(squad_name)};font-size:0.85rem;font-weight:600;'>{squad_name}</span>
                            <span style='color:{border_color};font-size:0.8rem;font-weight:600;'>Profile {'' if cluster_int is None else cluster_int}: {profile_name}</span>
                        </div>
                        <div style='font-size:0.85rem;color:#6b7280;'>
                            Age: <span style='font-weight:700;color:#111827;'>{age_text}</span>
                            <span style='margin:0 0.4rem;'>|</span>
                            <span style='font-weight:700;color:{arch_color};'>{primary_arch}</span>
                        </div>
                    </div>
                    <div style='display:flex;align-items:center;gap:0.75rem;margin:0.25rem 0 0.5rem 0;'>
                        <div style='display:flex;align-items:center;gap:0.35rem;font-size:0.72rem;color:#000000;font-weight:600;'>
                            <span style='display:inline-block;width:10px;height:10px;background:#000000;border-radius:2px;'></span> Player
                        </div>
                        <div style='display:flex;align-items:center;gap:0.35rem;font-size:0.72rem;color:{border_color};'>
                            <span style='display:inline-block;width:10px;height:10px;background:{border_color};border-radius:2px;'></span> Profile Avg
                        </div>
                        <div style='display:flex;align-items:center;gap:0.35rem;font-size:0.72rem;color:{arch_color};'>
                            <span style='display:inline-block;width:10px;height:10px;background:{arch_color};border-radius:2px;'></span> Arc. Avg
                        </div>
                    </div>
                    <div style='border-top:1px solid #e9ecef; margin:0.25rem 0 0.5rem 0;'></div>
                    <div>
                        {''.join(rows_html)}
                    </div>
                </div>
                """
                return card_html

            if selected_players:
                # 3 sütunlu satırlar halinde info kartları
                for start in range(0, len(selected_players), 3):
                    row_players = selected_players[start:start+3]
                    cols = st.columns(len(row_players), gap="medium")
                    for cidx, pname in enumerate(row_players):
                        with cols[cidx]:
                            card = build_player_info_card(pname)
                            if card is not None:
                                components.html(card, height=720, scrolling=True)

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
            st.markdown(f"""
                <h2 style='color: #2563eb; margin: 0 0 1rem 0; font-size: 1.8rem; font-weight: 700;'>
                    {category}
                </h2>
            """, unsafe_allow_html=True)
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
                title_font=dict(size=16, color='#000000'),
                legend=dict(font=dict(size=12))
            )
            cat_left_col, cat_right_col = st.columns([2, 1.5], gap="large")
            with cat_left_col:
                st.plotly_chart(fig_cat, use_container_width=True)

            # Kategori için info kartları (oyuncu vs profil ortalaması) sağda
            with cat_right_col:
                st.markdown("<h4 style='margin:0.25rem 0 0.5rem 0;'>Info Cards</h4>", unsafe_allow_html=True)

            def build_category_info_card(player_name_str, metrics_keys, df_scaled_local):
                pr = selected_rows[selected_rows["Player"] == player_name_str]
                if pr.empty:
                    return None
                idx_local = pr.index[0]
                player_scaled_loc = df_scaled_local.loc[idx_local]
                cluster_id_loc = pr.iloc[0].get("Cluster", None)
                try:
                    cluster_int_loc = int(cluster_id_loc) if cluster_id_loc is not None and not pd.isna(cluster_id_loc) else None
                except Exception:
                    cluster_int_loc = None
                if cluster_int_loc is None:
                    cluster_avg_loc = pd.Series([np.nan]*len(metrics_keys), index=[column_info[m] for m in metrics_keys])
                else:
                    # df_scaled_local kolonları zaten çevrilmiş başlıkları (column_info) kullanıyor olabilir; kontrol et
                    if list(df_scaled_local.columns) == [column_info[m] for m in metrics_keys]:
                        cluster_avg_loc = df_scaled_local[df["Cluster"] == cluster_int_loc].mean()
                        player_vals_series = player_scaled_loc
                        metric_labels = list(df_scaled_local.columns)
                    else:
                        cluster_avg_loc = df_scaled_local[df["Cluster"] == cluster_int_loc][metrics_keys].mean()
                        player_vals_series = player_scaled_loc[metrics_keys]
                        metric_labels = [column_info[m] for m in metrics_keys]

                # Archetype avg for current category
                primary_arch_cur = pr.iloc[0].get('Primary_Archetype', None)
                arch_color_rows = get_archetype_color(str(primary_arch_cur)) if primary_arch_cur is not None and not pd.isna(primary_arch_cur) else '#6b7280'
                if primary_arch_cur is None or pd.isna(primary_arch_cur):
                    archetype_avg_loc = pd.Series([np.nan]*len(metric_labels), index=metric_labels)
                else:
                    mask_arch = (df['Primary_Archetype'] == primary_arch_cur)
                    if list(df_scaled_local.columns) == metric_labels:
                        archetype_avg_loc = df_scaled_local[mask_arch].mean()
                    else:
                        archetype_avg_loc = df_scaled_local.loc[mask_arch, metrics_keys].mean()

                # Değerleri 0-100'e çevir
                p_vals = (player_vals_series.values * 100).astype(float)
                a_vals = (cluster_avg_loc.values * 100).astype(float)
                aa_vals = (archetype_avg_loc.values * 100).astype(float)

                # Kart üst bilgileri
                squad_name_loc = pr.iloc[0].get("Squad", "N/A")
                age_val_loc = pr.iloc[0].get("Age", None)
                age_text_loc = "N/A" if age_val_loc is None or pd.isna(age_val_loc) else f"{float(age_val_loc):.0f}"
                primary_arch_loc = pr.iloc[0].get('Primary_Archetype', 'N/A')
                arch_color_loc = get_archetype_color(str(primary_arch_loc))
                profile_name_loc = cluster_profiles.get(cluster_int_loc, {}).get("name", "N/A") if cluster_int_loc is not None else "N/A"
                border_color_loc = get_profile_color(cluster_int_loc) if cluster_int_loc is not None else '#6b7280'

                rows_html_loc = []
                for i, metric_label in enumerate(metric_labels):
                    pv = 0.0 if pd.isna(p_vals[i]) else float(p_vals[i])
                    av = 0.0 if pd.isna(a_vals[i]) else float(a_vals[i])
                    aav = 0.0 if pd.isna(aa_vals[i]) else float(aa_vals[i])
                    row = f"""
                    <div style='margin:0.3rem 0;'>
                        <div style='font-size:0.75rem;color:#6b7280;margin-bottom:0.15rem;'>{metric_label}</div>
                        <div style='display:flex;align-items:center;gap:0.5rem;'>
                            <div style='flex:1;'>
                                <div style='height:8px;background:#e9ecef;border-radius:999px;'>
                                    <div style='height:8px;width:{pv:.0f}%;background:#000000;border-radius:999px;'></div>
                                </div>
                            </div>
                            <div style='width:42px;text-align:right;font-size:0.75rem;color:#000000;font-weight:600;'>{pv:.0f}</div>
                        </div>
                        <div style='display:flex;align-items:center;gap:0.5rem;margin-top:0.15rem;'>
                            <div style='flex:1;'>
                                <div style='height:6px;background:#f1f5f9;border-radius:999px;'>
                                    <div style='height:6px;width:{av:.0f}%;background:{border_color_loc};border-radius:999px;'></div>
                                </div>
                            </div>
                            <div style='width:42px;text-align:right;font-size:0.72rem;color:{border_color_loc};'>{av:.0f}</div>
                        </div>
                        <div style='display:flex;align-items:center;gap:0.5rem;margin-top:0.12rem;'>
                            <div style='flex:1;'>
                                <div style='height:6px;background:#f1f5f9;border-radius:999px;'>
                                    <div style='height:6px;width:{aav:.0f}%;background:{arch_color_rows};border-radius:999px;'></div>
                                </div>
                            </div>
                            <div style='width:42px;text-align:right;font-size:0.72rem;color:{arch_color_rows};'>{aav:.0f}</div>
                        </div>
                    </div>
                    """
                    rows_html_loc.append(row)

                card_html_loc = f"""
                <div class='player-card' style='border: 2px solid {border_color_loc}; border-radius: 10px; padding: 1rem; background: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                    <div style='display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;justify-content:space-between;margin-bottom:0.4rem;'>
                        <div style='display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;'>
                            <h4 style='margin:0;color:#111827;font-size:1.0rem;'>{player_name_str}</h4>
                            <span style='color:{get_team_color(squad_name_loc)};font-size:0.85rem;font-weight:600;'>{squad_name_loc}</span>
                            <span style='color:{border_color_loc};font-size:0.8rem;font-weight:600;'>Profile {'' if cluster_int_loc is None else cluster_int_loc}: {profile_name_loc}</span>
                        </div>
                        <div style='font-size:0.85rem;color:#6b7280;'>
                            Age: <span style='font-weight:700;color:#111827;'>{age_text_loc}</span>
                            <span style='margin:0 0.4rem;'>|</span>
                            <span style='font-weight:700;color:{arch_color_loc};'>{primary_arch_loc}</span>
                        </div>
                    </div>
                    <div style='display:flex;align-items:center;gap:0.75rem;margin:0.25rem 0 0.5rem 0;'>
                        <div style='display:flex;align-items:center;gap:0.35rem;font-size:0.72rem;color:#000000;font-weight:600;'>
                            <span style='display:inline-block;width:10px;height:10px;background:#000000;border-radius:2px;'></span> Player
                        </div>
                        <div style='display:flex;align-items:center;gap:0.35rem;font-size:0.72rem;color:{border_color_loc};'>
                            <span style='display:inline-block;width:10px;height:10px;background:{border_color_loc};border-radius:2px;'></span> Profile Avg
                        </div>
                        <div style='display:flex;align-items:center;gap:0.35rem;font-size:0.72rem;color:{arch_color_rows};'>
                            <span style='display:inline-block;width:10px;height:10px;background:{arch_color_rows};border-radius:2px;'></span> Arc. Avg
                        </div>
                    </div>
                    <div style='border-top:1px solid #e9ecef; margin:0.25rem 0 0.5rem 0;'></div>
                    <div>
                        {''.join(rows_html_loc)}
                    </div>
                </div>
                """
                return card_html_loc

            if selected_players and cat_metrics_available:
                for start_idx in range(0, len(selected_players), 3):
                    row_players_loc = selected_players[start_idx:start_idx+3]
                    cols_loc = cat_right_col.columns(len(row_players_loc), gap="medium")
                    for cc, pname_loc in enumerate(row_players_loc):
                        with cols_loc[cc]:
                            card_loc = build_category_info_card(pname_loc, cat_metrics_available, df_cat_scaled)
                            if card_loc is not None:
                                components.html(card_loc, height=640, scrolling=True)

            

        # ---------------------------
        # Archetype Score Distribution (Before Similar Players)
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.2rem 0;'>
                <h2 style='font-size: 1.6rem; font-weight: 700; color: #2563eb; margin: 0;'>
                    Archetype Distribution Chart
                </h2>
                <p style='color:#6b7280; margin:0.25rem 0 0 0; font-size:0.9rem;'>
                    A comparative view of the selected players' scores in the 7 archetypes. The primary archetype bar is highlighted with a star and a bold border.
                </p>
            </div>
        """, unsafe_allow_html=True)

        archetypes_full = ['Anchor','DLP','BallWinner','BoxToBox','APM','Mezzala','ShadowStriker']
        arch_to_col = {a: f"{a}_Score" for a in archetypes_full}

        if selected_players:
            # Radar ile aynı oyuncu renk paleti
            try:
                player_color_map_rose = {name: player_colors[i % len(player_colors)] for i, name in enumerate(selected_players)}
            except Exception:
                _fallback_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']
                player_color_map_rose = {name: _fallback_colors[i % len(_fallback_colors)] for i, name in enumerate(selected_players)}
            fig_arch = go.Figure()
            for idx_p, player_name in enumerate(selected_players):
                prow = selected_rows[selected_rows["Player"] == player_name]
                if prow.empty:
                    continue
                prow = prow.iloc[0]
                # Y ekseni değerleri
                y_vals = []
                for a in archetypes_full:
                    coln = arch_to_col[a]
                    y_vals.append(float(prow.get(coln, np.nan)))
                # Renkler arketip rengi
                colors = [get_archetype_color(a) for a in archetypes_full]
                # Primary vurgusu: kalın kenarlık ve yıldız texti
                primary_arch = str(prow.get('Primary_Archetype', ''))
                marker_line_width = [2 if a == primary_arch else 0 for a in archetypes_full]
                marker_line_color = ["#111827" if a == primary_arch else "rgba(0,0,0,0)" for a in archetypes_full]
                # Oyuncu ismi (sadece ilk isim)
                full_name = str(prow.get('Player', ''))
                first_name = full_name.split(' ')[0] if full_name else ''
                text_labels = [f"{first_name}★" if a == primary_arch else first_name for a in archetypes_full]

                fig_arch.add_trace(go.Bar(
                    name=player_name,
                    x=archetypes_full,
                    y=y_vals,
                    marker=dict(color=colors, line=dict(width=marker_line_width, color=marker_line_color)),
                    text=text_labels,
                    textposition='outside',
                    cliponaxis=False
                ))

            fig_arch.update_layout(
                barmode='group',
                template='plotly_dark',
                yaxis=dict(title='Score (0-100)', rangemode='tozero'),
                xaxis=dict(title='Archetype'),
                legend=dict(font=dict(size=12)),
                showlegend=False
            )
            st.plotly_chart(fig_arch, use_container_width=True)

        # ---------------------------
        # Interactive Scatter Plot
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.2rem 0;'>
                <h2 style='font-size: 1.6rem; font-weight: 700; color: #2563eb; margin: 0;'>
                    Interactive Player Comparison
                </h2>
                <p style='color:#6b7280; margin:0.25rem 0 0 0; font-size:0.9rem;'>
                    Comparative analysis of selected players with other players. Choose your desired metrics on X and Y axes.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Metrik seçimi için dropdown'lar
        available_metrics = {
            'pass_PrgP': 'Progressive Passes',
            'poss_PrgC': 'Progressive Carries', 
            'std_xAG': 'Expected Assists (xAG)',
            'std_xG': 'Expected Goals (xG)',
            'def_Tkl': 'Tackles',
            'def_Int': 'Interceptions',
            'pass_KP': 'Key Passes',
            'shoot_Sh': 'Total Shots',
            'misc_Recov': 'Ball Recoveries',
            'pass_1/3': 'Passes into Final Third',
            'passt_Sw': 'Switches',
            'pass_Cmp%': 'Pass Completion %',
            'def_Tkl+Int': 'Defensive Actions',
            'gca_TO': 'Successful Dribbles leading to Goal Chance',
        }

        col_x, col_y = st.columns(2, gap="medium")
        with col_x:
            x_metric = st.selectbox(
                "X Axis Metric",
                options=list(available_metrics.keys()),
                format_func=lambda x: available_metrics[x],
                index=0,
                help="Select metric for X axis"
            )
        with col_y:
            y_metric = st.selectbox(
                "Y Axis Metric", 
                options=list(available_metrics.keys()),
                format_func=lambda x: available_metrics[x],
                index=2,
                help="Select metric for Y axis"
            )

        if selected_players and x_metric in df.columns and y_metric in df.columns:
            # Seçilen oyuncular ve diğer oyuncular
            selected_df = df[df['Player'].isin(selected_players)].copy()
            other_df = df[~df['Player'].isin(selected_players)].copy()
            
            # Scatter plot oluştur
            fig_scatter = go.Figure()
            
            # Diğer oyuncular (arka plan)
            if not other_df.empty:
                fig_scatter.add_trace(go.Scatter(
                    x=other_df[x_metric],
                    y=other_df[y_metric],
                    mode='markers',
                    name='Other Players',
                    marker=dict(
                        color='lightgray',
                        size=8,
                        opacity=0.6,
                        line=dict(width=1, color='white')
                    ),
                    text=other_df['Player'],
                    hovertemplate='<b>%{text}</b><br>' +
                                 f'{available_metrics[x_metric]}: %{{x:.2f}}<br>' +
                                 f'{available_metrics[y_metric]}: %{{y:.2f}}<br>' +
                                 '<extra></extra>'
                ))
            
            # Seçilen oyuncular (vurgulanmış) - Jitter ile üst üste gelme sorunu çözümü
            import random
            random.seed(42)  # Tutarlı jitter için
            # Renk eşlemesi: üstteki radar grafiklerde kullanılan palete uyumlu
            try:
                player_color_map = {name: player_colors[i % len(player_colors)] for i, name in enumerate(selected_players)}
            except Exception:
                # Fallback paleti
                _fallback_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']
                player_color_map = {name: _fallback_colors[i % len(_fallback_colors)] for i, name in enumerate(selected_players)}
            
            # Aynı pozisyondaki oyuncuları grupla
            position_groups = {}
            for player_name in selected_players:
                player_data = selected_df[selected_df['Player'] == player_name]
                if not player_data.empty:
                    player_row = player_data.iloc[0]
                    x_val = player_row[x_metric]
                    y_val = player_row[y_metric]
                    pos_key = f"{x_val:.3f}_{y_val:.3f}"
                    
                    if pos_key not in position_groups:
                        position_groups[pos_key] = []
                    position_groups[pos_key].append((player_name, player_row))
            
            # Her pozisyon grubu için jitter uygula
            for pos_key, players_at_pos in position_groups.items():
                base_x, base_y = pos_key.split('_')
                base_x, base_y = float(base_x), float(base_y)
                
                # Jitter miktarı (metrik değerlerine göre ayarlanmış)
                x_range = other_df[x_metric].max() - other_df[x_metric].min() if not other_df.empty else 1
                y_range = other_df[y_metric].max() - other_df[y_metric].min() if not other_df.empty else 1
                jitter_x = x_range * 0.02  # %2 jitter
                jitter_y = y_range * 0.02
                
                for i, (player_name, player_row) in enumerate(players_at_pos):
                    # Jitter hesapla (dairesel dağılım)
                    if len(players_at_pos) > 1:
                        angle = (2 * np.pi * i) / len(players_at_pos)
                        jitter_offset_x = jitter_x * np.cos(angle)
                        jitter_offset_y = jitter_y * np.sin(angle)
                    else:
                        jitter_offset_x = jitter_offset_y = 0
                    
                    # Oyuncu rengi: radar paleti ile aynı sırada
                    player_color = player_color_map.get(player_name, '#636EFA')
                    
                    # Hover metni (çoklu oyuncu uyarısı)
                    if len(players_at_pos) > 1:
                        hover_text = f"<b>{player_name}</b><br>⚠️ Multiple players at this position<br>" + \
                                   f'{available_metrics[x_metric]}: {base_x:.2f}<br>' + \
                                   f'{available_metrics[y_metric]}: {base_y:.2f}<br>'
                    else:
                        hover_text = f"<b>{player_name}</b><br>" + \
                                   f'{available_metrics[x_metric]}: {base_x:.2f}<br>' + \
                                   f'{available_metrics[y_metric]}: {base_y:.2f}<br>'
                    
                    fig_scatter.add_trace(go.Scatter(
                        x=[base_x + jitter_offset_x],
                        y=[base_y + jitter_offset_y],
                        mode='markers',
                        name=player_name,
                        marker=dict(
                            color=player_color,
                            size=20,  # Boyut artırıldı
                            symbol='star',
                            line=dict(width=3, color='white')
                        ),
                        text=[player_name],
                        hovertemplate=hover_text + '<extra></extra>'
                    ))
            
            # Grafik düzenleme
            fig_scatter.update_layout(
                title=f"Player Comparison: {available_metrics[y_metric]} vs {available_metrics[x_metric]}",
                xaxis_title=available_metrics[x_metric],
                yaxis_title=available_metrics[y_metric],
                template='plotly_dark',
                height=500,
                hovermode='closest',
                legend=dict(font=dict(size=12))
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)

        # ---------------------------
        # Defansif Aktivite Haritası
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.5rem 0;'>
                <h2 style='font-size: 2rem; font-weight: 800; color: #2563eb;'>
                    Defensive Activity Map
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Defansif aktivite haritası oluşturma
        
        # Haritaları 2'şer yan yana göster
        if len(selected_players) > 0:
            # İki sütunlu layout
            cols = st.columns(2)
            
            for i, player_name in enumerate(selected_players):
                col_index = i % 2
                with cols[col_index]:
                    player_row = selected_rows[selected_rows["Player"] == player_name]
                    if not player_row.empty:
                        st.markdown(f"""
                            <h3 style='color: #000000; margin: 0 0 0.5rem 0; font-size: 1.2rem; font-weight: 600;'>
                                {player_name}
                            </h3>
                        """, unsafe_allow_html=True)
                        
                        # Defansif aktivite verilerini al
                        def_def = player_row['def_Def 3rd'].iloc[0]
                        def_mid = player_row['def_Mid 3rd'].iloc[0]
                        def_att = player_row['def_Att 3rd'].iloc[0]
                        
                        # Bölgeleri ve değerlerini sözlük olarak sakla
                        defensive_actions = {
                            'DEF': def_def,
                            'MID': def_mid,
                            'ATT': def_att
                        }
                        
                        # Değerlere göre büyükten küçüğe sırala
                        sorted_actions = dict(sorted(defensive_actions.items(), key=lambda x: x[1], reverse=True))
                        
                        # Renkleri tanımla
                        colors = ['green', 'yellow', 'red']
                        color_map = {}
                        
                        # Sıralanmış bölgelere renkleri ata
                        for j, (region, value) in enumerate(sorted_actions.items()):
                            color_map[region] = colors[j]
                        
                        # Matplotlib figürü oluştur - kompakt ve 2'şer yan yana
                        plt.style.use('default')
                        fig, ax = plt.subplots(figsize=(6, 4))
                        fig.patch.set_facecolor('#ffffff')
                        ax.set_facecolor('#ffffff')
                        
                        # Futbol sahası arka planını yükle
                        try:
                            pitch_img = Image.open('pitch.png')
                            # Görseli 1/4 oranında küçült ve ortala
                            ax.imshow(pitch_img, extent=[25, 75, 25, 75], aspect='auto')
                        except FileNotFoundError:
                            # Eğer pitch.png bulunamazsa, basit bir saha çiz
                            ax.set_xlim(0, 100)
                            ax.set_ylim(0, 100)
                            ax.add_patch(patches.Rectangle((0, 0), 100, 100, linewidth=2, edgecolor='white', facecolor='green', alpha=0.3))
                            # Saha çizgileri
                            ax.plot([0, 100], [50, 50], 'w-', linewidth=2)
                            ax.plot([16.5, 16.5], [21, 79], 'w-', linewidth=2)
                            ax.plot([83.5, 83.5], [21, 79], 'w-', linewidth=2)
                            ax.plot([0, 0], [0, 100], 'w-', linewidth=2)
                            ax.plot([100, 100], [0, 100], 'w-', linewidth=2)
                        
                        # Bölgeleri çiz (pitch 25-75 aralığında olduğu için koordinatları ayarla)
                        regions = {
                            'DEF': (25, 25, 16.67, 50),      # Sol üçte birlik
                            'MID': (41.67, 25, 16.67, 50),   # Orta üçte birlik  
                            'ATT': (58.33, 25, 16.67, 50)    # Sağ üçte birlik
                        }
                        
                        for region, (x, y, width, height) in regions.items():
                            color = color_map[region]
                            value = defensive_actions[region]
                            
                            # Yarı saydam dikdörtgen ekle
                            rect = patches.Rectangle((x, y), width, height, 
                                                   facecolor=color, alpha=0.6, 
                                                   edgecolor='black', linewidth=2)
                            ax.add_patch(rect)
                            
                            # Bölge adı ve değeri ekle - Streamlit tema uyumlu
                            center_x = x + width/2
                            center_y = y + height/2
                            ax.text(center_x, center_y + 6, region, 
                                   fontsize=11, fontweight='600', ha='center', va='center',
                                   color='#1f2937', fontfamily='DejaVu Sans',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor='#ffffff', alpha=0.95, 
                                            edgecolor='#e5e7eb', linewidth=1))
                            ax.text(center_x, center_y - 6, f'{int(value)}', 
                                   fontsize=9, fontweight='700', ha='center', va='center',
                                   color='#6b7280', fontfamily='DejaVu Sans',
                                   bbox=dict(boxstyle="round,pad=0.2", facecolor='#f9fafb', alpha=1.0, 
                                            edgecolor='#d1d5db', linewidth=0.5))
                        
                        # Grafiği temizle
                        ax.set_xlim(0, 100)
                        ax.set_ylim(0, 100)
                        ax.axis('off')
                        
                        # Başlık ekle - tema uyumlu
                        fig.suptitle(f'{player_name} - Defensive Activity Distribution', 
                                   fontsize=12, fontweight='700', y=0.80, 
                                   fontfamily='DejaVu Sans', color='#2563eb')
                        
                        # Renk açıklaması ekle - açıklayıcı
                        legend_text = ""
                        for k, (region, color) in enumerate(color_map.items()):
                            if k > 0:
                                legend_text += " | "
                            legend_text += f"{region} Zone ({defensive_actions[region]} actions)"
                        
                        ax.text(50, 12, legend_text, fontsize=8, va='center', ha='center',
                               fontfamily='DejaVu Sans', fontweight='500', color='#374151',
                               bbox=dict(boxstyle="round,pad=0.3", facecolor='#ffffff', 
                                        alpha=0.95, edgecolor='#e5e7eb', linewidth=1))
                        
                        # Boşlukları optimize et - kompakt
                        plt.subplots_adjust(top=0.90, bottom=0.20, left=0.05, right=0.95)
                        st.pyplot(fig, use_container_width=True)
                        plt.close()
        
        # ---------------------------
        # Pas Gülü Grafiği (Rose Chart)
        # ---------------------------
        st.markdown(
            """
            <div style='margin: 3rem 0 1.2rem 0;'>
                <h2 style='font-size: 1.6rem; font-weight: 700; color: #2563eb; margin: 0;'>
                    Passing Rose Chart
                </h2>
                <p style='color:#6b7280; margin:0.25rem 0 0 0; font-size:0.9rem;'>
                    Four tactical passing categories (0–100) for the selected players.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if selected_players:
            def hex_to_rgba(hex_color, alpha=0.25):
                h = str(hex_color).lstrip('#')
                if len(h) != 6:
                    return f'rgba(37, 99, 235, {alpha})'
                r = int(h[0:2], 16)
                g = int(h[2:4], 16)
                b = int(h[4:6], 16)
                return f'rgba({r}, {g}, {b}, {alpha})'

            def safe_val(v):
                try:
                    f = float(v)
                    return 0.0 if pd.isna(f) else f
                except Exception:
                    return 0.0

            def safe_mean(values):
                nums = []
                for v in values:
                    try:
                        f = float(v)
                        if not pd.isna(f):
                            nums.append(f)
                    except Exception:
                        continue
                return float(np.mean(nums)) if len(nums) > 0 else 0.0

            for start_idx in range(0, len(selected_players), 2):
                row_players = selected_players[start_idx:start_idx + 2]
                cols = st.columns(len(row_players))
                for ci, pname in enumerate(row_players):
                    with cols[ci]:
                        pr = selected_rows[selected_rows["Player"] == pname]
                        if pr.empty:
                            continue
                        prow = pr.iloc[0]

                        puan_guvenli = safe_val(prow.get('pass_Cmp%', np.nan))
                        puan_oyunkurma = safe_mean([prow.get('pass_PrgP', np.nan), prow.get('pass_1/3', np.nan)])
                        puan_yaraticilik = safe_mean([prow.get('pass_KP', np.nan), prow.get('std_xAG', np.nan)])
                        puan_vizyon = safe_val(prow.get('passt_Sw', np.nan))

                        kategoriler = ['Safe Passing', 'Build-up', 'Creativity', 'Vision']
                        puanlar = [puan_guvenli, puan_oyunkurma, puan_yaraticilik, puan_vizyon]

                        r_vals = puanlar + [puanlar[0]]
                        theta_vals = kategoriler + [kategoriler[0]]

                        cluster_id = prow.get('Cluster', None)
                        try:
                            cluster_int = int(cluster_id) if cluster_id is not None and not pd.isna(cluster_id) else None
                        except Exception:
                            cluster_int = None
                        # Oyuncu rengi: Standard Stats radar paletiyle aynı
                        base_color = player_color_map_rose.get(pname, '#636EFA')

                        # Rose chart (Barpolar) - eşit açılı, petal görünümü
                        angles = list(np.linspace(0, 360, len(kategoriler), endpoint=False))
                        widths = [88] * len(kategoriler)

                        fig_rose = go.Figure()
                        fig_rose.add_trace(
                            go.Barpolar(
                                r=puanlar,
                                theta=angles,
                                width=widths,
                                marker=dict(
                                    color=[hex_to_rgba(base_color, 0.35)] * len(kategoriler),
                                    line=dict(color=base_color, width=0),
                                ),
                                name=pname,
                                hovertemplate=
                                    '<b>' + pname + '</b><br>' +
                                    '%{customdata[0]}: %{r:.1f}<extra></extra>',
                                customdata=[[k] for k in kategoriler],
                                opacity=0.95,
                            )
                        )
                        # Kategori ayırıcı çizgiler (merkezden dışa 4 çizgi)
                        for sep_angle in angles:
                            fig_rose.add_trace(
                                go.Scatterpolar(
                                    r=[0, 100],
                                    theta=[sep_angle + 45, sep_angle + 45],
                                    mode='lines',
                                    line=dict(color='rgba(209,213,219,0.9)', width=1),  # açık gri
                                    hoverinfo='skip',
                                    showlegend=False,
                                )
                            )
                        # Bar değer etiketleri (dışarıda metin olarak)
                        label_r = [min(100, float(v) + 6.0) for v in puanlar]
                        fig_rose.add_trace(
                            go.Scatterpolar(
                                r=label_r,
                                theta=angles,
                                mode='text',
                                text=[f"{float(v):.0f}" for v in puanlar],
                                textfont=dict(color='#ffffff', size=12),
                                hoverinfo='skip',
                                showlegend=False,
                            )
                        )
                        fig_rose.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 100],
                                    showticklabels=False,
                                    ticks='',
                                    showline=False,
                                    gridcolor='rgba(0,0,0,0)',
                                    gridwidth=0
                                ),
                                angularaxis=dict(
                                    direction='clockwise',
                                    rotation=90,
                                    tickmode='array',
                                    tickvals=angles,
                                    ticktext=kategoriler,
                                    ticks='',
                                    showline=False,
                                    gridcolor='rgba(0,0,0,0)',
                                    tickfont=dict(size=14, color='#000000', family='Inter, DejaVu Sans')
                                ),
                                bargap=0.02,
                            ),
                            showlegend=False,
                            title=f"{pname}: Passing Rose Chart",
                            template='plotly_dark',
                            height=420,
                            margin=dict(t=60, b=20, l=20, r=20),
                        )
                        st.plotly_chart(fig_rose, use_container_width=True)

        # ---------------------------
        # Reward & Security Gauges (Gauge)
        # ---------------------------
        st.markdown(
            """
            <div style='margin: 2.5rem 0 1.0rem 0;'>
                <h2 style='font-size: 1.6rem; font-weight: 700; color: #2563eb; margin: 0;'>
                    Reward & Security Gauges
                </h2>
                <p style='color:#6b7280; margin:0.25rem 0 0 0; font-size:0.9rem;'>
                    Reward shows how much the player drives and creates danger in possession. Security shows how safely the player keeps the ball with minimal turnovers.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if selected_players:
            def _safe_float(v):
                try:
                    f = float(v)
                    return 0.0 if pd.isna(f) else f
                except Exception:
                    return 0.0

            for pname in selected_players:
                prow_all = selected_rows[selected_rows["Player"] == pname]
                if prow_all.empty:
                    continue
                prow = prow_all.iloc[0]

                # Reward: pass_KP, pass_PPA, poss_PrgC, gca_TO (0-100 ortalama)
                reward_metrics = [
                    _safe_float(prow.get('pass_KP', 0)),
                    _safe_float(prow.get('pass_PPA', 0)),
                    _safe_float(prow.get('poss_PrgC', 0)),
                    _safe_float(prow.get('gca_TO', 0)),
                ]
                reward_score = int(round(float(np.mean(reward_metrics)) if len(reward_metrics) > 0 else 0.0))

                # Security: poss_Dis, poss_Mis (ters 0-100; yüksek = daha güvenli)
                security_raw = [
                    _safe_float(prow.get('poss_Dis', 0)),
                    _safe_float(prow.get('poss_Mis', 0)),
                ]
                security_inverted = [max(0.0, min(100.0, 100.0 - v)) for v in security_raw]
                security_score = int(round(float(np.mean(security_inverted)) if len(security_inverted) > 0 else 0.0))

                # Renk adımları
                steps_cfg = [
                    {'range': [0, 40], 'color': '#ef4444'},      # red
                    {'range': [40, 70], 'color': '#f59e0b'},     # yellow
                    {'range': [70, 100], 'color': '#10b981'},    # green
                ]

                # Reward Gauge
                reward_fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=reward_score,
                    title={'text': "Reward Profile", 'font': {'size': 16}},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': '#000000'},
                        'steps': steps_cfg,
                        'threshold': {'line': {'color': '#000000', 'width': 6}, 'thickness': 0.9, 'value': reward_score},
                    },
                    number={'suffix': '', 'font': {'size': 22}},
                ))
                reward_fig.update_layout(height=280, margin=dict(t=40, b=10, l=10, r=10), template='plotly_dark')

                # Security Gauge
                security_fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=security_score,
                    title={'text': "Security Profile", 'font': {'size': 16}},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': '#000000'},
                        'steps': steps_cfg,
                        'threshold': {'line': {'color': '#000000', 'width': 6}, 'thickness': 0.9, 'value': security_score},
                    },
                    number={'suffix': '', 'font': {'size': 22}},
                ))
                security_fig.update_layout(height=280, margin=dict(t=40, b=10, l=10, r=10), template='plotly_dark')

                st.markdown(f"**{pname}**", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(reward_fig, use_container_width=True)
                with c2:
                    st.plotly_chart(security_fig, use_container_width=True)

        # ---------------------------
        # Goal Contribution DNA (Donut)
        # ---------------------------
        st.markdown(
            """
            <div style='margin: 3rem 0 1.2rem 0;'>
                <h2 style='font-size: 1.6rem; font-weight: 700; color: #2563eb; margin: 0;'>
                    Goal Contribution DNA
                </h2>
                <p style='color:#6b7280; margin:0.25rem 0 0 0; font-size:0.9rem;'>
                    Percentage split of Goal Creating Actions (GCA) by action type.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if selected_players:
            labels_gca = [
                "Live Pass",
                "Dead Ball",
                "Take-on / Dribble",
                "Shot Rebound",
                "Fouled / Won Foul",
            ]
            color_gca = [
                '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'
            ]

            for start_idx in range(0, len(selected_players), 2):
                row_players = selected_players[start_idx:start_idx + 2]
                cols = st.columns(len(row_players))
                for ci, pname in enumerate(row_players):
                    with cols[ci]:
                        pr = selected_rows[selected_rows["Player"] == pname]
                        if pr.empty:
                            continue
                        prow = pr.iloc[0]

                        def _safe(v):
                            try:
                                f = float(v)
                                return 0.0 if pd.isna(f) else f
                            except Exception:
                                return 0.0

                        vals = [
                            _safe(prow.get('gca_PassLive', 0)),
                            _safe(prow.get('gca_PassDead', 0)),
                            _safe(prow.get('gca_TO', 0)),
                            _safe(prow.get('gca_Sh', 0)),
                            _safe(prow.get('gca_Fld', 0)),
                        ]
                        total_gca = float(np.sum(vals))
                        if total_gca <= 0:
                            st.info("Bu oyuncunun sezon boyunca kayıtlı bir gol pozisyonu yaratma aksiyonu bulunmamaktadır.")
                            continue

                        max_idx = int(np.argmax(vals)) if any(v > 0 for v in vals) else 0
                        pull_arr = [0.0] * len(vals)
                        pull_arr[max_idx] = 0.10

                        fig_donut = go.Figure([
                            go.Pie(
                                labels=labels_gca,
                                values=vals,
                                hole=0.5,
                                marker=dict(colors=color_gca, line=dict(color='white', width=1)),
                                sort=False,
                                direction='clockwise',
                                textinfo='percent',
                                textposition='inside',
                                insidetextorientation='radial',
                                pull=pull_arr,
                                hovertemplate='%{label}<br>%{value} Actions (%{percent})<extra></extra>',
                                name=pname,
                            )
                        ])

                        fig_donut.add_annotation(
                            text=f"Total GCA\n{int(total_gca)}",
                            x=0.5, y=0.5, showarrow=False,
                            font=dict(size=18, color='#ffffff')
                        )
                        fig_donut.update_traces(textfont=dict(color='#ffffff', size=12))
                        fig_donut.update_layout(
                            title=f"{pname}: Goal Contribution DNA",
                            template='plotly_dark',
                            showlegend=True,
                            height=420,
                            margin=dict(t=60, b=20, l=20, r=20),
                            legend=dict(font=dict(size=12))
                        )
                        st.plotly_chart(fig_donut, use_container_width=True)

        

        # ---------------------------
        # Similar Players
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.2rem 0;'>
                <h2 style='font-size: 1.6rem; font-weight: 700; color: #2563eb; margin: 0;'>
                    Similar Players
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Yeni yöntem: küme içi, 0-100 metrikler ile Öklidyen mesafe -> 0-100 benzerlik (Kart görünümü)
        for player_name in selected_players:
            top_sim = find_similar_players(df, player_name, top_k=3)
            if top_sim is None or top_sim.empty:
                st.info(f"No similar players found for {player_name}.")
                continue
            st.markdown(f"**Statistically Similar Profiles – {player_name}**")
            st.markdown("<br>", unsafe_allow_html=True)
            # 3 kartlık satır
            cols_cards = st.columns(min(3, len(top_sim)), gap="medium")
            for i in range(len(top_sim)):
                row = top_sim.iloc[i]
                pname = str(row.get('Player','N/A'))
                squad = str(row.get('Squad','N/A'))
                age_val = row.get('Age', np.nan)
                arch = str(row.get('Primary_Archetype','N/A'))
                sim = float(row.get('Similarity_Score', 0.0))
                arch_color = get_archetype_color(arch)
                team_color = get_team_color(squad)
                # Profile color (from Cluster of this player)
                try:
                    cluster_id_sim = df.loc[df['Player'] == pname, 'Cluster'].iloc[0]
                except Exception:
                    cluster_id_sim = None
                prof_color = get_profile_color(int(cluster_id_sim)) if cluster_id_sim is not None and not pd.isna(cluster_id_sim) else '#6b7280'
                age_display = 'N/A' if pd.isna(age_val) else f"{float(age_val):.0f}"
                with cols_cards[i % len(cols_cards)]:
                    st.markdown(f"""
                        <div class='player-card' style='border: 2px solid {prof_color};
                                    border-radius: 10px; padding: 1rem; 
                                    background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <div style='text-align: center;'>
                                <div style='color: {prof_color}; font-size: 0.8rem; font-weight: 700;'>#{i+1} MOST SIMILAR</div>
                                <h4 style='margin: 0.3rem 0; color: #111827; font-size: 1.05rem; background: linear-gradient(135deg, {prof_color}15, {prof_color}08); padding: 0.3rem 0.5rem; border-radius: 4px;'>
                                    {pname}
                                </h4>
                                <p style='margin: 0; color: {team_color}; font-size: 0.9rem; background: linear-gradient(135deg, {prof_color}12, {prof_color}05); padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600;'>
                                    {squad}
                                </p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; 
                                    margin-top: 0.8rem; font-size: 0.85rem;'>
                            <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                <div style='color: #888; font-size: 0.7rem;'>Age</div>
                                <div style='font-weight: 600; color: #111827;'>{age_display}</div>
                            </div>
                            <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                <div style='color: #888; font-size: 0.7rem;'>Archetype</div>
                                <div style='font-weight: 700; color: {arch_color};'>{arch}</div>
                            </div>
                            <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px; grid-column: span 2;'>
                                <div style='color: #888; font-size: 0.7rem;'>Similarity Score</div>
                                <div style='font-weight: 800; color: {get_rating_color(sim)};'>{sim:.1f}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

        # ---------------------------
        # Compare All Player Profiles
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.2rem 0;'>
                <h2 style='font-size: 1.6rem; font-weight: 700; color: #2563eb; margin: 0;'>
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
        # / Excel Report
        # ---------------------------
        st.markdown("""
            <div style='margin: 3rem 0 1.2rem 0;'>
                <h2 style='font-size: 1.6rem; font-weight: 700; color: #2563eb; margin: 0;'>
                    Download Report
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        if len(selected_players) == 1:
            # PDF Print özelliği
            player_name = selected_players[0]
            
            # Print CSS ve JavaScript ekle
            st.markdown("""
            <style>
            @media print {
                body * {
                    visibility: hidden;
                }
                .print-area, .print-area * {
                    visibility: visible;
                }
                .print-area {
                    position: absolute;
                    left: 0;
                    top: 0;
                    width: 100%;
                }
                .no-print {
                    display: none !important;
                }
                .page-break {
                    page-break-before: always;
                }
            }
            .print-btn {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            .print-btn:hover {
                background-color: #c82333;
            }
            </style>
            
            <script>
            function printPage() {
                // Print dialog'u aç
                window.print();
            }
            
            // Sayfa yüklendiğinde print fonksiyonunu hazırla
            document.addEventListener('DOMContentLoaded', function() {
                console.log('Print function ready');
            });
            </script>
            """, unsafe_allow_html=True)
            
            # Print butonu - Streamlit components ile
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"📄 {player_name} - PDF Print", 
                           type="primary", 
                           use_container_width=True,
                           help="Sayfayı PDF olarak yazdırmak için tıklayın"):
                    st.markdown("""
                    <script>
                    setTimeout(function() {
                        window.print();
                    }, 100);
                    </script>
                    """, unsafe_allow_html=True)
            
            # Print alanını işaretle
            st.markdown('<div class="print-area">', unsafe_allow_html=True)

            
        
        elif len(selected_players) > 1:
            # PDF Print özelliği - Çoklu oyuncu karşılaştırması
            players_list = ", ".join(selected_players)
            
            # Print butonu - Streamlit components ile
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"📄 {len(selected_players)} Oyuncu Karşılaştırması - PDF Print", 
                           type="primary", 
                           use_container_width=True,
                           help="Sayfayı PDF olarak yazdırmak için tıklayın"):
                    st.markdown("""
                    <script>
                    setTimeout(function() {
                        window.print();
                    }, 100);
                    </script>
                    """, unsafe_allow_html=True)
            
            # Print alanını işaretle
            st.markdown('<div class="print-area">', unsafe_allow_html=True)

            

    # Call the analysis function
    update_player_view(player_select)
    
    # Print alanını kapat
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0 1.5rem 0;'>
        <h1 style='font-size: 1.8rem; font-weight: 600; margin: 0; color: #2563eb;'>
            League Leaders Statistics
        </h1>
        <p style='color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
            Comprehensive leaderboards showing the top performers in different key metrics
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Instructions box
    with st.expander("About This Section (Click to expand)", expanded=False):
        st.markdown("""
        **League Leaders Statistics**
        - Comprehensive leaderboards across multiple performance categories
        - Creative & Passing, Defensive, Attacking, and Dribble specialists
        - Advanced metrics combining multiple statistics for deeper insights
        
        **How to Interpret:**
        - Each table shows top 5 performers in specific categories
        - Metrics are calculated using sophisticated formulas
        - Filters ensure meaningful comparisons (minimum thresholds)
        - Higher scores indicate better performance in that specific area
        """)
    
    st.markdown("---")
    
    # Create sub-tabs for League Leaders
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        " Creative & Passing Leaders",
        " Defensive Leaders", 
        " Attacking Leaders"
    ])
    
    with sub_tab1:
        # Creative & Passing Leaders content
        st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; text-align: center; color: #2563eb;'>
                 Creative & Passing Leaders
            </h2>
            <p style='text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;'>
                Advanced passing metrics and creative playmaking analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #2563eb;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #2563eb; font-size: 1rem;'>Key Pass Efficiency</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Per 90 minutes</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'pass_KP' in df.columns and 'std_Min' in df.columns:
                df['key_pass_efficiency'] = (df['pass_KP'] / (df['std_Min'] / 90)).fillna(0)
                creative_leaders = df.nlargest(5, 'key_pass_efficiency')[['Player', 'Squad', 'key_pass_efficiency']].copy()
                creative_leaders.columns = ['Player', 'Team', 'Key Passes per 90']
                creative_leaders['Key Passes per 90'] = creative_leaders['Key Passes per 90'].round(2)
                st.dataframe(creative_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Key passes or minutes data not found")
        
        with col2:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #28a745;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #28a745; font-size: 1rem;'>Key Pass Efficiency</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Progressive to key pass conversion</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'pass_KP' in df.columns and 'pass_PrgP' in df.columns:
                # Calculate key pass efficiency: KP / PrgP * 100
                df['key_pass_efficiency'] = (df['pass_KP'] / df['pass_PrgP'] * 100).fillna(0)
                # Filter out players with very low progressive passes to avoid misleading ratios
                qualified_players = df[df['pass_PrgP'] >= 10]  # Minimum 10 progressive passes
                if not qualified_players.empty:
                    efficiency_leaders = qualified_players.nlargest(5, 'key_pass_efficiency')[['Player', 'Squad', 'key_pass_efficiency', 'pass_KP', 'pass_PrgP']].copy()
                    efficiency_leaders.columns = ['Player', 'Team', 'Efficiency %', 'Key Passes', 'Progressive Passes']
                    efficiency_leaders['Efficiency %'] = efficiency_leaders['Efficiency %'].round(1)
                    efficiency_leaders['Key Passes'] = efficiency_leaders['Key Passes'].round(1)
                    efficiency_leaders['Progressive Passes'] = efficiency_leaders['Progressive Passes'].round(1)
                    st.dataframe(efficiency_leaders, use_container_width=True, hide_index=True)
                else:
                    st.info("No players with 10+ progressive passes found")
            else:
                st.info("Key passes or progressive passes data not found")
        
        with col3:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #ffc107;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #ffc107; font-size: 1rem;'>Maestro</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Risk & creativity balance</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'pass_KP' in df.columns and 'pass_PPA' in df.columns and 'std_xAG' in df.columns and 'pass_Cmp%' in df.columns:
                # Calculate maestro: (KP * 2) + PPA + (xAG * 3) - ((100 - Cmp%) / 10)
                df['maestro_score'] = ((df['pass_KP'] * 2) + df['pass_PPA'] + (df['std_xAG'] * 3) - ((100 - df['pass_Cmp%']) / 10)).fillna(0)
                maestro_leaders = df.nlargest(5, 'maestro_score')[['Player', 'Squad', 'maestro_score', 'pass_KP', 'pass_PPA', 'std_xAG', 'pass_Cmp%']].copy()
                maestro_leaders.columns = ['Player', 'Team', 'Maestro Score', 'Key Passes', 'Penalty Passes', 'xAG', 'Pass %']
                maestro_leaders['Maestro Score'] = maestro_leaders['Maestro Score'].round(1)
                maestro_leaders['Key Passes'] = maestro_leaders['Key Passes'].round(1)
                maestro_leaders['Penalty Passes'] = maestro_leaders['Penalty Passes'].round(1)
                maestro_leaders['xAG'] = maestro_leaders['xAG'].round(1)
                maestro_leaders['Pass %'] = (maestro_leaders['Pass %'] * 100).round(1)
                st.dataframe(maestro_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Maestro calculation data not found")
        
        # Second row of Creative & Passing Leaders
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #6f42c1;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #6f42c1; font-size: 1rem;'>Vertical Playmaker</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Progressive passing threat</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'pass_PrgP' in df.columns and 'pass_1/3' in df.columns and 'pass_PPA' in df.columns:
                # Calculate vertical playmaker: PrgP + (1/3 * 2) + (PPA * 5)
                df['vertical_playmaker'] = (df['pass_PrgP'] + (df['pass_1/3'] * 2) + (df['pass_PPA'] * 5)).fillna(0)
                vertical_leaders = df.nlargest(5, 'vertical_playmaker')[['Player', 'Squad', 'vertical_playmaker', 'pass_PrgP', 'pass_1/3', 'pass_PPA']].copy()
                vertical_leaders.columns = ['Player', 'Team', 'Vertical Score', 'Progressive Passes', 'Final Third', 'Penalty Passes']
                vertical_leaders['Vertical Score'] = vertical_leaders['Vertical Score'].round(1)
                vertical_leaders['Progressive Passes'] = vertical_leaders['Progressive Passes'].round(1)
                vertical_leaders['Final Third'] = vertical_leaders['Final Third'].round(1)
                vertical_leaders['Penalty Passes'] = vertical_leaders['Penalty Passes'].round(1)
                st.dataframe(vertical_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Vertical playmaker data not found")
        
        with col5:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #dc3545;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #dc3545; font-size: 1rem;'>Press-Resistant Passer</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Reliable under pressure</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'pass_Cmp%' in df.columns and 'poss_Dis' in df.columns:
                # Calculate press-resistant passer: Cmp% / (Dis + 1)
                df['press_resistant'] = (df['pass_Cmp%'] / (df['poss_Dis'] + 1)).fillna(0)
                # Filter out players with very low dispossessions to avoid misleading ratios
                qualified_passers = df[df['poss_Dis'] >= 5]
                if not qualified_passers.empty:
                    press_leaders = qualified_passers.nlargest(5, 'press_resistant')[['Player', 'Squad', 'press_resistant', 'pass_Cmp%', 'poss_Dis']].copy()
                    press_leaders.columns = ['Player', 'Team', 'Reliability Ratio', 'Pass %', 'Dispossessions']
                    press_leaders['Reliability Ratio'] = press_leaders['Reliability Ratio'].round(2)
                    press_leaders['Pass %'] = (press_leaders['Pass %'] * 100).round(1)
                    press_leaders['Dispossessions'] = press_leaders['Dispossessions'].round(1)
                    st.dataframe(press_leaders, use_container_width=True, hide_index=True)
                else:
                    st.info("No qualified passers found")
            else:
                st.info("Pass accuracy or dispossessions data not found")
        
        with col6:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #17a2b8;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #17a2b8; font-size: 1rem;'>Visionary</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Long-range passing vision</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'passt_Sw' in df.columns and 'passt_TB' in df.columns:
                # Calculate visionary: Sw + (TB * 3)
                df['visionary_score'] = (df['passt_Sw'] + (df['passt_TB'] * 3)).fillna(0)
                visionary_leaders = df.nlargest(5, 'visionary_score')[['Player', 'Squad', 'visionary_score', 'passt_Sw', 'passt_TB']].copy()
                visionary_leaders.columns = ['Player', 'Team', 'Vision Score', 'Switches', 'Through Balls']
                visionary_leaders['Vision Score'] = visionary_leaders['Vision Score'].round(1)
                visionary_leaders['Switches'] = visionary_leaders['Switches'].round(1)
                visionary_leaders['Through Balls'] = visionary_leaders['Through Balls'].round(1)
                st.dataframe(visionary_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Switch or through ball data not found")
    
    with sub_tab2:
        # Defensive Leaders content
        st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; text-align: center; color: #2563eb;'>
                 Defensive Leaders
            </h2>
            <p style='text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;'>
                Defensive efficiency, intelligence, and high-press specialists
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_def1, col_def2 = st.columns(2)
        
        with col_def1:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #2563eb;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #2563eb; font-size: 1rem;'>Defensive Efficiency</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Per 90 minutes</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'def_Tkl' in df.columns and 'def_Int' in df.columns and 'std_Min' in df.columns:
                df['defensive_efficiency'] = ((df['def_Tkl'] + df['def_Int']) / (df['std_Min'] / 90)).fillna(0)
                defensive_leaders = df.nlargest(5, 'defensive_efficiency')[['Player', 'Squad', 'defensive_efficiency']].copy()
                defensive_leaders.columns = ['Player', 'Team', 'Tackles+Int per 90']
                defensive_leaders['Tackles+Int per 90'] = defensive_leaders['Tackles+Int per 90'].round(2)
                st.dataframe(defensive_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Defensive or minutes data not found")
        
        with col_def2:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #28a745;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #28a745; font-size: 1rem;'>Recovery Rate</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Per 90 minutes</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'misc_Recov' in df.columns and 'std_Min' in df.columns:
                df['recovery_rate'] = (df['misc_Recov'] / (df['std_Min'] / 90)).fillna(0)
                recovery_leaders = df.nlargest(5, 'recovery_rate')[['Player', 'Squad', 'recovery_rate']].copy()
                recovery_leaders.columns = ['Player', 'Team', 'Recoveries per 90']
                recovery_leaders['Recoveries per 90'] = recovery_leaders['Recoveries per 90'].round(2)
                st.dataframe(recovery_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Recovery or minutes data not found")
        
        # Second row of Defensive Leaders
        col_def3, col_def4 = st.columns(2)
        
        with col_def3:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #ffc107;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #ffc107; font-size: 1rem;'>Defensive Intelligence</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Interceptions vs Tackles ratio</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'def_Int' in df.columns and 'def_Tkl' in df.columns:
                # Calculate defensive intelligence: Int / Tkl
                df['defensive_intelligence'] = (df['def_Int'] / df['def_Tkl']).fillna(0)
                # Filter out players with very low defensive actions
                qualified_defenders = df[(df['def_Tkl'] >= 5) & (df['def_Int'] >= 3)]
                if not qualified_defenders.empty:
                    intelligence_leaders = qualified_defenders.nlargest(5, 'defensive_intelligence')[['Player', 'Squad', 'defensive_intelligence', 'def_Int', 'def_Tkl']].copy()
                    intelligence_leaders.columns = ['Player', 'Team', 'Intelligence Ratio', 'Interceptions', 'Tackles']
                    intelligence_leaders['Intelligence Ratio'] = intelligence_leaders['Intelligence Ratio'].round(2)
                    intelligence_leaders['Interceptions'] = intelligence_leaders['Interceptions'].round(1)
                    intelligence_leaders['Tackles'] = intelligence_leaders['Tackles'].round(1)
                    st.dataframe(intelligence_leaders, use_container_width=True, hide_index=True)
                else:
                    st.info("No qualified defenders found")
            else:
                st.info("Interceptions or tackles data not found")
        
        with col_def4:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #6f42c1;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #6f42c1; font-size: 1rem;'>High Press Percentage</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Defensive actions in attacking third</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'def_Att 3rd' in df.columns and 'def_Def 3rd' in df.columns and 'def_Mid 3rd' in df.columns:
                # Calculate high press percentage
                df['total_def_actions'] = df['def_Def 3rd'] + df['def_Mid 3rd'] + df['def_Att 3rd']
                df['high_press_pct'] = (df['def_Att 3rd'] / df['total_def_actions'] * 100).fillna(0)
                # Filter out players with very low defensive actions
                qualified_pressers = df[df['total_def_actions'] >= 10]
                if not qualified_pressers.empty:
                    press_leaders = qualified_pressers.nlargest(5, 'high_press_pct')[['Player', 'Squad', 'high_press_pct', 'def_Att 3rd', 'total_def_actions']].copy()
                    press_leaders.columns = ['Player', 'Team', 'High Press %', 'Attacking Third', 'Total Actions']
                    press_leaders['High Press %'] = press_leaders['High Press %'].round(1)
                    press_leaders['Attacking Third'] = press_leaders['Attacking Third'].round(1)
                    press_leaders['Total Actions'] = press_leaders['Total Actions'].round(1)
                    st.dataframe(press_leaders, use_container_width=True, hide_index=True)
                else:
                    st.info("No qualified pressers found")
            else:
                st.info("Defensive third data not found")
    
    with sub_tab3:
        # Attacking Leaders content
        st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; text-align: center; color: #2563eb;'>
                 Attacking Leaders
            </h2>
            <p style='text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;'>
                Clinical finishing, penalty area threat, and set piece specialists
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col5, col6, col7 = st.columns(3)
        
        with col5:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #2563eb;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #2563eb; font-size: 1rem;'>Most Clinical Finishers</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Goals vs xG efficiency <span style='color: #dc3545; font-size: 0.75rem; font-weight: 500;'>*Minimum 5 goals required*</span></p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'std_Gls' in df.columns and 'std_xG' in df.columns and 'Gls' in df.columns:
                # Filter players with at least 5 goals
                qualified_finishers = df[df['Gls'] >= 5]
                if not qualified_finishers.empty:
                    # Calculate goals vs xG ratio (clinical finishing)
                    qualified_finishers = qualified_finishers.copy()
                    qualified_finishers['clinical_ratio'] = qualified_finishers['std_Gls'] / qualified_finishers['std_xG'].replace(0, 0.1)  # Avoid division by zero
                    clinical_leaders = qualified_finishers.nlargest(5, 'clinical_ratio')[['Player', 'Squad', 'std_Gls', 'std_xG', 'clinical_ratio']].copy()
                    clinical_leaders.columns = ['Player', 'Team', 'Goals', 'xG', 'Goals/xG Ratio']
                    clinical_leaders['Goals/xG Ratio'] = clinical_leaders['Goals/xG Ratio'].round(2)
                    clinical_leaders['Goals'] = clinical_leaders['Goals'].round(1)
                    clinical_leaders['xG'] = clinical_leaders['xG'].round(1)
                    st.dataframe(clinical_leaders, use_container_width=True, hide_index=True)
                else:
                    st.info("No players with 5+ goals found")
            else:
                st.info("Goals or xG data not found")
        
        with col6:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #28a745;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #28a745; font-size: 1rem;'>Penalty Area Threat</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Danger in and around penalty area</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'pass_PPA' in df.columns and 'poss_CPA' in df.columns and 'std_PrgR' in df.columns:
                # Calculate penalty area threat: PPA + CPA + PrgR
                df['penalty_area_threat'] = (df['pass_PPA'] + df['poss_CPA'] + df['std_PrgR']).fillna(0)
                threat_leaders = df.nlargest(5, 'penalty_area_threat')[['Player', 'Squad', 'penalty_area_threat', 'pass_PPA', 'poss_CPA', 'std_PrgR']].copy()
                threat_leaders.columns = ['Player', 'Team', 'Threat Score', 'Penalty Passes', 'Penalty Carries', 'Penalty Receives']
                threat_leaders['Threat Score'] = threat_leaders['Threat Score'].round(1)
                threat_leaders['Penalty Passes'] = threat_leaders['Penalty Passes'].round(1)
                threat_leaders['Penalty Carries'] = threat_leaders['Penalty Carries'].round(1)
                threat_leaders['Penalty Receives'] = threat_leaders['Penalty Receives'].round(1)
                st.dataframe(threat_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Penalty area data not found")
        
        with col7:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #ffc107;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #ffc107; font-size: 1rem;'>One-Man Army</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Individual skill creating positions</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'gca_TO' in df.columns and 'gca_Fld' in df.columns and 'poss_CPA' in df.columns:
                # Calculate one-man army: (TO * 10) + (Fld * 5) + CPA
                df['one_man_army'] = ((df['gca_TO'] * 10) + (df['gca_Fld'] * 5) + df['poss_CPA']).fillna(0)
                army_leaders = df.nlargest(5, 'one_man_army')[['Player', 'Squad', 'one_man_army', 'gca_TO', 'gca_Fld', 'poss_CPA']].copy()
                army_leaders.columns = ['Player', 'Team', 'Army Score', 'Take-Ons', 'Fouls Won', 'Penalty Carries']
                army_leaders['Army Score'] = army_leaders['Army Score'].round(1)
                army_leaders['Take-Ons'] = army_leaders['Take-Ons'].round(1)
                army_leaders['Fouls Won'] = army_leaders['Fouls Won'].round(1)
                army_leaders['Penalty Carries'] = army_leaders['Penalty Carries'].round(1)
                st.dataframe(army_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Individual skill data not found")
        
        # Second row of Attacking & Ball Carrying Leaders
        col8, col9 = st.columns(2)
        
        with col8:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #6f42c1;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #6f42c1; font-size: 1rem;'>Set Piece Maestro</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Dead ball specialist</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'gca_PassDead' in df.columns and 'passt_Crs' in df.columns:
                # Calculate set piece maestro: (PassDead * 10) + Crs
                df['set_piece_maestro'] = ((df['gca_PassDead'] * 10) + df['passt_Crs']).fillna(0)
                maestro_leaders = df.nlargest(5, 'set_piece_maestro')[['Player', 'Squad', 'set_piece_maestro', 'gca_PassDead', 'passt_Crs']].copy()
                maestro_leaders.columns = ['Player', 'Team', 'Maestro Score', 'Dead Ball Assists', 'Crosses']
                maestro_leaders['Maestro Score'] = maestro_leaders['Maestro Score'].round(1)
                maestro_leaders['Dead Ball Assists'] = maestro_leaders['Dead Ball Assists'].round(1)
                maestro_leaders['Crosses'] = maestro_leaders['Crosses'].round(1)
                st.dataframe(maestro_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Set piece data not found")
        
        with col9:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #dc3545;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #dc3545; font-size: 1rem;'>Most Clinical Playmakers</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Assists vs xAG efficiency <span style='color: #dc3545; font-size: 0.75rem; font-weight: 500;'>*Minimum 5 assists required*</span></p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'std_Ast' in df.columns and 'std_xAG' in df.columns and 'Ast' in df.columns:
                # Filter players with at least 5 assists
                qualified_playmakers = df[df['Ast'] >= 5]
                if not qualified_playmakers.empty:
                    # Calculate assists vs xAG ratio (clinical playmaking)
                    qualified_playmakers = qualified_playmakers.copy()
                    qualified_playmakers['playmaking_ratio'] = qualified_playmakers['std_Ast'] / qualified_playmakers['std_xAG'].replace(0, 0.1)  # Avoid division by zero
                    playmaking_leaders = qualified_playmakers.nlargest(5, 'playmaking_ratio')[['Player', 'Squad', 'std_Ast', 'std_xAG', 'playmaking_ratio']].copy()
                    playmaking_leaders.columns = ['Player', 'Team', 'Assists', 'xAG', 'Assists/xAG Ratio']
                    playmaking_leaders['Assists/xAG Ratio'] = playmaking_leaders['Assists/xAG Ratio'].round(2)
                    playmaking_leaders['Assists'] = playmaking_leaders['Assists'].round(1)
                    playmaking_leaders['xAG'] = playmaking_leaders['xAG'].round(1)
                    st.dataframe(playmaking_leaders, use_container_width=True, hide_index=True)
                else:
                    st.info("No players with 5+ assists found")
            else:
                st.info("Assists or xAG data not found")
        
        # Dribble & Ball Carrying Specialists section
        st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h2 style='font-size: 1.5rem; font-weight: 600; text-align: center; color: #2563eb;'>
                 Dribble & Ball Carrying Specialists
            </h2>
            <p style='text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 0.5rem;'>
                Progressive ball carrying, press resistance, and end-product dribbling
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_drib1, col_drib2 = st.columns(2)
        
        with col_drib1:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #2563eb;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #2563eb; font-size: 1rem;'>Progressive Ball Carrier</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Vertical ball carrying threat</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'poss_PrgC' in df.columns and 'poss_1/3' in df.columns and 'poss_CPA' in df.columns:
                # Calculate progressive ball carrier: PrgC + (1/3 * 2) + (CPA * 5)
                df['progressive_carrier'] = (df['poss_PrgC'] + (df['poss_1/3'] * 2) + (df['poss_CPA'] * 5)).fillna(0)
                carrier_leaders = df.nlargest(5, 'progressive_carrier')[['Player', 'Squad', 'progressive_carrier', 'poss_PrgC', 'poss_1/3', 'poss_CPA']].copy()
                carrier_leaders.columns = ['Player', 'Team', 'Carrier Score', 'Progressive Carries', 'Final Third', 'Penalty Area']
                carrier_leaders['Carrier Score'] = carrier_leaders['Carrier Score'].round(1)
                carrier_leaders['Progressive Carries'] = carrier_leaders['Progressive Carries'].round(1)
                carrier_leaders['Final Third'] = carrier_leaders['Final Third'].round(1)
                carrier_leaders['Penalty Area'] = carrier_leaders['Penalty Area'].round(1)
                st.dataframe(carrier_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Ball carrying data not found")
        
        with col_drib2:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #28a745;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #28a745; font-size: 1rem;'>Press Breaker</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Reliable under pressure</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'poss_Carries' in df.columns and 'poss_Dis' in df.columns:
                # Calculate press breaker: Carries / (Dis + 1)
                df['press_breaker'] = (df['poss_Carries'] / (df['poss_Dis'] + 1)).fillna(0)
                # Filter out players with very low carries to avoid misleading ratios
                qualified_carriers = df[df['poss_Carries'] >= 20]
                if not qualified_carriers.empty:
                    breaker_leaders = qualified_carriers.nlargest(5, 'press_breaker')[['Player', 'Squad', 'press_breaker', 'poss_Carries', 'poss_Dis']].copy()
                    breaker_leaders.columns = ['Player', 'Team', 'Reliability Ratio', 'Total Carries', 'Dispossessions']
                    breaker_leaders['Reliability Ratio'] = breaker_leaders['Reliability Ratio'].round(2)
                    breaker_leaders['Total Carries'] = breaker_leaders['Total Carries'].round(1)
                    breaker_leaders['Dispossessions'] = breaker_leaders['Dispossessions'].round(1)
                    st.dataframe(breaker_leaders, use_container_width=True, hide_index=True)
                else:
                    st.info("No players with 20+ carries found")
            else:
                st.info("Carries or dispossessions data not found")
        
        # Second row of Dribble & Ball Carrying Specialists
        col_drib3, col_drib4 = st.columns(2)
        
        with col_drib3:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #ffc107;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #ffc107; font-size: 1rem;'>End-Product Dribbler</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Dribbling with goal threat</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'gca_TO' in df.columns and 'poss_Carries' in df.columns:
                # Calculate end-product dribbler: (TO * 100) / Carries
                df['end_product_dribbler'] = ((df['gca_TO'] * 100) / df['poss_Carries']).fillna(0)
                # Filter out players with very low carries to avoid misleading ratios
                qualified_dribblers = df[df['poss_Carries'] >= 20]
                if not qualified_dribblers.empty:
                    dribbler_leaders = qualified_dribblers.nlargest(5, 'end_product_dribbler')[['Player', 'Squad', 'end_product_dribbler', 'gca_TO', 'poss_Carries']].copy()
                    dribbler_leaders.columns = ['Player', 'Team', 'End-Product %', 'Take-Ons', 'Total Carries']
                    dribbler_leaders['End-Product %'] = dribbler_leaders['End-Product %'].round(1)
                    dribbler_leaders['Take-Ons'] = dribbler_leaders['Take-Ons'].round(1)
                    dribbler_leaders['Total Carries'] = dribbler_leaders['Total Carries'].round(1)
                    st.dataframe(dribbler_leaders, use_container_width=True, hide_index=True)
                else:
                    st.info("No players with 20+ carries found")
            else:
                st.info("Take-ons or carries data not found")
        
        with col_drib4:
            st.markdown("""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #6f42c1;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #6f42c1; font-size: 1rem;'>Dribble Impact Score</h4>
            <p style='margin: 0; color: #6c757d; font-size: 0.8rem;'>Progressive carries + defensive disruption</p>
        </div>
        """, unsafe_allow_html=True)
            
            if 'poss_PrgC' in df.columns and 'gca_TO' in df.columns:
                # Calculate dribble impact: PrgC + (gca_TO * 10)
                df['dribble_impact'] = (df['poss_PrgC'] + (df['gca_TO'] * 10)).fillna(0)
                dribble_leaders = df.nlargest(5, 'dribble_impact')[['Player', 'Squad', 'dribble_impact', 'poss_PrgC', 'gca_TO']].copy()
                dribble_leaders.columns = ['Player', 'Team', 'Impact Score', 'Progressive Carries', 'Take-Ons']
                dribble_leaders['Impact Score'] = dribble_leaders['Impact Score'].round(1)
                dribble_leaders['Progressive Carries'] = dribble_leaders['Progressive Carries'].round(1)
                dribble_leaders['Take-Ons'] = dribble_leaders['Take-Ons'].round(1)
                st.dataframe(dribble_leaders, use_container_width=True, hide_index=True)
            else:
                st.info("Progressive carries or take-ons data not found")



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
        minutes_trend = df.groupby('Minutes_Bin', observed=False).agg({
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
    
    minutes_trends = df_minutes.groupby('Minutes_Bin', observed=False).agg({
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
