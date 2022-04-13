import locale
import sys
from os import environ

if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, 'rus_rus')
else:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
environ['TZ'] = 'Europe/Moscow'

global tt


def main():
    pass


if __name__ == "main":
    main()
