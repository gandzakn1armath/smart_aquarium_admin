from time import sleep
import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("aquarium_key.json")
firebase_admin.initialize_app(cred)

db=firestore.client()



bot = telebot.TeleBot('5214025271:AAHXYu-8FBD9TAwDVgn2syC7xzveH8gqU-s')


@bot.message_handler(commands=["start","help"])
def start(message, res=False):
    bot.send_message(message.from_user.id, "Welcome to Armath Aquarium Bot")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Login")
    item2 = types.KeyboardButton("Sign Up")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.from_user.id, 'Please Check',
                     reply_markup=markup)




@bot.message_handler(func=lambda m: True)
def echo_all(message):
    print(message)
    id = message.from_user.id
    if message.text == "Sign Up":
        list = db.collection('user')
        users = list.stream()
        for user in users:
            print(user.id)
            print(user.get("first_name"))
            print(user.get("phone_number"))
        bot.send_message(id, "Please write your number")
        bot.register_next_step_handler(message, reg_number)

def reg_number(message):
    phone_number = message.text
    print(phone_number)


# Запускаем бота
bot.infinity_polling()

