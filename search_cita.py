import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ICR_1 as ICR
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import string
import base64
from telegram_integration import telegram_bot_sendtext
from telegram_integration import telegram_bot_sendpic


def get_cita(id, cd, chatid_monitoring, token):
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
    try:
        driver = webdriver.Chrome("C:/Users/USR/Downloads/chromedriver.exe", options=chrome_options)
        driver.get(url)
    except Exception as e:
        telegram_bot_sendtext("Брат, у нас драйвер откинулся((((", chatid_monitoring)
        print(e)
        return False, "ERROR DRIVER"

    time.sleep(6)
    try:
        captcha_element = driver.find_element_by_id("ctl00_MainContent_imgSecNum")
    except Exception as e:
        try:
            driver.save_screenshot("screenshots/errorcaptcha.png")
        except Exception as e:
            print('Error: couldn`t make a screenshot')
            print(e)
        telegram_bot_sendpic("screenshots/errorcaptcha.png", "Я капчу не нашел(((", chatid_monitoring)
        print(e)
        driver.quit()
        return False, "ERROR CAPTCHA"

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
        str("screenshots/captcha.jpg")
    )
    with open(img_path, "wb") as f:
        f.write(base64.b64decode(img_base64))

    captcha = ICR.get_captcha(img_path)

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
    except:
        driver.quit()
        return False, "Captcha identification has failed, trying again...."


    try:
        texto = "нет свободного времени"
        posted = driver.find_element(by=By.ID, value="center-panel").text
        driver.quit()
        print(posted)
        telegram_bot_sendtext("Брат, я угадал капчу)", chatid_monitoring)
        if texto in posted.lower():
            time.sleep(60)
            return False, "No citas availables"
        else:
            ry:
                driver.save_screenshot("screenshots/good.png")
            except:
                print('Error: couldn`t make a screenshot')
            return True, "РОТА ПОДЪЕМ НАХУЙ"
    except Exception as e:
        driver.save_screenshot("screenshots/posted.png")
        telegram_bot_sendpic("screenshots/posted.png", "Брат, у нас опять что-то сломалось((", chatid_monitoring)
        print(e)
        driver.quit()
        return False, "ERROR POSTED"
