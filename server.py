from time import sleep
import telebot
from telebot import types

"""
cred = credentials.Certificate("aquarium_key.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

list = db.collection('user')
users = list.stream()

for user in users:
    print(user.id)
    print(user.get("first_name"))

"""



bot = telebot.TeleBot('5214025271:AAHXYu-8FBD9TAwDVgn2syC7xzveH8gqU-s')

@bot.message_handler(commands=["start"])
def start(message, res=False):
    bot.send_message(message.chat.id, "Welcome to Armath Aquarium Bot")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Login")
    item2 = types.KeyboardButton("Sign Up")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Please Check',
                     reply_markup=markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(message)


# Запускаем бота
bot.polling(none_stop=True, interval=0)

