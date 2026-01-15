import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data
import os

st.set_page_config(page_title="Dashboard Contábil", layout="wide")

st.title("📊 Visão Geral da Operação")
st.markdown("---")

# --- Session Management ---
if 'current_file_path' not in st.session_state or not st.session_state['current_file_path']:
    st.info("👋 Para começar, faça o upload de uma planilha na **Página Inicial** ou selecione um histórico.")
    st.stop()
    
file_path = st.session_state['current_file_path']
if not os.path.exists(file_path):
    st.error("Arquivo não encontrado. Por favor, carregue novamente na Home.")
    st.session_state['current_file_path'] = None
    st.stop()

df = load_data(file_path)

if df is None:
    st.stop()

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🔍 Filtros de Visualização")
    
    # Date Range Filter
    if 'Dia' in df.columns:
        min_date = df['Dia'].min().date()
        max_date = df['Dia'].max().date()
        date_range = st.date_input(
            "Período",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Responsible Filter
    responsaveis = ['Todos'] + sorted(list(df['Responsavel'].unique())) if 'Responsavel' in df.columns else []
    selected_resp = st.selectbox("Responsável", responsaveis)

# --- Filtering Logic ---
df_filtered = df.copy()

# Date Filter
if 'Dia' in df.columns and len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_filtered[
        (df_filtered['Dia'].dt.date >= start_date) & 
        (df_filtered['Dia'].dt.date <= end_date)
    ]

# Responsible Filter
if selected_resp != 'Todos':
    df_filtered = df_filtered[df_filtered['Responsavel'] == selected_resp]

# --- KPIs ---
total_recs = len(df_filtered)
total_qtd = df_filtered['Quantidade'].sum() if 'Quantidade' in df_filtered.columns and pd.api.types.is_numeric_dtype(df_filtered['Quantidade']) else 0
pending_count = len(df_filtered[df_filtered['Status'] == 'Pendente']) if 'Status' in df_filtered.columns else 0
# Calculation of resolution %
if total_recs > 0:
    resolved_count = len(df_filtered[df_filtered['Status'] == 'Resolvido'])
    efficiency = (resolved_count / total_recs) * 100
else:
    efficiency = 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Registros Totais", total_recs)
col2.metric("Volume (Qtd)", f"{total_qtd:,.0f}")
col3.metric("Pendências Ativas", pending_count, delta_color="inverse")
col4.metric("Taxa de Resolução", f"{efficiency:.1f}%")

st.markdown("###") # Spacer

# --- Professional Charts ---
col_charts_top1, col_charts_top2 = st.columns([2, 1])

with col_charts_top1:
    st.subheader("📅 Ocorrências por Dia")
    if 'Dia' in df_filtered.columns:
        # Aggregate by day
        daily_counts = df_filtered.groupby(df_filtered['Dia'].dt.date).size().reset_index(name='Contagem')
        fig_trend = px.area(daily_counts, x='Dia', y='Contagem', template='plotly_white')
        fig_trend.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            xaxis_title=None,
            yaxis_title=None,
            height=300
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("Coluna 'Dia' não encontrada.")

with col_charts_top2:
    st.subheader("📌 Status Atual")
    if 'Status' in df_filtered.columns:
        status_counts = df_filtered['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig_donut = px.pie(status_counts, values='Count', names='Status', hole=0.6, template='plotly_white')
        fig_donut.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            height=300
        )
        st.plotly_chart(fig_donut, use_container_width=True)

col_charts_bot1, col_charts_bot2 = st.columns(2)

with col_charts_bot1:
    st.subheader("⚠️ Top Inconsistências")
    if 'Inconsistencias' in df_filtered.columns:
        inc_counts = df_filtered['Inconsistencias'].value_counts().head(5).reset_index()
        inc_counts.columns = ['Inconsistencia', 'Contagem']
        
        fig_bar = px.bar(inc_counts, y='Inconsistencia', x='Contagem', orientation='h', text='Contagem', template='plotly_white')
        fig_bar.update_layout(
            yaxis=dict(autorange="reversed"),
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title=None,
            yaxis_title=None
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with col_charts_bot2:
    st.subheader("🏆 Produtividade por Responsável")
    if 'Responsavel' in df_filtered.columns:
        # Stacked bar by status for each responsible
        resp_status = df_filtered.groupby(['Responsavel', 'Status']).size().reset_index(name='Contagem')
        
        fig_stack = px.bar(resp_status, x='Responsavel', y='Contagem', color='Status', template='plotly_white')
        fig_stack.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title=None,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_stack, use_container_width=True)
