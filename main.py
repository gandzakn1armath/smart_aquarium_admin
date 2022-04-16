import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("aquarium_key.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

db.collection('person').add({'name':'John', 'age':77})