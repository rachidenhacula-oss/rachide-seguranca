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
        "titulo": "Polícia de Moçambique reforça patrulhamento nos centros urbanos",
        "fonte": "Portal de Notícias de Moçambique, Boletim de Segurança Pública"
    }

def gerar_critica_academica(noticia):
    print("A gerar analise...")
    return (
        f"📌 *TÍTULO:* {noticia['titulo'].upper()}\n\n"
        f"🌐 *FONTES:* {noticia['fonte']}\n\n"
        f"🔬 *ANÁLISE PROFUNDA:* O incremento do contingente policial nas artérias urbanas reflete "
        f"uma resposta tática imediata à pressão social e ao índice de criminalidade reportado. "
        f"Contudo, sob uma perspetiva socioeconómica e estrutural, esta medida mitiga apenas "
        f"os sintomas visíveis da insegurança, sem resolver as causas profundas, como o desemprego "
        f"jovem e a falta de iluminação pública. A eficácia a longo prazo desta política pública "
        f"depende da integração de inteligência policial, transparência institucional e "
        f"programas de policiamento comunitário que aproximem o cidadão das forças de autoridade.\n\n"
        f"💬 *SUA OPINIÃO:* Qual é a sua leitura sobre este reforço? Acredita que o policiamento "
        f"ostensivo é suficiente para garantir a segurança sustentável na sua região? Deixe o seu comentário!"
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
    print("⏰ Relógio de agendamento ativado...")
    while True:
        agora = datetime.datetime.now()
        # Modificado para enviar de 6 em 6 horas (00:00, 06:00, 12:00, 18:00 UTC)
        if (agora.hour % 6 == 0) and agora.minute == 0:
            print(f"⏰ Horário atingido ({agora.hour:02d}:00 UTC).")
            noticia = buscar_dados_seguranca()
            critica = gerar_critica_academica(noticia)
            enviar_para_whatsapp(critica)
            time.sleep(61)  # Evita disparos múltiplos no mesmo minuto
        time.sleep(30)

@app.route('/')
def home():
    return "Bot Ativo! 🚀", 200

if __name__ == "__main__":
    print("🚀 EXECUTANDO DISPARO DE TESTE INICIAL...")
    # Executa o teste imediatamente na thread principal para garantir o funcionamento
    noticia_teste = buscar_dados_seguranca()
    critica_teste = gerar_critica_academica(noticia_teste)
    enviar_para_whatsapp(critica_teste)
    
    print("🔄 Iniciando o relógio de agendamento em segundo plano...")
    t = threading.Thread(target=loop_relogio_horario, daemon=True)
    t.start()
    
    porta = int(os.environ.get("PORT", 10000))
    print(f"📡 Iniciando Servidor Web Flask na porta {porta}...")
    app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False)
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
    print("⏰ Relogio de agendamento ativado...")
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

if __name__ == "__main__":
    print("🚀 EXECUTANDO DISPARO DE TESTE INICIAL...")
    # Executa o teste imediatamente na thread principal para garantir que roda
    noticia_teste = buscar_dados_seguranca()
    critica_teste = gerar_critica_academica(noticia_teste)
    enviar_para_whatsapp(critica_teste)
    
    print("🔄 Iniciando o relogio de agendamento em segundo plano...")
    t = threading.Thread(target=loop_relogio_horario, daemon=True)
    t.start()
    
    porta = int(os.environ.get("PORT", 10000))
    print(f"📡 Iniciando Servidor Web Flask na porta {porta}...")
    app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False)
