import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("aquarium_key.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

first_name = input("input first name\n")
last_name = input("input last name\n")
phone_number = input("input phone number\n")
password = input("input password\n")

db.collection('user').add({'first_name':first_name,
                           'last_name':last_name,
                           'phone_number':phone_number,
                           'password':password,
                           'telegram_id':"null",
                           'bobber':0,
                           'feed':0,
                           'filter':0,
                           'heater':0,
                           'led_white':0,
                           'led_yellow':0,
                           'water_acidity':0,
                           'water_temperature':0,
                           'temperature':0,
                           'humidity':0 })
print("Finish")