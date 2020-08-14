# для запуска указать прямой путь до питона в окружении и вызвать проект:
# Пример, проект (папка с файлами: /tele_bot_heroes/), лежит в: /home/truba/myuser/project/ , и окружение тоже внутри проекта
# нужно вызвать:
# cd /home/myuser/project/ && /home/myuser/project/tele_bot_heroes/venv/bin/python tele_bot_heroes
# После запуститься бот.
# Команду можно и в демон и в крон

import os

base_dir = os.path.abspath(os.curdir)

BOT_TOKEN = None
YANDEX_SECRET_KEY = None
YANDEX_SHOP_ID = None
ADMIN_USER_ID = None                    # Чтобы узнать нужно подключится к боту: @userinfobot
ALERT_NEW_PAYMENT_CLICK = True          # Оповещать если был клик по кнопке "ОПЛАТИТЬ"
ALERT_NEW_PAYMENT_MAIL = True
ERROR_ALERT_NEW_PAYMENT_CLICK = True    # Оповещать если в работе бота была ошибка
PAYMENT_LOG_FILE = base_dir + '/tele_bot_heroes/files/payments.txt'
ALERT_LOG_FILE = base_dir + '/tele_bot_heroes/files/alerts.txt'


EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
ADMIN_EMAILS = []                       # Список email админов для уведомлений
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

try:
    from local_settings import *
except ImportError:
    pass