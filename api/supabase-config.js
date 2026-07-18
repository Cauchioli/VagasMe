export default function handler(req, res) {
  // Permitir CORS para requisições do frontend
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Lê as variáveis de ambiente da Vercel (configuradas no dashboard),
  // com fallback para as credenciais do projeto Vagas.me
  const supabaseUrl =
    process.env.SUPABASE_URL ||
    process.env.NEXT_PUBLIC_SUPABASE_URL ||
    'https://aedpamfnemsdofbaxueo.supabase.co';

  const supabaseKey =
    process.env.SUPABASE_ANON_KEY ||
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
    'sb_publishable_94iW9NQBM8FD4OKwxwWz3A_9fikcPu9';

  res.status(200).json({ supabaseUrl, supabaseKey });
}
