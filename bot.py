import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
import warnings
from datetime import datetime

logging.basicConfig(filename='bot.log', level=logging.INFO)
warnings.filterwarnings("ignore", category=DeprecationWarning)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    update.message.reply_text("Добро пожаловать!")

def planet_constellation(update, context):
    current_datetime = datetime.now()
    planet_constellation = {
        "Jupiter": ephem.constellation(ephem.Jupiter(current_datetime)),
        "Mars": ephem.constellation(ephem.Mars(current_datetime)),
        "Mercury": ephem.constellation(ephem.Mercury(current_datetime)),
        "Neptune": ephem.constellation(ephem.Neptune(current_datetime)),
        "Pluto": ephem.constellation(ephem.Pluto(current_datetime)),
        "Saturn": ephem.constellation(ephem.Saturn(current_datetime)),
        "Uranus": ephem.constellation(ephem.Uranus(current_datetime)),
        "Venus": ephem.constellation(ephem.Venus(current_datetime))
    } 
    words = update.message.text.split()
    for word in words:
        try:
            constellation = planet_constellation.get(word)
        except KeyError:
            constellation = None
        if constellation:
            update.message.reply_text(word)
            update.message.reply_text(constellation)

def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()