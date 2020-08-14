#!./venv/bin/python
import json
import os
import sys
import os
import telebot
import settings

from telebot import types
from datetime import datetime
from core import BotBody


bot = telebot.TeleBot(settings.BOT_TOKEN)
bot_body = BotBody(bot)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Забронировать Online')
        keyboard.row('Где мы находимся?')
        keyboard.row('Прайс', 'Акции')
        keyboard.row('Девайсы', 'Железо')
        bot.send_message(message.chat.id, 'Выберите нужные услуги', reply_markup=keyboard)
    except:
        bot_body.send_error(message)

@bot.callback_query_handler(func=lambda call: True)
def is_callback(query):
    data = query.data
    try:
        if data in bot_body.get_services_list():
            bot_body.get_serivce_times(query, data)
        elif 'select_time:' in data:
            bot_body.choice_time(query, data)
        elif 'date__' in data:
            bot_body.select_date(query, data)
        else:
            bot.send_message(query.message.chat.id, 'Команда не найдена', reply_markup=None)
    except:
        bot_body.send_error(query.message)

@bot.message_handler(content_types=["text"])
def url(message):
    try:
        if message.text == 'Бронирование времени':
            bot_body.get_serivices(message)
        elif message.text == 'Просмотреть выбранные услуги':
            bot_body.get_serivices_choosen(message)
        elif message.text == 'Очистить':
            bot_body.clear_cart(message)
        elif message.text == 'Оплатить':
            bot_body.go_to_pay(message)
        elif message.text == 'Забронировать Online':
            bot_body.get_services_after_click(message)
        elif message.text == '↩️ Назад':
            bot_body.back_to_menu(message)
        elif message.text == 'Прайс':
            bot_body.get_price_list(message)
        elif message.text == 'Акции':
            bot_body.get_promo_link(message)
        elif message.text == 'Железо':
            bot_body.get_hardware_list(message)
        elif message.text == 'Девайсы':
            bot_body.get_devices_list(message)
        elif message.text == 'Где мы находимся?':
            bot_body.get_location(message)
    except:
        bot_body.send_error(message)


def start_bot():
    bot.polling(none_stop=True)