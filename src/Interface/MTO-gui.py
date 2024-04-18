from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
from kivy.uix.textinput import TextInput
from kivy.config import Config

import sys
sys.path.append("src")

from MTO.MTO import encrypt_message, decrypt_message, EncryptionError, DecryptionError

# Define the main screen
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.widgets = self._create_widgets()  # Guarda una copia de los widgets iniciales
        self.update_widgets()

    def _create_widgets(self):    
        layout = GridLayout(cols=1, padding=20, spacing=20,)

        self.Etiqueta = Label(text='Hola, que deseas hacer el dia de hoy?',font_size=40)
        layout.add_widget(self.Etiqueta)
        layout2 = GridLayout(cols=2, padding=20, spacing=20)
        # Button to go to Screen One
        screen_one_button = Button(text="Encriptar Mensaje", font_size=20)
        screen_one_button.bind(on_press=self.go_to_screen_one)
        layout2.add_widget(screen_one_button)

        # Button to go to Screen Two
        screen_two_button = Button(text="Desencriptar mensaje", font_size=20)
        screen_two_button.bind(on_press=self.go_to_screen_two)
        layout2.add_widget(screen_two_button)
        layout.add_widget(layout2)

        self.add_widget(layout)
        
        return layout

    def go_to_screen_one(self, instance):
        self.manager.current = 'screen_one'  # Access ScreenManager through app
        

    def go_to_screen_two(self, instance):
        self.manager.current = 'screen_two'  # Access ScreenManager through app
        

    def update_widgets(self):
        self.clear_widgets()  # Limpiar los widgets existentes
        self.add_widget(self.widgets)  # Agregar los widgets guardados

    def go_back_to_main(self, instance):
        self.manager.current = 'main'  # Acceder al ScreenManager a través de la app




class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        
        self.widgets = self._create_widgets()  # Guarda una copia de los widgets iniciales
        self.update_widgets()
    
    def _create_widgets(self):    
        # Label and button to return to the main screen
        layout = GridLayout(cols=1, padding=20, spacing=20)
        self.etiqueta = Label(text="Encriptar mensaje", font_size=24)
        layout.add_widget(self.etiqueta)
        self.Texto = TextInput(font_size=40,
                      size_hint_y=None,
                      height=100,
                      text='Escriba aqui lo que desea encriptar')
        self.Texto.bind(focus=self.on_text_focus)  # Agregar el enlace al evento on_focus
        layout.add_widget(self.Texto)
        self.Texto2 = TextInput(font_size=40,
                      size_hint_y=None,
                      height=100,
                      text='Escriba aqui la contraseña')
        self.Texto2.bind(focus=self.on_text_focus) 
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
        return layout

    def update_widgets(self):
        self.clear_widgets()  # Limpiar los widgets existentes
        self.add_widget(self.widgets)  # Agregar los widgets guardados

    def go_back_to_main(self, instance):
        self.manager.current = 'main'  # Acceso al ScreenManager a través de la app
        # Limpiar los campos de texto
        self.Texto.text = 'Escriba aqui lo que desea encriptar'
        self.Texto2.text = 'Escriba aqui la contraseña'
        # Restablecer el texto inicial de la etiqueta
        self.etiqueta.text = "Encriptar mensaje"
        
    def EncriptMessage(self, value):
        try:
            message = self.Texto.text
            password = self.Texto2.text
            encrypted_message = encrypt_message(message, password)
            self.etiqueta.text = "Mensaje encriptado: " + encrypted_message
            # Habilitar la copia del mensaje encriptado al portapapeles
            Clipboard.copy(encrypted_message)
        except EncryptionError as e:
            self.etiqueta.text =  str(e)
    
    def on_text_focus(self, instance, focused):
        if focused:
            if instance.text == 'Escriba aqui lo que desea encriptar':
                instance.text = ''  # Borrar el texto inicial cuando se enfoca el campo de texto
        if focused:
            if instance.text == 'Escriba aqui la contraseña':
                instance.text = ''  # Borrar el texto inicial cuando se enfoca el campo de texto

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
        self.Texto.bind(focus=self.on_text_focus)  # Agregar el enlace al evento on_focus
        layout.add_widget(self.Texto)
        self.Texto2 = TextInput(font_size=40,
                      size_hint_y=None,
                      height=100,
                      text='Escriba aqui la contraseña')
        self.Texto2.bind(focus=self.on_text_focus) 
        layout.add_widget(self.Texto2) 

        layout2 = GridLayout(cols=2, padding=20, spacing=20)
        decrypt_button = Button(text="Desencriptar", font_size=20)
        decrypt_button.bind(on_press=self.DesencriptMessage)
        layout2.add_widget(decrypt_button)
        
        back_button = Button(text="Volver a la Principal", font_size=20)
        back_button.bind(on_press=self.go_back_to_main)
        layout2.add_widget(back_button)
        layout.add_widget(layout2)

        self.etiqueta = Label(text='', font_size=20)
        layout.add_widget(self.etiqueta)  # Añadir la etiqueta para mostrar el mensaje desencriptado

        self.add_widget(layout)

    def go_back_to_main(self, instance):
        self.manager.current = 'main'  # Acceso al ScreenManager a través de la app
        # Limpiar los campos de texto
        self.Texto.text = 'Escriba aqui lo que desea desencriptar'
        self.Texto2.text = 'Escriba aqui la contraseña'
        # Restablecer el texto inicial de la etiqueta
        self.etiqueta.text = "Desencriptar mensaje"
        
    def DesencriptMessage(self, value):
        try:
            # Obtener el mensaje encriptado del portapapeles
            ciphertext = self.Texto.text
            password = self.Texto2.text
            decrypted_message = decrypt_message(ciphertext, password)
            self.etiqueta.text = "Mensaje desencriptado: " + decrypted_message
        except DecryptionError as e:
            self.etiqueta.text = str(e)
    
    def on_text_focus(self, instance, focused):
        if focused:
            if instance.text == 'Escriba aqui lo que desea desencriptar':
                instance.text = ''  # Borrar el texto inicial cuando se enfoca el campo de texto
        if focused:
            if instance.text == 'Escriba aqui la contraseña':
                instance.text = ''  # Borrar el texto inicial cuando se enfoca el campo de texto
    

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