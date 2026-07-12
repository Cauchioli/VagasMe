/**
 * Vértice OS — Script de Autopostagem de Carrossel no Instagram via Meta Graph API.
 * Este script lê as imagens do carrossel locais, assume que foram deployadas no site público,
 * cria os contêineres individuais no Meta, cria o contêiner do carrossel com a legenda,
 * e publica de forma 100% automática no Instagram feed.
 */

const fs = require('fs');
const path = require('path');

// Carrega as variáveis do .env ou do ambiente
const ACCESS_TOKEN = process.env.META_PAGE_ACCESS_TOKEN;
const IG_USER_ID = process.env.META_IG_USER_ID;
const SITE_URL = process.env.SITE_URL;

// Argumento: Caminho da pasta do post (ex: marketing/conteudo/slug-data)
const postFolder = process.argv[2];

if (!postFolder) {
  console.error("Erro: Informe o caminho da pasta do post. Ex: node postar-instagram.js marketing/conteudo/slug-data");
  process.exit(1);
}

if (!ACCESS_TOKEN || !IG_USER_ID || !SITE_URL) {
  console.error("Erro: Credenciais ausentes no arquivo .env (META_PAGE_ACCESS_TOKEN, META_IG_USER_ID, SITE_URL).");
  process.exit(1);
}

// Helper para fazer requisições POST HTTP nativas
async function metaRequest(endpoint, params) {
  const url = `https://graph.facebook.com/v20.0/${endpoint}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      access_token: ACCESS_TOKEN,
      ...params
    })
  });
  const data = await response.json();
  if (data.error) {
    throw new Error(data.error.message);
  }
  return data;
}

async function main() {
  try {
    const slug = path.basename(postFolder).split('-')[0]; // Pega o slug do post
    const instaFolder = path.join(postFolder, 'instagram');
    
    if (!fs.existsSync(instaFolder)) {
      throw new Error(`Pasta do Instagram não encontrada em: ${instaFolder}`);
    }

    // Lê a legenda do post
    const captionPath = path.join(postFolder, 'legenda.md');
    let caption = "";
    if (fs.existsSync(captionPath)) {
      caption = fs.readFileSync(captionPath, 'utf-8').trim();
    } else {
      console.warn("Aviso: Arquivo legenda.md não encontrado. Publicando sem legenda.");
    }

    // Lista os slides em PNG
    const files = fs.readdirSync(instaFolder)
      .filter(f => f.startsWith('slide-') && f.endsWith('.png'))
      .sort(); // Garante ordem slide-01, slide-02...

    if (files.length < 2) {
      throw new Error("Um carrossel do Instagram precisa ter pelo menos 2 slides.");
    }

    console.log(`=== Iniciando publicação automática de ${files.length} slides para o Instagram ===`);
    console.log(`Slug detectado: ${slug}`);
    
    // Passo 1: Criar contêiner de imagem para cada slide
    const childrenIds = [];
    for (let i = 0; i < files.length; i++) {
      const fileName = files[i];
      // A imagem precisa estar acessível publicamente no seu site para o Meta puxar
      const imageUrl = `${SITE_URL}/img/posts/${slug}/${fileName}`;
      console.log(`[${i+1}/${files.length}] Criando contêiner para: ${imageUrl}`);
      
      const itemContainer = await metaRequest(`${IG_USER_ID}/media`, {
        image_url: imageUrl,
        is_carousel_item: true
      });
      
      childrenIds.push(itemContainer.id);
      // Evita limite de taxa rápido
      await new Promise(r => setTimeout(r, 2000));
    }

    console.log("Todos os contêineres individuais criados:", childrenIds);

    // Passo 2: Criar contêiner do Carrossel principal
    console.log("Criando contêiner do Carrossel com a legenda...");
    const carouselContainer = await metaRequest(`${IG_USER_ID}/media`, {
      media_type: 'CAROUSEL',
      caption: caption,
      children: childrenIds
    });

    console.log("Contêiner do Carrossel criado com sucesso. ID:", carouselContainer.id);

    // Passo 3: Publicar o Carrossel
    console.log("Publicando o post no feed do Instagram...");
    const publishResult = await metaRequest(`${IG_USER_ID}/media_publish`, {
      creation_id: carouselContainer.id
    });

    console.log("====================================================");
    console.log("✔ SUCESSO! Post publicado no Instagram.");
    console.log("ID do Post:", publishResult.id);
    console.log("====================================================");

  } catch (error) {
    console.error("❌ ERRO na publicação do Instagram:", error.message);
    process.exit(1);
  }
}

main();
