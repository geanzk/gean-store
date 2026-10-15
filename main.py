import os
from telegram.ext import ApplicationBuilder
import mercadopago

# Lê os tokens configurados nas variáveis de ambiente da Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

# Inicializa o Mercado Pago
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

def main():
    # Cria a aplicação compatível com a versão 21.9
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    print("🤖 Bot gean-store ONLINE e rodando com sucesso! 🚀")
    
    # Inicia o bot corretamente
    application.run_polling()

if __name__ == "__main__":
    main()
