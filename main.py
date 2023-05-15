from googletrans import Translator, constants
from gtts import gTTS
from pygame import mixer
# from translate import Translator
# from deepgram import Deepgram

import os
import time
import speech_recognition as sr

def translatetext(MyText):
    translator = Translator()
    translation = translator.translate(MyText, dest="ja")
    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
    return translation


def textToSpeech(translatedText):
    speech = gTTS(translatedText.text, lang='ja')
    speech.save('testTranslation.mp3')

    mixer.init()
    mixer.music.load("testTranslation.mp3")
    mixer.music.play()

    x = mixer.Sound("testTranslation.mp3")
    time.sleep(x.get_length())
    mixer.music.unload()
    if os.path.exists("testTranslation.mp3"):
        os.remove("testTranslation.mp3")

def speechToText():
    r = sr.Recognizer()

    print(sr.Microphone.list_microphone_names())
    while 1:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("finished_adjust")
                audio = r.listen(source, timeout=2)
                print("finished_listened")
                MyText = r.recognize_google(audio)
                print("finished_recognized")
                print(MyText)
                translatedtext = translatetext(MyText)
                textToSpeech(translatedtext)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except LookupError:
            print("Cannot understand audio")
        except sr.UnknownValueError:
            print("unknown error occurred")
        except sr.WaitTimeoutError:
            print("Nothing is being said")


speechToText()
