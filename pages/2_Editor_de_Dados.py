import streamlit as st
import pandas as pd
import os
import time
import json
from datetime import date
from dateutil.relativedelta import relativedelta
from utils import load_data, load_options, save_options_file, save_settings, load_settings, SETTINGS_FILE

st.set_page_config(page_title="Gestão de Ocorrências", layout="wide")

from auth import require_login
require_login()

st.title("Gestão de Ocorrências")


# --- Session Management ---
if 'current_file_path' not in st.session_state or not st.session_state['current_file_path']:
    st.info("Nenhuma planilha carregada. Vá para a **Página Inicial** para começar.")
    st.stop()
    
file_path = st.session_state['current_file_path']
if not os.path.exists(file_path):
    st.error("Arquivo não encontrado. Recarregue na Home.")
    st.session_state['current_file_path'] = None
    st.stop()

# Load Data
df = load_data(file_path)
if df is None:
    st.stop()

# --- Options Management ---
saved_options = load_options()
current_resp = list(df['Responsavel'].unique()) if 'Responsavel' in df.columns else []
current_inc = list(df['Inconsistencias'].unique()) if 'Inconsistencias' in df.columns else []

all_responsaveis = sorted(list(set(saved_options.get("responsavel", []) + current_resp + ["Outro"])))
all_inconsistencias = sorted(list(set(saved_options.get("inconsistencias", []) + current_inc + ["Outro"])))
all_status = sorted(list(set(saved_options.get("status", ['Pendente', 'Resolvido', 'Em Análise', 'Cancelado']))))

# --- Data Editor Config ---
# --- Layout Containers ---
table_container = st.container()
bulk_container = st.container()

# --- Data Editor Config ---
today = date.today()
min_date = today - relativedelta(years=1) # 1 Year window logic

column_cfg = {
    "Dia": st.column_config.DateColumn(
        "Dia",
        format="DD/MM/YYYY",
        min_value=min_date, 
        max_value=today,
        help="Data da ocorrência (Últimos 2 meses)",
        width="medium",
        required=True
    ),
    "Quantidade": st.column_config.TextColumn(
        "Quantidade",
        help="Máximo 5 dígitos",
        width="small",
        max_chars=5,
        validate=r"^\d{1,5}$",
        required=True
    ),
    "Inconsistencias": st.column_config.SelectboxColumn(
        "Inconsistências",
        options=all_inconsistencias,
        width="large",
        required=True
    ),
    "Status": st.column_config.SelectboxColumn(
        "Status",
        options=all_status,
        width="medium",
        required=True
    ),
    "Responsavel": st.column_config.SelectboxColumn(
        "Responsável",
        options=all_responsaveis,
        width="medium",
        required=True
    ),
    "Selecionar": st.column_config.CheckboxColumn(
        "Selecionar",
        help="Selecione para edição em lote",
        default=False,
        width="small"
    )
}


# --- Entry Dialog Logic ---
# --- Entry Dialog Logic ---
# --- Entry Dialog Logic ---
# --- Filter Logic Helper ---
def render_filters(df_input):
    with st.expander("Filtros & Pesquisa", expanded=False):
        # Search Bar
        search_term = st.text_input("Buscar (Nome, etc...)", placeholder="Digite para filtrar...")
        
        # Filter Columns
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_resp = st.multiselect("Responsável", all_responsaveis)
        with col_f2:
            f_status = st.multiselect("Status", all_status)
        f_inc = st.multiselect("Inconsistência", all_inconsistencias)


        rows_to_show = st.slider("Linhas Visíveis (Rolagem)", min_value=5, max_value=100, value=15, step=5)
        
    # Apply Logic
    df_out = df_input.copy()
    if search_term:
        mask = df_out.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        df_out = df_out[mask]
        
    if f_resp and 'Responsavel' in df_out.columns:
        df_out = df_out[df_out['Responsavel'].isin(f_resp)]
    if f_status and 'Status' in df_out.columns:
        df_out = df_out[df_out['Status'].isin(f_status)]
    if f_inc and 'Inconsistencias' in df_out.columns:
        df_out = df_out[df_out['Inconsistencias'].isin(f_inc)]
        
    return df_out, rows_to_show

