from telegram import Update, Bot
from telegram.ext import CallbackContext
from src.utils.config.config import TELEGRAM_TOKEN
import logging

bot = Bot(token=TELEGRAM_TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bem-vindo! Como posso facilitar seu dia hoje?\nFaça uma pergunta, como: Quantos processos ativos citam minha empresa?')

def iniciar_bot_telegram(webhook_url):
    bot.set_webhook(url=webhook_url)
    logging.info(f"Webhook configurado para: {webhook_url}")
