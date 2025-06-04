import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

# Configuração da página
st.set_page_config(
    page_title="🚀 ROADMAP de Projetos",
    page_icon="🚀",
    layout="wide"
)

# Caminho do "banco de dados" CSV (adaptado para funcionar local e na nuvem)
import platform
if platform.system() == "Windows":
    CAMINHO_DADOS = r"C:\Users\vpaschoa\OneDrive - CARGLASS AUTOMOTIVA LTDA\Documentos\roadmap_projetos.csv"
else:
    # Para Streamlit Cloud ou outros sistemas
    CAMINHO_DADOS = "data/roadmap_projetos.csv"

# Função para criar dados de exemplo
def criar_dados_exemplo():
    hoje = datetime.now().date()
    dados = {
        'ID': [1, 2, 3, 4],
        'Nome do Projeto': [
            'Sistema de Login',
            'API de Pagamentos', 
            'Dashboard',
            'App Mobile'
        ],
        'Início': [
            hoje,
            hoje + timedelta(days=30),
            hoje + timedelta(days=60),
            hoje + timedelta(days=90)
        ],
        'Fim': [
            hoje + timedelta(days=45),
            hoje + timedelta(days=75),
            hoje + timedelta(days=105),
            hoje + timedelta(days=135)
        ],
        'Responsável': [
            'Backend Team',
            'FinTech Team',
            'Data Team',
            'Mobile Team'
        ]
    }
    return pd.DataFrame(dados)

# Função para salvar dados no CSV (adaptado para funcionar local e na nuvem)
def salvar_dados(df):
    try:
        # Garantir que o diretório existe
        diretorio = os.path.dirname(CAMINHO_DADOS)
        if diretorio:  # Só criar se o diretório não estiver vazio
            os.makedirs(diretorio, exist_ok=True)
        
        # Salvar no CSV
        df.to_csv(CAMINHO_DADOS, index=False)
        return True
    except Exception as e:
        st.error(f"❌ Erro ao salvar: {e}")
        # Fallback: salvar localmente
        try:
            os.makedirs('data', exist_ok=True)
            df.to_csv('data/roadmap_projetos.csv', index=False)
            st.info("💾 Dados salvos localmente em 'data/roadmap_projetos.csv'")
            return True
        except Exception as e2:
            st.error(f"❌ Erro também no salvamento local: {e2}")
            return False

# Função para carregar dados do CSV (adaptado para funcionar local e na nuvem)
def carregar_dados():
    try:
        if os.path.exists(CAMINHO_DADOS):
            df = pd.read_csv(CAMINHO_DADOS)
            df['Início'] = pd.to_datetime(df['Início']).dt.date
            df['Fim'] = pd.to_datetime(df['Fim']).dt.date
            return df
        elif os.path.exists('data/roadmap_projetos.csv'):
            # Fallback: carregar do arquivo local
            df = pd.read_csv('data/roadmap_projetos.csv')
            df['Início'] = pd.to_datetime(df['Início']).dt.date
            df['Fim'] = pd.to_datetime(df['Fim']).dt.date
            return df
        else:
            # Se não existe, criar dados de exemplo e salvar
            df = criar_dados_exemplo()
            salvar_dados(df)
            return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return criar_dados_exemplo()

# Função para obter próximo ID
def obter_proximo_id(df):
    if df.empty or 'ID' not in df.columns:
        return 1
    return df['ID'].max() + 1

# Título principal
st.title("🚀 ROADMAP de Projetos")
st.markdown("### Gerencie seus projetos de forma simples!")
st.info(f"📂 **Base de dados:** `{CAMINHO_DADOS}`")

# Carregar dados
if 'df_projetos' not in st.session_state:
    st.session_state.df_projetos = carregar_dados()

df = st.session_state.df_projetos

# Sidebar para adicionar projeto
with st.sidebar:
    st.header("➕ Novo Projeto")
    
    with st.form("novo_projeto"):
        nome = st.text_input("Nome do Projeto:")
        inicio = st.date_input("Data de Início:")
        fim = st.date_input("Data de Fim:")
        responsavel = st.selectbox("Responsável:", [
            'Backend Team', 'Frontend Team', 'Data Team', 
            'Mobile Team', 'QA Team', 'DevOps Team'
        ])
        
        if st.form_submit_button("🚀 Criar Projeto"):
            if nome and inicio <= fim:
                novo_id = obter_proximo_id(df)
                novo_projeto = pd.DataFrame({
                    'ID': [novo_id],
                    'Nome do Projeto': [nome],
                    'Início': [inicio],
                    'Fim': [fim],
                    'Responsável': [responsavel]
                })
                
                st.session_state.df_projetos = pd.concat([df, novo_projeto], ignore_index=True)
                if salvar_dados(st.session_state.df_projetos):
                    st.success("✅ Projeto criado e salvo!")
                    st.rerun()
            else:
                st.error("❌ Verifique os dados!")

