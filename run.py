import pickle
import pyautogui
import time
import os
from PIL import Image, ImageDraw
import pytesseract
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import pickle
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
import requests
import json
import webbrowser
from object_detection.utils import label_map_util

#open webpage and navigate to desired website

url = 'https://www.spotify.com/us/signup/'
chrome_path = '/usr/bin/google-chrome %s --incognito'
webbrowser.get(chrome_path).open(url)
time.sleep(7)

#take a screenshot of the entire webpage
pyautogui.screenshot('findbox.png')
print("opened website and screenshotted")

#detect the location of the unclicked captcha
os.system('python3 object_detection/findbox.py')

#get the coordinates of the unclicked captcha from pickle
f = open('store.pckl', 'rb')
coordinates = pickle.load(f)
f.close()

xmin = coordinates[0]
ymin = coordinates[1]
xmax = coordinates[2]
ymax = coordinates[3]
print(xmin, ymin, xmax, ymax)

#get screen resolution and calculate checkbox location
dimensions = pyautogui.size()
xvalue = xmin + (dimensions[0] * 0.02)
yvalue = ((ymax+ymin)/2)
pyautogui.click(xvalue, yvalue)
print("clicked captcha")
time.sleep(3)

while(True):
    #screenshot clicked captcha and determine its coordinates
    pyautogui.screenshot('captcha.png')
    print("loaded captcha")
    os.system('python3 object_detection/cropbox.py')

    f = open('crop.pckl', 'rb')
    crop_coordinates = pickle.load(f)
    f.close()

    #crop the captcha image
    the_image = Image.open('captcha.png')
    cropped_image = the_image.crop((0.92*crop_coordinates[0],0.95*crop_coordinates[1],crop_coordinates[2],crop_coordinates[3]))
    cropped_image.save('cropped.png')

    cropwidth, cropheight = cropped_image.size
    text_image = cropped_image.crop((0, 0, cropwidth, int(0.22*cropheight)))
    text_image.save('textimage.png')
    final_image = cropped_image.crop((0, int(0.26*cropheight), cropwidth, cropheight))
    final_image.save('finalimage.png')

    #use ocr to read the captcha's text
    print("attempting ocr")


    def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
        payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
        with open(filename, 'rb') as f:
                r = requests.post('https://api.ocr.space/parse/image',files={filename: f},data=payload,)
        return r.content.decode()


    y = json.loads(ocr_space_file('textimage.png', overlay=False, api_key='9841a0c9eb88957', language='eng'))
    print(y["ParsedResults"][0]["ParsedText"])
    text = y["ParsedResults"][0]["ParsedText"]

    #determine size of captcha grid (eg. 3x3, 4x4, 2x3)
    os.system('python3 label_image.py finalimage.png')
    f = open('classify.pckl', 'rb')
    captchatype = pickle.load(f)
    print("the captcha is " + captchatype)
    f.close()
	
    if ("car" in text or "vehicle" in text):
        captchaclass = "car"
    elif ("bus" in text):
        captchaclass = 'bus'
    elif ("hydrant" in text):
        captchaclass = 'hydrant'
    elif ("light" in text):
        captchaclass = 'light'
    elif ("bicycle" in text):
        captchaclass = 'bicycle'
    else:
        sys.exit("image class currently not suppored")

    #detect objects in the captcha
    os.system('python3 detect.py ' + captchatype + " " + captchaclass)
    f = open('final.pckl', 'rb')
    boxbool = pickle.load(f)
    f.close()

    #click the boxes that have detected objects

    screenWidth = dimensions[0]
    screenHeight = dimensions[1]
    print("width and height are " + str(screenWidth) + "," + str(screenHeight))

    #get coordinates of 9 boxes
    finalxmin = 0.9*crop_coordinates[0]
    finalymin = 0.9*crop_coordinates[1] + (0.25*cropheight)
    finalxmax = crop_coordinates[2]
    finalymax = crop_coordinates[3]

    print("final values: " + str(finalxmin) + "," + str(finalymin) + ";" + str(finalxmax) + "," + str(finalymax))

    debug_image = the_image.crop((finalxmin,finalymin,finalxmax,finalymax))
    debug_image.save('debug.png')

    finalwidth,finalheight = final_image.size

    if captchatype == '3x3':
        boxwidth = finalwidth / 3
        boxheight = finalheight / 3
        print("box dimensions" + str(boxwidth) + "," + str(boxheight))

        if boxbool[0]:
            clickx = finalxmin + (0.5*boxwidth)
            clicky = finalymin + (0.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[1]:
            clickx = finalxmin + (1.5*boxwidth)
            clicky = finalymin + (0.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[2]:
            clickx = finalxmin + (2.5*boxwidth)
            clicky = finalymin + (0.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[3]:
            clickx = finalxmin + (0.5*boxwidth)
            clicky = finalymin + (1.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[4]:
            clickx = finalxmin + (1.5*boxwidth)
            clicky = finalymin + (1.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[5]:
            clickx = finalxmin + (2.5*boxwidth)
            clicky = finalymin + (1.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[6]:
            clickx = finalxmin + (0.5*boxwidth)
            clicky = finalymin + (2.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[7]:
            clickx = finalxmin + (1.5*boxwidth)
            clicky = finalymin + (2.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[8]:
            clickx = finalxmin + (2.5*boxwidth)
            clicky = finalymin + (2.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3.3)
        clickx = finalxmin + (2.75*boxwidth)
        clicky = finalymin + (3.3*boxheight)
        pyautogui.click(clickx,clicky)
    elif captchatype == '4x4':
        boxwidth = finalwidth / 4
        boxheight = finalheight / 4
        print("box dimensions" + str(boxwidth) + "," + str(boxheight))

        if boxbool[0]:
            clickx = finalxmin + (0.5*boxwidth)
            clicky = finalymin + (0.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[1]:
            clickx = finalxmin + (1.5*boxwidth)
            clicky = finalymin + (0.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[2]:
            clickx = finalxmin + (2.5*boxwidth)
            clicky = finalymin + (0.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[3]:
            clickx = finalxmin + (3.5*boxwidth)
            clicky = finalymin + (0.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[4]:
            clickx = finalxmin + (0.5*boxwidth)
            clicky = finalymin + (1.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[5]:
            clickx = finalxmin + (1.5*boxwidth)
            clicky = finalymin + (1.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[6]:
            clickx = finalxmin + (2.5*boxwidth)
            clicky = finalymin + (1.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[7]:
            clickx = finalxmin + (3.5*boxwidth)
            clicky = finalymin + (1.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[8]:
            clickx = finalxmin + (0.5*boxwidth)
            clicky = finalymin + (2.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[9]:
            clickx = finalxmin + (1.5*boxwidth)
            clicky = finalymin + (2.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[10]:
            clickx = finalxmin + (2.5*boxwidth)
            clicky = finalymin + (2.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[11]:
            clickx = finalxmin + (3.5*boxwidth)
            clicky = finalymin + (2.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[12]:
            clickx = finalxmin + (0.5*boxwidth)
            clicky = finalymin + (3.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[13]:
            clickx = finalxmin + (1.5*boxwidth)
            clicky = finalymin + (3.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[14]:
            clickx = finalxmin + (2.5*boxwidth)
            clicky = finalymin + (3.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)

        if boxbool[15]:
            clickx = finalxmin + (3.5*boxwidth)
            clicky = finalymin + (3.5*boxheight)
            pyautogui.click(clickx,clicky)
            time.sleep(3)
    
        clickx = finalxmin + (3.5*boxwidth)
        clicky = finalymin + (4.3*boxheight)
        pyautogui.click(clickx,clicky)
    print("one cycle complete")








