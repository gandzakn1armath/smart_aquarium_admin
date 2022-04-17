import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import telepot
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

def handle(msg):
    chat_id = msg['chat']['id']
    telegramText = msg['text'].lower()

    print("Message received from " + str(chat_id))
    print("Message  " + telegramText)

    if telegramText == "/start":
        bot.sendMessage(chat_id, "Welcome to Armath Aquarium Bot")
        bot.sendMessage(chat_id, "Input your phone number")





bot = telepot.Bot('5214025271:AAHXYu-8FBD9TAwDVgn2syC7xzveH8gqU-s')
bot.message_loop(handle)
