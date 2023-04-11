import telebot
import json
import os

bot_token = "BOT TOKEN"
bot = telebot.TeleBot(bot_token)
print("Started")
print("By Yamete_Kudasai_Oni_Chan")


try:
    os.mkdir('data')
except:
    pass


@bot.message_handler(commands=['start'])
def StartHandler(message):
    if message.text == '/start':
        bot.reply_to(message, f"Hello {message.from_user.first_name},\nWelcome to {bot.get_me().first_name}")
    if len(message.text.split()) == 2:
        file = message.text.split()[1]
        file_data = open(f"data/{file}.json", "rb")
        file_data = json.loads(file_data.read())
        if file_data['file_type'] == 'photo':
            bot.send_photo(message.chat.id, file_data['file_id'], reply_to_message_id=message.id)
        if file_data['file_type'] == 'document':
            bot.send_document(message.chat.id, file_data['file_id'], reply_to_message_id=message.id)
        if file_data['file_type'] == 'video':
            bot.send_video(message.chat.id, file_data['file_id'], reply_to_message_id=message.id)


@bot.message_handler(content_types=["photo"])
def AddFile(message):
    admins = open("admin_list.txt", "r").read().splitlines()
    for admin in admins:
        if str(message.from_user.id) == admin:
            data_file = open("data/" + message.photo[2].file_unique_id + ".json", "w")
            data = {
                'file_type': f'{message.content_type}',
                'file_id': message.photo[2].file_id
            }
            json.dump(data, data_file)
            bot.send_message(message.chat.id,
                             f"success saved\nlink to get file\nt.me/{bot.get_me().username}?start={message.photo[2].file_unique_id}",
                             reply_to_message_id=message.id)


@bot.message_handler(content_types=["video"])
def AddFile(message):
    admins = open("admin_list.txt", "r").read().splitlines()
    for admin in admins:
        if str(message.from_user.id) == admin:
            data_file = open("data/" + message.video.file_unique_id + ".json", "w")
            data = {
                'file_type': f'{message.content_type}',
                'file_id': message.video.file_id
            }
            json.dump(data, data_file)
            bot.send_message(message.chat.id,
                             f"success saved\nlink to get file\nt.me/{bot.get_me().username}?start={message.video.file_unique_id}",
                             reply_to_message_id=message.id)


@bot.message_handler(content_types=["document"])
def AddFile(message):
    admins = open("admin_list.txt", "r").read().splitlines()
    for admin in admins:
        if str(message.from_user.id) == admin:
            data_file = open("data/" + message.document.file_unique_id + ".json", "w")
            data = {
                'file_type': f'{message.content_type}',
                'file_id': message.document.file_id
            }
            json.dump(data, data_file)
            bot.send_message(message.chat.id,
                             f"success saved\nlink to get file\nt.me/{bot.get_me().username}?start={message.document.file_unique_id}",
                             reply_to_message_id=message.id)


bot.infinity_polling()
