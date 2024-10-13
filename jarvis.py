import speech_recognition as sr
import pyttsx3 as tts
import webbrowser as wb
import os
import spacy
from spacy.tokens import Doc
import subprocess as sp
import wikipediaapi as wiki

app_keys={
    "app":["application","app"],
    "google":["browser","web","google","chrome"],
    "notepad":["note","notes","writing","write","notepad"],
    "calc":["calculation","calculations","addition","subtraction","multiplication","division","add","subtract","multiply","divide","calculator"],
    "youtube":["youtube","music","sound","song","songs","play"],
    "facebook":["facebook"],
}
word_keys={
    "open":["open","play","launch"],
    "search":["search","find","play"]
}
casual_keys={
    "how are you":["how","are","you","doing","going","whats up",],
    "tell me about youself":["tell","me","about","yourself","who","are","you"],
    "hey":["hello","hey","hi"],
    "i am fine":["fine","ok","alright","feeling","well"],
    "jarvis":["jarvis"]
}
search_keys=["what","is","tell","me","about","know","do","you"]

def speak(sent:str):
    engine=tts.init()
    engine.say(sent)
    engine.setProperty('rate',50)
    engine.runAndWait()
    return

def listen():
    recognize=sr.Recognizer()
    with sr.Microphone() as source:
        cont=3
        while cont:
            recognize.adjust_for_ambient_noise(source)
            print("Listening...")
            audio=recognize.listen(source)
            cont=1
            try:
                text=recognize.recognize_google(audio)
                os.system("cls")
                return text
            except Exception as e:
                cont-=1
        if(cont==0):
            return 1
    
def google_search(srch:str=None):
    if srch!=None:
        wb.open(f"https://www.google.com/search?q={srch}")
        return
    wb.open(f"https://www.google.com/")

def apps_working(doc:Doc):
    userDemand=0
    for token in doc:
        if token.lemma_.lower() in word_keys["open"] or token.lemma_.lower() in word_keys["search"]:
            userDemand+=1
   
    for token in doc:
        for k in app_keys:
            if token.lemma_.lower() in app_keys[k]:
                speak(f"Openning {token.text}")
                if k=='google':
                    if userDemand>=2:
                        srch=search_text(doc)
                        speak("here are the results of your search")
                        google_search(srch)
                    else:
                        google_search()
                    return 0
                elif k=="calc":
                    sp.Popen("calc.exe")
                    return 0
                elif k=="notepad":
                    sp.Popen("notepad.exe")
                    return 0
                elif k=="youtube":
                    if userDemand>=2 or token.lemma_.lower()=="play":
                        srch=search_text(doc)
                        speak("here are the results of your search")
                        youtube(srch)
                    else:
                        youtube()
                    return 0
                elif k=="facebook":
                    wb.open("https://www.facebook.com")
                    return 0
    return 1

def search_text(doc:Doc):
    srch=""
    c=0
    for t in doc:
        if t.lemma_.lower() in word_keys['search'] or t.lemma_.lower()=="is" or t.lemma_.lower()=="about" and not c:
            c=1
        elif c:
            srch=srch+" "+t.text
    return srch

def youtube(srch:str=None):
    if srch!=None:
        wb.open(f"https://www.youtube.com/results?search_query={srch}")
    else:
        wb.open("https://www.youtube.com")

def casual_chat(doc:Doc):
    frequency={
    "how are you":0,
    "tell me about youself":0,
    "hey":0,
    "i am fine":0,
    "jarvis":0
    }
    for token in doc:
        for k in casual_keys:
            if token.lemma_.lower() in casual_keys[k]:
                frequency[k]+=1
    max ="hey"
    for f in frequency:
        if frequency[f]>frequency[max]:
            max=f
    if max=="hey":
        speak("heyyyy")
        return 0
    elif max=="how are you":
        speak("i am fine and i hope you doing well too")
        return 0
    elif max=="i am fine":
        speak("nice to hear that!")
        return 0
    elif max=="tell me about youself":
        speak("Hello Ahmad, I am JARVIS, your personal AI assistant. I can help you with various tasks like managing your schedule, browsing the web, and even performing complex calculations. How can I assist you today?")
        return 0
    elif max=="jarvis":
        speak("yes i am listening")
        return 0
    return 1
                    
def identify_category(input:str):
    nlp=spacy.load("en_core_web_sm")
    doc=nlp(input)
    print("Procesing...")
    categoriesFrequency={
        "app":0,
        "search":0,
        "casual":0
    }
    for token in doc:
        if any(token.lemma_.lower() in app_keys[key] for key in app_keys) or token.lemma_.lower() in word_keys["open"]:
            categoriesFrequency["app"]+=1
        elif token.lemma_.lower()in word_keys["search"] or token.lemma_.lower() in search_keys:
            categoriesFrequency["search"]+=1
        if any(token.lemma_.lower() in casual_keys[key] for key in casual_keys):
            categoriesFrequency["casual"]+=1
                
    max="app"
    for k in categoriesFrequency:
        if categoriesFrequency[k]>categoriesFrequency[max]:
            max=k
    if max=="app":
        return apps_working(doc) 
    elif max=="casual":
        return casual_chat(doc) 
    elif max=="search":
        search(doc)

def search(doc:Doc):
    srch=search_text(doc)
    wik=wiki.Wikipedia("en")
    page=wik.page(srch)
    if page.exists():
        speak(f"here's a summary on Topic: {srch} {page.summary[:150]}")
        return 0
    else:
        return 1
    
    
if __name__=="__main__":
    while True:
        os.system("cls")
        text=listen()
        if text=="stop":
            break
        if(identify_category(text)):
            speak("It seems like your message is a bit unclear. Could you clarify what you're asking or if you need assistance with something specific? I'm here to help!")
        
    
        
    
                
    