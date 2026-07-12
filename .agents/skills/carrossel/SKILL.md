---
name: carrossel
description: >
  Cria carrosséis e posts visuais interativos para o Instagram com o Design System da Vértice e simulação do app.
  Lê o template HTML e gera os slides com glows, tipografia editorial (Fraunces/Outfit) e lógica de arrasto.
  Use quando o usuário pedir "carrossel", "post", "conteúdo pro instagram", "criar imagem",
  "gerar foto", "post educativo", ou /carrossel.
---

# /carrossel — Carrossel e Posts Visuais Interativos (Vértice OS)

Esta habilidade cria posts e carrosséis com visual premium de alto nível editorial (Fraunces + Outfit), gerando um arquivo HTML interativo completo que simula a navegação real do Instagram (arrastar slides, teclado setas) no navegador.

---

## 🛠️ Dependências e Recursos

* **Identidade Visual:** `identidade/design-guide.md` (ler antes de definir as cores e handle).
* **Template Base:** `templates/carrossel_template.html` (ler e utilizar como esqueleto estrutural).
* **Avatar de Perfil:** Se o arquivo `identidade/logo.png` existir, converter em Base64 para injetar na tag do avatar. Caso contrário, usar a imagem do perfil do cache de métricas em `app/instagram_cache.json`.
* **Saída:** Gravar o arquivo HTML gerado em `marketing/conteudo/carrossel-[slug-do-tema]-[data]/carrossel.html` e criar a legenda final pronta em `legenda.txt` na mesma pasta.

---

## 📐 Padrão de Layouts dos Slides

Ao gerar a marcação HTML para a tag `{{SLIDES_HTML}}` do template, use a seguinte estrutura de classes e estilos para cada slide:

### Estrutura Geral de um Slide:
```html
<div class="slide">
  <!-- Glow decorativo de fundo (opcional, posicionado em cantos) -->
  <div class="glow glow-gold" style="width:320px;height:320px;top:-80px;right:-80px"></div>
  
  <!-- Marca d'água decorativa no fundo (opcional, ex: ponto de interrogação ou numeral) -->
  <div class="ghost-bg" style="font-size:180px;bottom:-20px;right:-20px">?</div>
  
  <div class="sc" style="justify-content:space-between; gap: 14px;">
    <!-- Conteúdo do Slide -->
  </div>
  
  <!-- Barra de progresso inferior (gerada dinamicamente) -->
  <div class="prog-wrap">
    <div class="prog-track">
      <div class="prog-fill" style="width: 9% /* calculo: (num_slide/total)*100 */"></div>
    </div>
    <span class="prog-count">1 / 11</span>
  </div>
  
  <!-- Seta de arrastar (incluso apenas se não for o último slide) -->
  <div class="swipe-r">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="rgba(255,255,255,0.22)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </div>
</div>
```

### Tipos de Layout de Conteúdo:

1. **CAPA (Slide 1):**
   * Contém a eyebrow/categoria do post: `<div class="tag">Métricas · Posicionamento</div>`.
   * Título principal com Fraunces eOutfit: `<div class="h1">Você sabe quanto está pagando por <em>cliente fechado?</em></div>`. Use `<em>` para dar o tom dourado/itálico característico da Vértice.
   * Linha de separação: `<div class="rule-gold" style="margin-bottom:14px"></div>`.
   * Subtítulo / descrição: `<p class="body">A conta que a maioria dos escritórios nunca faz.</p>`.

2. **DADO / NÚMERO GRANDE:**
   * Contém um número gigante e chamativo: `<div class="metric gold sz-xl">R$ 0</div>` (classes de tamanho: `sz-xl` 96px, `sz-lg` 64px, `sz-md` 40px).
   * Texto de apoio logo abaixo explicando o indicador.

3. **CARD DETALHADO (Informação / Dica):**
   * Use caixas de destaque translúcidas para agrupar conceitos: 
     - Card padrão: `<div class="card"><p class="body">Conteúdo</p></div>`.
     - Card em destaque (dourado): `<div class="card-gold"><p class="body">Mensagem Crítica</p></div>`.

4. **PASSO A PASSO (Steps):**
   * Use linhas ordenadas:
     ```html
     <div class="step-row">
       <div class="step-num">01</div>
       <div>
         <div class="step-title">Título do Passo</div>
         <p class="body" style="font-size:11px">Descrição do passo.</p>
       </div>
     </div>
     ```

5. **CTA FINAL (Último Slide):**
   * Resumo forte do post.
   * Apresenta 3 ações claras em lista com emojis ilustrativos (Salva, Comenta, Chama no direct).
   * Contém a pílula de CTA centralizada: `<div class="cta-pill">@handle <span style="opacity:.35;margin:0 4px">·</span> Vértice</div>`.

---

## 🚀 Workflow de Execução

1. **Ideação:** A partir do tema ou do acervo do RAG, planeje o fluxo de conteúdo dividindo-o em **5 a 11 slides** (sendo o Slide 1 a Capa e o último o CTA).
2. **Carregar Memória:** Obtenha o `@handle` e o `SUBTITLE` do negócio a partir do [design-guide.md](file:///c:/Users/WINDOWS11/Documents/identidade/design-guide.md). Se o design-guide estiver vazio, use o default `@leocauchiolli` e `Vértice · Posicionamento & IA` (para a marca do Leo).
3. **Puxar Avatar:** Se houver um arquivo de avatar em base64 pré-salvo, utilize-o. Se não, busque a imagem de perfil salva no cache local do Instagram.
4. **Montar Slides:** Escreva o HTML estruturado correspondente a cada slide dentro das especificações acima.
5. **Montar Dots (Pontinhos):** Gere a div de dots baseada no número total de slides:
   - Ex (para 5 slides): `<div class="dot active"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>`.
6. **Gerar HTML Final:** Leia o [carrossel_template.html](file:///c:/Users/WINDOWS11/Documents/templates/carrossel_template.html), substitua todos os placeholders (`{{HANDLE}}`, `{{SLIDES_HTML}}`, `{{DOTS_HTML}}`, etc.) e grave o resultado na pasta de marketing do tema.
7. **Gerar Legenda:** Escreva uma legenda no padrão de tom de voz da marca (curta, assertiva e contendo chamada para ação e hashtags) e salve-a na mesma pasta.
