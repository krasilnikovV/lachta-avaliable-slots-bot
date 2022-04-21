import logging
from datetime import datetime

import boto3
import telebot

import config

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

if config.bot_token is None:
    logging.error("telegram bot token is not specified!")
    exit(-2)

bot = None

try:
    bot = telebot.TeleBot(config.bot_token, parse_mode='MarkdownV2')
except Exception as ex:
    logging.exception("telegram bot token is incorrect", exc_info=ex, stack_info=False)
    exit(-2)


def build_message(schedule: dict):
    message = ''

    msg_dict = {}
    for k_doctor, v_doctor in schedule.items():
        _doc = msg_dict['*ДОКТОР*: \n' + f'[{k_doctor}]({v_doctor.get("url", "")})\n'] = {}
        for k_clinic, v_clinic in v_doctor.items():
            if k_clinic == "url":
                continue
            _clinic = _doc[f'*КЛИНИКА:* _{k_clinic}_\n'] = {}
            date = ""
            i = 0
            _date = None
            for dt in v_clinic:
                if date != f'*__{dt.strftime("%a, %d %b %y")}__*\n':
                    date = f'*__{dt.strftime("%a, %d %b %y")}__*\n'
                    _date = _clinic[f'*__{dt.strftime("%a, %d %b %y")}__*\n'] = []
                    if i >= 7:
                        break
                    i += 1
                _date.append(f'{dt.strftime("%H:%M")}')

    for k_doctor, v_doctor in msg_dict.items():
        if v_doctor:
            message += k_doctor
            for k_clinic, v_clinic in v_doctor.items():
                if v_clinic:
                    message += k_clinic
                    for k_date, v_date in v_clinic.items():
                        if v_date:
                            message += k_date
                            message += '\t'
                            message += ', '.join(v_date)
                            message += '\n'
    return message


def send_schedule(user_id: int, msg: str = "", schedule=None):
    if schedule is None:
        schedule = {}
    msg = msg if msg else build_message(schedule)
    try:
        get_object_response = s3.get_object(Bucket='lahta-state', Key='object_test')
        response_body = get_object_response['Body'].read()
    except:
        response_body = b''
    print(response_body)
    print(response_body == bytes(msg, 'UTF-8'))
    print(bytes(msg, 'UTF-8'))
    if response_body and str(response_body.decode('UTF-8')) == msg:
        return
    bot.send_message(
        user_id,
        msg
    )
    s3.put_object(Bucket='lahta-state', Key='object_test', Body=msg)
