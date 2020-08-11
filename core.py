import time
import os
import telebot

from datetime import datetime
from telebot import types
from math import ceil
from yandex_checkout import Configuration, Payment
import local_settings

base_dir = os.path.abspath(os.curdir)


class Cart(object):
    def __init__(self):
        self.items = {}

    def add_item(self, callback_key, cost):
        if not callback_key in self.items:
            self.items[callback_key] = cost
        else:
            del self.items[callback_key]

    @property
    def get_cost(self):
        value = sum(list(self.items.values()))
        return value if value else 0

    def clear(self):
        self.items = {}

    def check_item_exists(self, key, time):
        key_str = '%s__%s' % (key, time)
        return key_str in self.items

    def get_list_items(self, safe=False):
        result_dict = {}
        msg = ''
        for service_key_data, cost in self.items.items():
            service_key, select_time = service_key_data.split('__')
            service_name = [i for i in BotBody.servises if BotBody.servises[i]['key'] == service_key][0]
            result_dict.setdefault(service_name, [])
            result_dict[service_name].append(select_time)
        for service_name, times in result_dict.items():
            msg += '''{0}
    {1}\n'''.format('<b>{0}</b>'.format(service_name) if not safe else service_name, '\n    '.join(['<em>%s</em>' % time if not safe else time for time in times]))
        return msg + ('<b>Итого: {0}руб.</b>'.format(self.get_cost) if not safe else '') if msg else '<em>Пока ничего не выбрано</em>'


