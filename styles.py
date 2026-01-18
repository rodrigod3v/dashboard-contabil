import streamlit as st

def apply_custom_css():
    """
    Applies custom CSS styles to the Streamlit app.
    Call this function at the beginning of the page render.
    """
    st.markdown("""
    <style>
        /* Rounded Inputs */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stDateInput input {
            border-radius: 12px !important;
        }
        
        /* Buttons Colors */
        button[kind="primaryFormSubmit"] {
            border-radius: 20px !important;
            background-color: #ff4b4b !important; /* Secondary Color for Add to List */
            border: none !important;
        }
        
        div[data-testid="column"] button[kind="primary"] { 
            /* Targetting the 'Save All' button outside form */
            background-color: #6c5ce7 !important; /* Purple for Save All */
            border-radius: 20px !important;
        }
        
        /* Dark Mode Contrast Improvements */
        .stMarkdown h3 {
            color: #e0e0e0 !important;
        }

        /* HIDE CALENDAR POPUP */
        div[data-baseweb="calendar"] {
            display: none !important;
        }
        div[data-baseweb="popover"] > div {
             /* This runs a risk of hiding selectbox popovers if they share structure, 
                but usually calendar is distinct. 
                Let's stick to 'calendar' attribute which BaseWeb uses. */
        }
    </style>
    """, unsafe_allow_html=True)
