import telebot
import json
import os

bot_token = "BOT TOKEN"
bot = telebot.TeleBot(bot_token)

def create_data_dir():
    try:
        os.mkdir('data')
    except:
        pass

def get_file_data(message):
    file_type = message.content_type
    file_id = None
    if file_type == 'photo':
        file_id = message.photo[2].file_id
    elif file_type == 'document':
        file_id = message.document.file_id
    elif file_type == 'video':
        file_id = message.video.file_id
    return file_id, file_type

def save_file(message):
    admins = open("admin_list.txt", "r").read().splitlines()
    for admin in admins:
        if str(message.from_user.id) == admin:
            file_id, file_type = get_file_data(message)
            if file_id:
                data_file = open(f"data/{file_id}.json", "w")
                data = {
                    'file_type': file_type,
                    'file_id': file_id
                }
                json.dump(data, data_file)
                bot.send_message(message.chat.id,
                                 f"success saved\nlink to get file\nt.me/{bot.get_me().username}?start={file_id}",
                                 reply_to_message_id=message.id)

@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.text == '/start':
        bot.reply_to(message, f"Hello {message.from_user.first_name},\nWelcome to {bot.get_me().first_name}")
    elif len(message.text.split()) == 2:
        file = message.text.split()[1]
        try:
            with open(f"data/{file}.json", "rb") as file_data:
                file_data = json.loads(file_data.read())
                file_type = file_data['file_type']
                file_id = file_data['file_id']
                if file_type == 'photo':
                    bot.send_photo(message.chat.id, file_id, reply_to_message_id=message.id)
                elif file_type == 'document':
                    bot.send_document(message.chat.id, file_id, reply_to_message_id=message.id)
                elif file_type == 'video':
                    bot.send_video(message.chat.id, file_id, reply_to_message_id=message.id)
        except FileNotFoundError:
            bot.reply_to(message, "File not found")

@bot.message_handler(content_types=["photo", "video", "document"])
def add_file(message):
    create_data_dir()
    save_file(message)

if __name__ == '__main__':
    print("Started")
    print("By Yamete_Kudasai_Oni_Chan")
    bot.infinity_polling()
