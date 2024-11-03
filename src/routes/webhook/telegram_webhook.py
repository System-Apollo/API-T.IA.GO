from flask import request,Blueprint
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler
from src.utils.config.config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)
application = Application.builder().token(TELEGRAM_TOKEN).build()
webhook = Blueprint('webhook', __name__)

@webhook.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    application.update_queue.put(update)
    return 'ok'
