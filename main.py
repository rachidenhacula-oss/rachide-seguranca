import time
import datetime
# Certifique-se de que estas bibliotecas estão instaladas ou importadas no seu projeto original
# Ex: pip install twilio requests
from twilio.rest import Client
import requests
import os
# CONFIGURAÇÕES DA TWILIO (Substitua com as suas credenciais reais)
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
NUMERO_TWILIO = 'whatsapp:+14155238886'  # Número da Sandbox Twilio
NUMERO_DESTINO = 'whatsapp:+258840258114'  # O seu número de Moçambique

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def buscar_dados_seguranca():
    """
    Simula ou procura notícias. 
    Ajustado para garantir foco estrito em Moçambique e Segurança.
    """
    print("A procurar notícias sobre segurança nacional e pública em Moçambique...")
    
    # Exemplo de estrutura de dados que o seu raspador/API deve recolher
    dados_noticia = {
        "titulo": "Polícia da República de Moçambique reforça patrulhamento em pontos estratégicos",
        "fonte": "Portal de Notícias de Moçambique",
        "link": "https://exemplo.com",
        # Imagem real da notícia (necessita de um link direto de imagem válido na internet)
        "imagem_url": "https://unsplash.com" 
    }
    return dados_noticia

def gerar_critica_academica(noticia):
    """
    Gera uma crítica construtiva e académica com base na notícia de segurança.
    """
    contexto_noticia = f"Notícia: {noticia['titulo']} (Fonte: {noticia['fonte']})"
    
    # Aqui entra a sua chamada de Inteligência Artificial (ex: OpenAI, Gemini, etc.)
    # O prompt abaixo garante o tom académico e construtivo exigido
    prompt_instrucao = (
        "Atue como um analista sénior de segurança pública. Gere uma crítica académica, "
        "estritamente construtiva, focada em soluções estruturais, baseando-se no seguinte cenário de Moçambique: "
    )
    
    print("A gerar análise académica via IA...")
    # Exemplo de resposta que a sua IA deve retornar respeitando a instrução:
    analise_gerada = (
        f"📝 *ANÁLISE ACADÉMICA DE SEGURANÇA NACIONAL*\n\n"
        f"*Evento:* {noticia['titulo']}\n"
        f"*Fonte:* {noticia['fonte']}\n\n"
        f"*Crítica Construtiva:* O reforço operacional reportado demonstra uma resposta tática imediata. "
        f"Contudo, sob a ótica das políticas públicas de segurança, sugere-se a integração de modelos "
        f"de policiamento comunitário e o investimento em tecnologias de videovigilância preditiva. "
        f"A sustentabilidade da ordem pública em Moçambique requer uma abordagem multidimensional, "
        f"articulando a presença dissuasora com a mitigação das causas socioeconómicas subjacentes."
    )
    return analise_gerada

def enviar_para_whatsapp(texto_critica, imagem_url):
    """
    Envia o texto da crítica académica juntamente com a imagem da fonte pelo WhatsApp.
    """
    try:
        mensagem = client.messages.create(
            from_=NUMERO_TWILIO,
            body=texto_critica,
            media_url=[imagem_url],  # Anexa a imagem da notícia à mensagem
            to=NUMERO_DESTINO
        )
        print(f"Mensagem enviada com sucesso! SID: {mensagem.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para a Twilio: {e}")

# CICLO PRINCIPAL - CONTROLO VITALÍCIO DE HORÁRIO
if __name__ == "__main__":
    print("🤖 Robô de Segurança Moçambique iniciado com sucesso.")
    print("A aguardar os horários programados (08:00 e 20:00)...")
    
    while True:
        # Obtém a hora atual do local onde o script está a rodar
        agora = datetime.datetime.now()
        hora_atual = agora.hour
        minuto_atual = agora.minute
        
        # Só dispara se for exatamente 08:00 da manhã OU 20:00 da noite
        if (hora_atual == 8 or hora_atual == 20) and minuto_atual == 0:
            print(f"⏰ Horário de disparo atingido ({hora_atual:02d}:00). A processar...")
            
            # 1. Recolhe a notícia focada em segurança em Moçambique
            noticia = buscar_dados_seguranca()
            
            # 2. Transforma a notícia numa crítica construtiva/académica
            critica_final = gerar_critica_academica(noticia)
            
            # 3. Dispara para o WhatsApp com texto e imagem da fonte
            def enviar_para_whatsapp(texto_critica, imagem_url):
    """
    Envia o texto da crítica académica juntamente com a imagem da fonte pelo WhatsApp.
    """
    try:
        mensagem = client.messages.create(
            from_=NUMERO_TWILIO,
            body=texto_critica,
            media_url=[imagem_url],  # Anexa a imagem da notícia à mensagem
            to=NUMERO_DESTINO
        )
        print(f"Mensagem enviada com sucesso! SID: {mensagem.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

# =========================================================
# SERVIDOR WEB PARA O RENDER E RECEBIMENTO DA TWILIO
# =========================================================
from http.server import BaseHTTPRequestHandler, HTTPServer

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Mantém o Render feliz dizendo que o bot está online ao abrir o link
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write("Bot de Segurança Ativo! 🚀".encode('utf-8'))

    def do_POST(self):
        # Recebe a mensagem da Twilio, evita o erro 501 e responde com sucesso
        self.send_response(200)
        self.send_header('Content-type', 'text/xml; charset=utf-8')
        self.end_headers()
        resposta_twilio = "<Response></Response>"
        self.wfile.write(resposta_twilio.encode('utf-8'))
        
        # Opcional: Aciona a lógica de envio ao receber mensagens
        print("Mensagem recebida do WhatsApp! A processar fluxo...")
        noticia = buscar_dados_seguranca()
        critica = gerar_critica_academica(noticia)
        enviar_para_whatsapp(critica, noticia["imagem_url"])

if __name__ == "__main__":
    # O Render passa a porta dinamicamente na variável de ambiente PORT, padrão 10000
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), WebhookHandler)
    print(f"Servidor do Bot rodando na porta {porta}...")
    server.serve_forever()
