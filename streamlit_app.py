import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os

# --- Configurações da Página ---
st.set_page_config(layout="wide", page_title="ROADMAP Interativa 🚀", initial_sidebar_state="expanded")

# --- Caminho para o arquivo de dados ---
DATA_DIR = "data"
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.csv") # Usaremos CSV para simplicidade

# Garante que a pasta 'data' exista
os.makedirs(DATA_DIR, exist_ok=True)

# --- Funções de Carregamento e Salvamento de Dados ---
@st.cache_data(show_spinner=False) # Cache para carregar dados apenas uma vez
def load_projects_data():
    if os.path.exists(PROJECTS_FILE):
        df = pd.read_csv(PROJECTS_FILE)
        # Converte colunas de data para o formato datetime
        df['Início Previsto'] = pd.to_datetime(df['Início Previsto'])
        df['Fim Previsto'] = pd.to_datetime(df['Fim Previsto'])
        return df
    else:
        # Dados iniciais se o arquivo não existir
        initial_data = {
            'Projeto': ['Lançamento App V1', 'Melhoria UX Dashboard', 'Integração API Externa', 'Campanha Marketing Q3', 'Revisão Processo Interno', 'Entrega MVP Feature X'],
            'Início Previsto': ['2025-01-01', '2025-02-15', '2025-03-10', '2025-04-01', '2025-05-01', '2025-06-01'],
            'Fim Previsto': ['2025-03-31', '2025-04-30', '2025-05-20', '2025-06-15', '2025-07-31', '2025-06-20'],
            'Responsável/Status': ['Pilotando', 'Em desenvolvimento TI', 'Em desenvolvimento Vini', 'Entregue', 'Em Análise', 'Entrega de MVP']
        }
        df = pd.DataFrame(initial_data)
        df['Início Previsto'] = pd.to_datetime(df['Início Previsto'])
        df['Fim Previsto'] = pd.to_datetime(df['Fim Previsto'])
        df.to_csv(PROJECTS_FILE, index=False) # Salva os dados iniciais
        return df

def save_projects_data(df):
    df['Início Previsto'] = df['Início Previsto'].dt.strftime('%Y-%m-%d') # Formata para salvar como string
    df['Fim Previsto'] = df['Fim Previsto'].dt.strftime('%Y-%m-%d')
    df.to_csv(PROJECTS_FILE, index=False)
    st.session_state['projects_df'] = load_projects_data() # Recarrega o cache para refletir as mudanças

# Inicializa o DataFrame no session_state para persistir durante a sessão
if 'projects_df' not in st.session_state:
    st.session_state['projects_df'] = load_projects_data()

df_projects = st.session_state['projects_df']

# --- Definição de Cores e Legenda (Configurável) ---
st.sidebar.header("🎨 Configuração de Cores")
st.sidebar.markdown("Defina as cores para cada status/responsável.")

# Dicionário padrão de cores (pode ser editado na UI)
default_color_map = {
    'Pilotando': '#1f77b4',          # Azul
    'Em desenvolvimento TI': '#d62728',     # Vermelho
    'Em desenvolvimento Vini': '#2ca02c',  # Verde
    'Entregue': '#ff7f0e',           # Laranja
    'Entrega de MVP': '#9467bd',     # Roxo
    'Em Análise': '#8c564b',         # Marrom
    'Concluído': '#17becf',          # Ciano
    'Atrasado': '#e377c2',           # Rosa
    'Não Iniciado': '#7f7f7f',       # Cinza
}

# Pegar todos os valores únicos de 'Responsável/Status' do DataFrame
all_statuses = df_projects['Responsável/Status'].unique()
configured_colors = {}

for status in all_statuses:
    # Use st.color_picker para permitir a seleção de cores pelo usuário
    configured_colors[status] = st.sidebar.color_picker(
        f"Cor para '{status}'",
        value=default_color_map.get(status, '#CCCCCC') # Usa cor padrão ou cinza claro
    )

st.sidebar.markdown("---") # Linha divisória na sidebar

# --- Título Principal ---
st.title("ROADMAP de Projetos 📈")
st.markdown("Visualize e gerencie o cronograma dos seus projetos de forma interativa.")

# --- Seção do Gráfico de Gantt ---
st.header("Visualização da Roadmap")

fig = px.timeline(
    df_projects,
    x_start="Início Previsto",
    x_end="Fim Previsto",
    y="Projeto",
    color="Responsável/Status", # Coluna usada para colorir as barras
    color_discrete_map=configured_colors, # Usamos o mapa de cores configurado
    hover_name="Projeto",
    hover_data={
        "Início Previsto": "|%d/%m/%Y",
        "Fim Previsto": "|%d/%m/%Y",
        "Responsável/Status": True
    },
    title="Cronograma Detalhado dos Projetos"
)

# Inverter o eixo Y para que os projetos mais recentes apareçam no topo
fig.update_yaxes(autorange="reversed")

# Adicionar uma linha para a data atual (hoje)
today = datetime.datetime.now()
fig.add_vline(
    x=today.timestamp() * 1000, # Plotly usa milissegundos para timestamps
    line_dash="dash",
    line_color="red",
    annotation_text=f"Hoje: {today.strftime('%d/%m/%Y')}",
    annotation_position="top left",
    annotation_font_color="red"
)

