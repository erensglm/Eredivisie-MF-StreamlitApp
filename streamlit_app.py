import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF
from sklearn.preprocessing import MinMaxScaler
import os

# Modern Professional Styling with Gradients
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container - Eredivisie theme */
    .main {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F0 50%, #FFEBE0 100%);
    }
    
    /* Custom gradient backgrounds */
    .gradient-text {
        background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Sidebar styling - Eredivisie orange */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FF6600 0%, #E55D00 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Metric cards - Eredivisie orange */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Buttons - Eredivisie orange */
    .stButton > button {
        background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 102, 0, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 102, 0, 0.6);
    }
    
    /* Expander container - Add spacing between expanders */
    [data-testid="stExpander"] {
        margin: 1.5rem 0 !important;
    }
    
    /* Expander styling - Eredivisie orange theme */
    .streamlit-expanderHeader {
        background: rgba(255, 102, 0, 0.1);
        border-radius: 12px;
        border: 2px solid rgba(255, 102, 0, 0.3);
        font-weight: 600;
        padding: 1rem 1.5rem !important;
        color: #FF6600 !important;
        box-shadow: 0 4px 15px rgba(255, 102, 0, 0.15);
        transition: all 0.3s ease;
        cursor: pointer;
        backdrop-filter: blur(10px);
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 102, 0, 0.15);
        box-shadow: 0 6px 25px rgba(255, 102, 0, 0.3);
        transform: translateY(-2px);
        border: 2px solid rgba(255, 133, 51, 0.5);
    }
    
    .streamlit-expanderHeader svg {
        stroke: #FF6600 !important;
        filter: drop-shadow(0 2px 4px rgba(255, 102, 0, 0.3));
    }
    
    .streamlit-expanderHeader p {
        color: #FF6600 !important;
    }
    
    .streamlit-expanderHeader span {
        color: #FF6600 !important;
    }
    
    [data-testid="stExpanderDetails"] {
        border: 2px solid rgba(255, 102, 0, 0.2);
        border-top: none;
        border-radius: 0 0 12px 12px;
        background: rgba(255, 102, 0, 0.05);
        padding: 1.5rem;
        margin-top: -2px;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Tabs - Eredivisie orange theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(255, 102, 0, 0.1) 0%, rgba(255, 133, 51, 0.1) 100%);
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid rgba(255, 102, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(255, 102, 0, 0.2) 0%, rgba(255, 133, 51, 0.2) 100%);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
        color: white !important;
    }
    
    /* Cards with gradient borders */
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }
    
    /* Divider - Eredivisie orange */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FF6600, #FF8533, transparent);
    }
    
    /* Multiselect selected items - #254D8D color */
    [data-baseweb="tag"] {
        background-color: #254D8D !important;
        border-color: #1e3a6d !important;
    }
    
    [data-baseweb="tag"] span {
        color: white !important;
    }
    
    /* Multiselect dropdown items */
    [data-baseweb="popover"] [role="option"] {
        color: #1f2937 !important;
    }
    
    /* Age slider - handles mavi */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #254D8D !important;
    }
    
    /* Info boxes - Orange theme */
    .stAlert {
        background-color: rgba(255, 102, 0, 0.1) !important;
        border: 1px solid rgba(255, 102, 0, 0.3) !important;
    }
    
    .stAlert [data-testid="stMarkdownContainer"] p {
        color: #FF6600 !important;
    }
    
    .stAlert [data-testid="stMarkdownContainer"] strong {
        color: #FF6600 !important;
    }
    
    /* Success boxes - Orange theme */
    div[data-baseweb="notification"] {
        background-color: rgba(255, 102, 0, 0.1) !important;
        border-left-color: #FF6600 !important;
    }
    
    div[data-baseweb="notification"] p {
        color: #FF6600 !important;
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

with st.expander("COLUMN DESCRIPTIONS (Click to expand)", expanded=False):
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
st.set_page_config(
    page_title=" Eredivisie U24 Midfielders Analytics", 
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Eredivisie U24 Midfielders Analytics Dashboard\nProfessional scouting and player analysis tool powered by data science.\n Emin Eren Sağlam"
    }
)

# Hero Section with Modern Gradient
st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #FF6600 0%, #FF8533 50%, #FFA500 100%); 
                border-radius: 24px; margin-bottom: 3rem; box-shadow: 0 20px 60px rgba(255, 102, 0, 0.4);
                position: relative; overflow: hidden;'>
        <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                    background: url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.05\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
                    opacity: 0.3;'></div>
        <div style='position: relative; z-index: 1;'>
            <h1 style='color: white; font-size: 3.5rem; margin: 0; font-weight: 800; 
                       letter-spacing: -1px; text-shadow: 0 4px 20px rgba(0,0,0,0.3);
                       background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       background-clip: text;'>
                 Eredivisie U24 Midfielders
            </h1>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.3rem; margin: 1rem 0 0.5rem 0; 
                      font-weight: 500; text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>
                Professional Scouting & Analytics Dashboard
            </p>
            <p style='color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;'>
                Advanced player analysis powered by data science
            </p>
            <p style='color: rgba(255,255,255,0.95); font-size: 1.3rem; margin: 1rem 0 0.5rem 0; 
                      font-weight: 500; text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>
                <a href='https://www.linkedin.com/in/erensglm' target='_blank' 
                   style='color: rgba(255,255,255,0.95); text-decoration: none; 
                          transition: opacity 0.3s ease;'>
                    Created by Emin Eren Sağlam
                </a>
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Project Overview & Scoring System - Side by Side Cards
col_info1, col_info2 = st.columns(2, gap="large")

