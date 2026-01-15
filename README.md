# Dashboard de Controle Contábil

Este é um projeto de dashboard interativo para análise de planilhas de contabilidade, desenvolvido em **Python** com **Streamlit**.

## Funcionalidades
- **Importação de Planilhas**: Suporte para arquivos Excel (.xlsx) e CSV.
- **Métricas Chave**: Visualização rápida de total de inconsistências, pendências e responsáveis.
- **Gráficos Interativos**: Distribuição de erros por responsável e status.
- **Filtros Dinâmicos**: Filtre os dados por dia, responsável ou status.
- **Modelo de Exemplo**: Download de planilha modelo diretamente na aplicação.

## Pré-requisitos
Para rodar este projeto, você precisará ter o **Python** instalado em seu computador.

1. Baixe e instale o Python (versão 3.8 ou superior): [python.org/downloads](https://www.python.org/downloads/)
2. Verifique a instalação abrindo o terminal (Prompt de Comando ou PowerShell) e digitando:
   ```bash
   python --version
   ```

## Instalação e Execução

Siga os passos abaixo para configurar e rodar o dashboard:

1. **Abra o terminal** na pasta do projeto.
   
2. **(Opcional, mas recomendado) Crie um ambiente virtual**:
   Isso evita conflitos com outras instalações do Python.
   ```bash
   python -m venv venv
   ```
   - No Windows, ative com:
     ```bash
     .\venv\Scripts\activate
     ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o Dashboard**:
   ```bash
   streamlit run app.py
   ```

5. O dashboard abrirá automaticamente no seu navegador padrão (geralmente em `http://localhost:8501`).

## Estrutura da Planilha
Para que o dashboard funcione corretamente, sua planilha deve conter as seguintes colunas:
- `Dia`: Data do registro.
- `Quantidade`: Quantidade associada.
- `Inconsistencias`: Descrição do problema.
- `Status`: Ex: Pendente, Resolvido.
- `Responsavel`: Nome do responsável.

> **Nota**: Ao abrir o dashboard pela primeira vez, você pode baixar um arquivo modelo csv clicando no botão disponível na tela inicial.
