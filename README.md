# 📊 Dashboard Contábil & Editor de Dados

Este projeto é uma aplicação web completa desenvolvida em **Streamlit** para gerenciamento, análise e edição de dados contábeis/operacionais.

O sistema foi desenhado para ser intuitivo, com foco em produtividade, permitindo desde a visualização de KPIs até a correção de dados em planilhas locais ou integradas ao Google Sheets.

---

## 🚀 Funcionalidades Principais

### 1. 🏠 Home (Início)
- **Central de Upload**: Suporte para arquivos `.csv` e `.xlsx`.
- **Histórico Inteligente**: Acesso rápido aos últimos arquivos trabalhados com um cache local eficiente.
- **Modelos**: Download direto de templates para padronização da entrada de dados.

### 2. 📊 Dashboard Profissional
Visualização de dados analítica e responsiva:
- **KPIs em Tempo Real**: Volume, Pendências, Taxa de Resolução.
- **Gráfico de Ocorrências**: Evolução temporal do volume de trabalho (Barras).
- **Inconsistências**: Ranking dos principais erros (Pareto/Barras).
- **Status da Operação**: Visão geral da distribuição de status (Rosca).
- **Produtividade da Equipe**: Performance individual por tipo de entrega.

### 3. 📝 Editor de Dados (CRUD)
- **Edição em Grade**: Interface estilo Excel para correção rápida.
- **Filtros Avançados**: Busque por texto, responsável, status ou erro.
- **Validação Automática**:
  - Datas restritas a 1 ano.
  - Campos numéricos validados.
- **Integração Google Sheets**:
  - Envie dados tratados para a nuvem com um clique.
  - Guia passo-a-passo integrado para configuração de API.
  - Alertas visuais e feedback de sucesso.

### 4. ⚙️ Configurações
- **Gerenciamento de Listas**: Adicione ou remova opções dos menus suspensos:
  - Responsáveis
  - Status
  - Tipos de Inconsistência
- **Persistência**: As configurações são salvas em `options.json` e carregadas automaticamente.

### 5. 🔐 Sistema de Segurança
- **Login por Chave de Acesso**: O sistema é protegido contra acesso não autorizado.
- **Tokens Individuais**: Acesso liberado apenas via chaves geradas pelo administrador.
- **Gerador de Chaves**: Script administrativo `generate_key.py` para criar novos acessos seguros.

---

## 📂 Estrutura do Projeto

```
/
├── Home.py                  # Página Inicial (Entry Point)
├── utils.py                 # Funções auxiliares (Load/Save/Cache)
├── pages/
│   ├── 1_📊_Dashboard.py    # Página de Analytics
│   ├── 2_📝_Editor_de_Dados.py # Página de Edição
│   └── 3_⚙️_Configuracoes.py # Página de Ajustes
├── cache_data/              # Armazenamento temporário de arquivos
├── options.json             # Opções salvas (listas dinâmicas)
└── requirements.txt         # Dependências do projeto
```

---

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.8+
- Bibliotecas listadas em `requirements.txt`

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
streamlit run Home.py
```

---

## 📦 Dependências Principais
- **Streamlit**: Framework de UI.
- **Pandas**: Manipulação de dados.
- **Plotly**: Gráficos interativos.
- **Gspread / OAuth2Client**: Integração com Google Sheets.
- **Watchdog**: Monitoramento de sistema de arquivos (opcional para reload).

---

## 💡 Dicas de Uso
- **Navegação**: Use a barra lateral para alternar entre as páginas.
- **Mobile**: A aplicação é 100% responsiva. Gire o celular para ver gráficos em tela cheia.
- **Segurança**: Arquivos `.json` de credenciais nunca devem ser commitados no Git (use `.gitignore`).