with col_info1:
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 102, 0, 0.08) 0%, rgba(255, 133, 51, 0.08) 100%);
                    border-radius: 16px; padding: 2rem; height: 100%;
                    border: 2px solid rgba(255, 102, 0, 0.3);
                    box-shadow: 0 8px 32px rgba(255, 102, 0, 0.15);'>
            <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
                <h3 style='color: #FF6600; margin: 0; font-size: 1.4rem; font-weight: 700;'>
                    About This Dashboard
                </h3>
            </div>
            <p style='color: #254D8D; font-size: 1rem; line-height: 1.8; margin: 0;'>
                This comprehensive analytics platform provides data-driven insights into <strong style='color: #FF6600;'>Eredivisie's most promising young midfielders</strong> (under 24). 
                Using advanced clustering algorithms and statistical analysis, we identify three distinct player profiles to help scouts, 
                analysts, and teams make informed decisions.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 102, 0, 0.08) 0%, rgba(255, 165, 0, 0.08) 100%);
                    border-radius: 16px; padding: 2rem; height: 100%;
                    border: 2px solid rgba(255, 102, 0, 0.3);
                    box-shadow: 0 8px 32px rgba(255, 102, 0, 0.15);'>
            <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
                <h3 style='color: #FF6600; margin: 0; font-size: 1.4rem; font-weight: 700;'>
                    Scoring System
                </h3>
            </div>
            <p style='color: #254D8D; font-size: 1rem; line-height: 1.8; margin: 0;'>
                All performance metrics are scored on a <strong style='color: #FF6600;'>0-100 scale</strong>. 
                A score of <strong style='color: #10b981;'>0</strong> represents the <em>lowest</em> performance, 
                while <strong style='color: #4ade80;'>100</strong> represents the <em>highest</em>. 
                For example, a player with 85 in passing demonstrates superior passing ability compared to others in the dataset.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin: 2.5rem 0;'></div>", unsafe_allow_html=True)

# Quick Stats Cards with Modern Gradients
col1, col2, col3, col4 = st.columns(4, gap="large")
with col1:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%); 
                    padding: 2rem 1.5rem; border-radius: 20px; text-align: center; 
                    box-shadow: 0 10px 40px rgba(255, 102, 0, 0.4);
                    transition: transform 0.3s ease; position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -50%; right: -20%; width: 200px; height: 200px; 
                        background: rgba(255,255,255,0.1); border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <h2 style='color: white; margin: 0; font-size: 2.8rem; font-weight: 800; 
                           text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>48</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1rem; 
                          font-weight: 600; letter-spacing: 0.5px;'>TOTAL PLAYERS</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FFA500 0%, #FFB84D 100%); 
                    padding: 2rem 1.5rem; border-radius: 20px; text-align: center; 
                    box-shadow: 0 10px 40px rgba(255, 165, 0, 0.4);
                    transition: transform 0.3s ease; position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -50%; right: -20%; width: 200px; height: 200px; 
                        background: rgba(255,255,255,0.1); border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <h2 style='color: white; margin: 0; font-size: 2.8rem; font-weight: 800; 
                           text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>3</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1rem; 
                          font-weight: 600; letter-spacing: 0.5px;'>PLAYER PROFILES</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FF8533 0%, #FFA64D 100%); 
                    padding: 2rem 1.5rem; border-radius: 20px; text-align: center; 
                    box-shadow: 0 10px 40px rgba(255, 133, 51, 0.4);
                    transition: transform 0.3s ease; position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -50%; right: -20%; width: 200px; height: 200px; 
                        background: rgba(255,255,255,0.1); border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <h2 style='color: white; margin: 0; font-size: 2.8rem; font-weight: 800; 
                           text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>18-24</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1rem; 
                          font-weight: 600; letter-spacing: 0.5px;'>AGE RANGE</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FFB84D 0%, #FFC966 100%); 
                    padding: 2rem 1.5rem; border-radius: 20px; text-align: center; 
                    box-shadow: 0 10px 40px rgba(255, 184, 77, 0.4);
                    transition: transform 0.3s ease; position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -50%; right: -20%; width: 200px; height: 200px; 
                        background: rgba(255,255,255,0.1); border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <h2 style='color: white; margin: 0; font-size: 2.8rem; font-weight: 800; 
                           text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>18</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1rem; 
                          font-weight: 600; letter-spacing: 0.5px;'>TEAMS</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Player Profiles Section with Modern Design
