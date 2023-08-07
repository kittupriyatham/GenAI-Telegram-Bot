import botogram
import openai
from config import TOKEN, ORG, KEY

bot = botogram.create(TOKEN)

openai.organization = ORG
openai.api_key = KEY


@bot.command("chat")
def chatgpt(chat, message, args):
    print("chat name =", chat.name)
    # print(displayUserInfo(message))
    print("name =", message.sender.name)
    print("username =", message.sender.username)
    prompt = " ".join(args)
    print("prompt =", prompt)
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=2000)
    # print(response)
    res = (dict(response)["choices"][0]["text"][2:])
    print(res)
    print()
    chat.send(res)


@bot.command("image")
def image(chat, message, args):
    print(chat.name)
    # print(displayUserInfo(message))
    print("name =", message.sender.name)
    print("username", message.sender.username)
    prompt = " ".join(args)
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    print(prompt)
    print(response)
    print(response['data'][0]['url'])
    print()
    chat.send_photo(url=response['data'][0]['url'])


# @bot.command("video")
# def video(chat, message, args):
#     print(chat.name)
#     # print(displayUserInfo(message))
#     print("name =", message.sender.name)
#     print("username", message.sender.username)
#     prompt = " ".join(args)
#     print()
#     chat.send("video part yet to be built")
#
#
# @bot.command("meme")
# def meme(chat, message, args):
#     print(chat.name)
#     # print(displayUserInfo(message))
#     print("name =", message.sender.name)
#     print("username", message.sender.username)
#     prompt = " ".join(args)
#     print()
#     chat.send("meme part yet to be built")
#
#
# @bot.command("speak")
# def speak(chat, message, args):
#     print(chat.name)
#     # print(displayUserInfo(message))
#     print("name =", message.sender.name)
#     print("username", message.sender.username)
#     prompt = " ".join(args)
#     print()
#     chat.send("speak part yet to be built")


if __name__ == "__main__":
    bot.run()
