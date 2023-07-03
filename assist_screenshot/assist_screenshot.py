# -*- coding: utf-8 -*-
"""
            Strings recognition on PC display for giving designers design insight

                                assist_screenshot.py
    
    Copyright (C) 2023  P. Q.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""python modules for strings recognition"""
import re
import time
import pyocr
from PIL import ImageGrab, Image
import win32gui

"""python modules for utilizing knowledge port"""
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

uttr_max_length = 500
host_url = r'https://kp.engineering-brain.com/'

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

def is_japanese(str):

    MIN_JPNSTR = 5
    JPNRATIO_TH = 3.0

    jpnstr_list = re.findall(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+', str)
    engstr_list = re.findall('[a-z]+|[A-Z]+', str)

    if len(engstr_list) != 0:
        jpn_ratio = float(len(jpnstr_list) / len(engstr_list))
    else:
        jpn_ratio = 100.0

    return True if len(jpnstr_list) > MIN_JPNSTR and jpn_ratio >= JPNRATIO_TH else False

def main_fnc():

    # 初期化
    pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    tools = pyocr.get_available_tools()
    tool = tools[0]

    previous_text = ''
    MIN_STRLEN = 10

    time.sleep(60)

    # 10分ごとにループ
    while True:
        # アクティブなウィンドウのハンドルを取得
        active_window_handle = win32gui.GetForegroundWindow()

        # アクティブなウィンドウの座標を取得
        window_rect = win32gui.GetWindowRect(active_window_handle)

        # スクリーンショットを撮影
        screenshot = ImageGrab.grab(window_rect)
        #screenshot = ImageGrab.grab() # In the case of whole display
        screenshot.save('screenshot.png')

        # OCRによるテキストの抽出
        text = tool.image_to_string(Image.open('screenshot.png'), lang='jpn', builder=pyocr.builders.TextBuilder(tesseract_layout=6))

        # 抽出したテキストを表示
        #print('text =',text)

        # テキストを保存
        with open('text.txt', 'w', encoding='utf-8') as f:
            f.write(text)

        # Divide extracted text to several sentences 
        adj_text = re.split(r'\n\n|。|．',text)


        adj_text_jp = []
        for str in adj_text:
            str = re.sub(r'\n| ', '', str)

            # Whether extracted strings are japanese or not
            if is_japanese(str) == True and len(str) > MIN_STRLEN:
                adj_text_jp.append(str)
                print('str =', str)

        # 前回のテキストと比較し、同じであればスキップ
        if adj_text_jp == previous_text:
            time.sleep(600)
            continue

        # Related knowledge is shown for each string recognized on display
        num_str = 0
        for str in adj_text_jp:
            if str in previous_text:
                # Skip when extracted string is included in previous screen shot
                continue
            else:
                if len(str) <= uttr_max_length:
                    request_to_brain(str)
                    num_str += 1
                    time.sleep(15)
                else:
                    continue

        # 前回のテキストを更新
        previous_text = adj_text_jp

        # 10分待機
        standby = 600 - num_str * 15
        if standby <= 0:
            pass
        else:
            time.sleep(standby)

if __name__ == '__main__':

    # Login to knowledge passport
    init_url = host_url + r'assistant/'
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(init_url)
    except:
        try:
            driver = webdriver.Edge(EdgeChromiumDriverManager().install())
            driver.get(init_url)
        except:
            print('Please install Google Chrome or Microsoft Edge as web browser.')
            exit(0)

    #Wait 60 seconds for login
    try:
        wait = WebDriverWait(driver, 60)
        isUrl = wait.until(expected_conditions.url_contains(init_url))
    except:
        print('TimeoutException is raised.')
        print('Please execute this application again and enter email and password within 30 seconds.')
        driver.close()
    else:
        print(isUrl)

    # Read exclusive words not to be requested
    try:
        with open(SET_FILE_NAME, 'r', encoding='utf-8') as set_f:

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

    # Strings recognition
    main_fnc()

