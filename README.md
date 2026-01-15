# 📊 Dashboard de Controle Contábil

Uma aplicação interativa para visualização, validação e gerenciamento de inconsistências contábeis. Desenvolvido em Python com Streamlit.

---

## 🚀 Funcionalidades Principais

### 1. Visualização e Upload
- **Suporte a Arquivos**: Aceita planilhas no formatos `.xlsx` e `.csv`.
- **Histórico Inteligente**: Menu lateral que salva os últimos 3 arquivos acessados para troca rápida.
- **KPIs Automáticos**: Cards de resumo (Total, Pendentes, Resolvidos) e gráficos interativos.

### 2. Edição de Dados (`Data Editor`)
Altere os dados diretamente na tabela interativa:
- **Quantidade**: Validada para aceitar apenas números de até 3 dígitos.
- **Data**: Calendário inteligente restrito aos últimos 2 meses (evita erros de digitação de ano).
- **Status/Responsável**: Seleção via menu dropdown.
- **Opções Dinâmicas**: Cadastre novos *Responsáveis* ou *Tipos de Inconsistência* pelo menu lateral sem precisar mexer no código.

### 3. Integração Google Sheets ☁️
Exporte sua planilha editada diretamente para o Google Drive com um clique.
- Salva o e-mail e nome da planilha usados pela última vez.
- Instruções integradas para configuração de acesso.

---

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior instalado.

### Passo a Passo

1. **Clone o repositório** (ou baixe os arquivos):
   ```bash
   git clone https://github.com/rodrigod3v/dashboard-contabil.git
   cd dashboard-contabil
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o Painel**:
   ```bash
   streamlit run app.py
   ```
   O navegador abrirá automaticamente no endereço `http://localhost:8501`.

---

## 🤖 Como Configurar o "Robô" do Google (Google Sheets API)

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

---

## 🆘 Solução de Problemas Comuns (Troubleshooting)

### 🚨 Erro 403: "The user's Drive storage quota has been exceeded"
Esse erro geralmente é falso e indica falta de permissão, não falta de espaço.

**Solução:**
1. Verifique se a **Google Drive API** foi ativada no passo 4 acima.
2. **Método Infalível**:
   - Crie uma planilha manualmente no seu Google Drive (ex: "Relatorio_Final").
   - Compartilhe ela com o **e-mail do robô** (que aparece na tela do dashboard).
   - No Dashboard, digite o nome exato "Relatorio_Final" e clique em enviar. Isso força o robô a editar um arquivo seu em vez de tentar criar um novo.

### 💾 "As alterações não salvaram no meu arquivo original"
Por segurança, navegadores não permitem que sites editem arquivos locais no seu PC (`C:\...`).
- **O que o sistema faz**: Salva na memória interna (cache). Se você reabrir o app, as mudanças estarão lá.
- **Para ter o arquivo**: Clique no botão **"📥 Baixar Planilha Atualizada"** e substitua o arquivo antigo manualmente.

---

## 📂 Estrutura de Arquivos Importantes
- `app.py`: Código principal.
- `settings.json`: Salva suas preferências (nome da planilha e e-mail).
- `options.json`: Salva novos responsáveis e inconsistências cadastrados.
- `cache_data/`: Pasta onde o histórico de arquivos é mantido.