class BotBody(object):

    vk_group_link = 'https://vk.com/public189415514'
    servises = {
        'Запись в зону Standart': {
            'times': {
                '08:00-09:00': 50, '09:00-10:00': 50, '10:00-11:00': 50, '11:00-12:00': 50,
                '12:00-13:00': 50, '13:00-14:00': 50, '14:00-15:00': 50, '15:00-16:00': 50,
                '16:00-17:00': 50, '17:00-18:00': 50, '18:00-19:00': 50, '19:00-20:00': 50,
                '20:00-21:00': 50, '21:00-22:00': 50,
            },
            'key': 'standart_service',
        },
        'Запись в зону Pro': {
            'times': {
                '08:00-09:00': 60, '09:00-10:00': 60, '10:00-11:00': 60, '11:00-12:00': 60,
                '12:00-13:00': 60, '13:00-14:00': 100, '14:00-15:00': 100, '15:00-16:00': 100,
                '16:00-17:00': 100, '17:00-18:00': 100, '18:00-19:00': 110, '19:00-20:00': 110,
                '20:00-21:00': 110, '21:00-22:00': 110,
            },
            'key': 'pro_service',
        },
        'Запись в зону Vip': {
            'times': {
                '08:00-09:00': 80, '09:00-10:00': 80, '10:00-11:00': 80, '11:00-12:00': 80,
                '12:00-13:00': 80, '13:00-14:00': 120, '14:00-15:00': 120, '15:00-16:00': 120,
                '16:00-17:00': 120, '17:00-18:00': 120, '18:00-19:00': 130, '19:00-20:00': 130,
                '20:00-21:00': 130, '21:00-22:00': 130,
            },
            'key': 'vip_service',
        },
        'Пакеты (День/Ночь) Standart': {
            'times': {
                '08:00-18:00': 700, '22:00-08:00': 300,
            },
            'key': 'standart_day_night_service',
        },
        'Пакеты (День/Ночь) Pro': {
            'times': {
                '22:00-08:00': 400,
            },
            'key': 'pro_day_night_service',
        },
        'Пакеты (День/Ночь) Vip': {
            'times': {
                '08:00-22:00': 1000, '22:00-08:00': 500,
            },
            'key': 'vip_day_night_service',
        },
        'PS4 Pro': {
            'times': {
                '08:00-09:00': 150, '09:00-10:00': 150, '10:00-11:00': 150, '11:00-12:00': 150,
                '12:00-13:00': 150, '13:00-14:00': 150, '14:00-15:00': 150, '15:00-16:00': 150,
                '16:00-17:00': 150, '17:00-18:00': 150, '18:00-19:00': 150, '19:00-20:00': 150,
                '20:00-21:00': 150, '21:00-22:00': 150,
            },
            'key': 'ps4_pro',
        },
        'VR': {
            'times': {
                '08:00-09:00': 200, '09:00-10:00': 200, '10:00-11:00': 200, '11:00-12:00': 200,
                '12:00-13:00': 200, '13:00-14:00': 200, '14:00-15:00': 200, '15:00-16:00': 200,
                '16:00-17:00': 200, '17:00-18:00': 200, '18:00-19:00': 200, '19:00-20:00': 200,
                '20:00-21:00': 200, '21:00-22:00': 200,
            },
            'key': 'vr_service',
        }
    }

    def __init__(self, bot):
        self.bot = bot
        self.selected_times = {}
        self.cart = Cart()
        self.user_id = None
        self.user_first_name = None
        self.user_last_name = None
        self.username = None
        self.order_id = None

    def check_user_data(self, msg):
        self.user_id = msg.from_user.id if self.user_id is None else self.user_id
        self.user_first_name = msg.from_user.first_name if self.user_first_name is None else self.user_first_name
        self.user_last_name = msg.from_user.last_name if self.user_last_name is None else self.user_last_name
        self.username = msg.from_user.username if self.username is None else self.username
        return 'user_id: {0}, first_name: {1}, last_name: {2}, username: {3}'.format(self.user_id, self.user_first_name, self.user_last_name, self.username)

    def clear_cart(self, message):
        self.cart.clear()
        self.bot.send_message(message.chat.id, 'Список выбранных услуг был очищен', parse_mode='html')

    def get_serivices_choosen(self, message):
        self.check_user_data(message)
        msg_result = self.cart.get_list_items()
        self.bot.send_message(message.chat.id, """Выбранные услуги: 
{0}""".format(msg_result), parse_mode='html')

    def go_to_pay(self, message):
        self.check_user_data(message)
        if self.cart.get_cost > 0:
            url = self.create_order()
            markup = types.InlineKeyboardMarkup()
            service_btn = types.InlineKeyboardButton(text='ОПЛАТИТЬ', url=url)
            markup.add(service_btn)
            self.save_order_log()
            self.bot.send_message(message.chat.id, """<b>К оплате: {0}</b>\n\n<em>Для оплаты нажмите на кнопку оплатить и перейдите на страницу оплаты.</em>""".format(self.cart.get_cost), reply_markup=markup, parse_mode='html')
            if local_settings.ADMIN_USER_ID is not None and local_settings.ALERT_NEW_PAYMENT_CLICK and message.chat.id != local_settings.ADMIN_USER_ID:
                self.bot.send_message(local_settings.ADMIN_USER_ID, 'Пользователь совершил клик по оплате.\n{0}'.format(self.get_order_description(True)), reply_markup=None)
        else:
            self.bot.send_message(message.chat.id, 'Вы не выбрали ни одной услуги', parse_mode='html')

    def get_serivices(self, message, is_drop=False):
        self.check_user_data(message)
        markup = types.InlineKeyboardMarkup()
        for service_name, serice_data in self.servises.items():
            service_btn = types.InlineKeyboardButton(text=service_name, callback_data=serice_data['key'])
            markup.add(service_btn)
        self.bot.send_message(message.chat.id, "<em>⬇️ доступные услуги</em>" if not is_drop else '⬇️', reply_markup=markup, parse_mode='html')

    def get_serivce_times(self, query, select_serivce):
        self.check_user_data(query.message)
        self.bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="Доступные варианты", parse_mode='html',)
        self.bot.edit_message_reply_markup(query.from_user.id, query.message.message_id, reply_markup=self.get_times_btns(select_serivce))

    def get_times_btns(self, select_serivce):
        markup = types.InlineKeyboardMarkup()
        select_serivce_data = BotBody.get_need_item(self.servises, select_serivce)
        result_temp = [
            types.InlineKeyboardButton('{0}{1}'.format('✔️ ' if self.cart.check_item_exists(select_serivce, serivce_time) else '', serivce_time),
            callback_data='select_time::%s__%s' % (select_serivce, serivce_time)) for serivce_time, serivce_cost in select_serivce_data['times'].items()
        ]
        for row in self.parting(result_temp, 3 if len(result_temp) > 6 else (2 if 3 < len(result_temp) < 6 else 1)):
            markup.add(*row)
        return markup

    def get_services_after_click(self, message):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Бронирование времени')
        keyboard.row('Просмотреть выбранные услуги', 'Очистить')
        keyboard.row('Оплатить', '↩️ Назад')
        self.bot.send_message(message.chat.id, '<b>Выберите нужные услуги</b>', parse_mode='html', reply_markup=keyboard)
        self.get_serivices(message)

    def get_location(self, message):
        self.bot.send_message(message.chat.id, 'Санкт-Петербург, Гороховая ул., 49',)
        self.bot.send_location(message.from_user.id, 59.927261, 30.323459)

    def back_to_menu(self, message):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Какие игры есть?', 'Есть акция?')
        keyboard.row('Где мы находимся?', 'Еда и напитки')
        keyboard.row('Забронировать Online')
        self.bot.send_message(message.chat.id, 'Выберите нужные услуги', reply_markup=keyboard)

    def get_promo_link(self, message):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Перейти в группу', url=self.vk_group_link))
        self.bot.send_message(message.chat.id, 'За другими акциями клуба следите в оффициальной группе <b>Community Heroes в VK</b>!', parse_mode='html', reply_markup=markup)

    def get_games_list(self, message):
        msg = '''<b>На наших компьютерах установлены:</b>
<em>-Rainbow Six Siege
-Osu
-Dota
-2Dota
-Underlords
-ApexLegends
-Left4Dead2
-StarCraft II
-Warcraft III
-World ofWarships
-World of Warcraft
-Heroes of the Storm
-Fortnite
-World of Tanks
-Warface
-Heartstone
-Overwatch CS:GO
-CS 1.6
-PUBG
-PUBG Lite
-League of Legends
-Destiny 2
-FACEIT
-PUBG Lite</em>'''
        self.bot.send_message(message.chat.id, msg, parse_mode='html')

    def get_eats_list(self, message):
        msg = '''<b>В нашем клубе продаются напитки:</b>
<em>-Coca Cola
-Fanta
-Sprite
-Pulpy
-Red Bull</em>
А также батончики
<em>-Mars
-Bounty
-Snickers</em>'''
        self.bot.send_message(message.chat.id, msg, parse_mode='html')

    def parting(self, inter_list, parts):
        part_len = ceil(len(inter_list) / parts)
        return [inter_list[part_len * k:part_len * (k + 1)] for k in range(parts)]

    @staticmethod
    def get_need_item(_dict, key):
        if _dict is None:
            _dict = BotBody.servises
        return _dict.get([i for i in _dict if _dict[i]['key'] == key][0])

    def get_services_list(self):
        return [self.servises[i]['key'] for i in self.servises]

    def get_cost(self, service_key, time):
        choice_service = BotBody.get_need_item(self.servises, service_key)
        return choice_service['times'][time]

    def choice_time(self, query, callback_data):
        self.check_user_data(query.message)
        select_service_key, select_time = [i.strip() for i in callback_data.split('::')[-1].split('__') if i]
        self.cart.add_item('%s__%s' % (select_service_key, select_time), self.get_cost(select_service_key, select_time))
        self.bot.answer_callback_query(query.id, show_alert=True, text="Дата выбрана")
        self.get_serivce_times(query, select_service_key)

    def get_order_description(self, full=False):
        self.order_id = str(time.time())[:10]
        msg = '''№заказа:{5}
Имя: {1}
Username: {3}
Фамилия: {2}
Дата: {4}
Состав: {6}
'''.format(self.user_id or '-', self.user_first_name or '-', self.user_last_name or '-', self.username or '-', str(datetime.now()), self.order_id, self.cart.get_list_items(safe=True))
        msg = '\n'.join([i.strip() for i in msg.split('\n')])
        return msg[:128] if not full else msg

    def create_order(self):
        Configuration.account_id = local_settings.YANDEX_SHOP_ID
        Configuration.secret_key = local_settings.YANDEX_SECRET_KEY
        self.payment = Payment.create({
            "amount": {
                "value": str(float(self.cart.get_cost)),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://mywifi24.ru"
            },
            "capture": True,
            "description": self.get_order_description(),
            "metadata": {
                "order_id": str(self.order_id)
            }
        })
        self.confirmation_url = self.payment.confirmation.confirmation_url
        return self.confirmation_url

    def send_error(self, message):
        self.bot.send_message(message.chat.id, 'Произошла ошибка попробуйте повтроить позже.', reply_markup=None)
        if local_settings.ADMIN_USER_ID is not None and local_settings.ERROR_ALERT_NEW_PAYMENT_CLICK:
            self.bot.send_message(local_settings.ADMIN_USER_ID, 'Произошла ошибка при работе с ботом у пользователя: {0}'.format(self.check_user_data(message)), reply_markup=None)

    def save_order_log(self):
        path = base_dir + '/tele_bot_heroes/order_log/'
        file_name = '{0}.txt'.format(self.order_id)
        file = path + file_name
        if not os.path.exists(path):
            os.mkdir(path)
        with open(file, 'w') as f:
            f.write(str(self.get_order_description(True)))
        print('write to file : ' + str(file))
