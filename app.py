from flask import Flask, render_template
from telegrambot import MessageListener

app = Flask(__name__)


@app.route('/')
def index():
    ml = MessageListener()
    ml.bot.start()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
