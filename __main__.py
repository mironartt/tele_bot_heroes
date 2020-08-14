import sys
import os
from start import start_bot
from payment_checker import start_check

if __name__ == '__main__':
    if 'payment_checker' not in sys.argv:
        print('----- START BOT')
        start_bot()
    else:
        print('----- START PAYMENT CHECKER')
        start_check()



