from search_cita import get_cita
from telegram_integration import telegram_bot_sendtext
from telegram_integration import telegram_bot_sendpic
import json

def main() -> None:
    
    with open('json_data_template.json') as json_file:
        data = json.load(json_file)

    chatid = data['keys']['telegram_chat_id']
    id = data['keys']['web_id']
    cd = data['keys']['web_cd']
    chatid_monitoring = data['keys']['telegram_chat_id_monitoring']
    #url = "http://gyumri.kdmid.ru/queue/OrderInfo.aspx?id=" + id + "&cd=" + cd
    url_null = "https://gyumri.kdmid.ru/queue/OrderInfo.aspx"

    while True:
        check = False
        while check == False:
            check, result = get_cita(id , cd, chatid_monitoring)
            print(result)

        telegram_bot_sendtext(result + "\n" + url_null, chatid)
        telegram_bot_sendpic("screenshots/good.png", "Свободные даты для записи:", chatid)

if __name__ == '__main__':
    main()