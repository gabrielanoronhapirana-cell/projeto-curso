"""
RetailBot AI — Knowledge Base (FAQ)
Simulates a RAG-powered institutional knowledge hub.
"""

FAQ_ENTRIES = [
    {
        "topic": "trocas_devolucoes",
        "keywords": ["troca", "trocar", "devolução", "devolver", "devolutiva", "arrependimento", "defeito"],
        "question": "Qual é a política de trocas e devoluções?",
        "answer": (
            "📋 **Política de Trocas e Devoluções:**\n"
            "• **Prazo:** Até **30 dias** após a compra para troca ou devolução.\n"
            "• **Condição:** O produto deve estar em sua embalagem original, sem uso, com etiquetas.\n"
            "• **Defeito:** Em caso de defeito de fabricação, o prazo é de **90 dias** (conforme CDC).\n"
            "• **Arrependimento (online):** Até **7 dias** após o recebimento, sem necessidade de justificativa.\n"
            "• **Como solicitar:** Em qualquer loja física com o comprovante de compra, ou pelo nosso SAC."
        ),
    },
    {
        "topic": "formas_pagamento",
        "keywords": ["pagamento", "pagar", "cartão", "pix", "boleto", "parcela", "parcelamento", "crédito", "débito"],
        "question": "Quais são as formas de pagamento aceitas?",
        "answer": (
            "💳 **Formas de Pagamento:**\n"
            "• **Cartão de crédito:** Visa, Mastercard, Elo, Amex — em até **10x sem juros**.\n"
            "• **Cartão de débito:** Visa, Mastercard, Elo.\n"
            "• **Pix:** Pagamento instantâneo com **5% de desconto**.\n"
            "• **Boleto bancário:** Vencimento em 3 dias úteis.\n"
            "• **Vale-presente:** Aceito em lojas físicas e online."
        ),
    },
    {
        "topic": "horario_funcionamento",
        "keywords": ["horário", "horario", "funcionamento", "aberta", "aberto", "abre", "fecha", "expediente"],
        "question": "Qual o horário de funcionamento das lojas?",
        "answer": (
            "🕐 **Horário de Funcionamento:**\n"
            "• **Segunda a Sábado:** 10h às 22h (lojas em shopping) / 09h às 19h (lojas de rua).\n"
            "• **Domingos e Feriados:** 14h às 20h (lojas em shopping) / Fechadas (lojas de rua).\n"
            "• **Atendimento online (RetailBot):** 24/7, sempre disponível! 🤖"
        ),
    },
    {
        "topic": "frete_entrega",
        "keywords": ["frete", "entrega", "envio", "prazo", "despacho", "transportadora", "sedex", "correios", "rastrear", "rastreamento"],
        "question": "Como funciona o frete e os prazos de entrega?",
        "answer": (
            "🚚 **Frete e Entrega:**\n"
            "• **Frete grátis** para compras acima de **R$ 299,90**.\n"
            "• **Prazo padrão:** 5 a 10 dias úteis.\n"
            "• **Prazo expresso (SEDEX):** 2 a 4 dias úteis.\n"
            "• **Click & Collect:** Retire na loja em até **2 horas** após confirmação do pagamento.\n"
            "• **Rastreamento:** Acompanhe pelo código de rastreio enviado por e-mail e SMS."
        ),
    },
    {
        "topic": "programa_fidelidade",
        "keywords": ["fidelidade", "pontos", "programa", "benefício", "vantagem", "cashback", "recompensa"],
        "question": "Como funciona o programa de fidelidade?",
        "answer": (
            "⭐ **Programa de Fidelidade RetailClub:**\n"
            "• **Acúmulo:** Ganhe **1 ponto** a cada **R$ 1,00** em compras.\n"
            "• **Resgate:** A partir de **500 pontos**, troque por descontos ou produtos exclusivos.\n"
            "• **Níveis:** Bronze → Prata → Ouro → Diamante, com benefícios crescentes.\n"
            "• **Cashback Diamante:** Membros Diamante recebem **5% de cashback** em todas as compras.\n"
            "• **Cadastro:** Gratuito, diretamente no app ou em qualquer loja."
        ),
    },
    {
        "topic": "click_collect",
        "keywords": ["click", "collect", "retire", "retirada", "reserva", "reservar", "buscar", "loja"],
        "question": "Como funciona o Click & Collect?",
        "answer": (
            "🛒 **Click & Collect (Retire na Loja):**\n"
            "• **Como funciona:** Escolha o produto, reserve online e retire na loja de sua preferência.\n"
            "• **Prazo de retirada:** Até **24 horas** após a confirmação da reserva.\n"
            "• **Documentos:** Apresente um documento com foto e o código de reserva.\n"
            "• **Pagamento:** Pode ser feito online ou no momento da retirada na loja."
        ),
    },
    {
        "topic": "lgpd_privacidade",
        "keywords": ["lgpd", "privacidade", "dados", "pessoal", "consentimento", "política de privacidade"],
        "question": "Como vocês tratam meus dados pessoais?",
        "answer": (
            "🔒 **Política de Privacidade (LGPD):**\n"
            "• Seus dados são tratados conforme a **Lei Geral de Proteção de Dados (LGPD)**.\n"
            "• Utilizamos seus dados apenas para **processar pedidos, reservas e melhorar sua experiência**.\n"
            "• Você pode solicitar a **exclusão de seus dados** a qualquer momento.\n"
            "• Nunca compartilhamos suas informações com terceiros sem sua autorização.\n"
            "• Para dúvidas: privacidade@retailbot.com.br"
        ),
    },
]


def search_knowledge_base(query: str) -> str | None:
    """
    Search the FAQ knowledge base using keyword matching.
    In production, this would use vector similarity search (RAG).
    
    Returns the best matching answer or None if no match is found.
    """
    query_lower = query.lower()
    
    best_match = None
    best_score = 0
    
    for entry in FAQ_ENTRIES:
        score = sum(1 for kw in entry["keywords"] if kw in query_lower)
        if score > best_score:
            best_score = score
            best_match = entry
    
    if best_match and best_score > 0:
        return best_match["answer"]
    
    return None
