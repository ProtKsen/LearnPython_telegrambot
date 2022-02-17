import logging
import datetime
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)


def print_planet_constellation(update, context):
    user_text = update.message.text.split(' ')
    planet_name = user_text[1].title()
    current_day = datetime.datetime.now().day
    command_dict = {
        'Mercury': ephem.Mercury(current_day),
        'Venus': ephem.Venus(current_day),
        'Mars': ephem.Mars(current_day),
        'Jupiter': ephem.Jupiter(current_day),
        'Saturn': ephem.Saturn(current_day),
        'Uranus': ephem.Uranus(current_day),
        'Neptune': ephem.Neptune(current_day)
    }
    if planet_name in command_dict.keys():
        planet = command_dict[planet_name]
        constellation = ephem.constellation(planet)
        update.message.reply_text(constellation)
    else:
        update.message.reply_text('Некорректное название планеты')


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text.upper())


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", print_planet_constellation))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
