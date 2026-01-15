import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
import time

# Configuração da Página
st.set_page_config(page_title="Dashboard Contábil", layout="wide")

CACHE_DIR = "cache_data"
HISTORY_FILE = "upload_history.json"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def save_uploaded_file(uploaded_file):
    # Salva o arquivo fisicamente
    ext = os.path.splitext(uploaded_file.name)[1]
    if not ext:
        ext = ".csv" if uploaded_file.type == 'text/csv' else ".xlsx"
    
    # Nome único para evitar conflito
    filename = f"{int(time.time())}_{uploaded_file.name}"
    file_path = os.path.join(CACHE_DIR, filename)

    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Atualiza histórico
        history = load_history()
        # Remove duplicatas de nome se houver (mantendo o mais recente)
        history = [h for h in history if h['original_name'] != uploaded_file.name]
        
        # Adiciona no topo
        history.insert(0, {
            "path": file_path,
            "original_name": uploaded_file.name,
            "timestamp": time.time()
        })
        
        # Mantém apenas os 3 últimos
        # Opcional: deletar arquivos físicos removidos do histórico
        if len(history) > 3:
            removed = history.pop()
            if os.path.exists(removed['path']):
                try:
                    os.remove(removed['path'])
                except:
                    pass
        
        save_history(history)
        return file_path
    except Exception as e:
        st.error(f"Erro ao salvar cache: {e}")
        return None

def load_data(file_input):
    try:
        # Se for string (caminho do arquivo), abre o arquivo
        if isinstance(file_input, str):
            if file_input.endswith('.csv'):
                df = pd.read_csv(file_input)
            else:
                df = pd.read_excel(file_input)
        # Se for buffer (File Uploader)
        else:
            if file_input.name.endswith('.csv'):
                df = pd.read_csv(file_input)
            else:
                df = pd.read_excel(file_input)
        
        # Normalização básica
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None

