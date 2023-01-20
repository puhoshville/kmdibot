import json
import time


# RECOMMENDATION
# Before starting the program, write the key "time" = time.time() to stats.json.
# Otherwise, on the first Sunday, get a zero result in the "Number of checks per hour" parameter


def stat_r():
    with open("stats.json") as f:
        a = json.load(f)
        a["requests"] += 1

    with open("stats.json", "w") as f:
        json.dump(a, f, indent=2, ensure_ascii=False)


def stat_wc():
    with open("stats.json") as f:
        a = json.load(f)
        a["win_captcha"] += 1

    with open("stats.json", "w") as f:
        json.dump(a, f, indent=2, ensure_ascii=False)


def stat_lc():
    with open("stats.json") as f:
        a = json.load(f)
        a["lose_captcha"] += 1

    with open("stats.json", "w") as f:
        json.dump(a, f, indent=2, ensure_ascii=False)


def stat_er():
    with open("stats.json") as f:
        a = json.load(f)
        a["error"] += 1

    with open("stats.json", "w") as f:
        json.dump(a, f, indent=2, ensure_ascii=False)


def stat_clear():
    with open("stats.json") as f:
        a = json.load(f)
        a["requests"] = 0
        a["win_captcha"] = 0
        a["lose_captcha"] = 0
        a["error"] = 0
        a["time"] = time.time()

    with open("stats.json", "w") as f:
        json.dump(a, f, indent=2, ensure_ascii=False)


def stat_print():
    with open("stats.json") as f:
        a = json.load(f)
        st_pr = 'Запросов на сайт  =  ' + str(a['requests']) + '\n' + \
                'Угадано капч  =  ' + str(a['win_captcha']) + '\n' + \
                'Не угадано капч  =  ' + str(a['lose_captcha']) + '\n' + \
                '% распознавания  =  ' + str(round(
            100 * a['win_captcha'] / (a['lose_captcha'] + a['win_captcha']), 2)) + '%\n' + \
                'Количество ошибок  =  ' + str(a['error']) + '\n' + \
                'Кол-во проверок в час  =  ' + str(round((a['win_captcha'] / ((time.time() - a['time']) / 3600)), 2))
        return st_pr
