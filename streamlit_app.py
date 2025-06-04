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

# Função para criar dados de exemplo
def criar_dados_exemplo():
    hoje = datetime.now().date()
    dados = {
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

# Função para salvar dados
def salvar_dados(df):
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/projetos.csv', index=False)

# Função para carregar dados
def carregar_dados():
    try:
        if os.path.exists('data/projetos.csv'):
            df = pd.read_csv('data/projetos.csv')
            df['Início'] = pd.to_datetime(df['Início']).dt.date
            df['Fim'] = pd.to_datetime(df['Fim']).dt.date
            return df
        else:
            return criar_dados_exemplo()
    except:
        return criar_dados_exemplo()

# Título principal
st.title("🚀 ROADMAP de Projetos")
st.markdown("### Gerencie seus projetos de forma simples!")

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
                novo_projeto = pd.DataFrame({
                    'Nome do Projeto': [nome],
                    'Início': [inicio],
                    'Fim': [fim],
                    'Responsável': [responsavel]
                })
                
                st.session_state.df_projetos = pd.concat([df, novo_projeto], ignore_index=True)
                salvar_dados(st.session_state.df_projetos)
                st.success("✅ Projeto criado!")
                st.rerun()
            else:
                st.error("❌ Verifique os dados!")

# Área principal - dividida em duas colunas
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📊 Cronograma dos Projetos")
    
    if not df.empty:
        # Criar gráfico de Gantt
        fig = px.timeline(
            df,
            x_start="Início",
            x_end="Fim",
            y="Nome do Projeto",
            color="Responsável",
            title="Timeline dos Projetos",
            text="Nome do Projeto"  # Adicionar texto nas barras
        )
        
        # Configurar altura e mostrar texto nas barras
        fig.update_layout(height=400)
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
        
        # Configurar eixo X para mostrar quinzenas
        fig.update_xaxes(
            dtick="M1",  # Intervalo mensal
            tickformat="%b\n%Y",  # Formato do mês
            ticklabelmode="period"
        )
        
        # Adicionar linhas verticais para quinzenas
        # Pegar range de datas dos projetos
        data_min = df['Início'].min()
        data_max = df['Fim'].max()
        
        # Gerar datas de quinzenas no período
        from dateutil.relativedelta import relativedelta
        import calendar
        
        current_date = data_min.replace(day=1)  # Primeiro dia do mês inicial
        end_date = data_max + relativedelta(months=1)
        
        while current_date <= end_date:
            # Primeira quinzena (dia 1)
            fig.add_vline(
                x=current_date,
                line_width=1,
                line_dash="dot",
                line_color="gray",
                opacity=0.5
            )
            
            # Segunda quinzena (dia 16)
            dia_16 = current_date.replace(day=16)
            fig.add_vline(
                x=dia_16,
                line_width=1,
                line_dash="dot", 
                line_color="gray",
                opacity=0.5
            )
            
            # Adicionar labels das quinzenas
            mes_nome = current_date.strftime("%b")
            ano = current_date.strftime("%Y")
            
            # Label primeira quinzena
            fig.add_annotation(
                x=current_date + relativedelta(days=7),  # Meio da primeira quinzena
                y=-0.7,
                text=f"01-15/{mes_nome}",
                showarrow=False,
                font=dict(size=10, color="gray"),
                xanchor="center"
            )
            
            # Label segunda quinzena
            ultimo_dia = calendar.monthrange(current_date.year, current_date.month)[1]
            fig.add_annotation(
                x=dia_16 + relativedelta(days=7),  # Meio da segunda quinzena
                y=-0.7,
                text=f"16-{ultimo_dia}/{mes_nome}",
                showarrow=False,
                font=dict(size=10, color="gray"),
                xanchor="center"
            )
            
            # Próximo mês
            current_date += relativedelta(months=1)
        
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
    # Mostrar tabela editável
    st.subheader("📝 Projetos Atuais")
    
    # Seletor para excluir projeto
    col_edit, col_delete = st.columns([3, 1])
    
    with col_delete:
        st.subheader("🗑️ Excluir")
        projeto_para_excluir = st.selectbox(
            "Selecione projeto para excluir:",
            [""] + df['Nome do Projeto'].tolist()
        )
        
        if projeto_para_excluir and st.button("🗑️ Excluir Projeto"):
            st.session_state.df_projetos = df[df['Nome do Projeto'] != projeto_para_excluir]
            salvar_dados(st.session_state.df_projetos)
            st.success(f"✅ Projeto '{projeto_para_excluir}' excluído!")
            st.rerun()
    
    with col_edit:
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

# Footer
st.markdown("---")
st.markdown("💡 **Dica**: Use a barra lateral para adicionar novos projetos!")
