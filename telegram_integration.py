import requests
import json

with open('json_data_template.json') as json_file:
    data = json.load(json_file)

token = data['keys']['telegram_token']

def telegram_bot_sendtext(bot_message, chatid):

    data = {"chat_id": chatid, "text": bot_message}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    ret = requests.post(url, data=data)
    if ret.ok == False:
        print("Error sending the message")


def telegram_bot_sendpic(path, caption, chatid):

    data = {"chat_id": chatid, "caption": caption}
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(path, "rb") as image_file:
        ret = requests.post(url, data=data, files={'photo': image_file})
    if ret.ok == False:
        print("Error sending the photo")
