from googletrans import Translator, constants
from gtts import gTTS
from kivy.uix.boxlayout import BoxLayout
from pygame import mixer
# from translate import Translator
# from deepgram import Deepgram

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import StringProperty

import asyncio
import pyaudio
import os
import time
import speech_recognition as sr
import threading


class MainWidget(BoxLayout):
    # mic status
    my_text = StringProperty("Mic is not on")
    # translation result
    my_text2 = StringProperty()

    # ignore, meant for the clock thing that I tried to implement
    textForMicStatus = ""
    textFromTranslation = ""
    isTransButtonDisabled = False

    def on_button_click(self):
        # print("A"+self.my_text.)

        ##SO MANY DEBUG PRINTS
        # print("B12"+self.textForMicStatus)
        # print("Yes, Button Is clicked")

        # KIVY WHY YOU NO WORK, WHY DO THE SPEECH METHOD FIRST AND THEN UPDATE THE TEXT LABEL!!!, MIGHT BE THREADING
        # THING OR SOMETHING IDK

        # self.ids.transbutton.disabled = True
        # self.my_text = "Mic is on"

        threading.Thread(target=speechToText()).start()

        # self.ids.transbutton.disabled = False

        ##SO MANY DEBUG PRINTS
        # print("A" + self.my_text)
        # print("B22" + self.textForMicStatus)

    # Attempt in using kivy's clock package, but it keeps asking for dt as parameter. But in the kivy documentation,
    # theres no reference of dt being passed as parameter
    """
    def update(self, dt):
        if (self.textFromTranslation==True):
            self.ids.transbutton.disabled = True
        else:
            self.ids.transbutton.disabled = False
        self.update_myTextLabel()
        self.update_myText2Label()
    def update_myTextLabel(self):
        self.my_text = self.textForMicStatus
    def update_myText2Label(self):
        self.my_text2 = self.textFromTranslation

    """


class TransApp(App):
    def build(self):
        app = MainWidget()

        ##Ignore, debuging and experimenting with clocks
        # print("A"+MainWidget.my_text)
        # print("B11"+MainWidget.textForMicStatus)
        # Clock.schedule_interval(app.update, 0.5)

        return MainWidget()

        ##Ignore, debuging
        # print("A" + MainWidget.my_text)
        # print("B21" + MainWidget.textForMicStatus)


def translatetext(MyText):
    # note: the translation python package uses a workaround by sending the text directly to google translate's
    # website, not using Google's cloud services (they do offer it but like hell I am using up my free $200 credit
    # from google cloud just for a measly translation prototype, and also that would also burn my credit from the
    # amount of debugging)

    translator = Translator()

    # each language is indetifyed by a 2 letter initial according to some database, e.g: JA = japanese, EN = english
    translation = translator.translate(MyText, dest="ja")

    # For debug
    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    return translation


def textToSpeech(translatedText):
    # A text speech package that uses google's text to speech to speak words from the given string, idk how it is
    # completely free as the google cloud one is paid but if its a good workaround that keeps my cost to 0,
    # then yea i am gonna use it. also its like the only package that I found so far that has japanese speech
    speech = gTTS(translatedText.text, lang='ja')

    # for some reason to play the audio, you must save it as a mp3 and then play it. If I let it be, its gonna make
    # 1m+ and beyond of them. the amount of space required would be crazy. So i later created some code where it
    # disposes it when its done speaking, TAKE THAT ONLINE FREE TUTORIALS for making translation apps, you didn't
    # even bother thinking of that!
    speech.save('testTranslation.mp3')

    # uses pygame, cuz the simple playaudio package had some very sus crap when I was downloading it (according to my
    # antivirus)
    mixer.init()
    mixer.music.load("testTranslation.mp3")
    mixer.music.play()

    # most getto way of obtaining the length of the music
    x = mixer.Sound("testTranslation.mp3")
    time.sleep(x.get_length())
    # unload the audio, just in case
    mixer.music.unload()

    # bye bye mp3, we don't need you anymore
    if os.path.exists("testTranslation.mp3"):
        os.remove("testTranslation.mp3")


def speechToText():
    # sets up the voice recognizer object
    r = sr.Recognizer()

    # MainWidget.textForMicStatus = "Mic is On"
    # print(MainWidget.my_text)

    # debug, need to know if my audio driver is there
    print(sr.Microphone.list_microphone_names())

    # need an infinite loop to allow users to retry until the app recongizes a voice
    while 1:

        # actions like not speaking or nothing being heard counts as an exception, so we need to catch them
        try:
            # makes sure it gets the mic
            with sr.Microphone() as source:

                # adjusts for bg noise
                r.adjust_for_ambient_noise(source, duration=1)

                # listens for voices, if no voice for 2 secs, creates WaitTimeoutError exception
                print("finished_adjust")
                audio = r.listen(source, timeout=2)

                # found voice and is now converting it to text
                print("finished_listened")
                MyText = r.recognize_google(audio)
                print("finished_recognized")

                # send text to translation and text to speech method
                # print(MyText)
                translatedtext = translatetext(MyText)
                textToSpeech(translatedtext)

                # since we successful got the voice, we can break out of the loop and stop
                break

        # exceptions, the print messages would give you a clear idea as to what they are. Except for the request
        # error, thats for failing to request results from the text to speech, speech to text, and translation packages
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except LookupError:
            print("Cannot understand audio")
        except sr.UnknownValueError:
            print("unknown error occurred")
        except sr.WaitTimeoutError:
            print("Nothing is being said")

    # Debug stuff and updating kivy label, which barely works properly atm
    # MainWidget.textForMicStatus = "Mic is not on"
    MainWidget.textFromTranslation = f"{translatedtext.origin} ({translatedtext.src}) --> {translatedtext.text} ({translatedtext.dest})"
    print("Ended")


# LAUNCH THE APPPP
if __name__ == '__main__':
    TransApp().run()

# speechToText()
