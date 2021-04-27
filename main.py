import os

import kivy
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard

from filesharer import FileSharer

import webbrowser
import speech_recognition as sr
import textwrap as tw

Builder.load_file('frontend.kv')


class StartScreen(Screen):
    welcome_text = """Don't you just hate taking notes on lectures? Well, you came to the right place. Here, we all hate taking notes. 
That's why I made an app to take notes for me. 

All you need is a sound file that is downloaded on your computer (MUST BE A .wav FILE) or a working microphone.
If you choose the microphone option, you will be asked to enter the number of seconds you want to speak with 
microphone. As soon as you press the start button, the microphone will start."""

    def from_file(self):
        self.manager.current = 'audio_screen'

    def from_mic(self):
        self.manager.current = 'mic_screen'


class MicScreen(Screen):
    mic_image = 'mic_image.png'

    def start(self):
        r = sr.Recognizer()
        mic = sr.Microphone()

        record_time = self.ids.time_text.text if self.ids.time_text.text else 5

        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source, duration=float(record_time))

        self.filepath = 'recognized.txt'
        recognized = r.recognize_google(audio)
        t_w = tw.TextWrapper()
        recognized = t_w.fill(recognized)
        if len(recognized) > 0:
            words_as_bytes = bytes(recognized, 'utf-8')
            with open(self.filepath, 'wb') as file:
                file.write(words_as_bytes)

        fs = FileSharer(self.filepath)
        self.url = fs.share()

        self.manager.current = 'display_screen'
        self.manager.current_screen.ids.link_text.text = self.url


class AudioScreen(Screen):

    def convert(self):
        home = os.path.expanduser("~")
        os.chdir(os.path.join(home, "Downloads"))
        
        r = sr.Recognizer()
        audio_file = os.path.abspath(self.ids.file.text)
        audio_file = sr.AudioFile(audio_file)

        with audio_file as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)

        self.filepath = 'recognized.txt'
        recognized = r.recognize_google(audio)
        t_w = tw.TextWrapper()
        recognized = t_w.fill(recognized)
        words_to_bytes = bytes(recognized, 'utf-8')
        with open(self.filepath, 'wb') as file:
            file.write(words_to_bytes)

        fs = FileSharer(self.filepath)
        self.url = fs.share()

        self.manager.current = 'display_screen'
        self.manager.current_screen.ids.link_text.text = self.url


class DisplayScreen(Screen):

    def copy(self):
        link = self.ids.link_text.text
        Clipboard.copy(link)
        self.ids.copy_button.text = 'Link Copied!'

    def open(self):
        link = self.ids.link_text.text
        webbrowser.open(link)


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()

main_app = MainApp()
main_app.build()
main_app.run()
