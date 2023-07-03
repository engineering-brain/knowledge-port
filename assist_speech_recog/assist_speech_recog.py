# -*- coding: utf-8 -*-
"""
            Speech recognition for giving designers design insight

                        assist_speech_recog.py

@author: P. Q.
"""
import speech_recognition as sr

"""other python modules"""
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service

uttr_max_length = 500
host_url = r'https://kp.engineering-brain.com/'
#host_url = r'http://localhost:8000/'

SET_FILE_NAME = 'setting.txt'
exclusions = []

def request_to_brain(query):

    #Speech recognition result is set to utterance
    utterance = query

    #Check exclusions after translation from Roman to Kanji
    ex_flag = 0
    for ex_word in exclusions:
        if ex_word in utterance:
            print('ex_word =', ex_word)
            ex_flag = 1
            break

    if ex_flag == 0:

        q_data = {'user_utter':utterance}
        qs = urllib.parse.urlencode(q_data)
        print(qs)

        assist_url = host_url + r'assistant/create/'
        assist_url = assist_url + '?' + qs
        print(assist_url)

        driver.get(assist_url)
        #webbrowser.open(assist_url)

if __name__ == '__main__':

    #system = EbdmSystem()

    init_url = host_url + r'assistant/'
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(init_url)
    except:
        try:
            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
            driver.get(init_url)
        except:
            print('Please install Google Chrome or Microsoft Edge as web browser.')
            exit(0)

    #Wait 30 seconds for login
    try:
        wait = WebDriverWait(driver, 30)
        isUrl = wait.until(expected_conditions.url_contains(init_url))
    except:
        print('TimeoutException is raised.')
        print('Please execute this application again and enter email and password within 30 seconds.')
        driver.close()
    else:
        print(isUrl)

    #Read exclusive words not to be requested
    try:
        with open(SET_FILE_NAME, 'r') as set_f:

            ex_word = set_f.readline()
            exclusions.append(ex_word.strip())

            while ex_word:
                ex_word = set_f.readline()
                exclusions.append(ex_word.strip())
    
        exclusions = [x for x in exclusions if x != '']
        print(exclusions)
    except OSError as e:
        #print(e)
        print('Exclusive words are not considered because of no setting.txt.' )

    r = sr.Recognizer()

    while True:
        print('Listening...')

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        print('Now to recognize it...')

        try:
            query = r.recognize_google(audio, language='ja-JP')
            print(query)

            if r.recognize_google(audio, language='ja-JP') == "ストップ":
                logout_url = host_url + r'accounts/logout/'
                driver.get(logout_url)
                print('end')
                break

            elif len(query) <= uttr_max_length:
                #Knowledge request to engineering brain
                request_to_brain(query)

        except sr.UnknownValueError:
            print('Could not understand audio.')
        except sr.RequestError as e:
            print('Could not request results from Google Speech Recognition service; {0}'.format(e))

    driver.close()





