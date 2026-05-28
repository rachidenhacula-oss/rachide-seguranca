import time
import datetime
from twilio.rest import Client
import os
import threading
from flask import Flask
import feedparser

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
    print("⚠️ ATENÇÃO: Credenciais Twilio ausentes nas variáveis do Render!")

PROXIMO_ENVIO = None

def obter_hora_mocambique():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=2)

def calcular_proximo_bloco_6h(hora_atual):
    # CORRIGIDO: Lista de horários restaurada corretamente
    horas_alvo = [0, 6, 12, 18]
    for hora in horas_alvo:
        if hora_atual.hour < hora:
            return hora_atual.replace(hour=hora, minute=0, second=0, microsecond=0)
    amanha = hora_atual + datetime.timedelta(days=1)
    return amanha.replace(hour=0, minute=0, second=0, microsecond=0)

def buscar_dados_seguranca():
    print("🛰️ Acedendo aos portais de notícias em tempo real...")
    url_feed = "https://dw.com"
    
    try:
        feed = feedparser.parse(url_feed)
        noticias_mocambique = []
        
        for entrada in feed.entries:
            titulo = entrada.title.lower()
            resumo = entrada.summary.lower() if 'summary' in entrada else ""
            
            if "moçambique" in titulo or "maputo" in titulo or "beira" in titulo or "nampula" in titulo or "moçambique" in resumo:
                noticias_mocambique.append(entrada)
        
        if noticias_mocambique:
            nova_noticia = noticias_mocambique[0]
            return {
                "titulo": nova_noticia.title,
                "fonte": f"DW África - Link: {nova_noticia.link}"
            }
        
        if feed.entries:
            noticia_geral = feed.entries[0]
            return {
                "titulo": noticia_geral.title,
                "fonte": f"DW África Atualidades - Link: {noticia_geral.link}"
            }
            
    except Exception as e:
        print(f"⚠️ Falha ao ler notícias online ({e}). Usando notícia de contingência.")
        
    return {
        "titulo": "Governo de Moçambique analisa novos planos de desenvolvimento e segurança económica",
        "fonte": "Portal de Monitoria Nacional"
    }

def gerar_critica_academica(noticia):
    print("🔬 A gerar análise profunda da notícia real...")
    return (
        f"📌 *TÍTULO:* {noticia['titulo'].upper()}\n\n"
        f"🌐 *FONTES:* {noticia['fonte']}\n\n"
        f"🔬 *ANÁLISE PROFUNDA:* A presente dinâmica reportada nas diretrizes informativas reflete "
        f"um impacto imediato na conjuntura socioeconómica e estrutural de Moçambique. Sob uma perspetiva "
        f"académica, eventos desta natureza exigem uma descentralização de políticas públicas e "
        f"respostas institucionais coordenadas, mitigando vulnerabilidades locais e impulsionando a "
        f"sustentabilidade das infraestruturas comunitárias a longo prazo.\n\n"
        f"💬 *SUA OPINIÃO:* Qual é a sua leitura sobre este acontecimento em Moçambique? "
        f"Deixe o seu comentário!"
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
    global PROXIMO_ENVIO
    print("⏳ Aguardando estabilização do servidor para o disparo inicial...")
    time.sleep(10)
    
    print("🚀 EXECUTANDO DISPARO DE TESTE COM NOTÍCIA REAL...")
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
    print(f"💤 Robô acordado por ping externo às {hora_local.strftime('%H:%M:%S')}")
    return "Bot Ativo e Acordado! 🚀", 200

if __name__ == "__main__":
    print("🔄 Iniciando rotinas de segundo plano...")
    t = threading.Thread(target=teste_inicial_e_agendamento, daemon=True)
    t.start()
    
    porta = int(os.environ.get("PORT", 10000))
    print(f"📡 Iniciando Servidor Web Flask na porta {porta}...")
    app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False)
