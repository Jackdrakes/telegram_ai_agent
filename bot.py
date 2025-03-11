from telegram import Update

from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import logging

from agent import run_agent


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start command")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your AI assistant.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text    
    logger.info(f"Received message: {message}")
    response = run_agent(message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def american_accent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    logger.info(f"Received /american_accent command with message: {message}")
    # Placeholder for the actual implementation of generating American accent variations
    response = f"Here are three ways to say '{message}' in an American accent:\n1. {message} (variation 1)\n2. {message} (variation 2)\n3. {message} (variation 3)"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    

def main():
    logger.info("Starting bot")
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    american_accent_handler = CommandHandler('american_accent', american_accent)
    application.add_handler(american_accent_handler)

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    application.run_polling()
    logger.info("Bot is polling")

if __name__ == '__main__':
    main()
