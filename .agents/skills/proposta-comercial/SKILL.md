---
name: proposta-comercial
description: >
  Cria uma Proposta Comercial Premium em HTML/A4 (pronta para imprimir em PDF) customizada com o tom e design do cliente do Vértice OS, incluindo o playbook comercial/pitch de vendas ocultável.
  Use quando o usuário pedir "criar proposta", "proposta comercial", "gerar proposta de venda", ou /proposta-comercial.
---

# /proposta-comercial — Gerador de Propostas de Alto Padrão (Vértice OS)

Esta habilidade lê as informações do cliente em `_memoria/` e o design do cliente em `identidade/design-guide.md` e gera automaticamente um arquivo HTML de Proposta Comercial Premium A4 configurado e calibrado para impressão perfeita (Ctrl+P para salvar em PDF) sem URLs ou cabeçalhos do navegador nas bordas.

---

## 🛠️ Dependências e Recursos

* **Dados de Entrada:**
  - `_memoria/empresa.md` (Nome da empresa, consultor).
  - `_memoria/estrategia.md` (Escopo acordado e metas).
  - `identidade/design-guide.md` (Cores hex oficiais e fontes da marca).
* **Template Base:** `templates/proposta_template.html` (HTML calibrado com `@page` e `@media print`).
* **Saída:** Gravar o arquivo final em `saidas/propostas/proposta_[nome-do-cliente].html`.

---

## 📐 Regras de Calibração e Design

A I.A. deve processar o template e substituir as seguintes variáveis:
1. **Cores da Marca:** Substituir `--color-primary` (geralmente escuro), `--color-accent` (geralmente dourado ou cor de destaque) e as fontes oficiais.
2. **Playbook/Pitch no Topo:** A I.A. deve injetar o painel `.pitch-panel` com o roteiro de vendas específico para o serviço do cliente (ex: se for advocacia, um roteiro sobre captação de clientes jurídicos; se for consultoria, um roteiro B2B). Este painel será automaticamente ocultado na impressão de PDF.
3. **Módulos de Escopo:** Injetar os cards contendo os entregáveis do escopo acordado em formato de grade limpa (`.module-card`).
4. **Tabela de Investimento:** Formatar a tabela de preços (`.proposal-table`) com o setup de implantação, upsells e recorrências.

---

## 🚀 Workflow de Execução

1. **Definição de Escopo:** Pergunte ao usuário sobre o nome do cliente, o serviço proposto e os preços a praticar (ou pegue automaticamente das metas vigentes).
2. **Leitura da Identidade:** Extraia as cores e fontes de `design-guide.md` do cliente.
3. **Compilação do HTML:** Substitua as tags `{{BRAND_TITLE}}`, `{{COLOR_PRIMARY}}`, etc., no arquivo `templates/proposta_template.html`.
4. **Gravação:** Salve o arquivo na pasta de saídas e forneça o link clicável para o usuário abrir e imprimir em um clique.
