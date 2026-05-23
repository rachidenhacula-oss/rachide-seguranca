import time
import datetime
from twilio.rest import Client
import requests
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
NUMERO_TWILIO = 'whatsapp:+14155238886'
NUMERO_DESTINO = 'whatsapp:+258840258114'

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def buscar_dados_seguranca():
    print("A procurar noticias...")
    return {
        "titulo": "Policia de Mocambique reforca patrulhamento",
        "fonte": "Portal de Noticias",
        "imagem_url": "https://unsplash.com"
    }

def gerar_critica_academica(noticia):
    print("A gerar analise...")
    return (
        f"📝 *TESTE DE SISTEMA - SEGURANÇA*\n\n"
        f"*Evento:* {noticia['titulo']}\n"
        f"*Fonte:* {noticia['fonte']}\n\n"
        f"*Analise:* O reforco operacional demonstra resposta imediata."
    )

def enviar_para_whatsapp(texto_critica, imagem_url):
    try:
        mensagem = client.messages.create(
            from_=NUMERO_TWILIO,
            body=texto_critica,
            media_url=[imagem_url],
            to=NUMERO_DESTINO
        )
        print(f"✅ Mensagem enviada! SID: {mensagem.sid}")
    except Exception as e:
        print(f"❌ Erro na Twilio: {e}")

def loop_relogio_horario():
    print("⏰ Relogio iniciado...")
    print("🚀 Executando disparo de teste inicial...")
    noticia_teste = buscar_dados_seguranca()
    critica_teste = gerar_critica_academica(noticia_teste)
    enviar_para_whatsapp(critica_teste, noticia_teste["imagem_url"])

    while True:
        agora = datetime.datetime.now()
        if (agora.hour == 8 or agora.hour == 20) and agora.minute == 0:
            print(f"⏰ Horario atingido ({agora.hour:02d}:00).")
            noticia = buscar_dados_seguranca()
            critica = gerar_critica_academica(noticia)
            enviar_para_whatsapp(critica, noticia["imagem_url"])
            time.sleep(61)
        time.sleep(30)

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write("Bot Ativo! 🚀".encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml; charset=utf-8')
        self.end_headers()
        self.wfile.write("<Response></Response>".encode('utf-8'))
        print("📩 Mensagem recebida!")
        noticia = buscar_dados_seguranca()
        critica = gerar_critica_academica(noticia)
        enviar_para_whatsapp(critica, noticia["imagem_url"])

if __name__ == "__main__":
    t = threading.Thread(target=loop_relogio_horario, daemon=True)
    t.start()
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), WebhookHandler)
    print(f"🚀 Servidor na porta {porta}...")
    server.serve_forever()
