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


def get_white_status(white_led):
    if white_led == 0:
        return "White led is off"
    else:
        return "White led is on"


def get_yellow_status(yellow_led):
    if yellow_led == 0:
        return "Yellow led is off"
    else:
        return "Yellow led is on"


def get_filter_status(filter):
    if filter == 0:
        return "Filter is off"
    else:
        return "Filter is on"


def get_heater_status(heater):
    if heater == 0:
        return "Heater is off"
    else:
        return "Heater is on"


def get_water_acidity_status(water_acidity):
    if water_acidity <= 7:
        return "Water is clean"
    else:
        return "Water is not clean"
def get_bobber_status(bobber):
    if bobber == 0:
        return "Water is full"
    else:
        return "Water is scarce"



def get_user_id(telegram_id):
    users = db.collection('user').stream()
    for user in users:
        if telegram_id in user.get("telegram_id"):
            return user.id
    return None

def sensors_data (user_id):
    user_data = db.collection('user').document(user_id).get().to_dict()
    humidity = user_data.get("humidity")
    water_temp = user_data.get("water_temperature")
    temp = user_data.get("temperature")
    water_acidity = user_data.get("water_acidity")
    sensor_data = "Humidity " + str(humidity) + "%" + "\n" + \
                   "Water temperature " + str(water_temp) + "C" + "\n" + \
                   "Air temperature " + str(temp) + "C" + "\n" + \
                   get_water_acidity_status(water_acidity)


    return sensor_data

def login(user_id):
    global phone_number, password
    phone_number = ""
    password = ""
    keyboard = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="Login", callback_data='Login')
    keyboard.add(item1)
    bot.send_message(user_id, "Welcome to Armath Aquarium Bot", reply_markup=keyboard)


def get_user_sensors_data(user_id):
    user_data = db.collection('user').document(user_id).get().to_dict()
    led_white = user_data.get("led_white")
    led_yellow = user_data.get("led_yellow")
    heater = user_data.get("heater")
    filter = user_data.get("filter")
    humidity = user_data.get("humidity")
    water_temp = user_data.get("water_temperature")
    temp = user_data.get("temperature")
    water_acidity = user_data.get("water_acidity")
    bobber = user_data.get("bobber")
    sensors_data = get_white_status(led_white) + "\n" \
                   + get_yellow_status(led_yellow) + "\n" + \
                   get_heater_status(heater) + "\n" +\
                   get_filter_status(filter) + "\n" + \
                   "Humidity "+ str(humidity) +" %" + "\n" + \
                   "Water temperature " + str(water_temp) + " °C" + "\n" +\
                   "Air temperature " + str(temp) + " °C" + "\n" + \
                   get_water_acidity_status(water_acidity) + "\n" +\
                   get_bobber_status(bobber)


    return sensors_data


@bot.message_handler(commands=["start"])
def start(message, res=False):
    login(message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def echo_all(call):
    message = call.message
    text = call.data
    id = call.from_user.id
    if text == "Login":
        bot.send_message(id, "Please write your number")
        bot.register_next_step_handler(message, reg_number)
    elif text == "log out":
        user_id = get_user_id(id)
        telegram_ids = get_user_data(user_id, "telegram_id")
        telegram_ids.remove(id)
        db.collection('user').document(user_id).update({'telegram_id': telegram_ids})
        login(id)
    else:
        user_id = get_user_id(id)
        if user_id:
            if text == "white led":
                white = not get_user_data(user_id, "led_white")
                db.collection('user').document(user_id).update({'led_white': white})
                show_keyboard(id, get_white_status(white))
            elif text == "yellow led":
                yellow = not get_user_data(user_id, "led_yellow")
                db.collection('user').document(user_id).update({'led_yellow': yellow})
                show_keyboard(id, get_yellow_status(yellow))
            elif text == "filter":
                filter = not get_user_data(user_id, "filter")
                db.collection('user').document(user_id).update({'filter': filter})
                show_keyboard(id, get_filter_status(filter))
            elif text == "heater":
                heater = not get_user_data(user_id, "heater")
                db.collection('user').document(user_id).update({'heater': heater})
                show_keyboard(id, get_heater_status(heater))
            elif text == "feed":
                db.collection('user').document(user_id).update({'feed': 1})
                show_keyboard(id, "The fish are fed")
            elif text == "status":
                show_keyboard(id, get_user_sensors_data(user_id))
            elif text == "sensors":
                show_keyboard(id, sensors_data(user_id))
        else:
            login(id)


def reg_number(message):
    global phone_number
    id = message.from_user.id
    phone_number = message.text
    bot.send_message(id, "Please write your password")
    bot.register_next_step_handler(message, reg_password)


def show_keyboard(id, message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 3
    keyboard.add(types.InlineKeyboardButton(text="White led", callback_data='white led'),
                 types.InlineKeyboardButton(text="Yellow led", callback_data='yellow led'))
    keyboard.add(types.InlineKeyboardButton(text="Feed", callback_data='feed'),
                 types.InlineKeyboardButton(text="Filter", callback_data='filter'))
    keyboard.add(types.InlineKeyboardButton(text="Heater", callback_data='heater'))
    keyboard.add(types.InlineKeyboardButton(text="Status", callback_data='status'))
    keyboard.add(types.InlineKeyboardButton(text="Sensors", callback_data='sensors'))
    keyboard.add(types.InlineKeyboardButton(text="Log out", callback_data='log out'))
    bot.send_message(id, message, reply_markup=keyboard)


def reg_password(message):
    global password
    global phone_number
    id = message.from_user.id
    password = message.text
    is_check_number = False
    users = db.collection('user').stream()
    for user in users:
        user_phone_number = user.get("phone_number")
        user_password = user.get("password")

        if user_phone_number == phone_number and user_password == password:
            phone_number = ""
            password = ""
            is_check_number = True
            telegram_ids = list(user.get("telegram_id"))
            if message.from_user.id in telegram_ids:
                bot.send_message(id, "Your login successful")
            else:
                telegram_ids.append(message.from_user.id)
                db.collection('user').document(user.id).update({'telegram_id': telegram_ids})
                bot.send_message(id, "Your login successful")

        break

    if is_check_number:
        show_keyboard(message.from_user.id, "Please check")
    else:
        bot.send_message(id, "incorrect phone number or password, please write again")
        bot.register_next_step_handler(message, reg_number)

print("Start")
bot.polling(none_stop=True, interval=0)
