import threading
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("smart-aquarium.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-aquarium-e9439-default-rtdb.firebaseio.com/'
})

ref = db.reference('/')

Window.size = (300, 550)
KV = '''
Screen:
    MDCard:
        size_hint: None, None
        size: 300, 550
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 65
        spacing: 35
        orientation: 'vertical'
        MDIcon:
            icon: 'account'
            icon_color: 1, 1, 1, 1
            halign: 'center'
            font_size: 150
        MDTextFieldRound:
            id: first_name
            icon_left: "account-check"
            hint_text: "First Name"
            foreground_color: 1, 1, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20
            pos_hint: {"center_x": 0.5}
        MDTextFieldRound:
            id: last_name
            icon_left: "account-check"
            hint_text: "Last Name"
            foreground_color: 1, 1, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20            
            pos_hint: {"center_x": 0.5}
        MDTextFieldRound:
            id: phone_number
            icon_left: "phone"
            hint_text: "Phone Number"
            foreground_color: 1, 1, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20            
            pos_hint: {"center_x": 0.5}
        MDTextFieldRound:
            id: password
            icon_left: "eye-off"
            hint_text: "Password"
            foreground_color: 1, 1, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20            
            pos_hint: {"center_x": 0.5}
            password: True
        MDFillRoundFlatButton:
            text: "SIGN UP"
            font_size: 15
            pos_hint: {"center_x": 0.5}
            on_press: app.sign_up()
'''


class RegistrationApp(MDApp):
    dialog = None
    def build(self):
        # define theme colors
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Blue"
        self.screen = Builder.load_string(KV)
        return self.screen

    def registration(self):
        self.first_name = self.screen.ids.first_name
        self.last_name = self.screen.ids.last_name
        self.password = self.screen.ids.password
        self.phone_number = self.screen.ids.phone_number

        ref.push({"first_name": self.first_name.text,
                                   "last_name": self.last_name.text,
                                   "phone_number": self.phone_number.text,
                                   "password": self.password.text,
                                   "telegram_id": [""],
                                   "bobber": 0,
                                   "feed": 0,
                                   "filter": 0,
                                   "heater": 0,
                                   "led_white": 0,
                                   "led_yellow": 0,
                                   "water_acidity": 0,
                                   "water_temperature": 0,
                                   "temperature": 0,
                                   "humidity": 0})

    def sign_up(self):
        self.threadSignUp = threading.Thread(target=self.registration)
        self.threadSignUp.start()
        if not self.dialog:
            self.dialog = MDDialog(text="You are register successful",
                                   buttons=[MDFlatButton(text='CLOSE',on_release=self.close)])
        self.dialog.open()


    def close(self,instanse):
        self.dialog.dismiss()
        self.first_name.text = ""
        self.last_name.text = ""
        self.password.text = ""
        self.phone_number.text = ""

RegistrationApp().run()