st.markdown("""
    <div style='text-align: center; margin: 3rem 0 2rem 0;'>
        <h2 style='font-size: 2.5rem; font-weight: 800; margin: 0;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;'>
             Player Profile Types
        </h2>
        <p style='color: #888; font-size: 1.1rem; margin: 0.5rem 0 0 0;'>
            Understand the three distinct player profiles in our analysis
        </p>
    </div>
""", unsafe_allow_html=True)

# Add custom CSS for Player Profile expanders - tighter spacing
st.markdown("""
    <style>
        /* Reduce spacing for Player Profile expanders specifically */
        .player-profiles-section [data-testid="stExpander"] {
            margin: 0.5rem 0 !important;
        }
    </style>
    <div class="player-profiles-section">
""", unsafe_allow_html=True)

for cid, prof in cluster_profiles.items():
    # Calculate real cluster data
    cluster_data = df[df['Cluster'] == cid]
    real_player_count = len(cluster_data)
    
    with st.expander(f"PLAYER PROFILE {cid}: {prof['name']} (Click to view details)"):
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
                st.markdown("**Basic Statistics**")
                st.metric("Average Age", f"{real_avg_age:.1f}")
                st.metric("Average Minutes", f"{real_avg_minutes:.0f}")
                    
            with col2:
                st.markdown("**Performance Metrics**")
                st.caption("*(According to the 100-point rating system)*")
                st.metric(perf_label_1, f"{perf_metric_1:.2f}")
                st.metric(perf_label_2, f"{perf_metric_2:.2f}")
                    
            with col3:
                st.markdown("**Top Teams by Player Count**")
                top_teams = cluster_data['Squad'].value_counts().head(3)
                for team, count in top_teams.items():
                    st.markdown(f"• {team} ({count} players)")
        else:
            st.info("No players found in this player profile after filtering.")
                        
        st.markdown(f"**Playing Style**: {prof['detailed_stats'].get('playing_style', 'General midfielder')}")
        
        if 'key_strengths' in prof['detailed_stats']:
            st.markdown(f"**Key Strengths**: {', '.join(prof['detailed_stats']['key_strengths'])}")

# Close player profiles section div
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# STEP 2: SIDEBAR FILTERS
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

df_filtered = df[
    (df["Age"] >= age_filter[0]) &
    (df["Age"] <= age_filter[1]) &
    (df["Pos"].isin(pos_filter)) &
    (df["Squad"].isin(squad_filter)) &
    (df["Cluster"].isin(cluster_filter))
]

if player_search:
    df_filtered = df_filtered[df_filtered["Player"].str.contains(player_search, case=False, na=False)]

# Filtered Results Section with Modern Cards
st.markdown("""
    <div style='text-align: center; margin: 2rem 0 1rem 0;'>
        <h2 style='font-size: 2rem; font-weight: 800;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
             Filtered Players
        </h2>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")
with col1:
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                    padding: 1.5rem; border-radius: 16px; text-align: center;
                    border: 2px solid rgba(255, 102, 0, 0.3);'>
            <div style='font-size: 2.5rem; font-weight: 800; color: white;'>
                {len(df_filtered)}
            </div>
            <div style='color: white; font-weight: 600; margin-top: 0.5rem;'>Players Match</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    if len(df_filtered) > 0:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FFA500 0%, #FFB84D 100%);
                        padding: 1.5rem; border-radius: 16px; text-align: center;
                        border: 2px solid rgba(255, 165, 0, 0.3);'>
                <div style='font-size: 2.5rem; font-weight: 800; color: white;'>
                    {df_filtered['Age'].mean():.1f}
                </div>
                <div style='color: white; font-weight: 600; margin-top: 0.5rem;'>Average Age</div>
            </div>
        """, unsafe_allow_html=True)
with col3:
    if len(df_filtered) > 0:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FF8533 0%, #FFA64D 100%);
                        padding: 1.5rem; border-radius: 16px; text-align: center;
                        border: 2px solid rgba(255, 133, 51, 0.3);'>
                <div style='font-size: 2.5rem; font-weight: 800; color: white;'>
                    {df_filtered['std_Min'].mean():.0f}
                </div>
                <div style='color: white; font-weight: 600; margin-top: 0.5rem;'>Average Minutes</div>
            </div>
        """, unsafe_allow_html=True)

with st.expander("View Detailed Player Data (Click to expand table)", expanded=False):
    st.dataframe(df_filtered, use_container_width=True, height=400)

st.divider()


# ---------------------------
# STEP 4: TOP 5 PLAYERS BY PLAYER PROFILE
# ---------------------------
st.markdown("""
    <div style='text-align: center; margin: 3rem 0 2rem 0;'>
        <h1 style='font-size: 3rem; font-weight: 800; margin: 0;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;'>
            Top 5 Players by Player Profile
        </h1>
        <p style='color: #888; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>
            Discover the best performers in each player profile category
        </p>
    </div>