# Layout do Plotly
fig.update_layout(
    xaxis_title="Período",
    yaxis_title="Projeto",
    hovermode="x unified",
    height=500 # Altura fixa para melhor visualização
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

---

## 🚀 Edição e Gerenciamento de Projetos

st.markdown("Aqui você pode **adicionar novos projetos**, **atualizar prazos** e **responsáveis**.")

# Usamos um container para agrupar os elementos de edição
with st.container(border=True):
    st.subheader("📝 Editar Projetos Existentes")

    # Opção de edição via selectbox
    selected_project_name = st.selectbox(
        "Selecione um projeto para atualizar:",
        options=df_projects['Projeto'].tolist(),
        key="project_selector" # Chave única para o widget
    )

    # Encontrar o projeto selecionado e exibir seus detalhes para edição
    if selected_project_name:
        project_index = df_projects[df_projects['Projeto'] == selected_project_name].index[0]
        
        # Recupera os valores atuais
        current_start = df_projects.loc[project_index, 'Início Previsto'].date()
        current_end = df_projects.loc[project_index, 'Fim Previsto'].date()
        current_status_resp = df_projects.loc[project_index, 'Responsável/Status']

        # Campos de entrada para as novas datas e status/responsável
        col1, col2, col3 = st.columns(3)
        with col1:
            new_start_date = st.date_input(
                "Início Previsto",
                value=current_start,
                key=f"start_{selected_project_name}"
            )
        with col2:
            new_end_date = st.date_input(
                "Fim Previsto",
                value=current_end,
                key=f"end_{selected_project_name}"
            )
        with col3:
            new_status_resp = st.selectbox(
                "Responsável / Status",
                options=list(configured_colors.keys()), # Usa as chaves do dicionário de cores
                index=list(configured_colors.keys()).index(current_status_resp) if current_status_resp in configured_colors else 0,
                key=f"status_resp_{selected_project_name}"
            )
        
        # Botão para salvar as alterações
        if st.button(f"💾 Salvar Alterações para '{selected_project_name}'", key=f"save_btn_{selected_project_name}"):
            df_projects.loc[project_index, 'Início Previsto'] = new_start_date
            df_projects.loc[project_index, 'Fim Previsto'] = new_end_date
            df_projects.loc[project_index, 'Responsável/Status'] = new_status_resp
            
            save_projects_data(df_projects) # Salva no CSV
            st.success(f"✅ Projeto '{selected_project_name}' atualizado e salvo!")
            st.rerun() # Força a aplicação a recarregar e mostrar as mudanças

---

## ✨ Adicionar Novo Projeto

with st.container(border=True):
    st.subheader("➕ Adicionar um Novo Projeto")
    
    with st.form("add_project_form"):
        new_project_name = st.text_input("Nome do Novo Projeto")
        col_new1, col_new2, col_new3 = st.columns(3)
        with col_new1:
            new_project_start = st.date_input("Início Previsto", value=datetime.date.today())
        with col_new2:
            new_project_end = st.date_input("Fim Previsto", value=datetime.date.today() + datetime.timedelta(days=30))
        with col_new3:
            new_project_status_resp = st.selectbox(
                "Responsável / Status",
                options=list(configured_colors.keys()),
                index=0 # Padrão para o primeiro status
            )
        
        submitted = st.form_submit_button("Criar Novo Projeto")
        if submitted:
            if new_project_name and new_project_name not in df_projects['Projeto'].tolist():
                new_row = pd.DataFrame([{
                    'Projeto': new_project_name,
                    'Início Previsto': new_project_start,
                    'Fim Previsto': new_project_end,
                    'Responsável/Status': new_project_status_resp
                }])
                df_projects = pd.concat([df_projects, new_row], ignore_index=True)
                save_projects_data(df_projects) # Salva no CSV
                st.success(f"🎉 Projeto '{new_project_name}' adicionado e salvo!")
                st.rerun() # Força a aplicação a recarregar
            elif new_project_name:
                st.warning("⚠️ Um projeto com esse nome já existe. Por favor, escolha outro nome.")
            else:
                st.error("❗ O nome do projeto não pode ser vazio.")

---

### 3. `README.md` (Exemplo)

```markdown
# ROADMAP de Projetos

Esta é uma aplicação interativa de ROADMAP desenvolvida com Streamlit e Plotly.

## Funcionalidades

-   **Visualização de Gantt:** Veja o cronograma de seus projetos de forma clara e visual.
-   **Edição de Prazos:** Ajuste as datas de início e fim dos projetos diretamente na interface.
-   **Dados Persistentes:** As alterações são salvas e carregadas automaticamente (via `data/projects.csv`).
-   **Cores Configuráveis:** Defina as cores para diferentes status ou responsáveis diretamente na barra lateral.
-   **Adicionar Novos Projetos:** Crie novos projetos com seus prazos e responsáveis.

## Como Executar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/ROADMAP.git
    cd ROADMAP
    ```
2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: `venv\Scripts\activate`
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute a aplicação:**
    ```bash
    streamlit run streamlit_app.py
    ```
    A aplicação será aberta automaticamente no seu navegador.

## Como Fazer Deploy no Streamlit Community Cloud

1.  Certifique-se de que seus arquivos (`streamlit_app.py`, `requirements.txt`, `README.md` e a pasta `data/` com `projects.csv` se quiser dados iniciais) estejam no seu repositório GitHub.
2.  Vá para [share.streamlit.io](https://share.streamlit.io/).
3.  Faça login com sua conta GitHub.
4.  Clique em "New app" e selecione seu repositório e o arquivo `streamlit_app.py`.
5.  Clique em "Deploy!".

## Contribuindo

Sinta-se à vontade para abrir issues ou pull requests para melhorias.
