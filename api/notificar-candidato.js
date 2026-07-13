// Vercel Serverless Function: Notificação por E-mail do Candidato (Kanban Stage)

export default async function handler(req, res) {
  // Configurar cabeçalhos de CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Método não permitido. Utilize POST.' });
  }

  const { candidatoEmail, candidatoNome, vagaEmpresa, vagaCargo, novoStatus } = req.body;

  if (!candidatoEmail || !candidatoNome || !vagaEmpresa || !vagaCargo || !novoStatus) {
    return res.status(400).json({ error: 'Parâmetros incompletos. Por favor envie todos os dados do candidato e da vaga.' });
  }

  // Mapear status para textos amigáveis em português
  const statusTexts = {
    applied: {
      assunto: `Candidatura recebida no Vagas.me: ${vagaCargo} - ${vagaEmpresa}`,
      corpo: `Olá, ${candidatoNome}! Seu currículo foi enviado com sucesso para a vaga de ${vagaCargo} na empresa ${vagaEmpresa}. Fique atento ao painel para acompanhar as atualizações.`
    },
    triagem: {
      assunto: `Seu currículo entrou em triagem: ${vagaCargo} - ${vagaEmpresa}`,
      corpo: `Olá, ${candidatoNome}! O recrutador da empresa ${vagaEmpresa} iniciou a triagem do seu perfil para a oportunidade de ${vagaCargo}. Entraremos em contato caso seu fit seja compatível com a próxima etapa.`
    },
    entrevista: {
      assunto: `Parabéns! Entrevista agendada: ${vagaCargo} - ${vagaEmpresa}`,
      corpo: `Olá, ${candidatoNome}! Temos ótimas notícias: o recrutador da empresa ${vagaEmpresa} gostou do seu perfil e quer agendar uma entrevista para a vaga de ${vagaCargo}. Fique de olho no seu celular e e-mail para mais informações!`
    },
    proposta: {
      assunto: `Proposta de Contratação! ${vagaCargo} - ${vagaEmpresa}`,
      corpo: `Olá, ${candidatoNome}! Você avançou para a última fase! A empresa ${vagaEmpresa} enviará uma proposta oficial de contratação para a vaga de ${vagaCargo}. Parabéns pela conquista!`
    },
    rejeitado: {
      assunto: `Agradecimento pela participação: ${vagaCargo} - ${vagaEmpresa}`,
      corpo: `Olá, ${candidatoNome}. Agradecemos o tempo dedicado ao processo seletivo para a vaga de ${vagaCargo} na empresa ${vagaEmpresa}. No momento, optamos por seguir com outros perfis mais próximos dos requisitos imediatos, mas seu currículo ficará arquivado no nosso Banco de Talentos local para futuras vagas. Desejamos muito sucesso em sua jornada!`
    }
  };

  const template = statusTexts[novoStatus] || {
    assunto: `Atualização de status na vaga: ${vagaCargo}`,
    corpo: `Olá, ${candidatoNome}! O status da sua candidatura para ${vagaCargo} na empresa ${vagaEmpresa} foi atualizado para: ${novoStatus}.`
  };

  const RESEND_API_KEY = process.env.RESEND_API_KEY;

  if (RESEND_API_KEY) {
    try {
      const response = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${RESEND_API_KEY}`
        },
        body: JSON.stringify({
          from: 'Vagas.me <notificacao@vagas.me>',
          to: [candidatoEmail],
          subject: template.assunto,
          html: `
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #ffffff; color: #333333;">
              <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #8B26FD; margin: 0; font-size: 28px;">Vagas<span style="color: #666666;">.me</span></h1>
                <p style="color: #999999; font-size: 14px; margin: 5px 0 0 0;">O seu trabalho perto de você.</p>
              </div>
              <hr style="border: none; border-top: 1px solid #eeeeee; margin-bottom: 20px;">
              <h2 style="color: #333333; font-size: 18px;">Olá, ${candidatoNome}</h2>
              <p style="font-size: 15px; line-height: 1.6; color: #555555;">${template.corpo}</p>
              <hr style="border: none; border-top: 1px solid #eeeeee; margin-top: 30px; margin-bottom: 20px;">
              <div style="text-align: center; font-size: 12px; color: #999999;">
                Este e-mail é uma notificação automática enviada pela plataforma Vagas.me em nome do recrutador da empresa ${vagaEmpresa}.
              </div>
            </div>
          `
        })
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`Erro na API do Resend: ${errText}`);
      }

      const resData = await response.json();
      return res.status(200).json({ success: true, message: 'E-mail real enviado com sucesso via Resend!', data: resData });

    } catch (e) {
      console.error('Falha ao enviar e-mail via Resend:', e);
      return res.status(500).json({ error: 'Erro ao processar envio de e-mail pela API: ' + e.message });
    }
  }

  // Se não houver API Key de e-mail configurada, simula o envio com sucesso
  return res.status(200).json({
    success: true,
    mocked: true,
    message: `Envio simulado com sucesso! E-mail de notificação de status '${novoStatus}' seria disparado para ${candidatoEmail}.`,
    payload: {
      para: candidatoEmail,
      assunto: template.assunto,
      corpo: template.corpo
    }
  });
}