""", unsafe_allow_html=True)

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
        <div style='background: {profile_gradients[cid]}; 
                    padding: 2rem 1.5rem; border-radius: 20px; margin: 2rem 0;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
                    position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -50%; right: -10%; width: 300px; height: 300px; 
                        background: rgba(255,255,255,0.1); border-radius: 50%;'></div>
            <div style='position: relative; z-index: 1;'>
                <div style='display: flex; align-items: center; gap: 1rem;'>
                    <div style='font-size: 3rem;'>{profile_icons[cid]}</div>
                    <div>
                        <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 800; 
                                   text-shadow: 0 2px 10px rgba(0,0,0,0.2);'>
                            Profile {cid}: {cluster_profiles[cid]['name']}
                        </h2>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate cluster statistics from real data
    cluster_data = df_filtered[df_filtered['Cluster'] == cid]
    
    # Show individual standout features of top 5 players
    if len(cluster_data) > 0:
        with st.expander(f"Outstanding Features of Top 5 Players (Click to collapse)", expanded=True):
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
                        comment = "**Elite finisher and creator** - Both scores goals and provides assists"
                    elif gol > 2.0:
                        comment = "**Super goalscorer** - Team's most reliable goal machine"
                    elif asist > 1.5:
                        comment = "**Playmaker** - Constantly sets up teammates for goals"
                    elif xg > 2.0:
                        comment = "**High potential** - Statistically gets into very effective positions"
                    else:
                        comment = "**Balanced player** - Versatile profile contributing in many areas"
                        
                    st.write(f"**{idx}. {player['Player']}**: {comment}")
                    
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
                        comment = "**Experienced reliable** - Plays a lot and has high pass quality"
                    elif minutes > 2000:
                        comment = "**Hard-working engine** - Constantly plays in the team, gaining experience"
                    elif pas_success > 0.8:
                        comment = "**Technical ability** - Very high pass quality, reliable"
                    elif play_ratio > 0.5:
                        comment = "**Rising value** - Has gained coach's trust, potential"
                    else:
                        comment = "**Promising future** - Still raw but open to development profile"
                        
                    st.write(f"**{idx}. {player['Player']}**: {comment}")
                    
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
                        comment = "**Defensive wall** - Both aggressive and intelligent defending"
                    elif tackles > 3.0:
                        comment = "**Aggressive warrior** - Fighting style that doesn't let opponents breathe"
                    elif recoveries > 3.0:
                        comment = "**Smart cleaner** - Master of ball recovery through positioning"
                    elif interceptions > 2.0:
                        comment = "**Game reader** - Intelligent defender who intercepts opponent passes"
                    else:
                        comment = "**Reliable worker** - Quiet but effective, team's indispensable"
                        
                    st.write(f"**{idx}. {player['Player']}**: {comment}")
    
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
    st.markdown("### 🏆 Player Report")
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
                        <div style='border: 2px solid {border_colors.get(cid, border_colors[0])};
                                    border-radius: 10px; padding: 1rem; 
                                    background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <div style='text-align: center;'>
                                <div style='color: {border_colors.get(cid, border_colors[0])}; 
                                            font-size: 0.8rem; font-weight: 600;'>
                                    #{player_idx + 1}
                                </div>
                                <h4 style='margin: 0.3rem 0; color: #333; font-size: 1.1rem;'>
                                    {player['Player']}
                                </h4>
                                <p style='margin: 0; color: #666; font-size: 0.85rem;'>
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
                            <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                <div style='color: #888; font-size: 0.7rem;'>Position</div>
                                <div style='font-weight: 600; color: #333;'>{player['Pos']}</div>
                            </div>
                            <div style='text-align: center; padding: 0.4rem; background: #f5f5f5; border-radius: 5px;'>
                                <div style='color: #888; font-size: 0.7rem;'>Score</div>
                                <div style='font-weight: 600; color: {border_colors.get(cid, border_colors[0])};'>
                                    {score_value:.1f}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Archetype section
                    st.markdown(f"""
                        <div style='margin-top: 0.8rem; padding: 0.6rem; 
                                    background: linear-gradient(135deg, {border_colors.get(cid, border_colors[0])}15, {border_colors.get(cid, border_colors[0])}05);
                                    border-radius: 5px; text-align: center;'>
                            <div style='color: #888; font-size: 0.7rem; margin-bottom: 0.2rem;'>
                                Archetype
                            </div>
                            <div style='font-weight: 700; color: {border_colors.get(cid, border_colors[0])}; 
                                        font-size: 0.95rem;'>
                                {primary_archetype}
                            </div>
                            <div style='color: #666; font-size: 0.75rem; margin-top: 0.2rem;'>
                                Score: {archetype_score:.1f}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
    
    st.divider()
# ---------------------------
# STEP 3: RADAR + SIMILAR PLAYERS + PLAYER PROFILE
# ---------------------------
st.markdown("""
    <div style='text-align: center; margin: 3rem 0 2rem 0;'>
        <h1 style='font-size: 3rem; font-weight: 800; margin: 0;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;'>
            Player Analysis & Comparison
        </h1>
        <p style='color: #888; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>
            Deep dive into individual player performance with radar charts and similarity analysis
        </p>
    </div>
""", unsafe_allow_html=True)

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
    df_filtered["Player"].unique(), 
    default=[], 
    key="player_select",
    help="You can select multiple players for comparison"
)

