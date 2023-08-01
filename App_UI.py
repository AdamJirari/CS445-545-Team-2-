from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class WrapperApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Spotify Wrapper!')
        button = Button(text='test')

        layout.add_widget(label)
        layout.add_widget(button)

        return layout
WrapperApp.run()
