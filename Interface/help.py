from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput

import sys
sys.path.append("src")

from MTO.MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=2, padding=20, spacing=20)

        # Button to go to Screen One
        screen_one_button = Button(text="Ir a Pantalla Uno", font_size=20)
        screen_one_button.bind(on_press=self.go_to_screen_one)
        layout.add_widget(screen_one_button)

        # Button to go to Screen Two
        screen_two_button = Button(text="Ir a Pantalla Dos", font_size=20)
        screen_two_button.bind(on_press=self.go_to_screen_two)
        layout.add_widget(screen_two_button)

        # Button to encrypt message
        encrypt_button = Button(text="Encriptar", font_size=20)
        encrypt_button.bind(on_press=self.encrypt_message)
        layout.add_widget(encrypt_button)

        self.add_widget(layout)

    def go_to_screen_one(self, instance):
        self.manager.current = 'screen_one'

    def go_to_screen_two(self, instance):
        self.manager.current = 'screen_two'

    def encrypt_message(self, instance):
        # Llama a la función de encriptación desde encryption.py
        message = "Mensaje a encriptar"  # Reemplaza con el mensaje real que quieres encriptar
        encrypted_message = encrypt_message(message)
        print("Mensaje encriptado:", encrypted_message)

    def on_pre_enter(self, *args):
        # Limpia el contenido de las pantallas cuando vuelvas a la página principal
        self.manager.get_screen('screen_one').clear_widgets()
        self.manager.get_screen('screen_two').clear_widgets()

# Resto del código sigue igual...
# Define Screen One
class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        layout = GridLayout(cols=1, padding=20, spacing=20)

        # Label and button to return to the main screen
        self.etiqueta = Label(text="Encriptar mensaje", font_size=24)
        layout.add_widget(self.etiqueta)
        self.Texto = TextInput(font_size=40,
                      size_hint_y=None,
                      height=100,
                      text='Escriba aqui lo que desea encriptar')
        layout.add_widget(self.Texto)
        self.Texto2 = TextInput(font_size=40,
                      size_hint_y=None,
                      height=100,
                      text='Escriba aqui la contraseña')
        layout.add_widget(self.Texto2) 
        layout2 = GridLayout(cols=2, padding=20, spacing=20)
        encrypt_button = Button(text="Encriptar", font_size=20)
        encrypt_button.bind(on_press=self.EncriptMessage)
        layout2.add_widget(encrypt_button)
        
        back_button = Button(text="Volver a la Principal", font_size=20)
        back_button.bind(on_press=self.go_back_to_main)
        layout2.add_widget(back_button)
        layout.add_widget(layout2)

        self.add_widget(layout)

    def go_back_to_main(self, instance):
        self.manager.current = 'main'  # Access ScreenManager through app

    def EncriptMessage(self, value):
        try:
            self.etiqueta.text = "Hola"
        except Exception as err:
            self.etiqueta.text = Exception

# Define Screen Two
class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        layout = GridLayout(cols=1, padding=20, spacing=20)
        label = Label(text="Desencriptar mensaje", font_size=24)
        layout.add_widget(label)
        self.Texto = TextInput(font_size=40,
                      size_hint_y=None,
                      height=100,
                      text='Escriba aqui lo que desea desencriptar')
        layout.add_widget(self.Texto)
        self.Texto2 = TextInput(font_size=40,
                      size_hint_y=None,
                      height=100,
                      text='Escriba aqui la contraseña')
        layout.add_widget(self.Texto2) 

        layout2 = GridLayout(cols=2, padding=20, spacing=20)
        decrypt_button = Button(text="Desencriptar", font_size=20)
        decrypt_button.bind(on_press=self.go_back_to_main)
        layout2.add_widget(decrypt_button)
        
        back_button = Button(text="Volver a la Principal", font_size=20)
        back_button.bind(on_press=self.go_back_to_main)
        layout2.add_widget(back_button)
        layout.add_widget(layout2)



        self.add_widget(layout)

    def go_back_to_main(self, instance):
        self.manager.current = 'main'  # Access ScreenManager through app

# Create the ScreenManager and add the screens
class ScreenManagerApp(App):
    def __init__(self, **kwargs):
        super(ScreenManagerApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

        # Add the screens to the manager
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(ScreenOne(name='screen_one'))
        self.sm.add_widget(ScreenTwo(name='screen_two'))

        self.main_screen = self.sm.get_screen('main')

    def build(self):
        return self.sm

if __name__ == '__main__':
    ScreenManagerApp().run()

