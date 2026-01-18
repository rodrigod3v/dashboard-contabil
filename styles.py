import streamlit as st

def apply_custom_css():
    """
    Applies custom CSS styles (Dark/Professional Theme).
    """
    # Static Dark Palette
    main_bg = "#0e1117"
    sec_bg = "#262730"
    text_color = "#fafafa"
    border_color = "#414141"
        
    st.markdown(f"""
    <style>
        /* --- CSS VARIABLES (Streamlit System - FORCED DARK) --- */
        :root {{
            --primary-color: #ff4b4b;
            --background-color: {main_bg};
            --secondary-background-color: {sec_bg};
            --text-color: {text_color};
            --font: sans-serif;
            color-scheme: dark;
        }}
        
        /* --- GLOBAL CONTAINERS --- */
        .stApp {{
            background-color: {main_bg} !important;
            color: {text_color} !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: {sec_bg} !important;
        }}
        
        [data-testid="stHeader"] {{
            background-color: {main_bg} !important;
        }}
        
        /* --- TYPOGRAPHY --- */
        h1, h2, h3, h4, h5, h6, .stMarkdown, p, span, div, label, li, .stToast {{
             color: {text_color} !important;
        }}
        
        /* --- INPUTS & WIDGETS --- */
        /* Text Inputs, Text Areas, Select Boxes */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {{
            color: {text_color} !important;
            background-color: {sec_bg} !important;
            border-color: {border_color} !important;
            border-radius: 12px !important;
        }}
        
        /* Fix Selectbox Dropdown Menu */
        ul[data-baseweb="menu"], div[role="listbox"] {{
            background-color: {sec_bg} !important;
        }}
        
        li[role="option"] {{
             color: {text_color} !important;
             background-color: transparent !important;
        }}
        
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {{
             background-color: {main_bg} !important;
             font-weight: bold;
        }}

        /* Date Input */
        .stDateInput input {{
            border-radius: 12px !important;
            background-color: {sec_bg} !important;
            color: {text_color} !important;
        }}
        
        /* --- DATAFRAMES --- */
        div[data-testid="stDataFrame"] {{
            background-color: {sec_bg} !important;
            border: 1px solid {border_color};
        }}
        div[data-testid="stDataFrame"] div {{
            color: {text_color} !important;
        }}
        
        /* --- BUTTONS --- */
        button[kind="primaryFormSubmit"] {{
            border-radius: 20px !important;
            background-color: #ff4b4b !important;
            border: none !important;
            color: white !important;
        }}
        
        div[data-testid="column"] button[kind="primary"] {{ 
            background-color: #6c5ce7 !important;
            border-radius: 20px !important;
            color: white !important;
        }}
        
        /* --- UTILS --- */
        /* HIDE CALENDAR POPUP (User Preference) */
        div[data-baseweb="calendar"] {{
            display: none !important;
        }}
        
        /* --- HIDE STREAMLIT DEFAULT UI (Clean Look) --- */
        #MainMenu {{visibility: hidden;}}
        .stDeployButton {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stDecoration"] {{display: none;}}
    </style>
    """, unsafe_allow_html=True)
