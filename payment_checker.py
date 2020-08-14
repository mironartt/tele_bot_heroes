import os
import settings
from utils import check_payments, send_alerts

base_dir = os.path.abspath(os.curdir)

def start_check():
    print('start_check >  1')
    if settings.ALERT_NEW_PAYMENT_MAIL and settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
        try:
            check_payments()
        except:
            pass
        try:
            send_alerts()
        except:
            pass



