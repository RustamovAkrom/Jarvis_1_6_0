from vosk import Model, KaldiRecognizer
import pyaudio
import speech_recognition
import pygame
import yaml
from fuzzywuzzy import fuzz

import random
import json
import os
import time

from services import *

commands = dict(yaml.safe_load(open("components/commands.yaml", 'rt', encoding="utf-8")))

# commands = dict(yaml.safe_load(open('commands-example.yaml', 'rt', encoding="utf-8")))


def play_audio(name: str) -> None:
    if name != "greet":
        if name != "not_found":
            if name != "off":
                if name != "ok":
                    if name != "run":
                        if name != "stupid":
                            if name != "thanks":
                                return
                            else:
                                audio_file = "thanks.wav"
                        else:
                            audio_file = "stupid.wav"
                    else:
                        audio_file = "run.wav"
                else:
                    audio_file = f"ok{random.choice([1, 2, 3, 4])}.wav"
            else:
                audio_file = "off.wav"
        else:
            audio_file = "not_found.wav"
    else:
        audio_file = f"greet{random.choice([1, 2, 3])}.wav"

    pygame.init()
    try:
        pygame.mixer.music.load(f"jarvis-og/{audio_file}")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:
        print("Error playing audio ", e)
        
    finally:
        pygame.mixer.quit()
        pygame.quit()


def recongnition_cmd_yaml(text: str) -> dict:
    rc = {"commanda": "", "pracent": 0}
    for commanda, values in commands.items():
        for x in values:
            vrt = fuzz.ratio(text, x)
            if vrt > rc['pracent']:
                rc['commanda'] = commanda
                rc['pracent'] = vrt
    return rc


def speech_to_text_onlayin() -> str:
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 1000
    recognizer.pause_threshold = 0.5
    try:
        with micraphone as source:
            ansver = ""

            recognizer.adjust_for_ambient_noise(micraphone, duration=0.5)

            try:
                print("Listening...")
                audio = recognizer.listen(source, 5, 5)

                with open("micraphone-result.wav", "wb") as file:
                    file.write(audio.get_wav_data())
                
            except speech_recognition.WaitTimeoutError:
                ansver = "Can you check if you micraphone is on, please?"

            try:
                ansver = str(recognizer.recognize_google(audio, language="ru-RU")).lower()

            except speech_recognition.UnknownValueError:
                ansver = "Unknown value error."

            except speech_recognition.RequestError:
                ansver = speech_to_text_offline()
            return ansver
    except:
        # exit(1)
        return ansver


def speech_to_text_offline() -> str:
    ansver = ""
    if not os.path.exists(setting.VOSK_MODEL):
        print(
                "Please download the model from:\n"
                "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder."
            )
        exit(1)
    stream = audio.open(
        format = pyaudio.paInt16, channels = 1,
        rate = 16000, input = True, frames_per_buffer = 8000
    )
    stream.start_stream()
    while True:
        try:
            data = stream.read(4000)
        except:
            exit(1)
        if len(data) == 0:
            break
        if (res.AcceptWaveform(data)):
            ansver = json.loads(res.Result())
            return ansver['text']


def cmd(text: str) -> None:
    command_name = ""
    command_options = []
    print(f"command: {text}")


    text_spliting = text.split()
    if text_spliting:
        command_name = text_spliting[0]
        [command_options.append(str(input_part)) for input_part in text_spliting[1: len(text_spliting)]]
    print(command_name, command_options)
    
    yaml_data = recongnition_cmd_yaml(command_name)
    if yaml_data['pracent'] >= 70:
        play_audio('greet')
        globals()[commands[yaml_data['commanda']][0]['activate']](command_options)
    

def listening() -> str:
    if setting.ACTIVATE_ONLAYIN:
        voices_text = speech_to_text_onlayin()
    else:
        voices_text = speech_to_text_offline()
    return voices_text


def main():
    play_audio("run")

    time.sleep(0.5)
    ltime = time.time() - 1000

    while True:
        voices_text = listening()
        print(voices_text)
        for name in setting.ASISTENT_NAME:
            if fuzz.ratio(voices_text, name) >= 70:
                play_audio("greet")
                print("Yes, sir.")

                time.sleep(0.5)
                ltime = time.time()

                while (time.time() - ltime) <= 15:
                    voices = listening()
                    cmd(voices)
                
            
if __name__=="__main__":

    if not setting.ACTIVATE_ONLAYIN:
        model = Model(setting.VOSK_MODEL)
        audio = pyaudio.PyAudio()
        res = KaldiRecognizer(model, 16000)

    micraphone = speech_recognition.Microphone(setting.MICRAPHONE_DEVICE_INDEX)
    recognizer = speech_recognition.Recognizer()

if __name__=="__main__":
    main()
