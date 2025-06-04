# 🚀 Sistema de ROADMAP de Projetos

Um sistema completo para visualização e gerenciamento de cronogramas de projetos, desenvolvido com Streamlit, Python e tecnologias modernas.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração](#configuração)
- [Desenvolvimento](#desenvolvimento)
- [Contribuição](#contribuição)

## 🎯 Visão Geral

O Sistema de ROADMAP de Projetos é uma ferramenta web interativa que permite:

- **Visualização em Gráfico de Gantt**: Timeline interativo com zoom, pan e hover
- **Múltiplas Visualizações**: Timeline, Kanban e Lista
- **Gerenciamento Completo**: Criar, editar, excluir e acompanhar projetos
- **Persistência de Dados**: Suporte a SQLite, PostgreSQL, MySQL e CSV
- **Interface Moderna**: Design responsivo e intuitivo
- **Componentes Interativos**: Arrastar e soltar (em desenvolvimento)

## ✨ Funcionalidades

### 📊 Funcionalidades Implementadas

#### Visualização
- [x] Gráfico de Gantt interativo com Plotly
- [x] Visualização Kanban por status
- [x] Visualização em lista editável
- [x] Métricas e dashboards
- [x] Linha "Hoje" no cronograma
- [x] Cores customizáveis por responsável

#### Gerenciamento de Projetos
- [x] Criar novos projetos
- [x] Editar projetos existentes
- [x] Excluir projetos
- [x] Campos: nome, datas, responsável, prioridade, progresso, descrição
- [x] Validação de dados

#### Persistência
- [x] Salvamento em CSV (desenvolvimento)
- [x] Banco SQLite (produção)
- [x] Backup automático
- [x] Exportação de dados

#### Interface
- [x] Design responsivo
- [x] Sidebar com configurações
- [x] Temas de cores
- [x] Feedback visual (sucessos/erros)

### 🔄 Funcionalidades em Desenvolvimento

#### Interatividade Avançada
- [ ] Arrastar e soltar barras no gráfico
- [ ] Redimensionar duração de projetos
- [ ] Edição inline no timeline

#### Funcionalidades Avançadas
- [ ] Dependências entre projetos
- [ ] Marcos (milestones)
- [ ] Notificações de prazos
- [ ] Relatórios automatizados

#### Integrações
- [ ] Autenticação de usuários
- [ ] API REST
- [ ] Integração com calendários
- [ ] Webhooks

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Rápida

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd sistema-roadmap
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**:
```bash
streamlit run streamlit_app.py
```

4. **Acesse no navegador**:
```
http://localhost:8501
```

### Instalação com Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run streamlit_app.py
```

## 📖 Uso

### Primeira Execução

1. **Ao iniciar**, o sistema criará automaticamente:
   - Diretório `data/` para armazenamento
   - Arquivo `projects.csv` com projetos de exemplo
   - Banco SQLite (se configurado)

2. **Interface Principal**:
   - **Header**: Métricas e estatísticas gerais
   - **Área Central**: Gráfico de Gantt interativo
   - **Sidebar**: Configurações e controles
   - **Abas**: Editar, Criar e Excluir projetos

### Gerenciando Projetos

#### ➕ Criar Novo Projeto
1. Vá para a aba "➕ Novo Projeto"
2. Preencha os campos obrigatórios:
   - Nome do projeto
   - Data de início
   - Data de fim
   - Responsável/Status
3. Opcionalmente:
   - Descrição
   - Prioridade
   - Progresso inicial
4. Clique em "🚀 Criar Projeto"

#### ✏️ Editar Projeto
1. Vá para a aba "📝 Editar Projeto"
2. Selecione o projeto no dropdown
3. Modifique os campos desejados
4. Clique em "💾 Salvar Alterações"

#### 🗑️ Excluir Projeto
1. Vá para a aba "🗑️ Excluir Projeto"
2. Selecione o projeto
3. Revise os detalhes
4. Confirme a exclusão

### Configurações

#### 🎨 Cores dos Responsáveis
- Use a sidebar para configurar cores
- Cada responsável/status tem uma cor única
- Adicione novos responsáveis conforme necessário

#### 👁️ Modos de Visualização
- **Timeline**: Gráfico de Gantt tradicional
- **Kanban**: Cartões organizados por status
- **Lista**: Tabela editável com todos os projetos

#### 💾 Exportação
- Use o botão "📄 Exportar CSV" na sidebar
- Arquivo será baixado com data atual no nome

## 📁 Estrutura do Projeto

```
sistema-roadmap/
├── streamlit_app.py          # Aplicação Streamlit básica
├── app_avancado.py          # Aplicação com todas as funcionalidades
├── database_manager.py      # Gerenciamento de banco de dados
├── config.py               # Configurações do sistema
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
├── data/                  # Diretório de dados
│   ├── projects.csv       # Projetos (CSV)
│   ├── roadmap.db        # Banco SQLite
│   └── color_mapping.json # Mapeamento de cores
└── components/           # Componentes customizados
    └── interactive_gantt.html # Gráfico interativo
```

### Arquivos Principais

- **`streamlit_app.py`**: Versão básica e funcional
- **`app_avancado.py`**: Versão completa com todas as funcionalidades
- **`database_manager.py`**: Abstração para diferentes bancos de dados
- **`config.py`**: Configurações centralizadas

## ⚙️ Configuração

### Banco de Dados

O sistema suporta múltiplos tipos de armazenamento:

#### SQLite (Recomendado para produção)
```python
# config.py
DATABASE_TYPE = "sqlite"
DATABASE_URL = "data/roadmap.db"
```

#### CSV (Desenvolvimento)
```python
# config.py
DATABASE_TYPE = "csv"
DATABASE_URL = "data/projects.csv"
```

#### PostgreSQL (Produção avançada)
```python
# config.py
DATABASE_TYPE = "postgresql"
DATABASE_URL = "postgresql://user:pass@localhost/roadmap"
```

### Variáveis de Ambiente

Crie um arquivo `.env` para configurações sensíveis:

```env
DATABASE_URL=postgresql://user:password@localhost/roadmap
SECRET_KEY=sua-chave-secreta-aqui
ENVIRONMENT=production
```

### Configurações Avançadas

```python
# config.py
class Config:
    # Features habilitadas
    ENABLE_DRAG_DROP = True
    ENABLE_DEPENDENCIES = True
    ENABLE_NOTIFICATIONS = False
    
    # Autenticação
    ENABLE_AUTH = False
    AUTH_PROVIDERS = ["google", "github"]
    
    # Backup
    AUTO_BACKUP = True
    BACKUP_INTERVAL_HOURS = 24
```

## 🛠️ Desenvolvimento

### Executando em Modo de Desenvolvimento

```bash
# Usar a versão básica
streamlit run streamlit_app.py

# Usar a versão avançada
streamlit run app_avancado.py
```

### Estrutura de Classes

#### DatabaseManager
Gerencia a persistência de dados com suporte a múltiplos backends:

```python
# Exemplo de uso
from database_manager import DatabaseManager, DatabaseType, Project

db = DatabaseManager(DatabaseType.SQLITE)
project = Project(...)
project_id = db.create_project(project)
```

#### RoadmapApp
Classe principal da aplicação Streamlit:

```python
# app_avancado.py
app = RoadmapApp()
app.run()
```

### Adicionando Novas Funcionalidades

1. **Nova visualização**:
   - Adicione método `render_nova_view()` na classe `RoadmapApp`
   - Atualize o seletor de modo na sidebar

2. **Novo campo no projeto**:
   - Modifique a classe `Project` em `database_manager.py`
   - Atualize o schema do banco (SQLite)
   - Adicione campos nos formulários

3. **Nova integração**:
   - Crie módulo específico (ex: `email_notifier.py`)
   - Adicione configurações em `config.py`
   - Integre na aplicação principal

### Componentes Customizados

Para criar componentes Streamlit personalizados:
