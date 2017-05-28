from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
from PIL import Image
import random
import time
import captcha
import excel
import config
import winshell

customers_file, quantity_file, proxy_file, interval = config.input_data()
proxies_list = []
service_args = []
driver = webdriver.PhantomJS(executable_path="phantomjs.exe", service_args=service_args)

def set_startup():
    try:
        startFile = os.path.abspath(sys.argv[0])
        startup=winshell.startup()
        winshell.CreateShortcut (
            Path=os.path.join (startup, "FormFillScript.lnk"),
            Target=startFile,
            Icon=(startFile, 0),
            Description="Web Script",
            StartIn=os.path.abspath(None)
          )
    except:
        pass

def load_proxy():
    proxies_file = open(proxy_file, "r");
    for line in proxies_file:
        proxies_list.append(line)

def choose_proxy():
    proxy_adress = random.choice(proxies_list)
    service_args.append('--proxy=' + proxy_adress.strip())
    service_args.append("--proxy-type=http")
    print (service_args)

def element_screenshot(loc, size):
        im = Image.open('screenshot.png')
        left = loc['x']
        top = loc['y']
        right = loc['x'] + size['width']
        bottom = loc['y'] + size['height']
        im = im.crop((left, top, right, bottom))
        im.save("default.png")

def get_captcha(captcha_image, captcha_element):
    try:
        driver.save_screenshot("screenshot.png")
        loc = captcha_image.location
        size = captcha_image.size
        element_screenshot(loc, size)
        print (captcha.recognition())
        captcha_element.send_keys(captcha.recognition())
        submit_button = driver.find_element_by_class_name("btn-default")
        driver.save_screenshot("(0)screenshot.png")
        submit_button.click()
        try:
            element = WebDriverWait (driver, 10).until (EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
        except:
            pass
    except Exception:
        print (Exception)
        submit_button = driver.find_element_by_class_name("btn-default")
        driver.save_screenshot("(0)screenshot.png")
        submit_button.click()

def form_fill():
    driver.get("http://abtronics.ru/search/name/%D0%BA%D1%84%D1%82%D0%B2%D1%89%D1%8C")
    print (driver.title)
    row_number = config.getLastRow()
    driver.service_args = service_args
    element = WebDriverWait (driver, 20).until (EC.presence_of_element_located((By.NAME, "phone")))
    name, email, phone, product, manufacturer, quantity = excel.data(row_number, customers_file, quantity_file)
    name_element = driver.find_element_by_id("name")
    email_element = driver.find_elements_by_id("email")
    phone_element = driver.find_element_by_name("phone")
    product_element = driver.find_element_by_name("good")
    manufacturer_element = driver.find_element_by_name("manufacturer")
    quantity_element = driver.find_element_by_name("quantity")
    captcha_element = driver.find_element_by_name("captcha")
    captcha_image = driver.find_element_by_class_name("captcha-img")
    name_element.send_keys(name)
    email_element[1].send_keys(email)
    phone_element.send_keys(phone)
    product_element.send_keys(product)
    manufacturer_element.send_keys(manufacturer)
    quantity_element.send_keys(quantity)
    print ("Got all inputs")
    get_captcha(captcha_image, captcha_element)
    try:
        element = WebDriverWait (driver, 10).until (EC.presence_of_element_located((By.CLASS_NAME, "help_block")))
    except:
        pass
    driver.save_screenshot("screenshot.png")
    print ("Sent data")
    attempts = 0
    while ("Неправильная капча" in driver.page_source):
        print ("attempt #", attempts)
        refresh = driver.find_element_by_class_name("refresh_captcha")
        refresh.click()
        driver.save_screenshot("(1)screenshot.png")
        captcha_element = driver.find_element_by_name("captcha")
        captcha_image = driver.find_element_by_class_name("captcha-img")
        captcha_element.clear()
        driver.save_screenshot("(2)screenshot.png")
        get_captcha(captcha_image, captcha_element)
        driver.save_screenshot("(3)screenshot.png")
        attempts += 1

    log_file = open("execution.log", "a")
    log_file.write("[" + time.ctime() + "]:  Added data from row #" + str(row_number) + " from proxy:" + service_args[0] +"\n")
    config.change_row(row_number=row_number+1)
    print ("Moving to next input")

if __name__ == "__main__" :
    load_proxy()
    if (config.isFirstStart):
        set_startup()
        config.notFirstStart()
        print ("First start")
    while (True):
        print ("Woke up, time to work")
        choose_proxy()
        print ("Choosen Proxy")
        form_fill()
        print ("Filled form, falling asleep")
        service_args.pop()
        service_args.pop()
        time.sleep(interval*60)
