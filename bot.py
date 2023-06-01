# noinspection PyProtectedMember
from telegram import _update as Update
from telegram.ext import *
from config import TOKEN, ORG, KEY
import openai

openai.organization = ORG
openai.api_key = KEY


# commands
# noinspection PyUnusedLocal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Welcome to Bot")


# noinspection PyUnusedLocal
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
    The following commands are available:

    /start -> Welcome to the bot
    /help -> Get help
    /chat -> Chat with the bot
    /image -> Get an image
     """)


# noinspection PyUnusedLocal
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("chat name", update.message.chat.title)
    print("name =", update.message.from_user.first_name)
    print("username", update.message.from_user.username)
    if len(update.message.text.split()) == 1:
        await update.message.reply_text("Please provide a prompt")
        return
    prompt = update.message.text.replace("/chat", "").strip()
    print("chat " + prompt)
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt)
    res = (dict(response)["choices"][0]["text"].strip())
    print(res)
    await update.message.reply_text(res)


# noinspection PyUnusedLocal
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("chat name", update.message.chat.title)
    print("name =", update.message.from_user.first_name)
    print("username", update.message.from_user.username)
    if len(update.message.text.split()) == 1:
        await update.message.reply_text("Please provide a prompt")
        return
    prompt = update.message.text.replace("/image", "").strip()
    print("image " + prompt)
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024", response_format="url")
    res = (dict(response)["data"][0]["url"].strip())
    await update.message.reply_photo(photo=res)


# responses
# noinspection PyUnusedLocal
def handle_responses(text: str) -> str:
    return "Use available commands only"


# noinspection PyUnusedLocal
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    print(message_type)
    print(f'User ({update.message.from_user.username}) in {message_type} {update.message.chat.title}: '
          f'"{update.message.text.lower()}"')
    if message_type == "supergroup" or message_type == "group":
        if update.message.text.split()[0] != "/chat" or update.message.text.split()[0] != "/image":
            return
    text: str = str(update.message.text).lower()
    response = handle_responses(text)
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    await update.message.reply_text("An error occurred OpenAI API")


if __name__ == '__main__':
    print("Starting bot")
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("chat", chat))
    app.add_handler(CommandHandler("image", image))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # log all errors
    app.add_error_handler(error)

    # start the bot
    print("polling")
    app.run_polling(poll_interval=3, timeout=60)
