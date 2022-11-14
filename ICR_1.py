from PIL import Image
import pytesseract
import os


def get_captcha(img_path):
    captcha = pytesseract.image_to_string(
        Image.open(img_path),
        config='--psm 7 --oem 1 -c tessedit_char_whitelist=0123456789'
        )
    captcha = captcha.replace(" ", "").strip()
    print("captcha", captcha)
    path = os.getcwd()
    os.remove(path+"/screenshots/screenshot.png")

    return captcha
