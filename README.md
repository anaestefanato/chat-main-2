# Aplicação de Chat com Autenticação Básica

**Guia Completo** | **Stack:** FastAPI + Jinja2 + SQLite + SSE

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Setup Inicial do Projeto](#setup-inicial-do-projeto)
3. [Estrutura de Arquivos](#estrutura-de-arquivos)
4. [Dependências](#dependências)
5. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
6. [Sistema de Autenticação](#sistema-de-autenticação)
7. [Sistema de Chat](#sistema-de-chat)
8. [Frontend - Páginas](#frontend---páginas)
9. [Componente de Chat](#componente-de-chat)
10. [Arquivo Principal](#arquivo-principal)
11. [Executando a Aplicação](#executando-a-aplicação)

---

## Visão Geral

Este guia apresenta um passo a passo completo para criar uma aplicação web com:

- **Autenticação básica** (sem refresh tokens) usando sessões
- **Chat em tempo real** entre usuários logados usando Server-Sent Events (SSE)
- **4 páginas principais:** Login, Cadastro, Home (com widget de chat)
- **Componente de chat independente** e reutilizável

### Arquitetura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │ ←── │   FastAPI   │ ←── │   SQLite    │
│  (Jinja2)   │     │   Backend   │     │  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
       ↑                   │
       │                   │
       └───── SSE ─────────┘
        (Tempo Real)
```

---

## Setup Inicial do Projeto

Esta seção guia você na criação do projeto do zero, incluindo ambiente virtual, estrutura de pastas e integração com GitHub.

### 2.1 Criar Pasta do Projeto

1. Abra o **VS Code**
2. Vá em **File > Open Folder...**
3. Navegue até onde deseja criar o projeto
4. Clique em **New Folder** e crie uma pasta chamada `chat-app`
5. Selecione a pasta criada e clique em **Open**

### 2.2 Inicializar Repositório Git

1. Abra o terminal integrado: **Terminal > New Terminal** (ou `Ctrl+`` `)
2. Execute os comandos:

```bash
# Inicializa repositório Git
git init

# Configura usuário (se ainda não configurado globalmente)
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

### 2.3 Criar Arquivo .gitignore

Crie o arquivo `.gitignore` na raiz do projeto com o seguinte conteúdo:

```gitignore
# Ambiente virtual Python
.venv/
venv/
env/

# Arquivos Python compilados
__pycache__/
*.py[cod]
*$py.class

# Banco de dados SQLite
*.db

# Variáveis de ambiente
.env

# IDE
.vscode/
.idea/

# Sistema operacional
.DS_Store
Thumbs.db
```

### 2.4 Criar Ambiente Virtual Python

No terminal integrado do VS Code:

```bash
# Cria o ambiente virtual
python -m venv .venv

# Ativa o ambiente virtual
# No macOS/Linux:
source .venv/bin/activate

# No Windows:
.venv\Scripts\activate
```

Após ativar, você verá `(.venv)` no início da linha do terminal.

### 2.5 Selecionar Interpretador Python no VS Code

1. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no macOS)
2. Digite "Python: Select Interpreter"
3. Selecione o interpretador dentro da pasta `.venv`

### 2.6 Criar Estrutura de Diretórios

Execute no terminal:

```bash
mkdir -p model repo routes dtos util templates/components static/css static/js
```

### 2.7 Configurar VS Code para Debug (launch.json)

1. Crie a pasta `.vscode` na raiz do projeto:

```bash
mkdir .vscode
```

2. Crie o arquivo `.vscode/launch.json` com o conteúdo:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Chat App",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

Agora você pode executar o projeto com:
- **F5**: Executa com debugger (breakpoints funcionam)
- **Ctrl+F5**: Executa sem debugger (mais rápido)

### 2.8 Criar Repositório no GitHub

0. Adicione esse arquivo **CHAT.md** à raiz do projeto e renomeie para **README.md**.

1. Clique no ícone/extensão **Source Control** na barra de ferramentas do VSCode.

2. Adicione a mensagem "versao inicial" no campo de texto do commit e clique no botão **Commit**.

3. Clique no botão **Publish Branch**, selecione **Public Repository** na caixa de seleção que se abrir, e mantenha o nome **chat-app**.

---

## Estrutura de Arquivos

```
chat-app/
├── .vscode/
│   └── launch.json                  # Configuração de debug
├── .gitignore                       # Arquivos ignorados pelo Git
├── main.py                          # Ponto de entrada da aplicação
├── requirements.txt                 # Dependências Python
├── database.db                      # Banco SQLite (criado automaticamente)
│
├── model/                           # Modelos de dados
│   ├── usuario_model.py
│   ├── chat_sala_model.py
│   ├── chat_mensagem_model.py
│   └── chat_participante_model.py
│
├── repo/                            # Camada de repositório (acesso a dados)
│   ├── usuario_repo.py
│   ├── chat_sala_repo.py
│   ├── chat_mensagem_repo.py
│   └── chat_participante_repo.py
│
├── routes/                          # Rotas da API
│   ├── auth_routes.py
│   └── chat_routes.py
│
├── dtos/                            # Data Transfer Objects (validação)
│   ├── auth_dto.py
│   └── chat_dto.py
│
├── util/                            # Utilitários
│   ├── database.py
│   ├── security.py
│   ├── auth_decorator.py
│   ├── chat_manager.py
│   └── flash_messages.py
│
├── templates/                       # Templates Jinja2
│   ├── base.html
│   ├── login.html
│   ├── cadastro.html
│   ├── home.html
│   └── components/
│       └── chat_widget.html
│
└── static/                          # Arquivos estáticos
    ├── css/
    │   └── chat-widget.css
    └── js/
        └── chat-widget.js
```

---

## Dependências

### requirements.txt

```txt
# Framework Web
fastapi==0.115.0
uvicorn[standard]==0.32.0

# Templates
jinja2==3.1.4

# Validação
pydantic==2.9.2
pydantic[email]==2.9.2

# Segurança
passlib[bcrypt]==1.7.4
bcrypt>=3.2.0,<4.0.0
python-multipart==0.0.12

# Sessões
itsdangerous==2.2.0
```

### Instalação

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

---

## Configuração do Banco de Dados

(README copy truncated here for brevity. Full CHAT.md content is preserved in `CHAT.md`.)
