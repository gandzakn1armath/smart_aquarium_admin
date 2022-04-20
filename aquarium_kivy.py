from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window

Window.size = (550,400)
kv_login = '''
Screen:
    MDCard:
        size_hint: None, None
        size: 550, 400
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 65
        spacing: 35
        orientation: 'vertical'
        MDIcon:
            icon: 'account'
            icon_color: 1, 0, 0, 1
            halign: 'center'
            font_size: 150
        MDTextFieldRound:
            id: phone_number
            icon_left: "phone"
            hint_text: "Phone Number"
            line_color_focus: 1, 0, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20            
            pos_hint: {"center_x": 0.5}
        MDTextFieldRound:
            id: password
            icon_left: "eye-off"
            hint_text: "Password"
            line_color_focus: 1, 0, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20            
            pos_hint: {"center_x": 0.5}
            password: True
        MDFillRoundFlatButton:
            text: "LOGIN"
            font_size: 15
            pos_hint: {"center_x": 0.5}
            on_press: login()
'''
kv_aquarium='''
Screen:
    MDCard:
        size_hint: None, None
        size: 550, 550
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 65
        spacing: 35
        orientation: 'vertical'
        Image:
            source: "./res/icons/beaker_highres.png"
        Image:
            source: "./res/icons/jermachap.png"
            size_hint_x:0.25
        Image:
            source: "./res/icons/jermachap.png"
            size_hint_x:0.25
        Image:
            source: "./res/icons/lamp.jpg"
            size_hint_x:1.75
            pos_hint:{'center_x':0.75,'y':0.35}
        Image:
            source: "./res/icons/lamp.jpg"
            size_hint_x:1.75
        Image:
            source: "./res/icons/feed.png"
            pos_hint:{'center_x':0.95,'y':0.35}
            pos_hint:{'center_y':0.5,'y':0.15}
        Image:
            source: "./res/icons/aquarium.png"
            size_hint_x:1.75
            
            
'''
class AquariumApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen = Builder.load_string(kv_aquarium)
        return self.screen

class LoginApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.accent_palette = "Blue"
        self.screen = Builder.load_string(kv_login)
        return self.screen


AquariumApp().run()