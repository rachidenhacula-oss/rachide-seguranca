import os
import time
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from twilio.rest import Client

# 1. Configurações de chaves usando variáveis de ambiente do Render
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sua_chave_aqui")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "seu_sid_aqui")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "seu_token_aqui")

# Números de telefone para o WhatsApp (Formato internacional: +55... ou +258...)
WHATSAPP_DE = "whatsapp:+14155238886"  # Número padrão do Sandbox do Twilio
WHATSAPP_PARA = "whatsapp:+258840258114" # Substitua pelo SEU número do WhatsApp

# 2. Inicialização dos Clientes das APIs
client_openai = OpenAI(api_key=OPENAI_API_KEY)
client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def buscar_dados_seguranca():
    """Simula a coleta de dados públicos ou tópicos de segurança nacional."""
    # Como o Facebook bloqueia raspagem direta sem API oficial, usamos um agregador de notícias de segurança
    url = "https://defensenews.com" 
    try:
        resposta = requests.get(url, timeout=10)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        # Pega o título da manchete principal de segurança
        manchete = soup.find('h1').text.strip() if soup.find('h1') else "Discussões sobre Defesa e Estratégia Nacional"
        return manchete
    except Exception as e:
        return "Novas diretrizes e debates sobre Segurança Coletiva Regional"

def gerar_critica_academica(tema):
    """Usa a OpenAI para formular uma crítica formal e construtiva."""
    prompt = f"Com base no tema '{tema}', formule um texto curto para o Facebook de caráter crítico, acadêmico e construtivo sobre segurança nacional. Convide o público leitor a interagir nos comentários expondo seus pensamentos de forma democrática."
    
    try:
        resposta = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"Erro ao gerar IA: {str(e)}"

def enviar_para_whatsapp(texto_critica):
    """Envia o rascunho do texto gerado para validação do usuário via Twilio."""
    mensagem_formatada = f"🤖 *Robô de Segurança - Rascunho para Validação:*\n\n{texto_critica}\n\nSe gostou, copie o texto acima e publique na sua página!"
    try:
        mensagem = client_twilio.messages.create(
            from_=WHATSAPP_DE,
            body=mensagem_formatada,
            to=WHATSAPP_PARA
        )
        print(f"Mensagem de validação enviada com sucesso! SID: {mensagem.sid}")
    except Exception as e:
        print(f"Erro ao enviar WhatsApp: {str(e)}")

# Execução principal do script
if __name__ == "__main__":
    print("Iniciando varredura do Robô de Segurança...")
    tema_coletado = buscar_dados_seguranca()
    print(f"Tema detectado: {tema_coletado}")
    
    critica = gerar_critica_academica(tema_coletado)
    print("Crítica gerada pela Inteligência Artificial.")
    
    enviar_para_whatsapp(critica)
    print("Processo finalizado. Aguardando próxima execução.")