def main():
    st.title("📊 Dashboard de Controle Contábil")
    st.markdown("---")

    # Inicializa variavel de sessão para caminho atual
    if 'current_file_path' not in st.session_state:
        st.session_state['current_file_path'] = None
    
    # Inicializa chave do uploader para permitir reset
    if 'uploader_key' not in st.session_state:
        st.session_state['uploader_key'] = 0

    # Sidebar para Upload e Controle
    with st.sidebar:
        st.header("📂 Carregar Dados")
        # Usa a chave dinâmica para forçar reset quando necessário
        uploaded_file = st.file_uploader(
            "Insira sua planilha", 
            type=["xlsx", "csv"], 
            help="Arraste ou selecione seu arquivo Excel/CSV",
            key=f"uploader_{st.session_state['uploader_key']}"
        )
        
        st.markdown("---")
        
        # Histórico na Sidebar
        st.markdown("### 🕒 Histórico Recente")
        history = load_history()
        
        if not history:
            st.caption("Nenhum arquivo recente.")
        else:
            for item in history:
                col_hist1, col_hist2 = st.columns([0.85, 0.15])
                with col_hist1:
                    # Botão com nome do arquivo original
                    if st.button(f"📄 {item['original_name']}", key=f"btn_{item['timestamp']}", use_container_width=True):
                        st.session_state['current_file_path'] = item['path']
                        # Incrementa chave do uploader para limpar o campo de upload e evitar conflito
                        st.session_state['uploader_key'] += 1
                        st.rerun()
                
    
    df = None
    
    # Lógica de Carga dos Dados
    # Prioridade 1: Novo Upload (sempre sobrescreve a visão atual)
    if uploaded_file is not None:
        saved_path = save_uploaded_file(uploaded_file)
        st.session_state['current_file_path'] = saved_path
        df = load_data(saved_path)
    
    # Prioridade 2: Arquivo selecionado da sessão (histórico)
    elif st.session_state['current_file_path'] and os.path.exists(st.session_state['current_file_path']):
        df = load_data(st.session_state['current_file_path'])
        # Mostra qual arquivo está sendo visualizado
        with st.sidebar:
            st.success(f"Visualizando: **{os.path.basename(st.session_state['current_file_path']).split('_', 1)[-1]}**")
            if st.button("Fechar Arquivo", use_container_width=True):
                st.session_state['current_file_path'] = None
                st.rerun()

    # Caso arquivo da sessão tenha sido deletado externamente
    elif st.session_state['current_file_path']:
         st.session_state['current_file_path'] = None
         st.rerun()

    # Se temos dados carregados...
    if df is not None:
        # --- Validação de Estrutura ---
        required_columns = ['Dia', 'Quantidade', 'Inconsistencias', 'Status', 'Responsavel']
        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            st.error("⚠️ Estrutura de Arquivo Inválida")
            st.warning(f"Faltam as colunas: **{', '.join(missing_cols)}**")
            with st.expander("Ver dados carregados"):
                 st.dataframe(df.head())
        else:
            # --- Pré-processamento ---
            try:
                # Converte para datetime para ordenação e filtro
                df['Dia'] = pd.to_datetime(df['Dia'])
            except:
                st.sidebar.error("Erro ao processar datas na coluna 'Dia'.")

            # Ordenação de colunas
            cols_order = ['Dia', 'Quantidade', 'Inconsistencias', 'Status', 'Responsavel']
            other_cols = [c for c in df.columns if c not in cols_order]
            df = df[cols_order + other_cols]

            # --- Filtros (Sidebar) ---
            with st.sidebar:
                st.header("🔍 Filtros")
                responsaveis = ['Todos'] + list(df['Responsavel'].unique())
                selected_resp = st.selectbox("Responsável", responsaveis)

                statuses = ['Todos'] + list(df['Status'].unique())
                selected_status = st.selectbox("Status", statuses)

            # --- Aplicação dos Filtros ---
            df_filtered = df.copy()
            if selected_resp != 'Todos':
                df_filtered = df_filtered[df_filtered['Responsavel'] == selected_resp]
            if selected_status != 'Todos':
                df_filtered = df_filtered[df_filtered['Status'] == selected_status]

            # --- Dashboard Principal ---
            st.markdown("### 📈 Visão Geral")
            
            # KPIs em container
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                
                total_qtd = df_filtered['Quantidade'].sum() if 'Quantidade' in df_filtered.columns and pd.api.types.is_numeric_dtype(df_filtered['Quantidade']) else 0
                
                col1.metric("Registros", len(df_filtered), help="Total de linhas filtradas")
                col2.metric("Soma Quantidade", f"{total_qtd:,.0f}")
                col3.metric("Pendências", len(df_filtered[df_filtered['Status'] == 'Pendente']))
                col4.metric("Destaque", df_filtered['Responsavel'].mode()[0] if not df_filtered.empty else "-")

            st.markdown("---")

            # Gráficos
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.markdown("#### Por Responsável")
                if not df_filtered.empty:
                    # Prepara dados (value_counts e renomeação explicita para evitar erros de versão do Pandas)
                    resp_counts = df_filtered['Responsavel'].value_counts().reset_index()
                    resp_counts.columns = ['Responsavel', 'Registros']
                    
                    fig_resp = px.bar(resp_counts, x='Responsavel', y='Registros', color='Responsavel')
                    fig_resp.update_layout(showlegend=False, margin=dict(t=0,b=0))
                    st.plotly_chart(fig_resp, use_container_width=True)

            with col_chart2:
                st.markdown("#### Por Status")
                if not df_filtered.empty:
                    fig_status = px.pie(df_filtered, names='Status', hole=0.6)
                    fig_status.update_layout(margin=dict(t=0,b=0))
                    st.plotly_chart(fig_status, use_container_width=True)

            # Tabela Editável
            st.markdown("### 📋 Detalhamento (Editável)")
            
            # --- Gerenciamento de Opções Dinâmicas ---
            OPTIONS_FILE = "options.json"
            
            def load_options():
                if os.path.exists(OPTIONS_FILE):
                    try:
                        with open(OPTIONS_FILE, "r") as f:
                            return json.load(f)
                    except:
                        return {"responsavel": [], "inconsistencias": []}
                return {"responsavel": [], "inconsistencias": []}

            def save_options_file(data):
                with open(OPTIONS_FILE, "w") as f:
                    json.dump(data, f)
            
            saved_options = load_options()
            
            # Combina opções salvas com as existentes no DataFrame atual para garantir que nada quebre
            current_resp = list(df['Responsavel'].unique()) if 'Responsavel' in df.columns else []
            current_inc = list(df['Inconsistencias'].unique()) if 'Inconsistencias' in df.columns else []
            
            all_responsaveis = sorted(list(set(saved_options.get("responsavel", []) + current_resp + ["Outro"])))
            all_inconsistencias = sorted(list(set(saved_options.get("inconsistencias", []) + current_inc + ["Outro"])))

            # --- UI para Adicionar Opções ---
            with st.expander("➕ Adicionar Opções (Responsável / Inconsistência)"):
                col_add1, col_add2 = st.columns(2)
                with col_add1:
                    new_resp = st.text_input("Novo Responsável")
                    if st.button("Adicionar Responsável"):
                        if new_resp and new_resp not in saved_options.get("responsavel", []):
                            saved_options.setdefault("responsavel", []).append(new_resp)
                            save_options_file(saved_options)
                            st.success(f"'{new_resp}' adicionado!")
                            time.sleep(1)
                            st.rerun()
                
                with col_add2:
                    new_inc = st.text_input("Nova Inconsistência")
                    if st.button("Adicionar Inconsistência"):
                        if new_inc and new_inc not in saved_options.get("inconsistencias", []):
                            saved_options.setdefault("inconsistencias", []).append(new_inc)
                            save_options_file(saved_options)
                            st.success(f"'{new_inc}' adicionada!")
                            time.sleep(1)
                            st.rerun()

            # --- Configuração das Colunas para o Editor ---
            import datetime
            from dateutil.relativedelta import relativedelta # type: ignore

            today = datetime.date.today()
            # Interpretação da regra: "nunca seja posterior a 2 meses antes da data atual"
            # Literalmente: Date <= (Today - 2 months). Bloqueia dados recentes.
            # Assumindo erro de digitação para "anterior", ou seja, janela de 2 meses.
            # Vamos aplicar uma janela segura de: 
            # Min: 2 meses atrás (evita coisas muito antigas)
            # Max: Hoje (evita futuro incorreto, já que é inconsistência passada)
            
            min_date = today - relativedelta(months=2)
            max_date = today
            
            column_cfg = {
                "Dia": st.column_config.DateColumn(
                    "Dia",
                    format="DD/MM/YYYY",
                    min_value=min_date, # Limita data antiga
                    max_value=max_date, # Limita data futura/anos errados
                    help="Data da ocorrência (Últimos 2 meses)",
                    width="medium",
                    required=True
                ),
                "Quantidade": st.column_config.TextColumn(
                    "Quantidade",
                    help="Máximo 3 dígitos (0-999)",
                    width="small",
                    max_chars=3,
                    validate="^\d{1,3}$",
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
                    options=['Pendente', 'Resolvido', 'Em Análise', 'Cancelado'],
                    width="medium",
                    required=True
                ),
                "Responsavel": st.column_config.SelectboxColumn(
                    "Responsável",
                    options=all_responsaveis,
                    width="medium",
                    required=True
                )
            }

            # Garante que Quantidade seja string para aplicar validação
            df_editor_input = df_filtered.copy()
            if 'Quantidade' in df_editor_input.columns:
                df_editor_input['Quantidade'] = df_editor_input['Quantidade'].astype(str)
            
            # Ajuste de Datas para compatibilidade com o editor
            # Editor espera date ou datetime
            if 'Dia' in df_editor_input.columns:
                 df_editor_input['Dia'] = pd.to_datetime(df_editor_input['Dia']).dt.date

            # Editor
            edited_df = st.data_editor(
                df_editor_input,
                use_container_width=True,
                column_config=column_cfg,
                num_rows="dynamic",
                key="data_editor_main"
            )

            # Botão de Salvar
            if st.button("💾 Salvar Alterações", type="primary"):
                try:
                    # Lógica de Atualização Robusta (Index-based)
                    # 1. Carrega original
                    df_full = df.copy()
                    
                    # 2. Identifica mudanças usando índices
                    # Índices originais desta view filtrada
                    original_indices = df_editor_input.index
                    
                    # Índices retornados pelo editor
                    edited_indices = edited_df.index
                    
                    # A. Remover linhas deletadas
                    # Linhas que estavam no original_indices mas NÃO estão no edited_indices
                    # (Apenas para índices numéricos/originais; novos índices criados pelo Streamlit costumam ser diferentes ou não existir no original)
                    indices_to_remove = [i for i in original_indices if i not in edited_indices]
                    if indices_to_remove:
                        df_full = df_full.drop(indices_to_remove)
                    
                    # B. Atualizar e Adicionar linhas
                    # Separar linhas que já existiam (Update) das novas (Append)
                    
                    # Trata colunas antes do merge
                    if 'Quantidade' in edited_df.columns:
                         # Converte de volta para numérico para salvar corretamente se possível, ou mantem string
                         # O padrão CSV do user é numérico? Se sim, numeric.
                         edited_df['Quantidade'] = pd.to_numeric(edited_df['Quantidade'], errors='ignore')
                    
                    # Garante que Dia seja datetime para consistencia
                    if 'Dia' in edited_df.columns:
                        edited_df['Dia'] = pd.to_datetime(edited_df['Dia'])
                    
                    # Percorre o dataframe editado
                    new_rows = []
                    
                    for idx, row in edited_df.iterrows():
                        if idx in df_full.index:
                            # Atualiza existente
                            df_full.loc[idx] = row
                        else:
                            # Nova linha
                            new_rows.append(row)
                    
                    # Adiciona novas linhas se houver
                    if new_rows:
                        df_new = pd.DataFrame(new_rows)
                        df_full = pd.concat([df_full, df_new], ignore_index=True)
                    
                    # 3. Salva no disco
                    current_path = st.session_state['current_file_path']
                    if current_path:
                        if current_path.endswith('.csv'):
                            df_full.to_csv(current_path, index=False)
                        else:
                            df_full.to_excel(current_path, index=False)
                        
                        st.success("Alterações salvas e sincronizadas!")
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
            
            # Botão para Baixar o Arquivo Atualizado
            st.markdown("---")
            st.markdown("### 📤 Exportar Dados")
            
            col_down1, col_down2 = st.columns([1, 1])
            with col_down1:
                # Prepara o arquivo para download baseado no estado atual (df - que contém os dados carregados do disco)
                # Como st.rerun acontece após salvar, 'df' já estará atualizado na próxima execução.
                # Mas para garantir, usamos o próprio df_filtered ou lemos do disco se quiser o full.
                # O ideal é ler do disco para garantir consistência total.
                
                with open(st.session_state['current_file_path'], "rb") as f:
                    file_data = f.read()
                
                file_name = os.path.basename(st.session_state['current_file_path'])
                # Remove timestamp para o nome do arquivo de download ficar bonito
                if "_" in file_name:
                    download_name = file_name.split("_", 1)[-1]
                else:
                    download_name = file_name
                
                mime_type = "text/csv" if file_name.endswith(".csv") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                st.download_button(
                    label="📥 Baixar Planilha",
                    data=file_data,
                    file_name=f"EDITADO_{download_name}",
                    mime=mime_type,
                    type="secondary",
                    use_container_width=True
                )
            
            with col_down2:
                # --- Integração Google Sheets ---
                if 'show_gsheets_ui' not in st.session_state:
                    st.session_state['show_gsheets_ui'] = False

                if st.button("☁️ Enviar para Google Sheets", use_container_width=True):
                    st.session_state['show_gsheets_ui'] = not st.session_state['show_gsheets_ui']

            # Área de UI do Google Sheets (Expansível)
            if st.session_state['show_gsheets_ui']:
                 with st.container():
                    st.info("Configuração Google Sheets")
                    
                    with st.expander("❓ Como obter o arquivo credentials.json? (Tutorial)"):
                        st.markdown("""
                        **Custo: É gratuito!** (Dentro limites generosos do plano Free do Google Cloud).
                        
                        1. Acesse o **[Google Cloud Console](https://console.cloud.google.com/)**.
                        2. Na barra azul do topo, ao lado de **"Você está trabalhando em"**, clique no nome do projeto atual (ou em "Selecione um projeto").
                        3. Na janela que abrir, clique em **"Novo Projeto"** (canto superior direito).
                        4. Dê o nome "Dashboard Contabil" e clique em **Criar**.
                        5. Aguarde a notificação de criação e **selecione o novo projeto**.
                        4. Pesquise por **'Google Sheets API'** e clique em **Ativar**.
                        5. Pesquise por **'Google Drive API'** e clique em **Ativar** também.
                        6. Vá em **APIs e Serviços > Credenciais**.
                        7. Clique em **Criar Credenciais > Conta de Serviço**.
                        8. Dê um nome (ex: "robo-planilha") e clique em **Criar e Continuar**.
                        9. Nas etapas de "Permissões" e "Acesso", pode clicar apenas em **Concluir** (são opcionais).
                        10. **IMPORTANTE:** Clique no e-mail da conta que apareceu na lista (ex: `...iam.gserviceaccount.com`).
                        11. Vá na aba **Chaves** (no topo) > **Adicionar Chave** > **Criar nova chave** > **JSON**.
                        12. O download do arquivo `credentials.json` começará. Use-o no campo abaixo!
                        """)

                    # 1. Verifica Credenciais
                    creds_file = "credentials.json"
                    has_creds = os.path.exists(creds_file)
                    
                    if not has_creds:
                        st.warning("⚠️ Arquivo 'credentials.json' não encontrado.")
                        uploaded_creds = st.file_uploader("Faça upload do seu credentials.json (Service Account)", type="json", key="creds_upl")
                        if uploaded_creds:
                            with open(creds_file, "wb") as f:
                                f.write(uploaded_creds.getbuffer())
                            st.success("Credenciais salvas! Clique no botão novamente.")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.markdown(f"✅ Credenciais encontradas.")
                        
                        # Extrai o e-mail do robô para mostrar ao usuário
                        try:
                            with open(creds_file, 'r') as f:
                                creds_data = json.load(f)
                            robot_email = creds_data.get('client_email', 'Não encontrado')
                            st.info(f"📧 E-mail do Robô: `{robot_email}`")
                            st.caption("Dica: Se der erro de cota/permissão, crie uma planilha manualmente no seu Google Drive, compartilhe com esse e-mail acima e digite o nome dela abaixo.")
                        except:
                            pass
                        
                        # --- Persistência de Configurações (Email/Planilha) ---
                        SETTINGS_FILE = "settings.json"
                        
                        def load_settings():
                            if os.path.exists(SETTINGS_FILE):
                                try:
                                    with open(SETTINGS_FILE, "r") as f:
                                        return json.load(f)
                                except:
                                    return {}
                            return {}

                        def save_settings(s_name, s_email):
                            with open(SETTINGS_FILE, "w") as f:
                                json.dump({"sheet_name": s_name, "email_share": s_email}, f)

                        saved_settings = load_settings()
                        default_sheet_name = saved_settings.get("sheet_name", download_name.split('.')[0])
                        default_email_share = saved_settings.get("email_share", "")

                        sheet_name = st.text_input("Nome da Planilha no Google Sheets", value=default_sheet_name)
                        email_share = st.text_input("Seu E-mail Google (para compartilhar)", value=default_email_share)
                        
                        if st.button("🚀 Enviar Dados Agora"):
                            if not email_share and not sheet_name:
                                st.error("Preencha os campos.")
                            else:
                                # Salva as configurações para a próxima vez
                                save_settings(sheet_name, email_share)
                                
                                try:
                                    import gspread
                                    from oauth2client.service_account import ServiceAccountCredentials
                                    
                                    with st.spinner("Conectando ao Google Sheets..."):
                                        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                                        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
                                        client = gspread.authorize(creds)
                                        
                                        # 1. Tenta Abrir
                                        try:
                                            st.write(f"🔍 Procurando planilha: **{sheet_name}**...")
                                            sh = client.open(sheet_name)
                                            st.success("✅ Planilha encontrada!")
                                            worksheet = sh.get_worksheet(0)
                                            worksheet.clear()
                                        except gspread.SpreadsheetNotFound:
                                            st.warning(f"⚠️ Planilha '{sheet_name}' não encontrada ou não compartilhada com o robô.")
                                            st.write("🛠️ Tentando criar uma nova planilha (Isso pode falhar se a API Drive não estiver ativa)...")
                                            # 2. Tenta Criar (Fallback)
                                            try:
                                                sh = client.create(sheet_name)
                                                st.success("✅ Nova planilha criada!")
                                                worksheet = sh.get_worksheet(0)
                                                if email_share:
                                                    sh.share(email_share, perm_type='user', role='writer')
                                            except Exception as create_err:
                                                raise Exception(f"Falha ao CRIAR planilha: {str(create_err)}")

                                        # Envio de dados
                                        st.write("📤 Enviando dados...")
                                        # Recarregando do disco atualizado
                                        if st.session_state['current_file_path'].endswith('.csv'):
                                            df_export = pd.read_csv(st.session_state['current_file_path'])
                                        else:
                                            df_export = pd.read_excel(st.session_state['current_file_path'])

                                        df_export = df_export.astype(str)
                                        worksheet.update([df_export.columns.values.tolist()] + df_export.values.tolist())
                                        
                                        st.success(f"Sucesso! Planilha disponível no Google Drive de: {email_share}")
                                        st.balloons()
                                        
                                except Exception as e:
                                    error_msg = str(e)
                                    st.error("❌ Ocorreu um erro FATAL:")
                                    st.code(error_msg)
                                    
                                    if "403" in error_msg:
                                        st.markdown("### �️ Diagnóstico do Erro 403")
                                        st.warning("""
                                        **Se o erro aconteceu na etapa de CRIAR:**
                                        1. A **Google Drive API** não está ativada. (É diferente da Sheets API).
                                        2. Ou a cota de criação realmente excedeu.
                                        
                                        **SOLUÇÃO RECOMENDADA:**
                                        1. Crie a planilha manualmente no seu Google Drive.
                                        2. Compartilhe com o e-mail do robô (mostrado acima).
                                        3. Garanta que o nome digitado aqui seja **EXATAMENTE IGUAL** ao da planilha criada.
                                        """)
            
    else:
        # --- Tela Inicial (Empty State) ---
        st.markdown("### 👋 Bem-vindo ao Controle Contábil")
        
        col_intro, col_model = st.columns([2, 1])
        
        with col_intro:
             st.info("""
             **Para começar:**
             1. Utilize o painel lateral para carregar sua planilha.
             2. Ou selecione um dos arquivos recentes no **Histórico**.
             """)
        
        with col_model:
            with st.expander("Precisa de um modelo?", expanded=True):
                st.write("Baixe o template para preencher:")
                # Botão para baixar modelo
                example_data = {
                    'Dia': ['2023-10-01', '2023-10-01', '2023-10-02'],
                    'Quantidade': [10, 5, 2],
                    'Inconsistencias': ['Erro no lançamento X', 'Valor divergente Y', 'Conta não conciliada'],
                    'Status': ['Pendente', 'Resolvido', 'Em Análise'],
                    'Responsavel': ['Maria', 'João', 'Maria']
                }
                df_example = pd.DataFrame(example_data)
                @st.cache_data
                def convert_df(df):
                    return df.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Baixar CSV Modelo",
                    data=convert_df(df_example),
                    file_name='modelo_dashboard_contabil.csv',
                    mime='text/csv',
                    use_container_width=True
                )

        st.markdown("---")
        st.subheader("Como sua planilha deve ser:")
        st.code("""
Dia,Quantidade,Inconsistencias,Status,Responsavel
01/01/2024,10,"Erro de soma","Pendente","Ana"
        """, language="csv")

if __name__ == "__main__":
    main()