@st.dialog("Registrar Ocorrência", width="large")
def entry_form():
    if "pending_entries" not in st.session_state:
        st.session_state["pending_entries"] = []

    # --- Custom CSS Injection ---
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

    st.caption("Adicione vários registros e clique em 'Salvar Todos' ao final.")

    # Form to add to queue
    with st.form("new_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            new_dia = st.date_input("Data do Ocorrido", value=None, format="DD/MM/YYYY")
            new_qtd = st.text_input("Quantidade", max_chars=5, help="Máximo 5 dígitos")
            new_resp = st.selectbox("Responsável", all_responsaveis, index=None, placeholder="Selecione...")
            
        with col2:
            new_inc = st.selectbox("Inconsistência", all_inconsistencias, index=None, placeholder="Selecione...")
            new_stat = st.selectbox("Status", all_status, index=None, placeholder="Selecione...")
            

        
        # This button just adds to the list
        added = st.form_submit_button("Adicionar à Fila", type="primary", use_container_width=True)
        
        if added:
            # Validation
            if not new_dia:
                st.toast("A data é obrigatória.", icon="❌")
            elif not new_qtd or not new_qtd.isdigit():
                st.toast("A quantidade deve ser um número válido.", icon="❌")
            elif not new_resp:
                st.toast("O responsável é obrigatório.", icon="❌")
            elif not new_inc:
                st.toast("A inconsistência é obrigatória.", icon="❌")
            elif not new_stat:
                st.toast("O status é obrigatório.", icon="❌")
            else:
                entry = {
                    'Dia': new_dia,
                    'Quantidade': new_qtd,
                    'Inconsistencias': new_inc,
                    'Status': new_stat,
                    'Responsavel': new_resp
                }
                st.session_state["pending_entries"].append(entry)
                st.toast("Registro adicionado à fila!", icon=None)
                # Removed explicit rerun to avoid closing dialog

    # Layout for Pending Items (Buffer)
    if st.session_state["pending_entries"]:
        st.markdown("### Fila de Processamento")
        st.caption("Você pode editar ou excluir linhas aqui antes de salvar.")
        
        # Convert to DF for valid display
        df_pending = pd.DataFrame(st.session_state["pending_entries"])
        
        # Data Editor implementation
        edited_buffer = st.data_editor(
            df_pending,
            key="buffer_editor",
            num_rows="dynamic", # Allow add/delete
            use_container_width=True,
            column_config={
                "Dia": st.column_config.DateColumn("Dia", format="DD/MM/YYYY"),
                "Quantidade": st.column_config.TextColumn("Qtd", max_chars=5),
            }
        )
        
        col_actions = st.columns([1, 1])
        if col_actions[0].button("Limpar Fila"):
            st.session_state["pending_entries"] = []
            st.rerun()
            
        if col_actions[1].button("Salvar Todos e Finalizar", type="primary"):
            if edited_buffer.empty:
                st.toast("A fila está vazia.", icon="⚠️")
            else:
                try:
                    # Sync buffer edits back to logic
                    final_entries = edited_buffer.to_dict('records')
                    df_new = pd.DataFrame(final_entries)
                    
                    # Append locally to df
                    for col in df.columns:
                        if col not in df_new.columns:
                            df_new[col] = None 
                    
                    # Update main DF
                    updated_df = pd.concat([df, df_new], ignore_index=True)
                    
                    # Save to file
                    if file_path.endswith('.csv'):
                        updated_df.to_csv(file_path, index=False)
                    else:
                        writer_df = updated_df.copy()
                        if 'Dia' in writer_df.columns:
                            writer_df['Dia'] = pd.to_datetime(writer_df['Dia']).dt.date
                        writer_df.to_excel(file_path, index=False)
                    
                    st.toast(f"{len(df_new)} registros salvos com sucesso!", icon=None)
                    st.session_state["pending_entries"] = [] 
                    time.sleep(1.5) # Time to see the toast
                    st.rerun()
                    
                except Exception as e:
                    st.toast(f"Erro ao salvar: {e}", icon="❌")

with table_container:


    # --- Toolbar (Mode & Add) ---
    col_toolbar_1, col_toolbar_2 = st.columns([0.65, 0.35], gap="small")
    
    with col_toolbar_1:
         view_mode = st.radio("Modo de Interação", ["Modo Seleção", "Modo Individual"], horizontal=True, label_visibility="collapsed")
         
    with col_toolbar_2:
         if st.button("➕ Nova Ocorrência", type="primary", use_container_width=True):
             entry_form()

    selected_indices = []

    if view_mode == "Modo Seleção":
        # NATIVE SELECTION MODE
        st.info("⚠️ **Modo de Edição em Massa:** Selecione as linhas para edição em massa.")
        
        # Render Filters HERE (Below Balloon)
        df_filtered, rows_to_show = render_filters(df)
        
        # Prepare View
        df_editor_view = df_filtered.copy()
        if 'Quantidade' in df_editor_view.columns:
            df_editor_view['Quantidade'] = df_editor_view['Quantidade'].astype(str)
        if 'Dia' in df_editor_view.columns:
            df_editor_view['Dia'] = pd.to_datetime(df_editor_view['Dia']).dt.date
        
        # Configure columns for View
        view_config = column_cfg.copy()
        if "Selecionar" in view_config: del view_config["Selecionar"] # Remove checkbox config if present
        
        event = st.dataframe(
            df_editor_view,
            use_container_width=True,
            column_config=view_config,
            height=(rows_to_show * 35) + 38,
            on_select="rerun",
            selection_mode="multi-row",
            hide_index=True
        )
        
        if len(event.selection.rows) > 0:
            selected_indices = df_editor_view.iloc[event.selection.rows].index
            
        edited_df = df_editor_view # For reference in export, though not edited

    else:
        # CELL EDIT MODE
        st.warning("⚠️ **Modo de Edição Individual:** Clique no campo para editá-lo.")
        
        # Render Filters HERE (Below Balloon)
        df_filtered, rows_to_show = render_filters(df)
        
        # Prepare View
        df_editor_view = df_filtered.copy()
        if 'Quantidade' in df_editor_view.columns:
            df_editor_view['Quantidade'] = df_editor_view['Quantidade'].astype(str)
        if 'Dia' in df_editor_view.columns:
            df_editor_view['Dia'] = pd.to_datetime(df_editor_view['Dia']).dt.date
        
        # No 'Selecionar' column in this mode
        
        edited_df = st.data_editor(
            df_editor_view,
            use_container_width=True,
            column_config=column_cfg,
            num_rows="dynamic",
            key="editor_main",
            height=(rows_to_show * 35) + 38
        )
        
        # No bulk selection in this mode
        selected_indices = []

    # --- Save Logic (Only needed in Edit Mode) ---
    # --- Save Logic (Only needed in Individual Mode) ---
    if view_mode == "Modo Individual":
        if st.button("💾 Salvar Alterações Manuais", type="primary", use_container_width=True):
            try:
                # Prepare processed edited dataframe
                processed_edited = edited_df.copy()
                if 'Quantidade' in processed_edited.columns:
                    processed_edited['Quantidade'] = pd.to_numeric(processed_edited['Quantidade'], errors='ignore')
                if 'Dia' in processed_edited.columns:
                    processed_edited['Dia'] = pd.to_datetime(processed_edited['Dia'])
                    
                # Update logic:
                # 1. Update existing rows (intersection of indices)
                common_indices = processed_edited.index.intersection(df.index)
                if not common_indices.empty:
                    df.loc[common_indices] = processed_edited.loc[common_indices]
                    
                # 2. Add new rows (indices in edited but not in original)
                new_indices = processed_edited.index.difference(df.index)
                if not new_indices.empty:
                    new_rows = processed_edited.loc[new_indices]
                    df = pd.concat([df, new_rows])
                    
                # Write to disk
                if file_path.endswith('.csv'):
                    df.to_csv(file_path, index=False)
                else:
                    writer_df = df.copy()
                    if 'Dia' in writer_df.columns:
                        writer_df['Dia'] = pd.to_datetime(writer_df['Dia']).dt.date
                    writer_df.to_excel(file_path, index=False)
                    
                st.toast("Dados salvos com sucesso!", icon="✅")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.toast(f"Erro ao salvar: {e}", icon="❌")

# --- Bulk Edit Logic (Works for both modes) ---
with bulk_container:
    if view_mode == "Modo Seleção":
        num_selected = len(selected_indices)
        bulk_label = f"✏️ Edição em Lote ({num_selected} Selecionados)" if num_selected > 0 else "✏️ Edição em Lote"
        
        with st.expander(bulk_label, expanded=(num_selected > 0)):
            
            if num_selected > 0:
                c_bulk_1, c_bulk_2, c_bulk_3 = st.columns(3)
                
                with c_bulk_1:
                    use_resp = st.checkbox("Alterar Responsável")
                    val_resp = st.selectbox("Novo Responsável", all_responsaveis, disabled=not use_resp)
                    
                with c_bulk_2:
                    use_stat = st.checkbox("Alterar Status")
                    val_stat = st.selectbox("Novo Status", all_status, disabled=not use_stat)
                    
                with c_bulk_3:
                    use_inc = st.checkbox("Alterar Inconsistência")
                    val_inc = st.selectbox("Nova Inconsistência", all_inconsistencias, disabled=not use_inc)
                    
                col_b1, col_b2 = st.columns([0.75, 0.25], gap="small")
                
                with col_b1:
                    if st.button(f"Aplicar aos {num_selected} selecionados", type="primary", use_container_width=True):
                        try:
                            # Apply changes directly to Main DF based on selected_indices
                            updates_made = False
                            
                            if use_resp:
                                df.loc[selected_indices, 'Responsavel'] = val_resp
                                updates_made = True
                            if use_stat:
                                df.loc[selected_indices, 'Status'] = val_stat
                                updates_made = True
                            if use_inc:
                                df.loc[selected_indices, 'Inconsistencias'] = val_inc
                                updates_made = True
                                
                            if updates_made:
                                # Save logic
                                if file_path.endswith('.csv'):
                                    df.to_csv(file_path, index=False)
                                else:
                                    writer_df = df.copy()
                                    if 'Dia' in writer_df.columns:
                                        writer_df['Dia'] = pd.to_datetime(writer_df['Dia']).dt.date
                                    writer_df.to_excel(file_path, index=False)
                                    
                                st.toast(f"{num_selected} registros atualizados com sucesso!", icon="✅")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.toast("Nenhum campo selecionado para alteração.", icon="⚠️")
                        except Exception as e:
                             st.toast(f"Erro na edição em lote: {e}", icon="❌")

                with col_b2:
                    if st.button(f"🗑️ Excluir", type="secondary", use_container_width=True):
                         try:
                            df.drop(selected_indices, inplace=True)
                            
                            # Save logic
                            if file_path.endswith('.csv'):
                                df.to_csv(file_path, index=False)
                            else:
                                writer_df = df.copy()
                                if 'Dia' in writer_df.columns:
                                    writer_df['Dia'] = pd.to_datetime(writer_df['Dia']).dt.date
                                writer_df.to_excel(file_path, index=False)
                            
                            st.toast(f"{num_selected} registros excluídos!", icon="✅")
                            time.sleep(1)
                            st.rerun()
                         except Exception as e:
                            st.toast(f"Erro ao excluir: {e}", icon="❌")
                        
            else:
                st.write("Clique nas linhas da tabela acima para selecionar.")


# --- Export Section ---



col_dl, col_gs = st.columns([1, 1], gap="medium")

# --- Column 1: Local & Help ---
with col_dl:
    with st.container(border=True):
        st.subheader("Local e Ajuda")
        
        with open(file_path, "rb") as f:
            file_data = f.read()
                
        file_name = os.path.basename(file_path)
        clean_name = file_name.split("_", 1)[-1] if "_" in file_name else file_name
        mime_type = "text/csv" if file_name.endswith(".csv") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        st.download_button(
            label="Baixar Arquivo Atualizado",
            data=file_data,
            file_name=f"EDITADO_{clean_name}",
            mime=mime_type,
            use_container_width=True
        )


        st.subheader("Central de Ajuda")

        with st.expander("Como Configurar o \"Robô\" do Google (Google Sheets API)"):
            st.markdown("""
            Para usar o botão **"Enviar para Google Sheets"**, você precisa de um arquivo `credentials.json` gratuito.

            1. Acesse o **[Google Cloud Console](https://console.cloud.google.com/)**.
            2. Na barra azul do topo, clique no nome do projeto atual e depois em **"Novo Projeto"**. Dê o nome de *Dashboard Contabil*.
            3. Vá no menu **APIs e Serviços > Biblioteca**.
            4. Pesquise e ative duas APIs (uma de cada vez):
               - **Google Sheets API**
               - **Google Drive API** (Essencial para contornar erros de cota).
            5. Vá em **APIs e Serviços > Credenciais**.
            6. Clique em **Criar Credenciais > Conta de Serviço**.
            7. Dê um nome (ex: `robo-planilha`) e clique em **Criar e Continuar**.
            8. Pode pular as etapas opcionais clicando em **Concluir**.
            9. Na lista de contas, clique no e-mail do robô recém-criado (ex: `robo-planilha@...iam.gserviceaccount.com`).
            10. Vá na aba **Chaves** > **Adicionar Chave** > **Criar nova chave** > **JSON**.
            11. O download começará. **Renomeie esse arquivo para `credentials.json`** e coloque na pasta do projeto (ou faça upload pelo painel).
            """)

        with st.expander("Solução de Erros Comuns"):
            st.markdown("""
            **Erro 403: "Storage quota exceeded"**
            Geralmente é falta de permissão.
            1. Crie uma planilha no **seu** Google Planilhas.
            2. Compartilhe com o **e-mail do robô** (veja no arquivo JSON).
            3. No painel ao lado, use o **mesmo nome** da planilha.

            **"Não salvou no meu PC"**
            O navegador não edita seu arquivo local (`C:\...`).
            - Use o botão **"Baixar Arquivo Atualizado"** acima para salvar uma cópia.
            """)

        with st.expander("Dicas de Uso e Atalhos"):
            st.markdown("""
            **Atalhos do Editor**
            - **Enter**: Salva e vai para a linha de baixo.
            - **Delete**: Limpa a célula selecionada.
            - **Duplo Clique**: Edita a célula (Texto/Número).

            **� Regras para Manter o Layout**
            - **Datas**: Permitido até **1 ano atrás** (Evite datas muito antigas).
            - **Quantidade**: Máximo de **5 dígitos** (99.999).
            - **Textos**: Use nomes curtos em "Responsável" e "Status" para evitar que a tabela fique muito larga.
            """)

# --- Column 2: Google Sheets ---
with col_gs:
    with st.container(border=True):
        st.subheader("Google Sheets")
        
        creds_file = "credentials.json"
        if not os.path.exists(creds_file):
            st.warning("Arquivo de credenciais (`.json`) não encontrado.")
            uploaded_creds = st.file_uploader("Faça upload do arquivo de chaves do Google (JSON)", type="json", key="creds_up")
            if uploaded_creds is not None:
                with open(creds_file, "wb") as f:
                    f.write(uploaded_creds.getbuffer())
                st.success("Credenciais salvas! Recarregando...")
                time.sleep(1)
                st.rerun()
        else:
            st.success("Credenciais (`credentials.json`) detectadas.")
            
            with st.expander("Trocar Arquivo de Credenciais"):
                 started_creds = st.file_uploader("Substituir arquivo JSON", type="json", key="creds_replace")
                 if started_creds is not None:
                    with open(creds_file, "wb") as f:
                        f.write(started_creds.getbuffer())
                    st.success("Credenciais atualizadas! Recarregando...")
                    time.sleep(1)
                    st.rerun()

            saved_settings = load_settings()
            default_sheet = saved_settings.get("sheet_name", "")
            default_email = saved_settings.get("email_share", "")

            sheet_name = st.text_input("Nome da Planilha (Google Sheets)", value=default_sheet)
            email_share = st.text_input("Seu E-mail Google", value=default_email)
            
            if st.button("Enviar para Nuvem", use_container_width=True):
                if not sheet_name or not email_share:
                    st.error("Preencha todos os campos.")
                else:
                    save_settings(sheet_name, email_share)
                    try:
                        import gspread
                        from oauth2client.service_account import ServiceAccountCredentials
                        
                        with st.spinner("Sincronizando..."):
                            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
                            client = gspread.authorize(creds)
                            
                            try:
                                sh = client.open(sheet_name)
                            except:
                                sh = client.create(sheet_name)
                                sh.share(email_share, perm_type='user', role='writer')
                            
                            ws = sh.get_worksheet(0)
                            ws.clear()
                            
                            # Prepare data for upload (ensure strings)
                            df_upload = edited_df.copy().astype(str)
                            ws.update([df_upload.columns.values.tolist()] + df_upload.values.tolist())
                            
                            st.success(f"Sucesso! Acesse sua planilha no Drive: {email_share}")
                            st.balloons()
                    except Exception as e:
                        st.error(f"Erro na integração: {e}")


