import os
import logging
from telegram import Update, Chat
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

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

    def run(self):
        if not BOT_TOKEN or not ADMIN_ID:
            logger.error("BOT_TOKEN and ADMIN_ID environment variables must be set")
            return

        app = ApplicationBuilder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("setmessage", self.set_message))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))

        app.run_polling()

if __name__ == "__main__":
    bot = MentionBot()
    bot.run()
