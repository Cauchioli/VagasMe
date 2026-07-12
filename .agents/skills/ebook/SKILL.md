---
name: ebook
description: >
  Diagrama e gera e-books, playbooks e guias em formato Word (.docx) a partir de arquivos Markdown brutos, usando o Design System Vértice.
  Use quando o usuário pedir "criar ebook", "escrever playbook", "gerar manual", "diagramar texto", ou /ebook.
---

# /ebook — Diagramação Automática de E-books e Playbooks (Vértice OS)

Esta habilidade lê um arquivo de conteúdo em formato Markdown e o converte em um documento Word (.docx) impecavelmente formatado e diagramado com o Design System da Vértice (Slate + Dourado), incluindo Callout Boxes (avisos) e quebras de página automáticas.

---

## 🛠️ Dependências e Recursos

* **Entrada:** Arquivo `.md` bruto com o texto do e-book ou do playbook estratégico.
* **Script Motor:** `Pessoal/gerar_ebook_exito.js` (script Node.js que realiza o processamento).
* **Saída:** Gravar o arquivo Word diagramado final em `saidas/ebooks/[nome-do-ebook].docx`.

---

## 📐 Padrões de Diagramação e Estilos

O documento Word gerado segue as regras de design editorial:
1. **Tipografia:** Fonte principal `Outfit` para títulos e cabeçalhos, e `Inter` ou `Calibri` para o corpo do texto.
2. **Paleta de Cores:** Slate Escuro (`#1E293B`) para títulos principais, Ouro Vértice (`#B89047`) para subtítulos e destaques, e Slate Médio (`#334155`) para texto corrido.
3. **Parse de Markdown:** Tradução de `**negrito**`, `*itálico*` e `` `código` `` para estilos nativos do Word.
4. **Callout Boxes (Destaques):**
   - **Importante (Important):** Fundo vermelho suave (`#FEF2F2`), borda esquerda vermelha (`#EF4444`).
   - **Dica (Tip):** Fundo verde suave (`#ECFDF5`), borda esquerda verde (`#10B981`).
   - **Aviso (Warning):** Fundo amarelo suave (`#FFFBEB`), borda esquerda amarela/laranja (`#F59E0B`).

---

## 🚀 Workflow de Execução

1. **Leitura do Markdown:** Obtenha o conteúdo bruto que precisa ser transformado em e-book.
2. **Criação da Capa:** Insira uma capa de alta autoridade com o título em tamanho 36 bold, subtítulo e autoria da Vértice.
3. **Injeção de Callouts e Elementos:** O script Node.js processa o texto, detecta alertas em markdown (como `> [!IMPORTANT]`) e os converte em tabelas de Callout estilizadas com bordas coloridas.
4. **Geração:** Compila o arquivo `.docx` final e salva na pasta de saídas.
