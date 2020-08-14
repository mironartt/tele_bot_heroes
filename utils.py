import json
import time
import os
import settings
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from datetime import datetime
from yandex_checkout import Configuration, Payment
Configuration.account_id = settings.YANDEX_SHOP_ID
Configuration.secret_key = settings.YANDEX_SECRET_KEY


def save_payment(p_data, is_list=False):
    try:
        if not is_list:
            with open(settings.PAYMENT_LOG_FILE, 'a') as f:
                f.write(str(json.loads(p_data)) + '\n')
            order_id = p_data.get('metadata', {}).get('order_id')
            if order_id is not None:
                with open(settings.base_dir + '/tele_bot_heroes/logs/mails/' + '%s.txt' % str(order_id), 'w') as f:
                    f.write(str(json.loads(p_data)))
        else:
            with open(settings.PAYMENT_LOG_FILE, 'w') as f:
                for payment in p_data:
                    f.write(str(payment) + '\n')
    except:
        pass

def save_mail_log(mail_data):
    file = settings.base_dir + '/tele_bot_heroes/logs/mails/' + '{0}.txt'.format(datetime.now().strftime('%Y-%m-%d'))
    with open(file, 'a') as f:
        f.write(str(mail_data) + '\n')

def create_alert(payment_dict):
    order_id = payment_dict.get('metadata', {}).get('order_id')
    if order_id is None:
        return
    with open(settings.ALERT_LOG_FILE, 'a') as f:
        order = get_order(order_id)
        if order is None:
            return
        msg = 'ОПЛАТА ЗАКАЗА\nОПИСАНИЕ ЗАКАЗА:\n{0}\nДЕТАЛИ ОПЛАТЫ:\n{1}'.format(order, payment_dict)
        f.write(str({'msg': msg}) + '\n')


def get_order(order_id):
    orders_dir = settings.base_dir + '/tele_bot_heroes/logs/orders/'
    order_files = os.listdir(orders_dir)
    order = [i for i in order_files if order_id in i]
    if not order:
        return None
    order = open(orders_dir + order[0], 'r').read()
    return order


def check_payments():
    payments = [eval(str(i).strip()) for i in open(settings.PAYMENT_LOG_FILE, 'r').read().split('\n') if i]
    for num, payment in enumerate(payments):
        if payment.get('status') == 'succeeded':
            payments.remove(payment)
            continue
        try:
            _payment = Payment.find_one(payment['id'])
        except:
            continue
        payments[num] = json.loads(_payment.json())
        if _payment.status == 'succeeded':
            if settings.ALERT_NEW_PAYMENT_MAIL:
                create_alert(payments[num])
        time.sleep(0.5)
    save_payment(payments, True)
    return payments


def get_alerts():
    return [eval(str(i).strip())['msg'] for i in open(settings.ALERT_LOG_FILE, 'r').read().split('\n') if i]


def cleart_alerts():
    f = open(settings.ALERT_LOG_FILE, 'w')
    f.close()


def send_mail(mail_to, message):
    smtp_host = settings.EMAIL_HOST
    login = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    recipients_emails = mail_to
    subject = 'Успешная оплата заказа'

    msg = MIMEText(str(message), 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = login
    msg['To'] = recipients_emails

    s = smtplib.SMTP(smtp_host, 587, timeout=10)
    s.set_debuglevel(1)
    try:
        s.starttls()
        s.login(login, password)
        s.sendmail(msg['From'], recipients_emails, msg.as_string())
        save_mail_log({'mail_to': recipients_emails, 'message': message, 'subject': subject})
        print('-- NICE SEND')
    finally:
        print(msg)
        s.quit()
    return True


def send_alerts():
    alerts = get_alerts()
    for email in settings.ADMIN_EMAILS:
        for alert_msg in alerts:
            try:
                send_mail(email, alert_msg)
            except:
                pass
    cleart_alerts()