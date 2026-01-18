import streamlit as st

def apply_custom_css():
    """
    Applies the official Dark/Professional Theme CSS.
    Centralizes all styling, colors, and UI overrides.
    """
    # --- CONSTANTS: DARK THEME PALETTE ---
    MAIN_BG = "#0e1117"
    SEC_BG = "#262730"
    TEXT_COLOR = "#fafafa"
    BORDER_COLOR = "#414141"
    ACCENT_COLOR = "#ff4b4b"
        
    st.markdown(f"""
    <style>
        /* =========================================
           1. CORE VARIABLES & THEME SETUP
           ========================================= */
        :root {{
            --primary-color: {ACCENT_COLOR};
            --background-color: {MAIN_BG};
            --secondary-background-color: {SEC_BG};
            --text-color: {TEXT_COLOR};
            --font: "Source Sans Pro", sans-serif;
            color-scheme: dark; /* Force Browser Primitives to Dark Mode */
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
            background-color: {MAIN_BG} !important;
        }}

        /* =========================================
           3. TYPOGRAPHY
           ========================================= */
        h1, h2, h3, h4, h5, h6, 
        .stMarkdown, p, span, div, label, li, 
        .stToast, .stAlert {{
             color: {TEXT_COLOR} !important;
        }}
        
        /* =========================================
           4. FORM INPUTS & WIDGETS
           ========================================= */
           
        /* General Inputs (Text, Number, Date, Area) */
        .stTextInput input, 
        .stNumberInput input,
        .stDateInput input,
        .stTextArea textarea, 
        .stSelectbox div[data-baseweb="select"] > div {{
            color: {TEXT_COLOR} !important;
            background-color: {SEC_BG} !important;
            border: 1px solid {BORDER_COLOR} !important;
            border-radius: 8px !important;
        }}
        
        /* Selectbox Popovers (Menus) */
        ul[data-baseweb="menu"], div[role="listbox"] {{
            background-color: {SEC_BG} !important;
            border: 1px solid {BORDER_COLOR} !important;
        }}
        
        /* Dropdown Options */
        li[role="option"] {{
             color: {TEXT_COLOR} !important;
             background-color: transparent !important;
        }}
        
        /* Option Hover/Selection State */
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {{
             background-color: {MAIN_BG} !important;
             font-weight: 600;
        }}
        
        /* Input Labels */
        .stTextInput label, .stSelectbox label, .stDateInput label {{
            color: {TEXT_COLOR} !important;
            font-size: 0.9rem !important;
        }}

        /* =========================================
           5. DATA REPRESENTATION (TABLES/DATAFRAMES)
           ========================================= */
        div[data-testid="stDataFrame"] {{
            background-color: {SEC_BG} !important;
            border: 1px solid {BORDER_COLOR};
            border-radius: 8px;
        }}
        
        div[data-testid="stDataFrame"] div {{
            color: {TEXT_COLOR} !important;
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
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease;
        }}
        
        button[kind="primary"]:hover {{
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
        }}
        
        /* Secondary/Normal Buttons */
        button[kind="secondary"] {{
            background-color: {SEC_BG} !important;
            border: 1px solid {BORDER_COLOR} !important;
            color: {TEXT_COLOR} !important;
            border-radius: 8px !important;
        }}

        /* =========================================
           7. UTILITIES & CLEANUP
           ========================================= */
           
        /* Hide DatePicker Portal (Calendar Popup) - Optional Preference */
        div[data-baseweb="calendar"] {{
            display: none !important;
        }}
        
        /* Hide Streamlit Native UI Elements */
        #MainMenu {{visibility: hidden;}}
        .stDeployButton {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stDecoration"] {{display: none;}}
        
    </style>
    """, unsafe_allow_html=True)
