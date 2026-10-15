import os
from telegram.ext import ApplicationBuilder
import mercadopago

# Lê os tokens diretamente das variáveis de ambiente configuradas na Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

# Inicializa o Mercado Pago
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

def main():
    # Cria a aplicação do Telegram compatível com a versão 21.9
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    print("🤖 Bot gean-store ONLINE e rodando com sucesso! 🚀")
    
    # Inicia o bot
    application.run_polling()

if __name__ == "__main__":
    main()
    
    
