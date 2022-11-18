from PIL import Image
import pytesseract
import os
import cv2


def get_captcha(img_path):
    img = cv2.imread(img_path, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    withoutnoise = cv2.fastNlMeansDenoising(gray, None, 21, 7, 21)
    cv2.imwrite(img_path, withoutnoise)

    img = cv2.imread(img_path, 1)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=8, tileGridSize=(10, 10))
    cl = clahe.apply(l_channel)

    limg = cv2.merge((cl, a, b))

    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    cv2.imwrite(img_path, enhanced_img)
    
    captcha = pytesseract.image_to_string(
        Image.open(img_path),
        config='--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789'
        )
    captcha = captcha.replace(" ", "").strip()
    print("captcha", captcha)
    #path = os.getcwd()
    os.remove(img_path)

    return captcha
