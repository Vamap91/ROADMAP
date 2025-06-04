import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json

# Configuração da página
st.set_page_config(
    page_title="🚀 ROADMAP de Projetos",
    page_icon="🚀",
    layout="wide"
)

# Inicialização do estado da sessão
if 'projects_df' not in st.session_state:
    st.session_state.projects_df = None
if 'color_mapping' not in st.session_state:
    st.session_state.color_mapping = {}

def ensure_data_directory():
    """Garante que o diretório data/ existe"""
    if not os.path.exists('data'):
        os.makedirs('data')

def load_projects():
    """Carrega projetos do arquivo CSV ou cria dados de exemplo"""
    ensure_data_directory()
    csv_path = 'data/projects.csv'
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            df['Início Previsto'] = pd.to_datetime(df['Início Previsto'])
            df['Fim Previsto'] = pd.to_datetime(df['Fim Previsto'])
            return df
        except Exception as e:
            st.error(f"Erro ao carregar projetos: {e}")
            return create_sample_data()
    else:
        return create_sample_data()

def create_sample_data():
    """Cria dados de exemplo para inicialização"""
    today = datetime.now().date()
    sample_data = {
        'Nome do Projeto': [
            'Sistema de Autenticação',
            'API de Pagamentos',
            'Dashboard Analytics',
            'Mobile App MVP',
            'Integração ERP'
        ],
        'Início Previsto': [
            today,
            today + timedelta(days=30),
            today + timedelta(days=60),
            today + timedelta(days=90),
            today + timedelta(days=120)
        ],
        'Fim Previsto': [
            today + timedelta(days=45),
            today + timedelta(days=75),
            today + timedelta(days=105),
            today + timedelta(days=135),
            today + timedelta(days=180)
        ],
        'Responsável/Status': [
            'Backend Team',
            'FinTech Team',
            'Data Team',
            'Mobile Team',
            'Integration Team'
        ]
    }
    
    df = pd.DataFrame(sample_data)
    save_projects(df)
    return df

