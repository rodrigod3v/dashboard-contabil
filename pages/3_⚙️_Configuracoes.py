import streamlit as st
import time
from utils import load_options, save_options_file

st.set_page_config(page_title="Configurações", layout="wide")

from auth import require_login
require_login()

st.title("⚙️ Gerenciamento de Opções")
st.markdown("Aqui você pode adicionar ou remover itens das listas suspensas do sistema.")
st.markdown("---")

options = load_options()

# --- Helper Function for CRUD UI ---
def manage_list(title, key, item_name, help_text):
    st.subheader(f"{title}")
    st.markdown(f"*{help_text}*")
    
    current_items = options.get(key, [])
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("#### ➕ Adicionar")
        new_item = st.text_input(f"Novo {item_name}", key=f"add_{key}")
        if st.button(f"Salvar {item_name}", key=f"btn_add_{key}"):
            if new_item:
                if new_item not in current_items:
                    current_items.append(new_item)
                    current_items.sort()
                    options[key] = current_items
                    save_options_file(options)
                    st.success(f"'{new_item}' adicionado com sucesso!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Este item já existe na lista.")
            else:
                st.error("Digite um nome válido.")

    with col2:
        st.markdown("#### 🗑️ Remover")
        if current_items:
            to_remove = st.selectbox(f"Selecione para remover", ["Selecione..."] + current_items, key=f"rem_{key}")
            if st.button(f"Excluir {item_name}", key=f"btn_rem_{key}", type="primary"):
                if to_remove != "Selecione...":
                    current_items.remove(to_remove)
                    options[key] = current_items
                    save_options_file(options)
                    st.success(f"'{to_remove}' removido!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("A lista está vazia.")
    
    with st.expander(f"Ver Lista Completa ({len(current_items)})"):
        st.write(current_items)
    
    st.markdown("---")

# --- CRUD Sections ---
manage_list(
    "👥 Responsáveis", 
    "responsavel", 
    "Responsável", 
    "Nomes dos colaboradores que aparecem no filtro e na edição."
)

manage_list(
    "⚠️ Tipos de Inconsistências", 
    "inconsistencias", 
    "Inconsistência", 
    "Categorias de erros para classificação."
)

manage_list(
    "📌 Status do Processo", 
    "status", 
    "Status", 
    "Etapas do fluxo de trabalho (ex: Pendente, Resolvido)."
)
