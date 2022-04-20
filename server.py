from time import sleep
import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading

cred = credentials.Certificate("aquarium_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

phone_number = ""
password = ""
users = None
bot = telebot.TeleBot('5214025271:AAEMvGMgQhRuB19T9BSN5ViEnX1YjnB1Wxk')


def get_user_data(id, key):
    return db.collection('user').document(id).get().to_dict().get(key)


def update_database():

    while True:
        list = db.collection('user').stream()
        if list:
            print("datark che")
            global users
            users = list
            sleep(3600)
        else:
            print("datark e")
            sleep(60)


def get_user_id(telegram_id):
    global users
    for user in users:
        if telegram_id == user.get("telegram_id"):
            return user.id
    return None


@bot.message_handler(commands=["start"])
def start(message, res=False):
    global phone_number, password
    phone_number = ""
    password = ""
    bot.send_message(message.from_user.id, "Welcome to Armath Aquarium Bot")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Login")
    markup.add(item1)
    bot.send_message(message.from_user.id, 'Please Check',
                     reply_markup=markup)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    print(message)
    text = message.text
    id = message.from_user.id
    if text == "Login":
        bot.send_message(id, "Please write your number")
        bot.register_next_step_handler(message, reg_number)
    elif text == "white led":
        user_id = get_user_id(id)
        if user_id:
            white = get_user_data(user_id, "white_led")
            db.collection('user').document(user_id).update({'white_led': not white})


def reg_number(message):
    global phone_number
    id = message.from_user.id
    phone_number = message.text
    bot.send_message(id, "Please write your password")
    bot.register_next_step_handler(message, reg_password)


def reg_password(message):
    global password
    global phone_number
    global users
    id = message.from_user.id
    password = message.text
    is_check_number = False
    for user in users:
        user_phone_number = user.get("phone_number")
        user_password = user.get("password")
        telegram_id = user.get("telegram_id")
        if user_phone_number == phone_number and user_password == password:
            phone_number = ""
            password = ""
            is_check_number = True
            if telegram_id == "null":
                db.collection('user').document(user.id).update({'telegram_id': message.from_user.id})
                bot.send_message(id, "Your registration successful")
            else:
                bot.send_message(id, "Your login successful")
        break

    if is_check_number:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        white_led = types.KeyboardButton("white led")
        yellow_led = types.KeyboardButton("yellow led")
        feed = types.KeyboardButton("feed")
        filter = types.KeyboardButton("filter")
        heater = types.KeyboardButton("heater")
        status = types.KeyboardButton("status")
        sensors = types.KeyboardButton("sensors")
        markup.add(white_led)
        markup.add(yellow_led)
        markup.add(feed)
        markup.add(filter)
        markup.add(heater)
        markup.add(status)
        markup.add(sensors)
        bot.send_message(message.from_user.id, 'Please Check',
                         reply_markup=markup)
    else:
        bot.send_message(id, "incorrect phone number or password, please write again")
        bot.register_next_step_handler(message, reg_number)


threadUpdate = threading.Thread(target=update_database)
threadUpdate.start()

bot.infinity_polling()