def save_projects(df):
    """Salva projetos no arquivo CSV"""
    ensure_data_directory()
    csv_path = 'data/projects.csv'
    try:
        df.to_csv(csv_path, index=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar projetos: {e}")
        return False

def load_color_mapping():
    """Carrega mapeamento de cores do arquivo JSON"""
    ensure_data_directory()
    json_path = 'data/color_mapping.json'
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_color_mapping(color_mapping):
    """Salva mapeamento de cores no arquivo JSON"""
    ensure_data_directory()
    json_path = 'data/color_mapping.json'
    try:
        with open(json_path, 'w') as f:
            json.dump(color_mapping, f)
    except Exception as e:
        st.error(f"Erro ao salvar cores: {e}")

def create_gantt_chart(df, color_mapping):
    """Cria o gráfico de Gantt com Plotly"""
    if df.empty:
        return go.Figure()
    
    # Preparar dados para o gráfico
    gantt_data = []
    for idx, row in df.iterrows():
        gantt_data.append({
            'Task': row['Nome do Projeto'],
            'Start': row['Início Previsto'],
            'Finish': row['Fim Previsto'],
            'Resource': row['Responsável/Status'],
            'Description': f"Projeto: {row['Nome do Projeto']}<br>Responsável: {row['Responsável/Status']}<br>Duração: {(row['Fim Previsto'] - row['Início Previsto']).days} dias"
        })
    
    gantt_df = pd.DataFrame(gantt_data)
    
    # Criar cores para cada responsável/status
    unique_resources = gantt_df['Resource'].unique()
    colors = []
    for resource in unique_resources:
        if resource in color_mapping:
            colors.append(color_mapping[resource])
        else:
            # Cores padrão se não definida
            default_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
            colors.append(default_colors[len(colors) % len(default_colors)])
    
    # Criar gráfico de Gantt
    fig = px.timeline(
        gantt_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Resource",
        color_discrete_sequence=colors,
        title="📊 ROADMAP de Projetos - Cronograma Geral",
        hover_data=["Description"]
    )
    
    # Configurações do layout
    fig.update_layout(
        height=600,
        xaxis_title="📅 Cronograma",
        yaxis_title="🎯 Projetos",
        font=dict(size=12),
        title_font_size=20,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Adicionar linha vertical para "hoje"
    today = datetime.now()
    fig.add_vline(
        x=today,
        line_dash="dash",
        line_color="red",
        line_width=2,
        annotation_text="📍 Hoje",
        annotation_position="top"
    )
    
    # Configurar hover
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>" +
                      "Início: %{x}<br>" +
                      "Fim: %{x2}<br>" +
                      "<extra></extra>"
    )
    
    return fig

def main():
    # Header principal
    st.title("🚀 Sistema de ROADMAP de Projetos")
    st.markdown("### Gerencie e visualize o cronograma dos seus projetos de forma interativa")
    
    # Carregar dados
    if st.session_state.projects_df is None:
        st.session_state.projects_df = load_projects()
        st.session_state.color_mapping = load_color_mapping()
    
    df = st.session_state.projects_df
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("🎨 Configurações de Cores")
        
        # Obter responsáveis únicos
        unique_responsaveis = df['Responsável/Status'].unique() if not df.empty else []
        
        # Configurar cores para cada responsável
        color_mapping = st.session_state.color_mapping.copy()
        
        for responsavel in unique_responsaveis:
            default_color = color_mapping.get(responsavel, '#FF6B6B')
            color = st.color_picker(
                f"Cor para {responsavel}",
                value=default_color,
                key=f"color_{responsavel}"
            )
            color_mapping[responsavel] = color
        
        # Adicionar novo responsável/status
        st.subheader("➕ Adicionar Novo Status")
        new_status = st.text_input("Nome do novo status/responsável:")
        if new_status and new_status not in unique_responsaveis:
            new_color = st.color_picker(f"Cor para {new_status}", value='#FF6B6B')
            if st.button("Adicionar Status"):
                color_mapping[new_status] = new_color
                st.success(f"Status '{new_status}' adicionado!")
        
        # Salvar configurações de cor
        if color_mapping != st.session_state.color_mapping:
            st.session_state.color_mapping = color_mapping
            save_color_mapping(color_mapping)
    
    # Área principal dividida em colunas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de Gantt
        st.subheader("📊 Visualização do Cronograma")
        if not df.empty:
            fig = create_gantt_chart(df, st.session_state.color_mapping)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum projeto encontrado. Adicione um novo projeto para começar!")
    
    with col2:
        # Estatísticas rápidas
        st.subheader("📈 Estatísticas")
        if not df.empty:
            total_projetos = len(df)
            projetos_em_andamento = len(df[
                (df['Início Previsto'] <= pd.Timestamp.now()) & 
                (df['Fim Previsto'] >= pd.Timestamp.now())
            ])
            projetos_futuros = len(df[df['Início Previsto'] > pd.Timestamp.now()])
            
            st.metric("Total de Projetos", total_projetos)
            st.metric("Em Andamento", projetos_em_andamento)
            st.metric("Futuros", projetos_futuros)
            
            # Responsáveis únicos
            st.write("**👥 Responsáveis:**")
            for resp in df['Responsável/Status'].unique():
                count = len(df[df['Responsável/Status'] == resp])
                st.write(f"• {resp}: {count} projeto(s)")
    
    # Seção de edição de projetos
    st.header("✏️ Gerenciar Projetos")
    
    tab1, tab2 = st.tabs(["📝 Editar Projeto Existente", "➕ Adicionar Novo Projeto"])
    
    with tab1:
        if not df.empty:
            selected_project = st.selectbox(
                "Selecione um projeto para editar:",
                df['Nome do Projeto'].tolist()
            )
            
            if selected_project:
                project_row = df[df['Nome do Projeto'] == selected_project].iloc[0]
                
                with st.form("edit_project_form"):
                    st.subheader(f"Editando: {selected_project}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_start = st.date_input(
                            "Início Previsto:",
                            value=project_row['Início Previsto'].date()
                        )
                    with col2:
                        new_end = st.date_input(
                            "Fim Previsto:",
                            value=project_row['Fim Previsto'].date()
                        )
                    
                    # Lista de responsáveis (incluindo novos adicionados)
                    all_responsaveis = list(df['Responsável/Status'].unique()) + list(st.session_state.color_mapping.keys())
                    all_responsaveis = list(set(all_responsaveis))  # Remove duplicatas
                    
                    current_responsavel = project_row['Responsável/Status']
                    if current_responsavel in all_responsaveis:
                        default_index = all_responsaveis.index(current_responsavel)
                    else:
                        default_index = 0
                    
                    new_responsavel = st.selectbox(
                        "Responsável/Status:",
                        all_responsaveis,
                        index=default_index
                    )
                    
                    submitted = st.form_submit_button("💾 Salvar Alterações")
                    
                    if submitted:
                        if new_start <= new_end:
                            # Atualizar projeto
                            df.loc[df['Nome do Projeto'] == selected_project, 'Início Previsto'] = pd.Timestamp(new_start)
                            df.loc[df['Nome do Projeto'] == selected_project, 'Fim Previsto'] = pd.Timestamp(new_end)
                            df.loc[df['Nome do Projeto'] == selected_project, 'Responsável/Status'] = new_responsavel
                            
                            # Salvar e atualizar estado
                            if save_projects(df):
                                st.session_state.projects_df = df
                                st.success("✅ Projeto atualizado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao salvar o projeto.")
                        else:
                            st.error("❌ A data de início deve ser anterior à data de fim.")
        else:
            st.info("Nenhum projeto disponível para edição.")
    
    with tab2:
        with st.form("new_project_form"):
            st.subheader("Criar Novo Projeto")
            
            project_name = st.text_input("Nome do Projeto:")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Início Previsto:")
            with col2:
                end_date = st.date_input("Fim Previsto:")
            
            # Lista de responsáveis disponíveis
            all_responsaveis = list(set(df['Responsável/Status'].unique().tolist() + list(st.session_state.color_mapping.keys())))
            if not all_responsaveis:
                all_responsaveis = ['Backend Team', 'Frontend Team', 'Data Team', 'Mobile Team']
            
            responsavel = st.selectbox("Responsável/Status:", all_responsaveis)
            
            submitted = st.form_submit_button("🚀 Criar Projeto")
            
            if submitted:
                if project_name.strip():
                    if project_name not in df['Nome do Projeto'].values:
                        if start_date <= end_date:
                            # Criar novo projeto
                            new_project = pd.DataFrame({
                                'Nome do Projeto': [project_name],
                                'Início Previsto': [pd.Timestamp(start_date)],
                                'Fim Previsto': [pd.Timestamp(end_date)],
                                'Responsável/Status': [responsavel]
                            })
                            
                            # Adicionar ao DataFrame
                            updated_df = pd.concat([df, new_project], ignore_index=True)
                            
                            # Salvar e atualizar estado
                            if save_projects(updated_df):
                                st.session_state.projects_df = updated_df
                                st.success("✅ Novo projeto criado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao salvar o novo projeto.")
                        else:
                            st.error("❌ A data de início deve ser anterior à data de fim.")
                    else:
                        st.error("❌ Já existe um projeto com este nome.")
                else:
                    st.error("❌ O nome do projeto não pode estar vazio.")

if __name__ == "__main__":
    main()
