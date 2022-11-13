import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ICR_1 as ICR
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import random
import string
import base64


def get_cita(id, cd):
    width = 1000
    height = 500
    window_width = int(width) if width is not None else 1000
    window_height = int(height) if height is not None else 500
    display = Display(visible=0, size=(1366, 768))
    display.start()
    id = str(id)
    cd = str(cd)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    )

    url = "http://gyumri.kdmid.ru/queue/OrderInfo.aspx?id=" + id + "&cd=" + cd
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(6)
    driver.save_screenshot("screenshots/screenshot.png")
    captcha_element = driver.find_element_by_id("ctl00_MainContent_imgSecNum")

    # get binary image from captcha's div
    img_base64 = driver.execute_script(
        """
            var ele = arguments[0];
            var cnv = document.createElement('canvas');
            cnv.width = 200; cnv.height = 50;
            cnv.getContext('2d').drawImage(ele, 0, 0);
            return cnv.toDataURL('image/jpeg').substring(22);    
            """,
        captcha_element,
    )
    img_path = (
        str("screenshots/")
        + "".join([random.choice(string.ascii_letters) for i in range(10)])
        + str(".jpg")
    )
    with open(img_path, "wb") as f:
        f.write(base64.b64decode(img_base64))

    captcha = ICR.get_captcha(img_path)

    # inputElement = driver.find_element_by_id("ctl00_MainContent_txtCode")
    inputElement = driver.find_element(by=By.ID, value="ctl00_MainContent_txtCode")
    inputElement.send_keys(captcha)
    time.sleep(1)

    inputElement = driver.find_element(
        by=By.ID, value="ctl00_MainContent_ButtonA"
    ).click()
    time.sleep(1)

    try:
        inputElement = driver.find_element(
            by=By.ID, value="ctl00_MainContent_ButtonB"
        ).click()
        print("Eureka!!, Captcha correct")
        time.sleep(1)
        texto = "нет свободного времени"
        posted = driver.find_element(by=By.ID, value="center-panel").text
        print(posted)
        if texto in posted.lower():
            return True, "No citas availables"
        else:
            return True, "ATTENTION!! Citas Available!!!"
    except:
        return False, "Captcha identification has failed, trying again...."
