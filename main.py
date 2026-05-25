import time
import datetime
from twilio.rest import Client
import os
import threading
from flask import Flask

app = Flask(__name__)

# Configurações das credenciais da Twilio vindas do Render
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
NUMERO_TWILIO = 'whatsapp:+14155238886'
NUMERO_DESTINO = 'whatsapp:+258840258114'

if ACCOUNT_SID and AUTH_TOKEN:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
else:
    client = None
    print("⚠️ ATENÇÃO: TWILIO_ACCOUNT_SID ou TWILIO_AUTH_TOKEN não configurados no Render!")

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
        f"*Evento:* {noticia['titulo']}\n"
        f"*Fonte:* {noticia['fonte']}\n\n"
        f"*Analise:* O reforco operacional demonstra resposta imediata."
    )

def enviar_para_whatsapp(texto_critica):
    if not client:
        print("❌ Envio cancelado: Cliente Twilio não configurado nas variáveis de ambiente.")
        return
        
    try:
        mensagem = client.messages.create(
            from_=NUMERO_TWILIO,
            body=texto_critica,
            to=NUMERO_DESTINO
        )
        print(f"✅ CONEXÃO TWILIO OK! SID da Mensagem: {mensagem.sid}")
    except Exception as e:
        print(f"❌ ERRO DIRETAMENTE DA TWILIO: {e}")

def loop_relogio_horario():
    # Pequeno atraso apenas para o Flask subir primeiro no Render
    time.sleep(3)
    print("⏰ Relogio iniciado em segundo plano...")
    print("🚀 DISPARANDO MENSAGEM DE TESTE INICIAL AGORA...")
    
    noticia_teste = buscar_dados_seguranca()
    critica_teste = gerar_critica_academica(noticia_teste)
    enviar_para_whatsapp(critica_teste)

    while True:
        agora = datetime.datetime.now()
        # 06:00 UTC = 08:00 em Moçambique / 18:00 UTC = 20:00 em Moçambique
        if (agora.hour == 6 or agora.hour == 18) and agora.minute == 0:
            print(f"⏰ Horario atingido ({agora.hour:02d}:00 UTC).")
            noticia = buscar_dados_seguranca()
            critica = gerar_critica_academica(noticia)
            enviar_para_whatsapp(critica)
            time.sleep(61)
        time.sleep(30)

@app.route('/')
def home():
    return "Bot Ativo! 🚀", 200

# O bloco abaixo inicia a thread IMEDIATAMENTE junto com o servidor
if __name__ == "__main__":
    print("🔄 Iniciando a Thread do Bot do WhatsApp...")
    t = threading.Thread(target=loop_relogio_horario, daemon=True)
    t.start()
    
    porta = int(os.environ.get("PORT", 10000))
    print(f"📡 Iniciando Servidor Web Flask na porta {porta}...")
    app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False)

def enviar_para_whatsapp(texto_critica):
    if not client:
        print("❌ Envio cancelado: Cliente Twilio não configurado.")
        return
        
    try:
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
    
    # Teste imediato assim que a aplicação sobe
    noticia_teste = buscar_dados_seguranca()
    critica_teste = gerar_critica_academica(noticia_teste)
    enviar_para_whatsapp(critica_teste)

    while True:
        agora = datetime.datetime.now()
        # Horário do Render é UTC. 06h UTC = 08h em Moçambique / 18h UTC = 20h em Moçambique
        if (agora.hour == 6 or agora.hour == 18) and agora.minute == 0:
            print(f"⏰ Horario atingido ({agora.hour:02d}:00 UTC / {agora.hour+2:02d}:00 Local).")
            noticia = buscar_dados_seguranca()
            critica = gerar_critica_academica(noticia)
            enviar_para_whatsapp(critica)
            time.sleep(61)
        time.sleep(30)

@app.route('/')
def home():
    return "Bot Ativo! 🚀", 200

# CORREÇÃO AQUI: Executa a thread em segundo plano assim que a primeira requisição chega
@app.before_request
def iniciar_background_job():
    if not hasattr(app, 'thread_iniciada'):
        print("⚙️ Primeira requisição recebida. Iniciando tarefas em segundo plano...")
        t = threading.Thread(target=loop_relogio_horario, daemon=True)
        t.start()
        app.thread_iniciada = True

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False)
