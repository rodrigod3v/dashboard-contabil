import streamlit as st
import os
import pandas as pd
import time
from utils import load_history, save_uploaded_file

st.set_page_config(
    page_title="Home - Controle Contábil",
    page_icon=None,
    layout="wide"
)


from auth import check_password

# --- LOGIN CHECK ---
if not check_password():
    st.stop()  # Stop if not logged in


st.title("Início")
st.markdown("### Bem-vindo ao Sistema de Controle Contábil")

# Initialize Session State
if 'current_file_path' not in st.session_state:
    st.session_state['current_file_path'] = None

# --- Toast Queue Handler ---
if 'toast_next_run' in st.session_state and st.session_state['toast_next_run']:
    st.toast(st.session_state['toast_next_run'], icon=None)
    st.session_state['toast_next_run'] = None  # Clear after showing

# --- Main Layout ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("Carregar Nova Planilha")
    uploaded_file = st.file_uploader(
        "Selecione um arquivo Excel ou CSV", 
        type=["xlsx", "csv"],
        help="Estrutura esperada: Dia, Quantidade, Inconsistencias, Status, Responsavel"
    )
    
    if uploaded_file is not None:
        saved_path = save_uploaded_file(uploaded_file)
        if saved_path:
            st.session_state['current_file_path'] = saved_path
            st.toast(f"Arquivo **{uploaded_file.name}** carregado com sucesso!", icon="✅")
            
            # Show toast confirmation
            st.toast(f"Arquivo Ativo: {uploaded_file.name}", icon=None)
            st.info("Agora navegue para **Dashboard** ou **Editor de Dados** no menu lateral.")



    # --- Template Download ---
    with st.expander("Precisa de um modelo?"):
        st.write("Baixe a planilha padrão para começar:")
        example_data = {
            'Dia': ['2023-10-01'],
            'Quantidade': [10],
            'Inconsistencias': ['Exemplo de Erro'],
            'Status': ['Pendente'],
            'Responsavel': ['Nome']
        }
        df_example = pd.DataFrame(example_data)
        csv = df_example.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar Modelo CSV", csv, "modelo_dashboard.csv", "text/csv", use_container_width=True)

with col2:
    st.header("Histórico Recente")
    history = load_history()
    
    if not history:
        st.info("Nenhum arquivo no histórico.")
    else:
        for item in history:
            # Clean display name
            name = item['original_name']
            
            col_h1, col_h2 = st.columns([0.7, 0.3])
            with col_h1:
                st.text(f"{name}")
                st.caption(f"Salvo em: {pd.to_datetime(item['timestamp'], unit='s').strftime('%d/%m/%Y %H:%M')}")
            
            with col_h2:
                if st.button("Abrir", key=f"hist_{item['timestamp']}"):
                    if os.path.exists(item['path']):
                        st.session_state['current_file_path'] = item['path']
                        st.toast("Arquivo selecionado!", icon="✅")
                        # Clean name for toast
                        t_name = os.path.basename(item['path'])
                        if "_" in t_name: t_name = t_name.split("_", 1)[-1]
                        
                        # Queue toast for next run
                        st.session_state['toast_next_run'] = f"Arquivo Ativo: {t_name}"
                        st.rerun()
                    else:
                        st.toast("Arquivo não encontrado no cache.", icon="❌")

st.markdown("---")

st.markdown("### Dicas Rápidas")
st.info("**Editor de Dados:** Você pode corrigir erros diretamente na tabela, sem precisar reupar o arquivo.")
st.info("**Configurações:** Adicione novos responsáveis ou status personalizados no menu de Configurações.")
st.info("**Google Sheets:** Integre seu painel com o Google Drive para trabalho colaborativo em tempo real.")
