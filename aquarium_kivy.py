from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window


kv_login = '''
Screen:
    MDCard:
        size_hint: None, None
        size: 650,600
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
        size: 650,650
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 65
        spacing: 35
        orientation: 'vertical'
        MDFillRoundFlatButton:
            text:"White Led"
            background_color: 0,1,1,1
        MDFillRoundFlatButton:
            text:"Yellow Led"
            background_color:  0,1,1,1
        MDFillRoundFlatButton:
            text:"Filter"
            background_color: 0,1,1,1
        MDFillRoundFlatButton:
            text:"Heater"
            background_color: 0,1,1,1
        MDFillRoundFlatButton:
            text:"Feed"
            background_color:  0,1,1,1 
            
    BoxLayout:
        orientation:'vertical'
        Image:
            source: "./res/icons/beaker_highres.png"
        Image:
            source: "./res/icons/jermachap.png"
        Image:
            source: "./res/icons/jermachap.png"
        Image:
            source: "./res/icons/aquarium.png"
        Image:
            source: "./res/icons/humidity.png" 
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