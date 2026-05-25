import time
import datetime
from twilio.rest import Client
import os
import threading
from flask import Flask

app = Flask(__name__)

# Configurações da Twilio com fallback para testes locais se necessário
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
NUMERO_TWILIO = 'whatsapp:+14155238886'
NUMERO_DESTINO = 'whatsapp:+258840258114'

# Só inicializa o cliente se as variáveis existirem no Render
if ACCOUNT_SID and AUTH_TOKEN:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
else:
    client = None
    print("⚠️ ATENÇÃO: TWILIO_ACCOUNT_SID ou TWILIO_AUTH_TOKEN não foram configurados no Render!")

def buscar_dados_seguranca():
    print("A procurar noticias...")
    return {
        "titulo": "Policia de Mocambique reforca patrulhamento",
        "fonte": "Portal de Noticias"
    }

def gerar_critica_academica(noticia):
    print("A gerar analise...")
    return (
        f"📝 *TESTE DE SISTEMA - SEGURANÇA*\n\n"
        f"*Event:* {noticia['titulo']}\n"
        f"*Fonte:* {noticia['fonte']}\n\n"
        f"*Analise:* O reforco operacional demonstra resposta imediata."
    )

def enviar_para_whatsapp(texto_critica):
    if not client:
        print("❌ Envio cancelado: Cliente Twilio não configurado.")
        return
        
    try:
        # REMOVIDO O MEDIA_URL PARA FACILITAR O ENVIO
        mensagem = client.messages.create(
            from_=NUMERO_TWILIO,
            body=texto_critica,
            to=NUMERO_DESTINO
        )
        print(f"✅ Mensagem enviada com sucesso! SID: {mensagem.sid}")
    except Exception as e:
        print(f"❌ Erro crítico na Twilio: {e}")

def loop_relogio_horario():
    print("⏰ Relogio iniciado...")
    print("🚀 Executando disparo de teste inicial...")
    
    # Teste inicial para ver se funciona assim que o bot liga
    noticia_teste = buscar_dados_seguranca()
    critica_teste = gerar_critica_academica(noticia_teste)
    enviar_para_whatsapp(critica_teste)

    while True:
        agora = datetime.datetime.now()
        # Nota: O Render usa o horário UTC por padrão!
        if (agora.hour == 8 or agora.hour == 20) and agora.minute == 0:
            print(f"⏰ Horario atingido ({agora.hour:02d}:00 UTC).")
            noticia = buscar_dados_seguranca()
            critica = gerar_critica_academica(noticia)
            enviar_para_whatsapp(critica)
            time.sleep(61)
        time.sleep(30)

@app.route('/')
def home():
    return "Bot Ativo! 🚀", 200

# Função que dispara a thread DEPOIS que o Flask inicia para não travar o Render
@app.before_all_requests
def iniciar_background_job():
    # Garante que roda apenas uma vez
    if not hasattr(app, 'thread_iniciada'):
        t = threading.Thread(target=loop_relogio_horario, daemon=True)
        t.start()
        app.thread_iniciada = True

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False)
