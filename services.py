from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import os
import random
from tts import speak

import webbrowser
import wikipedia
import json
from fuzzywuzzy import fuzz

from config import setting

proposals = json.load(open("components/proposals.json", 'r', encoding="utf-8"))


def PlaceholderFile(path: str) -> str:
    musiks = os.listdir(path)
    return path + "/" + musiks[random.randint(0, len(musiks))]


def recognition_cmd_json(text: str):
    rc = {"commanda": "", "pracent": 0}
    for options in proposals:
        for x in options['tbr']:
            vrt = fuzz.ratio(text, x)
            if vrt > rc['pracent']:
                rc['commanda'] = options
                rc['pracent'] = vrt
    return rc


def Volume(volumes: int):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volumes / 100, None)
    

def music(path: str, play: int = 0, random_musik = True):
    if not os.path.exists(path): return f"Path -> ({path}) does not exist"

    musiks = os.listdir(path)
    musik_count = len(musiks)
    if random_musik:
        musik_number = random.randint(0, musik_count)
    else:
        musik_number = play
    musik = path + '/' + musiks[musik_number]
    os.startfile(musik)
    print(f"Play musik : {musiks[musik_number]}")


def VideoOnYouTube(search: str):
    url = f"https://www.youtube.com/results?search_query={search}"
    webbrowser.get().open(url)
    print(f"Searching on youtube video: {search}")


def Play(*args: tuple):
    if not args[0]: return
    
    
def Open(*args: tuple):
    if not args[0]: return
    for name in args[0]:
        for proposal in setting.PROPOSALS:
            if name in proposal:
                print(proposal)
                os.startfile(setting.PROPOSALS[proposal])
        

def DateTime(*args: tuple):
    if not args[0]: return
    print("DateTimeActivate")
    

def SearchingOnBrowser(*args: tuple):
    if not args[0]: return

    search = " ".join(*args)
    print(f"Searching: //{search}")
    url = f"https://www.google.com/search?q={ search }"
    webbrowser.get().open(url)
    print(f"Searching on browser: {search}")


def SearchingOnWikipedia(*args: tuple, lang: str = "ru", text_split: int = 3):
    if not args[0]: return

    search = " ".join(*args)
    print(f"Speaking: {search}")
    try:
        wikipedia.set_lang(lang)
        page = wikipedia.page((search))
        page.html
        texts = str(page.summary).split(".")[0: text_split]
        text = ". ".join(texts)
        print(f"\n\t\t{page.title}\n{text}")
        speak(text)
        return True
    
    except Exception as ex:
        print(ex)
        return False


__all__ = ("Play", 
           "Open", 
           "DateTime", 
           "SearchingOnBrowser", 
           "SearchingOnWikipedia", 
           "setting")