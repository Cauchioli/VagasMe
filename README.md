# Vagas.me — Recrutamento Inteligente por I.A.

O **Vagas.me** é uma plataforma SaaS (HETech) que transforma o processo de recrutamento e seleção corporativo. Ele combina o poder da Inteligência Artificial local para triagem semântica de currículos com um **Segundo Cérebro** (Obsidian) de contratação, **Dashboard Web interativo** em tempo real e gerenciamento de candidatos estilo Kanban.

---

## 🗺️ Estrutura do Repositório

O repositório está organizado para facilitar o desenvolvimento modular e implantação:

```
├── .agents/                 # Regras do Agente & Motores de Habilidades (Skills)
│   ├── AGENTS.md            # Leis operacionais e regras de design da marca
│   └── skills/              # As skills operacionais copiadas do template
├── _memoria/                # Contexto estratégico do projeto (Obsidian)
│   ├── empresa.md           # Fatos, serviços, stack e perfil da Vagas.me
│   ├── estrategia.md        # Gargalos atuais, marcos e foco do MVP
│   └── preferencias.md      # Tom de voz, escrita e diretrizes de comunicação
├── identidade/              # Design System do Cliente
│   └── design-guide.md      # Cores hexadecimais, fontes e caminhos de logo
├── app/                     # Painel Visual de Controle (Web App)
│   ├── app_backend.py       # Servidor local Python Flask/FastAPI (Porta 5000)
│   ├── index.html           # SPA Dashboard (Kanban de vagas, candidatos e match)
│   ├── crm_database.json    # Banco de dados leve dos Leads/Candidatos
│   └── instagram_cache.json # Cache de dados e métricas
├── rag/                     # Módulo RAG Local
│   └── rag_acervo.py        # Script Python para indexar notas e currículos
└── README.md                # Este guia
```

---

## 🧠 1. Configurando o Segundo Cérebro (Obsidian)

O Obsidian funciona como a base de dados de texto e documentação do projeto.

1. Baixe e instale o [Obsidian](https://obsidian.md/).
2. Aponte para a pasta `_memoria` ou crie um novo Vault contendo a documentação.
3. Copie o arquivo [.agents/AGENTS.md](file:///.agents/AGENTS.md) para a raiz do seu Obsidian para calibração automática do agente de IA.

---

## 🔍 2. Configurando o RAG Local (Triagem Segura)

A IA local lê e indexa os currículos de forma segura e local, respeitando a privacidade dos dados.

1. Vá para a pasta `/rag`:
   ```bash
   cd rag
   ```
2. Crie e ative o ambiente virtual Python:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   ```
3. Instale as dependências e rode o indexador:
   ```bash
   pip install -r requirements.txt
   python rag_acervo.py index
   ```

---

## 🖥️ 3. Iniciando o Web App (Dashboard)

O painel centraliza as vagas abertas, o pipeline de candidatos (Kanban) e a pontuação de match de currículos.

1. Inicie o servidor backend em `/app`:
   ```bash
   python app_backend.py
   ```
2. Abra o arquivo `/app/index.html` no navegador para acessar a central visual do Vagas.me.
