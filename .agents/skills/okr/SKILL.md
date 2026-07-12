---
name: okr
description: >
  Cria o planejamento estratégico de OKRs, metas anuais e rituais de gestão em formato Word (.docx) estruturado para o negócio do cliente.
  Use quando o usuário pedir "planejamento estratégico", "okrs", "metas trimestrais", "documento de gestão", ou /okr.
---

# /okr — Planejamento Estratégico de OKRs e Metas (Vértice OS)

Esta habilidade lê o contexto do cliente em `_memoria/` e escreve um arquivo Word (.docx) estruturado contendo o planejamento de metas, OKRs, organograma e rituais de gestão do negócio com base na lógica do script `gerar_okr.py`.

---

## 🛠️ Dependências e Recursos

* **Dados de Entrada:**
  - `_memoria/empresa.md` (Nome da empresa, fundadores, stack).
  - `_memoria/estrategia.md` (Foco atual, metas do trimestre).
* **Script Motor:** `scripts/gerar_okr.py` (ou executa o interpretador python no script original).
* **Saída:** Gravar o arquivo Word final em `saidas/planejamento/planejamento_okrs_[nome-empresa].docx`.

---

## 📐 Estrutura do Documento Gerado

O Word gerado deve seguir o padrão visual corporativo e sóbrio da Vértice (Slate + Azul + Dourado):
1. **Capa Centralizada:** Título da empresa em tamanho 30, subtítulo de planejamento em tamanho 18 e assinatura.
2. **Índice de Seções:** Organização do plano (Missão, Organograma, OKRs Q3/Q4, KPIs, Metas Anuais, Finanças, Rituais).
3. **Seção 1: Missão, Visão e Valores:** Declaração estruturada dos princípios do fundador.
4. **Seção 2: Estrutura & Organograma:** Papéis de cada membro ou setores.
5. **Seção 3: OKRs (Q3 + Q4):** Tabela contendo Objetivos (foco aspiracional) e Key Results (métricas de sucesso quantificáveis).
6. **Seção 4: KPIs por Área:** Métricas de monitoramento contínuo de Marketing, Vendas e Operação.
7. **Seção 5: Metas Anuais:** Horizonte estratégico de crescimento.
8. **Seção 6: Rituais de Gestão:** Frequência de reuniões de alinhamento (daily, weekly, mensal).

---

## 🚀 Workflow de Execução

1. **Leitura de Contexto:** Varra os arquivos `empresa.md` e `estrategia.md` do cliente para mapear o status atual.
2. **Personalização:** Se as metas em `estrategia.md` estiverem desatualizadas, pergunte ao cliente se deseja refiná-las antes.
3. **Geração do Código/Script:** Utilize o script Python local para montar o documento, preenchendo as tabelas de forma dinâmica com os dados do cliente.
4. **Exportação:** Salve o arquivo na pasta de saídas e avise o usuário onde o documento `.docx` de alta qualidade foi gravado.
