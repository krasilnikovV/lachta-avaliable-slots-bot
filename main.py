import locale
import logging
import sys
from os import environ

import helpers

if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, 'rus_rus')
else:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
environ['TZ'] = 'Europe/Moscow'

global tt


def main(*args, **kwargs):
    import lahta_parser
    import config
    import telegram_notifire
    raw_schedule = lahta_parser.get_doctors_schedule()
    for doctor in helpers.list_doctors:
        if doctor:
            ds = lahta_parser.DoctorSchedule(raw_schedule, doctor_id=doctor)
            ps = ds.get_pretty_schedule()
            for tg_user in config.tg_users:
                try:
                    identity = f'{str(tg_user)}-{str(doctor)}-{config.app_id}'
                    telegram_notifire.send_schedule(tg_user, schedule=ps, identity=identity)
                except Exception as ex:
                    logging.error(str(ex.__cause__), exc_info=ex)
                    pass


if __name__ == "main":
    main()
