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

PROXIMO_ENVIO = None

def obter_hora_mocambique():
    """Ajusta o horário padrão do servidor Render (UTC) para o fuso de Moçambique (UTC+2)"""
    return datetime.datetime.utcnow() + datetime.timedelta(hours=2)

def calcular_proximo_bloco_6h(hora_atual):
    """Define o próximo envio para os horários cheios: 00:00, 06:00, 12:00 ou 18:00"""
    horas_alvo = [0, 6, 12, 18]
    for hora in horas_alvo:
        if hora_atual.hour < hora:
            return hora_atual.replace(hour=hora, minute=0, second=0, microsecond=0)
    amanha = hora_atual + datetime.timedelta(days=1)
    return amanha.replace(hour=0, minute=0, second=0, microsecond=0)

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
        f"depende da integração de inteligência policial, transparência institutional e "
        f"programas de policiamento comunitário que aproximem o cidadão das forças de autoridade.\n\n"
        f"💬 *SUA OPINIÃO:* Qual é a sua leitura sobre este reforço? Acredita que o policiamento "
        f"ostensivo é suficiente para garantir a segurança sustentável na sua região? Deixe o seu comentário!"
    )

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

def teste_inicial_e_agendamento():
    """Roda em uma thread separada para não travar a inicialização do Flask no Render"""
    global PROXIMO_ENVIO
    time.sleep(5) # Aguarda 5 segundos para o servidor estabilizar
    
    print("🚀 EXECUTANDO DISPARO DE TESTE INICIAL...")
    noticia_teste = buscar_dados_seguranca()
    critica_teste = gerar_critica_academica(noticia_teste)
    enviar_para_whatsapp(critica_teste)
    
    print("⏰ Relógio de agendamento ativado...")
    hora_local = obter_hora_mocambique()
    PROXIMO_ENVIO = calcular_proximo_bloco_6h(hora_local)
    print(f"📅 Próximo envio programado para: {PROXIMO_ENVIO.strftime('%H:%M')} (Hora de Moçambique)")

    while True:
        hora_local = obter_hora_mocambique()
        if hora_local >= PROXIMO_ENVIO:
            print(f"⏰ Horário alvo atingido ({PROXIMO_ENVIO.strftime('%H:%M')}). Enviando...")
            noticia = buscar_dados_seguranca()
            critica = gerar_critica_academica(noticia)
            enviar_para_whatsapp(critica)
            
            PROXIMO_ENVIO = calcular_proximo_bloco_6h(hora_local + datetime.timedelta(minutes=5))
            print(f"📅 Próximo envio redefinido para: {PROXIMO_ENVIO.strftime('%H:%M')}")
            
        time.sleep(30)

@app.route('/')
def home():
    hora_local = obter_hora_mocambique()
    print(f"💤 Robô acordado por ping externo às {hora_local.strftime('%H:%M:%S')} (Hora de Moçambique)")
    return "Bot Ativo e Acordado! 🚀", 200

if __name__ == "__main__":
    print("🔄 Iniciando rotinas de segundo plano...")
    t = threading.Thread(target=teste_inicial_e_agendamento, daemon=True)
    t.start()
    
    porta = int(os.environ.get("PORT", 10000))
    print(f"📡 Iniciando Servidor Web Flask na porta {porta}...")
    app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False)
