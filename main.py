import os
import time
import asyncio
import mercadopago
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Pega as chaves de forma segura da nuvem
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

def criar_pagamento_pix(valor: float, descricao: str):
    payment_data = {
        "transaction_amount": valor,
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {
            "email": "cliente@email.com"
        }
    }
    result = sdk.payment().create(payment_data)
    response = result["response"]
    
    payment_id = response.get("id")
    point_of_interaction = response.get("point_of_interaction", {})
    transaction_data = point_of_interaction.get("transaction_data", {})
    qr_code = transaction_data.get("qr_code")
    
    return payment_id, qr_code

def verificar_status_pagamento(payment_id):
    result = sdk.payment().get(payment_id)
    return result["response"].get("status")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Comprar Produto (R$ 10,00)", callback_data="comprar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Olá! Seja bem-vindo à **Gean Store**.\n\n"
        "Clique no botão abaixo para adquirir o seu produto:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def botao_comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("⏳ Gerando o seu código Pix, aguarde...")

    valor_produto = 10.00  # Você pode alterar o preço aqui se quiser
    descricao_produto = "Gean Store - Produto Digital"

    try:
        payment_id, qr_code_pix = criar_pagamento_pix(valor_produto, descricao_produto)

        texto_mensagem = (
            f"✅ **Pix gerado com sucesso!**\n\n"
            f"**Valor:** R$ {valor_produto:.2f}\n"
            f"**Produto:** {descricao_produto}\n\n"
            f"📋 **Copie o código Pix Copia e Cola abaixo:**\n"
            f"`{qr_code_pix}`\n\n"
            f"⏳ Aguardando a confirmação do seu pagamento..."
        )

        await query.message.reply_text(texto_mensagem, parse_mode="Markdown")
        asyncio.create_task(monitorar_pagamento(query.message.chat_id, payment_id, context))

    except Exception as e:
        await query.message.reply_text(f"❌ Erro ao gerar o Pix: {e}")

async def monitorar_pagamento(chat_id, payment_id, context):
    tentativas = 0
    max_tentativas = 60  # Fica checando por até 10 minutos

    while tentativas < max_tentativas:
        await asyncio.sleep(10)
        tentativas += 1

        status = verificar_status_pagamento(payment_id)

        if status == "approved":
            await context.bot.send_message(
                chat_id=chat_id,
                text="🎉 **Pagamento Confirmado com Sucesso!**\n\n"
                     "Muito obrigado pela compra!\n"
                     "👉 **Seu link de acesso:** https://seu-link-ou-grupo-aqui.com",
                parse_mode="Markdown"
            )
            return
        elif status in ["cancelled", "rejected"]:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ O pagamento foi cancelado ou recusado."
            )
            return

    await context.bot.send_message(
        chat_id=chat_id,
        text="⏰ O tempo para pagamento via Pix expirou. Faça o pedido novamente se desejar."
    )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botao_comprar, pattern="^comprar$"))
    print("🤖 Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
