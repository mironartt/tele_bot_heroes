#!./venv/bin/python
import json
import os
import sys
import os
import telebot
import local_settings

from telebot import types
from datetime import datetime
from core import BotBody

bot = telebot.TeleBot(local_settings.BOT_TOKEN)
bot_body = BotBody(bot)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Какие игры есть?', 'Есть акция?')
        keyboard.row('Где мы находимся?', 'Еда и напитки')
        keyboard.row('Забронировать Online')
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
        else:
            bot.send_message(query.message.chat.id, 'Команда не найдена', reply_markup=None)
    except:
        bot_body.send_error(query.message)

@bot.message_handler(content_types=["text"])
def url(message):
    if message.text == 'Бронирование времени':
        try:
            bot_body.get_serivices(message)
        except:
            bot_body.send_error(message)
    elif message.text == 'Просмотреть выбранные услуги':
        try:
            bot_body.get_serivices_choosen(message)
        except:
            bot_body.send_error(message)
    elif message.text == 'Очистить':
        try:
            bot_body.clear_cart(message)
        except:
            bot_body.send_error(message)
    elif message.text == 'Оплатить':
        try:
            bot_body.go_to_pay(message)
        except:
            bot_body.send_error(message)
    elif message.text == 'Забронировать Online':
        bot_body.get_services_after_click(message)
    elif message.text == '↩️ Назад':
        bot_body.back_to_menu(message)
    elif message.text == 'Какие игры есть?':
        bot_body.get_games_list(message)
    elif message.text == 'Есть акция?':
        bot_body.get_promo_link(message)
    elif message.text == 'Еда и напитки':
        bot_body.get_eats_list(message)
    elif message.text == 'Где мы находимся?':
        bot_body.get_location(message)


def start_bot():
    bot.polling(none_stop=True)