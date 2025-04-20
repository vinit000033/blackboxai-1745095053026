import os
import logging
from telegram import Update, Chat
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "8000"))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class MentionBot:
    def __init__(self):
        self.custom_message = "Hello! You mentioned me."  # Default message

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello! I am your MentionBot. Admin can set a custom reply message using /setmessage command.")

    async def set_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            await update.message.reply_text("You are not authorized to set the message.")
            return

        if context.args:
            self.custom_message = " ".join(context.args)
            await update.message.reply_text(f"Custom message updated to:\n{self.custom_message}")
        else:
            await update.message.reply_text("Usage: /setmessage Your custom message here")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        chat = message.chat

        # Only process group messages
        if chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            # Check if bot is mentioned in the message entities
            if message.entities:
                bot_username = (await context.bot.get_me()).username.lower()
                for entity in message.entities:
                    if entity.type == "mention":
                        mentioned_text = message.text[entity.offset : entity.offset + entity.length].lower()
                        if mentioned_text == f"@{bot_username}":
                            # Reply with custom message
                            await message.reply_text(self.custom_message)

                            # Report mention to admin privately
                            user = message.from_user
                            report_text = (
                                f"User @{user.username or user.first_name} mentioned the bot in group '{chat.title}':\n"
                                f"Message: {message.text}"
                            )
                            await context.bot.send_message(chat_id=ADMIN_ID, text=report_text, parse_mode=ParseMode.HTML)
                            break

    async def on_startup(self, app: web.Application):
        # Set webhook on startup
        await app.bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook set to {WEBHOOK_URL}")

    async def on_shutdown(self, app: web.Application):
        # Remove webhook on shutdown
        await app.bot.delete_webhook()
        logger.info("Webhook deleted")

    def run(self):
        if not BOT_TOKEN or not ADMIN_ID or not WEBHOOK_URL:
            logger.error("BOT_TOKEN, ADMIN_ID, and WEBHOOK_URL environment variables must be set")
            return

        app = ApplicationBuilder().token(BOT_TOKEN).build()

        mention_bot = self

        app.add_handler(CommandHandler("start", mention_bot.start))
        app.add_handler(CommandHandler("setmessage", mention_bot.set_message))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mention_bot.handle_message))

        # Use aiohttp web server for webhook
        web_app = app.create_web_app()
        web_app.bot = app.bot

        web_app.on_startup.append(self.on_startup)
        web_app.on_shutdown.append(self.on_shutdown)

        web.run_app(web_app, port=PORT)

if __name__ == "__main__":
    bot = MentionBot()
    bot.run()
