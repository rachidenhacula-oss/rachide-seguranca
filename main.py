import time
import datetime
from twilio.rest import Client
import os
import threading
from flask import Flask

# Inicializa o Flask para manter o Render feliz
app = Flask(__name__)

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

@app.route('/')
def home():
    return "Bot Ativo! 🚀", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    print("📩 Mensagem recebida via Webhook!")
    return "<Response></Response>", 200

if __name__ == "__main__":
    # Inicia o relogio em segundo plano
    t = threading.Thread(target=loop_relogio_horario, daemon=True)
    t.start()
    
    # Inicia o servidor Flask na porta correta do Render
    porta = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=porta)
