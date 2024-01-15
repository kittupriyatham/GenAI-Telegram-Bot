from telegram import _update
from telegram.ext import *
from typing import Final
import google.generativeai as genai
import io
from PIL import Image
import cv2
import numpy


TOKEN: Final = "5692270027:AAF6TeCOMcyATcdjQqapxBJ9xxBzYDbfFQk"
BOT_USERNAME: Final = "@openai_chatgpt3_5_bot"

ORIGINAL_KEY: Final = "AIzaSyDUD14sIvqRFmJn3AAVln-fJLWMl_CZn2g"

KEY = ORIGINAL_KEY
genai.configure(api_key=KEY)

def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

def get_gemini_vision_response(text,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if text!="" or text is not none:
       response = model.generate_content([text,image])
    else:
       response = model.generate_content(image)
    return response.text

# commands
async def start(update: _update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Welcome to Bot")
    commands(update,context)
 # await update.message.reply_text("To continue, you must either enter the password to 'use_admin_api' or 'request_admin_api_password' by giving your username of your telegram account")

async def commands(update: _update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
    The following commands are available:
    /start -> Welcome to the bot
    /commands -> show list of available commands along with their usages
     """)
# /use_admin_api $Password$ -> Use Admin's Api Key
    # /request_admin_api_password $UserName$ -> Use user's Api Key (create your username if not done yet)
    # /logout -> reset Api Key
# responses
def handle_response(text: str) -> str:
    if text is not None:
        return get_gemini_response(text)


async def handle_message(update: _update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    print(f'User ({update.message.from_user.username}) in {message_type} {update.message.chat.title}:'
          f'"{update.message.text}"')
    # if KEY==None:
    #     await update.message.reply_text("API KEY is not set. Use command either /use_admin_api with password to set api or /request_admin_api_password with username to request the password.")
    # elif KEY!=ORIGINAL_KEY:
    #     await update.message.reply_text("")
    text = update.message.text
    if message_type == "supergroup" or message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            print("prompt =", new_text)
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: _update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    await update.message.reply_text("An error occurred at OpenAI API")


if __name__ == '__main__':
    print("Starting bot")
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("commands", commands))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # app.add_handler(MessageHandler(filters.PHOTO, handle_message))

    # log all errors
    app.add_error_handler(error)

    # start the bot
    print("polling")
    app.run_polling(poll_interval=3, timeout=60)