def update_player_view(selected_players):
    if not selected_players:
        st.info("Please select the player(s) you want to analyze.")
        return
        
    # Get data of selected players
    selected_rows = df_filtered[df_filtered["Player"].isin(selected_players)]
    if selected_rows.empty:
        st.warning("Selected players are outside filtering criteria.")
        return

    # Player Profile information of selected players
    unique_clusters = selected_rows["Cluster"].unique()
    
    # Show player profile information
    for cluster_id in unique_clusters:
        players_in_cluster = selected_rows[selected_rows["Cluster"] == cluster_id]["Player"].tolist()
        st.write(f"**Player Profile {cluster_id}: {cluster_profiles[cluster_id]['name']}** → {', '.join(players_in_cluster)}")
        st.caption(cluster_profiles[cluster_id]['description'])

    # ---------------------------
    # Multi-Player vs Cluster Radar
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
    
    # Add player profile averages
    # Chart renkler - birbirinden ayırt edilebilir
    cluster_colors = ['#1E88E5', '#43A047', '#FB8C00']  # Profile 0: Mavi, Profile 1: Yeşil, Profile 2: Turuncu
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
        
        # Add player profile averages
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
            df_metrics = df_filtered[radar_metrics].copy()
            selected_vector = player_row[radar_metrics].values.flatten()
            df_temp = df_filtered.copy()
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
    df_scaled_all = pd.DataFrame(MinMaxScaler().fit_transform(df_filtered[radar_metrics]),
                                 columns=radar_metrics, index=df_filtered.index)
    cluster_means_scaled = df_scaled_all.groupby(df_filtered["Cluster"]).mean()
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

update_player_view(player_select)

