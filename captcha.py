#coding=utf-8

from PIL import Image
from pytesseract import image_to_string
import re

def recognition():
    try:
        x = image_to_string(Image.open("default.png"))
        result = re.findall("\d", x)
        result_2 = ''.join(result)
        return result_2
    except:
        return "0"
