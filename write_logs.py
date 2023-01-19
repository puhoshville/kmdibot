from time import gmtime, strftime
import re


def wl(status, text):
    with open("logs", "a") as f:
        f.write(
            strftime("%a, %d %b %Y %H:%M:%S", gmtime()) +
            "\t" + status +
            "\t" + text + "\n"
        )

    if len(f.readlines()) == 15000:
        f = open("logs").readlines()
        for i in range(5000):
            f.pop(i)
        with open("logs", 'w') as F:
            F.writelines(f)


def form_st(not_a_string):
    now_string = re.sub("^\s+|\n|\r|\s+$", '', str(not_a_string))
    return now_string
