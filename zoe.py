import os
import time
import random
import tkinter
import playsound
import webbrowser
import subprocess
from tkinter import *
from gtts import gTTS
from time import ctime
import speech_recognition as sr
from PIL import ImageTk, Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


r = sr.Recognizer()
root = Tk()
root.title("Zorq - Student Voice Assistant")
mic = PhotoImage(file = "mic.png")
logo = PhotoImage(file = "Z-logo.png")
root.iconphoto(False, logo)
frame = Frame(root)
frame.pack()


def zorq_assistant():
    time.sleep(1)
    zorq_speak("This is Zorq. How may I help you?")
    voice_data = record_speech()
    respond(voice_data)


def build_screen():
    listenButton = Button(frame, text="Listen", command=zorq_assistant)
    micLogo = Label(frame, image=mic)
    cTitleLabel = Label(frame, text="Commands")
    cList = Listbox(frame)
    cList.insert(1, "Open")
    cList.insert(2, "what is your name")
    cList.insert(3, "what time is it")
    cList.insert(4, "search")
    cList.insert(5, "find location")
    cList.insert(6, "exit")

    listenButton.pack()
    micLogo.pack()
    cTitleLabel.pack()
    cList.pack()


def record_speech(ask = False):
    with sr.Microphone() as source:
        if ask:
            zorq_speak(ask)
        audio = r.listen(source)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)
        except sr.UnknownValueError:
            zorq_speak("Sorry I didn't get that.")
        except sr.RequestError:
            zorq_speak("Sorry my speech service is down.")
        return voice_data


def zorq_speak(audio_string):
    tts = gTTS(text=audio_string, lang="en")
    r = random.randint(1, 10000000)
    audio_file = "audio-"+ str(r) + ".mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)


def user_data(line = 0):
    file = open('user.txt')
    content = file.readlines()
    return content[line], content[line+1], content[line+2]


def auto_login_bot(element_id_1 = "", element_id_2 = "", element_id_3 = "", verification_id = ""):
    usernameStr, passwordStr, url = user_data(0)
    browser = webdriver.Chrome()
    browser.get((url))

    ignored_exceptions = (NoSuchElementException,StaleElementReferenceException,)

    username = WebDriverWait(browser, 5,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "i0116")))
    username.send_keys(usernameStr)

    password = WebDriverWait(browser, 5,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, "i0118")))
    password.send_keys(passwordStr)

    time.sleep(1) 
    signInButton = browser.find_element_by_id(element_id_1)
    signInButton.click()

    time.sleep(1) 
    noButton = browser.find_element_by_id(element_id_2)
    noButton.click()
    
    time.sleep(2) 
    continueButton = browser.find_element_by_class_name(element_id_3)
    continueButton.click()


def respond(voice_data):
    if "open" in voice_data:
        open = record_speech("What would you like to open?")
        if "School applications" in open:
            auto_login_bot("idSIButton9", "idBtn_Back", "VfPpkd-LgbsSe")
    if "what is your name" in voice_data:
        zorq_speak("My name is Zorq")
    if "what time is it" in voice_data:
        zorq_speak(ctime())
    if "search" in voice_data:
        search = record_speech("What would you like to search for?")
        url = "https://google.com/search?q=" + search
        webbrowser.get().open(url)
        zorq_speak("Here is what I found for " + search)
    if "find location" in voice_data:
        location = record_speech("What is the location?")
        url = "https://google.nl/maps/place/" + location + "/&amp;"
        webbrowser.get().open(url)
        zorq_speak("Here is the location of " + location)
    if "exit" in voice_data:
        zorq_speak("Goodbye")
        exit()


build_screen()
root.geometry("500x600")
root.mainloop()

