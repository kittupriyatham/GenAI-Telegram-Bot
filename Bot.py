import botogram
import openai


bot_api_key = "6090013295:AAENpI84l8p4Ya1rF23UgpX6Fuu4Hp_BKa4"

bot = botogram.create(bot_api_key)


openai.organization = "org-vTqTsNTqKQKonMUHpC0USOQy"
openai.api_key = "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"


@bot.command("chat")
def chatgpt(chat, message, args):
    print("chat name", chat.name)
    # print(displayUserInfo(message))
    print("name =", message.sender.name)
    print("username", message.sender.username)
    prompt = " ".join(args)
    print(prompt)
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=500)
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
    print(prompt)
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
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


# @bot.command("meme")
# def meme(chat, message, args):
#     print(chat.name)
#     # print(displayUserInfo(message))
#     print("name =", message.sender.name)
#     print("username", message.sender.username)
#     prompt = " ".join(args)
#     print()
#     chat.send("meme part yet to be built")


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
