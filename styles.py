import streamlit as st

def apply_custom_css():
    """
    Applies the official Dark/Professional Theme CSS.
    Centralizes all styling, colors, and UI overrides.
    """
    # --- CONSTANTS: LIGHT THEME PALETTE ---
    MAIN_BG = "#FFFFFF"
    SEC_BG = "#F8FAFC"
    TEXT_COLOR = "#334155" # Slate 700
    HEADER_COLOR = "#0f172a" # Slate 900
    ACCENT_COLOR = "#0D9488" # Teal 600
    BORDER_COLOR = "#E2E8F0" # Slate 200
        
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* =========================================
           1. CORE VARIABLES & THEME SETUP
           ========================================= */
        :root {{
            --primary-color: {ACCENT_COLOR};
            --background-color: {MAIN_BG};
            --secondary-background-color: {SEC_BG};
            --text-color: {TEXT_COLOR};
            --font: "Inter", sans-serif;
        }}

        /* =========================================
           2. GLOBAL CONTAINERS & LAYOUT
           ========================================= */
        .stApp {{
            background-color: {MAIN_BG} !important;
            color: {TEXT_COLOR} !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: {SEC_BG} !important;
            border-right: 1px solid {BORDER_COLOR};
        }}
        
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}

        /* =========================================
           3. TYPOGRAPHY
           ========================================= */
        h1, h2, h3, h4, h5, h6 {{
             color: {HEADER_COLOR} !important;
             font-family: 'Inter', sans-serif !important;
             font-weight: 700 !important;
        }}
        
        .stMarkdown, p, span, div, label, li, 
        .stToast, .stAlert {{
             color: {TEXT_COLOR} !important;
             font-family: 'Inter', sans-serif !important;
        }}
        
        /* Titles */
        h1 {{
            font-size: 2.25rem !important; /* 36px */
            letter-spacing: -0.025em;
        }}

        /* =========================================
           4. COMPONENTS & CARDS
           ========================================= */
           
        /* Custom Card Style for KPIs and Sections */
        .css-card {{
            background-color: white;
            border: 1px solid {BORDER_COLOR};
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        }}
           
        /* Upload Area Style */
        [data-testid="stFileUploader"] {{
            padding: 2rem;
            border: 2px dashed {ACCENT_COLOR};
            border-radius: 12px;
            background-color: #F0FDFA; /* Light Teal bg */
            text-align: center;
        }}
        
        [data-testid="stFileUploader"] section {{
            background-color: transparent !important;
        }}

        /* =========================================
           5. FORM INPUTS & WIDGETS
           ========================================= */
           
        /* Inputs */
        .stTextInput input, 
        .stNumberInput input,
        .stDateInput input,
        .stTextArea textarea, 
        .stSelectbox div[data-baseweb="select"] > div {{
            color: {TEXT_COLOR} !important;
            background-color: white !important;
            border: 1px solid {BORDER_COLOR} !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }}
        
        /* Focus State */
        .stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus {{
            border-color: {ACCENT_COLOR} !important;
            box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.2) !important;
        }}
        
        /* Menus/Dropdowns */
        ul[data-baseweb="menu"], div[role="listbox"] {{
            background-color: white !important;
            border: 1px solid {BORDER_COLOR} !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }}
        
        li[role="option"] {{
             color: {TEXT_COLOR} !important;
        }}
        
        /* Selected Option */
        li[role="option"][aria-selected="true"] {{
             background-color: #F0FDFA !important; /* Light Teal */
             color: {ACCENT_COLOR} !important;
             font-weight: 600;
        }}

        /* =========================================
           6. INTERACTIVE ELEMENTS (BUTTONS)
           ========================================= */
           
        /* Primary Action Buttons */
        button[kind="primaryFormSubmit"], 
        button[kind="primary"] {{
            background-color: {ACCENT_COLOR} !important;
            border: none !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 500 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease;
        }}
        
        button[kind="primary"]:hover {{
            background-color: #0F766E !important; /* Darker Teal */
            box-shadow: 0 4px 6px -1px rgba(13, 148, 136, 0.3);
        }}
        
        /* Secondary Buttons */
        button[kind="secondary"] {{
            background-color: white !important;
            border: 1px solid {BORDER_COLOR} !important;
            color: {TEXT_COLOR} !important;
            border-radius: 8px !important;
        }}

        /* =========================================
           7. TABLES & DATAFRAMES
           ========================================= */
        div[data-testid="stDataFrame"] {{
            border: 1px solid {BORDER_COLOR};
            border-radius: 8px;
            overflow: hidden;
        }}
        
        /* Header cells */
        div[data-testid="stDataFrame"] [role="columnheader"] {{
            background-color: #F8FAFC !important;
            color: {HEADER_COLOR} !important;
            font-weight: 600 !important;
        }}

        /* =========================================
           8. UTILITIES
           ========================================= */
        #MainMenu {{visibility: hidden;}}
        .stDeployButton {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
    </style>
    """, unsafe_allow_html=True)
