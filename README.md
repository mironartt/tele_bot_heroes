# tele_bot_heroes
# bot for https://community-heroes.gg/

Файл настроек: settings.py
В нем указываются ключи от я.кассы, токен бота и настройки уведомлений для админа

для запуска указать прямой путь до питона в окружении и вызвать проект:
Пример, проект (папка с файлами: /tele_bot_heroes/), лежит в: /home/truba/myuser/project/ , и окружение тоже внутри проекта
нужно вызвать:
cd /home/truba/myuser/project/ && /home/truba/myuser/project/tele_bot_heroes/venv/bin/python tele_bot_heroes
После запуститься бот.


Для запуска рассыльщика оповещений команда:
cd /home/truba/myuser/project/ && /home/truba/myuser/project/tele_bot_heroes/venv/bin/python tele_bot_heroes payment_checker 
Также нужно указать в settings.py (или переопределить в local_settings.py)
ALERT_NEW_PAYMENT_MAIL=True
Указать логин и пароль пользователя от почты в:
EMAIL_HOST_USER и EMAIL_HOST_PASSWORD 
В ADMIN_EMAILS указать списком адреса для рассылки.
Для лучшей работы поместить команду в крон
*/5	*	*	*	*	cd /home/truba/myuser/project/ && /home/truba/myuser/project/tele_bot_heroes/venv/bin/python tele_bot_heroes payment_checker