import time
import datetime
from twilio.rest import Client
import requests
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# CONFIGURAÇÕES DA TWILIO
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
NUMERO_TWILIO = 'whatsapp:+14155238886'
NUMERO_DESTINO = 'whatsapp:+258840258114'

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def buscar_dados_seguranca():
    print("A procurar notícias sobre segurança nacional...")
    return {
        "titulo": "Polícia da República de Moçambique reforça patrulhamento em pontos estratégicos",
        "fonte": "Portal de Notícias de Moçambique",
        "imagem_url": "https://unsplash.com" 
    }

def gerar_critica_academica(noticia):
    print("A gerar análise académica via IA...")
    return (
        f"📝 *TESTE DE SISTEMA - SEGURANÇA NACIONAL*\n\n"
        f"*Evento:* {noticia['titulo']}\n"
        f"*Fonte:* {noticia['fonte']}\n\n"
        f"*Crítica Construtiva:* O reforço operacional reportado demonstra uma resposta tática imediata. "
        f"Contudo, sugere-se a integração de modelos de policiamento comunitário."
    )

def enviar_para_whatsapp(texto_critica, imagem_url):
    try:
        mensagem = client.messages.create(
            from_=NUMERO_TWILIO,
            body=texto_critica,
            media_url=[imagem_url],  
            to=NUMERO_DESTINO
        )
        print(f"✅ Mensagem enviada com sucesso! SID: {mensagem.sid}")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem para a Twilio: {e}")

# CICLO DE HORÁRIO INDEPENDENTE
def loop_relogio_horario():
    print("⏰ Relógio interno iniciado. A monitorizar horários (08:00 e 20:00)...")
    
    # --- ENVIO DE TESTE IMEDIATO AO LIGAR O BOT ---
    print("🚀 Executando disparo de teste inicial...")
    noticia_teste = buscar_dados_seguranca()
    critica_teste = gerar_critica_academica(noticia_teste)
    enviar_para_whatsapp(critica_teste, noticia_teste["imagem_url"])
    # -----------------------------------------------

    while True:
        agora = datetime.datetime.now()
        if (agora.hour == 8 or agora.hour == 20) and agora.minute == 0:
            print(f"⏰ Horário atingido ({agora.hour:02d}:00). A processar envio diário...")
            noticia = buscar_dados_seguranca()
            critica = gerar_critica_academica(noticia)
            enviar_para_whatsapp(critica, noticia["imagem_url"])
            time.sleep(61) 
        time.sleep(30)

# SERVIDOR WEB PARA O RENDER
class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write("Bot de Segurança Ativo! 🚀".encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml; charset=utf-8')
        self.end_headers()
        resposta_twilio = "<Response></Response>"
        self.wfile.write(resposta_twilio.encode('utf-8'))
        
        print("📩 Mensagem recebida no WhatsApp Sandbox! A testar fluxo...")
        noticia = buscar_dados_seguranca()
        critica = gerar_critica_academica(noticia)
        enviar_para_whatsapp(critica, noticia["imagem_url"])

if __name__ == "__main__":
    t = threading.Thread(target=loop_relogio_horario, daemon=True)
    t.start()

    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), WebhookHandler)
    print(f"🚀 Servidor do Render a rodar na porta {porta}...")
    server.serve_forever()
