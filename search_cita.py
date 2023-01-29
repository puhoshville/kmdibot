from selenium import webdriver
import ICR_1 as ICR
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import base64
from telegram_integration import telegram_bot_sendtext
from telegram_integration import telegram_bot_sendpic
from write_logs import wl
from write_logs import form_st
import get_stats as gs
from time import gmtime, strftime


def get_cita(id, cd, chatid_monitoring):
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
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        telegram_bot_sendtext("ERROR DRIVER", chatid_monitoring)
        print(e)
        wl("ERR", "error driver\t" + form_st(e))
        return False, "ERROR DRIVER"

    # 01500 - Sunday 15:00 (+0 GMT)
    # 01505 - Sunday 15:05 (+0 GMT)
    if ((strftime("%w%-H%-M", gmtime()) >= "01500") &
        (strftime("%w%-H%-M", gmtime()) <= "01505")):
        telegram_bot_sendtext(gs.stat_print(), chatid_monitoring)
        gs.stat_clear()
        time.sleep(300)

    try:
        driver.get(url)
        gs.stat_r()
    except Exception as e:
        driver.quit()
        print(e)
        wl("ERR", "error url\t" + form_st(e))
        gs.stat_er()
        time.sleep(60)
        return False, "ERROR URL"

    time.sleep(6)
    try:
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
    except Exception as e:
        try:
            driver.save_screenshot("screenshots/errorcaptcha.png")
        except Exception as e:
            print('Error: couldn`t make a screenshot')
            print(e)
        telegram_bot_sendpic("screenshots/errorcaptcha.png", "ERROR CAPTCHA", chatid_monitoring)
        print(e)
        driver.quit()
        wl("ERR", "error captcha\t" + form_st(e))
        gs.stat_er()
        time.sleep(60)
        return False, "ERROR CAPTCHA"

    img_path = (
        str("screenshots/captcha.jpg")
    )

    time.sleep(6)
    try:
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(img_base64))
    except Exception as e:
        print(e)
        driver.quit()
        telegram_bot_sendtext(e, chatid_monitoring)
        wl("ERR", "error save captcha\t" + form_st(e))
        return False, "ERROR CAPTCHA"

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
        wl("OK", "Captcha correct\t" + captcha)
        gs.stat_wc()
        time.sleep(1)
    except:
        driver.quit()
        wl("OK", "Captcha is not guessed\t" + captcha)
        gs.stat_lc()
        return False, "Captcha identification has failed, trying again...."


    try:
        texto = "нет свободного времени"
        texte = "EX.DPGACISNULL"
        posted = driver.find_element(by=By.ID, value="center-panel").text
        driver.quit()
        print(posted)
        telegram_bot_sendtext("Брат, я угадал капчу)", chatid_monitoring)
        if texto in posted.lower():
            wl("OK", "No citas availables")
            time.sleep(60)
            return False, "No citas availables"
        elif texte in posted:
            wl("ERR", "EX.DPGACISNULL")
            gs.stat_er()
            time.sleep(10)
            return False, "EX.DPGACISNULL"
        else:
            try:
                driver.save_screenshot("screenshots/good.png")
            except:
                print('Error: couldn`t make a screenshot')
            driver.quit()
            wl("OK", "Citas availables")
            return True, "ВНИМАНИЕ ЕСТЬ ЗАПИСЬ!"
            
    except Exception as e:
        driver.save_screenshot("screenshots/posted.png")
        telegram_bot_sendpic("screenshots/posted.png", "Брат, у нас опять что-то сломалось((", chatid_monitoring)
        print(e)
        driver.quit()
        wl("ERR", "error posted\t" + form_st(e))
        gs.stat_er()
        return False, "ERROR POSTED"
