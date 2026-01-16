import streamlit as st
import os

def check_password():
    """Returns True if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if validate_key(st.session_state["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    def validate_key(input_key):
        try:
            # Check against access_keys.txt
            with open("access_keys.txt", "r") as f:
                allowed_list = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
            return input_key.strip() in allowed_list
        except FileNotFoundError:
            st.error("Arquivo de chaves (access_keys.txt) não encontrado.")
            return False

    if "password_correct" not in st.session_state:
        # First run, show input
        show_login_form(password_entered)
        return False
        
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        show_login_form(password_entered)
        st.error("🚫 Chave de acesso inválida.")
        return False
        
    else:
        # Password correct
        return True

def show_login_form(on_change_callback):
    st.image("https://cdn-icons-png.flaticon.com/512/295/295128.png", width=100)
    st.title("🔐 Acesso Restrito")
    st.markdown("Este sistema é protegido. Insira sua **Chave de Acesso** para continuar.")
    
    st.text_input(
        "Chave de Acesso", 
        type="password", 
        key="password", 
        on_change=on_change_callback,
        help="Solicite sua chave ao administrador."
    )
    st.info("ℹ️ Se você não tem uma chave, contate o suporte.")

def require_login():
    """
    Function to be called at the beginning of every page.
    Stops execution if not logged in.
    """
    if not check_password():
        st.stop()
