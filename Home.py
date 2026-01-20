import streamlit as st
import os
import pandas as pd
import time
from utils import load_history, save_uploaded_file
import styles

st.set_page_config(
    page_title="Contábil Gestão",
    page_icon="📂",
    layout="wide"
)

from auth import check_password

# Apply Styles
styles.apply_custom_css()

# --- LOGIN CHECK ---
if not check_password():
    st.stop()  # Stop if not logged in


# --- HEADER ---
st.title("Olá, Contador")
st.markdown("<p style='color: #64748B; margin-top: -15px; margin-bottom: 30px;'>Gerencie seus arquivos e inicie novos casos.</p>", unsafe_allow_html=True)

# Initialize Session State
if 'current_file_path' not in st.session_state:
    st.session_state['current_file_path'] = None

# Mark Home as Visited
st.session_state['visited_home'] = True

# --- Toast Queue Handler ---
if 'toast_next_run' in st.session_state and st.session_state['toast_next_run']:
    st.toast(st.session_state['toast_next_run'], icon=None)
    st.session_state['toast_next_run'] = None


# --- MAIN UPLOAD SECTION ---
upload_container = st.container()

with upload_container:
    col_up_1, col_up_2, col_up_3 = st.columns([1, 6, 1])
    with col_up_2:
        # Styled Upload Area (via CSS in styles.py)
        st.markdown("### Upload de Arquivos")
        st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.9rem;'>Arraste e solte seus arquivos <b>XLSX</b> ou <b>CSV</b> aqui para iniciar a análise automática.</p>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload Area", # Hidden label by CSS
            type=["xlsx", "csv"],
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            saved_path = save_uploaded_file(uploaded_file)
            if saved_path:
                st.session_state['current_file_path'] = saved_path
                st.toast(f"Arquivo **{uploaded_file.name}** carregado!", icon="✅")
                time.sleep(1)
                st.switch_page("pages/1_Dashboard.py")


st.markdown("---")


# --- NAVIGATION CARDS ---
col_card1, col_card2, col_card3 = st.columns(3)

def card_content(icon, title, desc, link_text):
    return f"""
    <div class="css-card">
        <div style="font-size: 1.5rem; margin-bottom: 10px;">{icon}</div>
        <h3 style="margin: 0; font-size: 1.1rem; color: #0f172a;">{title}</h3>
        <p style="color: #64748B; font-size: 0.9rem; margin: 8px 0 16px 0; min-height: 40px;">{desc}</p>
        <div style="color: #0D9488; font-weight: 600; font-size: 0.9rem; cursor: pointer;">
            {link_text} &rarr;
        </div>
    </div>
    """

with col_card1:
    if st.button("Ir para Editor", key="btn_editor", use_container_width=True):
        st.switch_page("pages/2_Editor_de_Dados.py")
    st.markdown(card_content("📝", "Editor de Dados", "Edite células de planilhas importadas diretamente na plataforma.", "Acessar"), unsafe_allow_html=True)

with col_card2:
    if st.button("Ir para Configurações", key="btn_config", use_container_width=True):
         st.switch_page("pages/3_Configuracoes.py")
    st.markdown(card_content("⚙️", "Configurações", "Ajuste suas preferências de auditoria e regras fiscais.", "Configurar"), unsafe_allow_html=True)

with col_card3:
    if st.button("Conectar Sheets", key="btn_sheets", use_container_width=True):
        st.toast("Integração em breve!", icon="🚧")
    st.markdown(card_content("📊", "Google Sheets", "Conecte sua conta Google para sincronização automática.", "Conectar"), unsafe_allow_html=True)

# Note: The buttons above are invisible overlays or just used for navigation logic if we keep standard buttons. 
# Ideally, we'd make the HTML clickable, but Streamlit restricts JS. 
# workaround: Put a full-width transparent button on top or just use standard buttons below.
# For now, I'll hide the standard buttons with CSS if needed or just leave them as functional links.
# Actually, let's keep it simple: Standard Styled Buttons.


# --- HISTORY SECTION ---
st.markdown("### 🕒 Histórico Recente")
history = load_history()

if history:
    # Convert history to DataFrame for better presentation
    data = []
    for item in history:
        data.append({
            "Nome do Arquivo": item['original_name'],
            "Data de Envio": pd.to_datetime(item['timestamp'], unit='s').strftime('%d/%m/%Y %H:%M'),
            "Caminho": item['path'] # Hidden
        })
    
    df_history = pd.DataFrame(data)
    
    # Display as a dataframe with selection
    # Using data_editor to simulate the "Action" button via selection? 
    # Or just a simple table. Let's use columns for a custom list view to match the design.
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; padding: 10px; background: #F8FAFC; border-radius: 8px 8px 0 0; font-weight: 600; color: #64748B; font-size: 0.85rem;">
        <div>NOME DO ARQUIVO</div>
        <div>DATA DE ENVIO</div>
        <div style="text-align: right;">AÇÃO</div>
    </div>
    """, unsafe_allow_html=True)
    
    for _, row in df_history.iterrows():
        col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
        with col_h1:
            st.markdown(f"**📄 {row['Nome do Arquivo']}**")
        with col_h2:
            st.text(row['Data de Envio'])
        with col_h3:
            if st.button("Abrir", key=f"open_{row['Caminho']}", use_container_width=True):
                if os.path.exists(row['Caminho']):
                    st.session_state['current_file_path'] = row['Caminho']
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    st.error("Arquivo não encontrado.")
        st.markdown("<hr style='margin: 5px 0; border-color: #F1F5F9;'>", unsafe_allow_html=True)

else:
    st.info("Nenhum arquivo processado ainda.")

