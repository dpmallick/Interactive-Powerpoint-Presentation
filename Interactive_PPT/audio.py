import speech_recognition as sr
import re
import pynput.keyboard as Keyboard
from pynput.keyboard import Key, Controller
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pyttsx3
# initialize Text-to-speech engine


class _TTS:

    engine = None
    rate = None

    def __init__(self):
        self.engine = pyttsx3.init()

    def start(self, text_):
        self.engine.setProperty("rate", 178)
        self.engine.say(text_)
        self.engine.runAndWait()


keyboard = Keyboard.Controller()



def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=5)

        try:
            # print("Recognizing...")
            query = r.recognize_google(audio)  # Using google for voice recognition. language='en-in'
            # print(f"User said: {query}\n")  # User query will be printed.

        except Exception as e:
            # print(e)
            # print("Say that again please...")  # Say that again will be printed in case of improper voice
            return "None"  # None string will be returned
        return query


def has_number(text):
    return any(char.isdigit() for char in text)

def audio_call():
    while True:
        query = takeCommand().lower()

        if 'happy' in query:
            if 'present' in query:
                # print('Present')

                text = "Presenting Screen"
                tts = _TTS()
                tts.start(text)
                del(tts)

                keyboard.press(Key.f5)
                keyboard.release(Key.f5)
            elif 'next' in query:
                # print('Next')
                text = 'Going to Next Screen'
                tts = _TTS()
                tts.start(text)
                del (tts)

                keyboard.press('n')
                keyboard.release('n')

            elif 'go back' in query:
                # print('go back')
                text = 'Going back to Previous Screen'
                tts = _TTS()
                tts.start(text)
                del (tts)

                keyboard.press('p')
                keyboard.release('p')
            elif 'end of slide' in query:
                # print('End of slide')

                text = 'Exiting Presentation Mode'
                tts = _TTS()
                tts.start(text)
                del (tts)

                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
            elif has_number(query):
                try:
                    go_to = re.findall('[0-9]+', query)[0]
                    # print(go_to)
                    text = f'Going to Screen {go_to}'
                    tts = _TTS()
                    tts.start(text)
                    del (tts)

                    if len(go_to) > 1:

                        keyboard.press(str(int(go_to) // 10))
                        keyboard.release(str(int(go_to) // 10))
                        keyboard.press(str(int(go_to) % 10))
                        keyboard.release(str(int(go_to) % 10))
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
                    else:
                        keyboard.press(go_to)
                        keyboard.release(go_to)
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
                except:
                    word = []
                    word.append(query)
                    query1 = 'go back'
                    query2 = 'end of slide'
                    word.append(query1)
                    word.append(query2)
                    vectorizer = TfidfVectorizer()
                    vector1 = vectorizer.fit_transform(word[0])
                    vector2 = vectorizer.transform(word[1])
                    vector3 = vectorizer.transform(word[2])
                    sim = cosine_similarity(vector1, vector2)
                    sim1 = cosine_similarity(vector1, vector3)
                    if (sim >= 0.7):
                        # print('go back')
                        keyboard.press('p')
                        keyboard.release('p')
                    elif (sim1 >= 0.7):
                        # print('end of slide')
                        keyboard.press(Key.esc)
                        keyboard.release(Key.esc)
                        keyboard.press(Key.esc)
                        keyboard.release(Key.esc)
                    else:
                        pass
            else:

                pass
        else:
            pass

# audio_call()