# ---------------------------
# STEP 6: SCATTER PLOT ANALYSES
# ---------------------------
st.markdown("""
    <div style='text-align: center; margin: 3rem 0 2rem 0;'>
        <h1 style='font-size: 3rem; font-weight: 800; margin: 0;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;'>
            Advanced Scatter Plot Analyses
        </h1>
        <p style='color: #888; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>
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
    
    for cluster_id in df_filtered['Cluster'].unique():
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        
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
        youngest_top_performer = df_filtered.loc[df_filtered['std_Gls'] + df_filtered['std_Ast'] > 1.5, 'Age'].min()
        st.metric("Youngest High Performer Age", f"{youngest_top_performer:.0f}" if not pd.isna(youngest_top_performer) else "N/A")
    with col2:
        avg_age_top_performers = df_filtered[df_filtered['std_Gls'] + df_filtered['std_Ast'] > 1.0]['Age'].mean()
        st.metric("Avg Age of Top Contributors", f"{avg_age_top_performers:.1f}" if not pd.isna(avg_age_top_performers) else "N/A")

with tab2:
    st.markdown("### Playing Time vs Effectiveness")
    st.markdown("Examine the relationship between minutes played and expected goal contributions.")
    
    # Minutes vs Effectiveness Scatter Plot
    fig_minutes = go.Figure()
    
    for cluster_id in df_filtered['Cluster'].unique():
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        
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
    st.markdown("### Passing Accuracy vs Creativity")
    st.markdown("Discover the balance between safe passing and creative playmaking.")
    
    # Passing vs Creativity Scatter Plot
    fig_passing = go.Figure()
    
    for cluster_id in df_filtered['Cluster'].unique():
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        
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
    st.markdown("### Defensive vs Offensive Contributions")
    st.markdown("Compare players' defensive work rate with their attacking output.")
    
    # Defense vs Attack Scatter Plot
    fig_def_att = go.Figure()
    
    for cluster_id in df_filtered['Cluster'].unique():
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        
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

st.divider()

# Summary insights section
st.markdown("""
    <div style='margin: 3rem 0 2rem 0;'>
        <h2 style='font-size: 2.2rem; font-weight: 800; text-align: center;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Key Insights from Scatter Analysis
        </h2>
        <p style='text-align: center; color: #888; font-size: 1rem; margin-top: 0.5rem;'>
            Statistical correlations and standout performers
        </p>
    </div>
""", unsafe_allow_html=True)

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("### Performance Trends")
    
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
    st.markdown("### Standout Players")
    
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
st.markdown("""
    <div style='text-align: center; margin: 3rem 0 2rem 0;'>
        <h1 style='font-size: 3rem; font-weight: 800; margin: 0;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;'>
            Trend & Line Chart Analyses
        </h1>
        <p style='color: #888; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>
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
    st.markdown("### Performance vs Playing Time")
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
    st.markdown("### Team Performance Comparison")
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
st.markdown("""
    <div style='margin: 3rem 0 2rem 0;'>
        <h2 style='font-size: 2.2rem; font-weight: 800; text-align: center;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Key Trend Insights
        </h2>
    </div>
""", unsafe_allow_html=True)

trend_insights_col1, trend_insights_col2 = st.columns(2)

with trend_insights_col1:
    st.markdown("### Performance Patterns")
    
    if not df_filtered.empty:
        # Age-performance correlation
        age_goal_corr = df_filtered['Age'].corr(df_filtered['std_Gls'])
        age_def_corr = df_filtered['Age'].corr(df_filtered['def_Tkl'] + df_filtered['def_Int'])
        
        st.write(f"• **Age-Goal Correlation**: {age_goal_corr:.3f}")
        st.write(f"• **Age-Defense Correlation**: {age_def_corr:.3f}")
        
        if age_goal_corr > 0.1:
            st.success("Older players tend to score more")
        elif age_goal_corr < -0.1:
            st.info("Younger players are more prolific")
        else:
            st.info("Age has minimal impact on scoring")
            
        if age_def_corr > 0.1:
            st.success("Older players are more defensive")
        elif age_def_corr < -0.1:
            st.info("Younger players defend more actively")
        else:
            st.info("Age doesn't affect defensive work")

with trend_insights_col2:
    st.markdown("### Peak Performance Insights")
    
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

# ---------------------------
# STEP 8: HISTOGRAM ANALYSES
# ---------------------------
st.markdown("""
    <div style='text-align: center; margin: 3rem 0 2rem 0;'>
        <h1 style='font-size: 3rem; font-weight: 800; margin: 0;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;'>
            Distribution Analysis (Histograms)
        </h1>
        <p style='color: #888; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>
            Understand how player metrics are distributed across the dataset
        </p>
    </div>
""", unsafe_allow_html=True)

with st.expander("Reading histograms (Click to expand)", expanded=False):
    st.markdown("""
    **What do histograms show?**
    - Height of bars indicates number of players in each range
    - Different colors represent different player profiles
    - Use 'overlay' mode to see profile distributions
    
    **Key insights:**
    - Identify common performance ranges
    - Spot outliers and exceptional players
    - Compare profile distributions
    """)

st.markdown("---")

# Create tabs for different histogram categories
hist_tab1, hist_tab2, hist_tab3, hist_tab4 = st.tabs([
    "Performance Metrics",
    "Playing Time",
    "Technical Skills",
    "Physical & Discipline"
])

with hist_tab1:
    st.markdown("### Goal & Assist Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Goals histogram
        fig_goals_hist = go.Figure()
        
        # Chart renkler
        hist_colors = {0: '#1E88E5', 1: '#43A047', 2: '#FB8C00'}
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_goals_hist.add_trace(go.Histogram(
                x=cluster_data['std_Gls'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_goals_hist.update_layout(
            title="Goals per Game Distribution",
            xaxis_title="Goals per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_goals_hist, use_container_width=True)
        
        # Stats
        st.metric("Average Goals", f"{df_filtered['std_Gls'].mean():.2f}")
        st.metric("Median Goals", f"{df_filtered['std_Gls'].median():.2f}")
    
    with col2:
        # Assists histogram
        fig_assists_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_assists_hist.add_trace(go.Histogram(
                x=cluster_data['std_Ast'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_assists_hist.update_layout(
            title="Assists per Game Distribution",
            xaxis_title="Assists per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_assists_hist, use_container_width=True)
        
        # Stats
        st.metric("Average Assists", f"{df_filtered['std_Ast'].mean():.2f}")
        st.metric("Median Assists", f"{df_filtered['std_Ast'].median():.2f}")
    
    # Combined G+A histogram
    st.markdown("### Total Goal Contributions (G+A)")
    
    df_filtered_copy = df_filtered.copy()
    df_filtered_copy['G+A'] = df_filtered_copy['std_Gls'] + df_filtered_copy['std_Ast']
    
    fig_ga_hist = go.Figure()
    
    for cluster_id in sorted(df_filtered['Cluster'].unique()):
        cluster_data = df_filtered_copy[df_filtered_copy['Cluster'] == cluster_id]
        fig_ga_hist.add_trace(go.Histogram(
            x=cluster_data['G+A'],
            name=f'Cluster {cluster_id}',
            opacity=0.7,
            nbinsx=20,
            marker_color=hist_colors.get(cluster_id, '#1E88E5')
        ))
    
    fig_ga_hist.update_layout(
        title="Goal Contributions Distribution by Cluster",
        xaxis_title="Goals + Assists per Game",
        yaxis_title="Number of Players",
        template='plotly_dark',
        barmode='overlay',
        height=400
    )
    
    st.plotly_chart(fig_ga_hist, use_container_width=True)

with hist_tab2:
    st.markdown("### Playing Time Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Minutes histogram
        fig_minutes_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_minutes_hist.add_trace(go.Histogram(
                x=cluster_data['std_Min'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_minutes_hist.update_layout(
            title="Minutes Played Distribution",
            xaxis_title="Total Minutes",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_minutes_hist, use_container_width=True)
        
        st.metric("Average Minutes", f"{df_filtered['std_Min'].mean():.0f}")
        st.metric("Median Minutes", f"{df_filtered['std_Min'].median():.0f}")
    
    with col2:
        # Matches played histogram
        fig_matches_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_matches_hist.add_trace(go.Histogram(
                x=cluster_data['std_MP'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_matches_hist.update_layout(
            title="Matches Played Distribution",
            xaxis_title="Number of Matches",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_matches_hist, use_container_width=True)
        
        st.metric("Average Matches", f"{df_filtered['std_MP'].mean():.1f}")
        st.metric("Median Matches", f"{df_filtered['std_MP'].median():.1f}")
    
    # Age distribution
    st.markdown("### Age Distribution")
    
    fig_age_hist = go.Figure()
    
    for cluster_id in sorted(df_filtered['Cluster'].unique()):
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        fig_age_hist.add_trace(go.Histogram(
            x=cluster_data['Age'],
            name=f'Cluster {cluster_id}',
            opacity=0.7,
            nbinsx=10,
            marker_color=hist_colors.get(cluster_id, '#1E88E5')
        ))
    
    fig_age_hist.update_layout(
        title="Player Age Distribution by Cluster",
        xaxis_title="Age",
        yaxis_title="Number of Players",
        template='plotly_dark',
        barmode='stack',
        height=400
    )
    
    st.plotly_chart(fig_age_hist, use_container_width=True)

with hist_tab3:
    st.markdown("### Technical Skills Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pass completion histogram
        fig_pass_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_pass_hist.add_trace(go.Histogram(
                x=cluster_data['pass_Cmp%'] * 100,  # Convert to percentage
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=20
            ))
        
        fig_pass_hist.update_layout(
            title="Pass Completion Rate Distribution",
            xaxis_title="Pass Success Rate (%)",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_pass_hist, use_container_width=True)
        
        st.metric("Avg Pass Success", f"{df_filtered['pass_Cmp%'].mean()*100:.1f}%")
    
    with col2:
        # Key passes histogram
        fig_kp_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_kp_hist.add_trace(go.Histogram(
                x=cluster_data['pass_KP'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_kp_hist.update_layout(
            title="Key Passes Distribution",
            xaxis_title="Key Passes per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_kp_hist, use_container_width=True)
        
        st.metric("Avg Key Passes", f"{df_filtered['pass_KP'].mean():.2f}")
    
    # Progressive passes and carries
    st.markdown("### Progressive Play")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_prog_pass = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_prog_pass.add_trace(go.Histogram(
                x=cluster_data['pass_PrgP'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_prog_pass.update_layout(
            title="Progressive Passes Distribution",
            xaxis_title="Progressive Passes per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=350
        )
        
        st.plotly_chart(fig_prog_pass, use_container_width=True)
    
    with col2:
        fig_prog_carry = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_prog_carry.add_trace(go.Histogram(
                x=cluster_data['poss_PrgC'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_prog_carry.update_layout(
            title="Progressive Carries Distribution",
            xaxis_title="Progressive Carries per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=350
        )
        
        st.plotly_chart(fig_prog_carry, use_container_width=True)

with hist_tab4:
    st.markdown("### Defensive Actions Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tackles histogram
        fig_tackles_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_tackles_hist.add_trace(go.Histogram(
                x=cluster_data['def_Tkl'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_tackles_hist.update_layout(
            title="Tackles per Game Distribution",
            xaxis_title="Tackles per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_tackles_hist, use_container_width=True)
        
        st.metric("Avg Tackles", f"{df_filtered['def_Tkl'].mean():.2f}")
    
    with col2:
        # Interceptions histogram
        fig_int_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_int_hist.add_trace(go.Histogram(
                x=cluster_data['def_Int'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_int_hist.update_layout(
            title="Interceptions per Game Distribution",
            xaxis_title="Interceptions per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=400
        )
        
        st.plotly_chart(fig_int_hist, use_container_width=True)
        
        st.metric("Avg Interceptions", f"{df_filtered['def_Int'].mean():.2f}")
    
    # Ball recoveries
    st.markdown("### Ball Recoveries")
    
    fig_recov_hist = go.Figure()
    
    for cluster_id in sorted(df_filtered['Cluster'].unique()):
        cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
        fig_recov_hist.add_trace(go.Histogram(
            x=cluster_data['misc_Recov'],
            name=f'Cluster {cluster_id}',
            opacity=0.7,
            nbinsx=20,
            marker_color=hist_colors.get(cluster_id, '#1E88E5')
        ))
    
    fig_recov_hist.update_layout(
        title="Ball Recoveries Distribution by Cluster",
        xaxis_title="Recoveries per Game",
        yaxis_title="Number of Players",
        template='plotly_dark',
        barmode='overlay',
        height=400
    )
    
    st.plotly_chart(fig_recov_hist, use_container_width=True)
    
    # Discipline
    st.markdown("### Discipline (Cards)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_yellow_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_yellow_hist.add_trace(go.Histogram(
                x=cluster_data['std_CrdY'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=10
            ))
        
        fig_yellow_hist.update_layout(
            title="Yellow Cards Distribution",
            xaxis_title="Yellow Cards",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=350
        )
        
        st.plotly_chart(fig_yellow_hist, use_container_width=True)
    
    with col2:
        fig_fouls_hist = go.Figure()
        
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            fig_fouls_hist.add_trace(go.Histogram(
                x=cluster_data['misc_Fls'],
                name=f'Profile {cluster_id}',
                opacity=0.7,
                nbinsx=15,
                marker_color=hist_colors.get(cluster_id, '#1E88E5')
            ))
        
        fig_fouls_hist.update_layout(
            title="Fouls Committed Distribution",
            xaxis_title="Fouls per Game",
            yaxis_title="Number of Players",
            template='plotly_dark',
            barmode='overlay',
            height=350
        )
        
        st.plotly_chart(fig_fouls_hist, use_container_width=True)

st.divider()

# Distribution Summary
st.markdown("""
    <div style='margin: 3rem 0 2rem 0;'>
        <h2 style='font-size: 2.2rem; font-weight: 800; text-align: center;
                   background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Distribution Insights
        </h2>
        <p style='text-align: center; color: #888; font-size: 1rem; margin-top: 0.5rem;'>
            Key findings from distribution analysis
        </p>
    </div>
""", unsafe_allow_html=True)

insights_col1, insights_col2, insights_col3 = st.columns(3)

with insights_col1:
    st.markdown("### Top Performers")
    
    if not df_filtered.empty:
        # Most prolific scorer
        top_scorer = df_filtered.nlargest(1, 'std_Gls')
        if not top_scorer.empty:
            st.write(f"**Top Scorer**: {top_scorer.iloc[0]['Player']} ({top_scorer.iloc[0]['std_Gls']:.2f} goals/game)")
        
        # Most creative
        top_assists = df_filtered.nlargest(1, 'std_Ast')
        if not top_assists.empty:
            st.write(f"**Top Assister**: {top_assists.iloc[0]['Player']} ({top_assists.iloc[0]['std_Ast']:.2f} assists/game)")
        
        # Most minutes
        most_minutes = df_filtered.nlargest(1, 'std_Min')
        if not most_minutes.empty:
            st.write(f"**Most Minutes**: {most_minutes.iloc[0]['Player']} ({most_minutes.iloc[0]['std_Min']:.0f} min)")

with insights_col2:
    st.markdown("### Distribution Stats")
    
    if not df_filtered.empty:
        # Goals standard deviation
        goals_std = df_filtered['std_Gls'].std()
        st.write(f"**Goals Variation**: σ = {goals_std:.3f}")
        
        # Pass accuracy range
        pass_range = df_filtered['pass_Cmp%'].max() - df_filtered['pass_Cmp%'].min()
        st.write(f"**Pass Accuracy Range**: {pass_range*100:.1f}%")
        
        # Age diversity
        age_range = df_filtered['Age'].max() - df_filtered['Age'].min()
        st.write(f"**Age Range**: {age_range:.0f} years")

with insights_col3:
    st.markdown("### Player Profile Characteristics")
    
    if not df_filtered.empty:
        for cluster_id in sorted(df_filtered['Cluster'].unique()):
            cluster_data = df_filtered[df_filtered['Cluster'] == cluster_id]
            cluster_size = len(cluster_data)
            cluster_pct = (cluster_size / len(df_filtered)) * 100
            
            st.write(f"**Profile {cluster_id}**: {cluster_size} players ({cluster_pct:.1f}%)")

st.divider()

# Modern Footer with Gradient
st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem; 
                background: linear-gradient(135deg, #FF6600 0%, #FF8533 50%, #FFA500 100%); 
                border-radius: 24px; margin-top: 4rem;
                box-shadow: 0 20px 60px rgba(255, 102, 0, 0.4);
                position: relative; overflow: hidden;'>
        <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                    background: url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.05\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
                    opacity: 0.2;'></div>
        <div style='position: relative; z-index: 1;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'></div>
            <h2 style='margin: 0; color: white; font-size: 2rem; font-weight: 800; 
                       text-shadow: 0 2px 10px rgba(0,0,0,0.2);
                       background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       background-clip: text;'>
                Eredivisie U24 Midfielders Scouting Dashboard
            </h2>
            <p style='margin: 1rem 0 0.5rem 0; font-size: 1.1rem; color: rgba(255,255,255,0.95); font-weight: 500;'>
                Professional player analysis and comparison tool
            </p>
            <p style='margin: 0; font-size: 1rem; color: rgba(255,255,255,0.8);'>
                Data-driven insights for scouts and analysts
            </p>
            <div style='margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2);'>
                <p style='margin: 0; font-size: 0.9rem; color: rgba(255,255,255,0.7);'>
                    Powered by Advanced Analytics & Machine Learning
                </p>
            </div>
                <p style='margin: 1rem 0 0.5rem 0; font-size: 1.1rem; color: rgba(255,255,255,0.95); font-weight: 500;'>
                    Emin Eren Sağlam
                </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Created by section - Sol alt
st.markdown("""
    <div style='text-align: left; margin-top: 2rem; padding: 1rem 0;'>
        <p style='font-size: 0.9rem; color: #888; margin: 0;'>
            Created by <a href='https://www.linkedin.com/in/erensglm' target='_blank' 
            style='color: #254D8D; text-decoration: none; font-weight: 600;
                   transition: color 0.3s ease;'>
            Emin Eren Sağlam</a>
        </p>
    </div>
""", unsafe_allow_html=True)

#streamlit run streamlit_app.py

