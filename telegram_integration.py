from telegram.ext import Updater


def telegram_bot_sendtext(bot_message, token, chatid):

    updater = Updater(token=token)
    updater.bot.send_message(chatid, bot_message)


def telegram_bot_sendpic(path, token, chatid):

    updater = Updater(token=token)
    updater.bot.send_photo(chatid, photo=open(path))
