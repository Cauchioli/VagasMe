# Vértice OS — Segundo Cérebro (Obsidian) & RAG Local

Este manual descreve o funcionamento, a taxonomia de organização e os passos operacionais do **Cérebro Digital Unificado** do Vértice OS. Ele combina a curadoria manual do **Obsidian** (para ideias refinadas e processos) com a capacidade de recall em massa do **RAG Local** (para arquivos pesados como contratos, PDFs, e-mails e playbooks brutos).

---

## 🧬 1. A Filosofia: Curadoria vs. Acervo Bruto

Para evitar que o seu espaço de trabalho no Obsidian fique lento ou poluído de arquivos mortos, separamos o conhecimento em duas camadas complementares:

```
┌──────────────────────────────────────────┐
│             OBSIDIAN VAULT               │
│ (Camada Curada: Notas Denses e Limpas)   │
└──────────────────┬───────────────────────┘
                   │ consulta (http)
┌──────────────────▼───────────────────────┐
│               RAG LOCAL                  │
│ (Acervo Bruto: GBs de PDFs, Docs e Logs)  │
└──────────────────────────────────────────┘
```

1. **Obsidian Vault (Alto Sinal):** Onde vivem apenas notas escritas por você ou filtradas pela I.A. Contém checklists de rotinas, resumos estratégicos, decisões importantes e lições aprendidas. É versionável e leve.
2. **RAG Local (Alto Recall):** O banco de dados semântico que armazena o acervo bruto de documentos (atas, relatórios longos, planilhas, arquivos de clientes). Ele vive fora do Obsidian e permite que a I.A. encontre fatos instantaneamente em qualquer documento do seu computador, citando a fonte.

---

## 🗂️ 2. Taxonomia Geral (Sua Estrutura de Notas)

No Obsidian, não organizamos notas apenas por temas (que mudam a todo momento), mas sim pelo **tipo e utilidade** da nota. Use esta estrutura de pastas e prefixos:

* **`00-mocs/` (Map of Content):** Notas-hubs que organizam temas ou projetos. Ex: `MOC-Comercial.md`, `MOC-Projetos.md`. É o índice visual do seu grafo.
* **`10-contexto/` (Pastas e Fichas de Casos / Projetos / Pessoas):** Dados temporais sobre algo específico. Use o prefixo **`CTX-`**. Ex: `CTX-Cliente-XPTO.md`, `CTX-Contrato-Parceria.md`.
* **`20-operacional/` (Procedimentos / Lições Reutilizáveis / Teses):** O conhecimento estruturado e perene da sua empresa. Use o prefixo **`OP-`**. Ex: `OP-Script-Fechamento.md`, `OP-Tese-Precificacao-Boutique.md`.
* **`90-templates/`:** Modelos de notas para criar novos CTXs ou OPs em um clique.
* **`AI/sessions/`:** Logs e históricos de conversas com copilotos de I.A.

---

## 🔍 3. RAG Local (Instalação e Uso Automático)

O sistema de busca do Vértice OS roda localmente no seu computador (100% offline e seguro para conformidade ética e LGPD).

### A. Instalação das Dependências
Para instalar o ecossistema automaticamente, abra o terminal na pasta raiz e execute:
```bash
python install_rag.py
```
*O script detectará se a sua máquina possui placas de processamento gráfico NVIDIA ou AMD dedicadas para acelerar a geração de IA, configurando o ambiente virtual (.venv) e instalando as bibliotecas ideais.*

### B. Indexando Documentos
Para indexar os seus arquivos e atualizar a base do assistente, basta executar:
```bash
python rag/rag_acervo.py index
```
*Dica: Você pode agendar este comando para rodar todas as noites, mantendo a I.A. atualizada com os novos documentos salvos no dia.*

### C. Rodando o Servidor
O servidor mantém o modelo carregado na memória RAM, garantindo respostas de busca instantâneas. Inicie-o com:
```bash
python rag/rag_server.py
```

---

## 🤝 4. Grounding (Ancoragem Anti-Alucinação)

Toda vez que a I.A. do Vértice OS redigir uma petição, artigo de blog, proposta comercial ou relatório financeiro, ela usará a ferramenta `rag.py` para buscar trechos reais do seu acervo.

Na saída gerada, a I.A. obrigatoriamente listará a **FONTE** (caminho absoluto do arquivo indexado) ao lado da afirmação correspondente. Isso elimina alucinações e garante rastreabilidade total de dados.
