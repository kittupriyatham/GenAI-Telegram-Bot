import openai

from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener

openai.organization = "org-vTqTsNTqKQKonMUHpC0USOQy"
openai.api_key = "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"


class MessageListener(Listener):  # Event listener must inherit Listener
    def __init__(self):
        self.bot = Bot("6090013295:AAENpI84l8p4Ya1rF23UgpX6Fuu4Hp_BKa4")

    def on_message(self, message):  # When message is received
        print("message =", message)
        if message.text.startswith('/start'):
            self.bot.send_message(message.chat.id, 'Hello user!\nThis is an example bot.')
        elif message.text.startswith('/chatgpt'):
            print(message)
            value = message.text[9:]
            response = openai.Completion.create(model="text-davinci-003", prompt=value, temperature=0, max_tokens=500)
            print("response =", dict(response)["choices"][0]["text"][2:])
            self.bot.send_message(message.chat.id, dict(response)["choices"][0]["text"][2:])
        elif message.text.startswith('/image'):
            value = message.text[7:]
            response = openai.Image.create(prompt=value, n=1, size="1024x1024")
            print("response =", response['data'][0]['url'])
            self.bot.send_photo(message.chat.id, response['data'][0]['url'])

    def on_command_failure(self, message, err=None):  # When command fails
        if err is not None:
            self.bot.send_message(message.chat.id,
                                  'Error in command:\n{err}')