# Área principal - dividida em duas colunas
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📊 Cronograma dos Projetos")
    
    if not df.empty:
        # Criar gráfico de Gantt com barra de rolagem
        fig = px.timeline(
            df,
            x_start="Início",
            x_end="Fim",
            y="Nome do Projeto",
            color="Responsável",
            title="Timeline dos Projetos",
            text="Nome do Projeto"
        )
        
        # Configurar altura e barra de rolagem
        fig.update_layout(
            height=400,
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        fig.update_traces(textposition="inside", textfont_size=12)
        
        # Adicionar linha vermelha para "hoje"
        hoje = datetime.now()
        fig.add_shape(
            type="line",
            x0=hoje, x1=hoje,
            y0=-0.5, y1=len(df)-0.5,
            line=dict(color="red", width=3, dash="dash")
        )
        
        # Adicionar anotação "HOJE"
        fig.add_annotation(
            x=hoje,
            y=len(df)-0.5,
            text="HOJE",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red",
            bgcolor="red",
            bordercolor="red",
            font=dict(color="white", size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Adicione projetos na barra lateral para ver o cronograma!")

with col2:
    st.subheader("📈 Resumo")
    
    if not df.empty:
        total = len(df)
        hoje = datetime.now().date()
        
        em_andamento = len(df[
            (df['Início'] <= hoje) & (df['Fim'] >= hoje)
        ])
        
        futuros = len(df[df['Início'] > hoje])
        
        st.metric("Total de Projetos", total)
        st.metric("Em Andamento", em_andamento)
        st.metric("Futuros", futuros)
        
        st.subheader("👥 Por Responsável")
        responsaveis = df['Responsável'].value_counts()
        for resp, count in responsaveis.items():
            st.write(f"• {resp}: {count}")

# Seção para editar/excluir projetos
st.header("✏️ Gerenciar Projetos")

if not df.empty:
    # Abas para diferentes operações
    tab1, tab2, tab3 = st.tabs(["📝 Editar Projeto", "📋 Projetos Atuais", "🗑️ Excluir"])
    
    with tab1:
        st.subheader("✏️ Editar Projeto")
        
        # Seletor de projeto para editar
        projeto_para_editar = st.selectbox(
            "Selecione um projeto para editar:",
            df['Nome do Projeto'].tolist(),
            key="editar_projeto"
        )
        
        if projeto_para_editar:
            # Buscar dados do projeto selecionado
            projeto_atual = df[df['Nome do Projeto'] == projeto_para_editar].iloc[0]
            
            with st.form("editar_projeto_form"):
                col_edit1, col_edit2 = st.columns(2)
                
                with col_edit1:
                    novo_nome = st.text_input(
                        "Nome do Projeto:", 
                        value=projeto_atual['Nome do Projeto']
                    )
                    nova_data_inicio = st.date_input(
                        "Data de Início:", 
                        value=projeto_atual['Início']
                    )
                
                with col_edit2:
                    opcoes_responsavel = ['Backend Team', 'Frontend Team', 'Data Team', 
                                        'Mobile Team', 'QA Team', 'DevOps Team']
                    
                    # Buscar índice do responsável atual de forma segura
                    try:
                        indice_atual = opcoes_responsavel.index(projeto_atual['Responsável'])
                    except ValueError:
                        # Se não encontrar, usar 0 como padrão
                        indice_atual = 0
                    
                    novo_responsavel = st.selectbox(
                        "Responsável:",
                        opcoes_responsavel,
                        index=indice_atual
                    )
                    nova_data_fim = st.date_input(
                        "Data de Fim:", 
                        value=projeto_atual['Fim']
                    )
                
                if st.form_submit_button("💾 Salvar Alterações"):
                    if novo_nome and nova_data_inicio <= nova_data_fim:
                        # Atualizar projeto
                        idx = df[df['Nome do Projeto'] == projeto_para_editar].index[0]
                        st.session_state.df_projetos.loc[idx, 'Nome do Projeto'] = novo_nome
                        st.session_state.df_projetos.loc[idx, 'Início'] = nova_data_inicio
                        st.session_state.df_projetos.loc[idx, 'Fim'] = nova_data_fim
                        st.session_state.df_projetos.loc[idx, 'Responsável'] = novo_responsavel
                        
                        if salvar_dados(st.session_state.df_projetos):
                            st.success("✅ Projeto atualizado e salvo!")
                            st.rerun()
                    else:
                        st.error("❌ Verifique os dados!")
    
    with tab2:
        st.subheader("📋 Projetos Atuais")
        
        # Mostrar tabela de projetos
        st.dataframe(df, use_container_width=True)
        
        # Botão para download CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Baixar CSV",
            data=csv,
            file_name=f"projetos_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.subheader("🗑️ Excluir Projeto")
        
        projeto_para_excluir = st.selectbox(
            "Selecione projeto para excluir:",
            [""] + df['Nome do Projeto'].tolist(),
            key="excluir_projeto"
        )
        
        if projeto_para_excluir:
            # Mostrar detalhes do projeto
            projeto_detalhes = df[df['Nome do Projeto'] == projeto_para_excluir].iloc[0]
            
            st.warning(f"""
            **⚠️ Você está prestes a excluir:**
            - **Projeto:** {projeto_detalhes['Nome do Projeto']}
            - **Período:** {projeto_detalhes['Início']} até {projeto_detalhes['Fim']}
            - **Responsável:** {projeto_detalhes['Responsável']}
            """)
            
            col_confirm, col_cancel = st.columns([1, 1])
            
            with col_confirm:
                if st.button("🗑️ CONFIRMAR EXCLUSÃO", type="primary"):
                    st.session_state.df_projetos = df[df['Nome do Projeto'] != projeto_para_excluir].reset_index(drop=True)
                    if salvar_dados(st.session_state.df_projetos):
                        st.success(f"✅ Projeto '{projeto_para_excluir}' excluído e salvo!")
                        st.rerun()
            
            with col_cancel:
                if st.button("❌ Cancelar"):
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("💡 **Dica**: Todos os dados são salvos automaticamente no seu PC!")
st.markdown(f"📂 **Localização:** `{CAMINHO_DADOS}`")
