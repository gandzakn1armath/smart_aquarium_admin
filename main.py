import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate("smart-aquarium.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-aquarium-e9439-default-rtdb.firebaseio.com/'
})

ref = db.reference('/')
ref.child("-N0E8J3ItyjCsWAJ-0l4").update({"first_name":"Torg"})
users = ref.get()

for key, value in users.items():
    user = ref.child(key)
    json_object = json.loads(json.dumps(user.get()))
    print(key)
    print(type(json_object))
    print(json_object["first_name"])

