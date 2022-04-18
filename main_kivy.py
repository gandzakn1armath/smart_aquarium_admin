from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
# set window size
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
            icon_color: 0, 0, 0, 0
            halign: 'center'
            font_size: 150
        MDTextFieldRound:
            id: first_name
            icon_left: "account-check"
            hint_text: "First Name"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20
            pos_hint: {"center_x": 0.5}
        MDTextFieldRound:
            id: last_name
            icon_left: "account-check"
            hint_text: "Last Name"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20            
            pos_hint: {"center_x": 0.5}
        MDTextFieldRound:
            id: phone_number
            icon_left: "phone"
            hint_text: "Phone Number"
            foreground_color: 1, 0, 1, 1
            size_hint_x: None
            width: 220
            font_size: 20            
            pos_hint: {"center_x": 0.5}
        MDTextFieldRound:
            id: password
            icon_left: "eye-off"
            hint_text: "Password"
            foreground_color: 1, 0, 1, 1
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


class LoginApp(MDApp):
    dialog = None
    def build(self):
        # define theme colors
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Blue"
        # load and return kv string
        return Builder.load_string(KV)

    def sign_up(self):
        print("aso")
        if not self.dialog:
            self.dialog = MDDialog(text="You are register succes")


        self.dialog.open()

    def close(self, instance):
        # close dialog
        self.dialog.dismiss()




    # run app
LoginApp().run()