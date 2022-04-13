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
    message_array = ['']
    doctor_str = ''
    clinic_str = ''
    date_str = ''
    time_str = ''
    message = ''
    for k_doctor, v_doctor in schedule.items():
        doctor_str += '*ДОКТОР*: \n'
        doctor_str += f'[{k_doctor}]({v_doctor.get("url", "")})\n'
        for k_clinic, v_clinic in v_doctor.items():
            if k_clinic == "url":
                continue
            clinic_str += f'*КЛИНИКА:* _{k_clinic}_\n'
            date = ""
            i = 0
            times = ''

            for dt in reversed(v_clinic):
                if date != f'*__{dt.strftime("%a, %d %b %y")}__*\n':
                    if times != '':
                        temp = [t.strip() for t in times.split(',')]
                        time_str += '\t'
                        time_str += ', '.join(temp)[:-2]
                        time_str += '\n'
                        times = ''
                    if i != 0:
                        message_array.append(time_str)
                        time_str = ''
                        message_array.append(date_str if message_array[-1] else '')
                        date_str = ''
                    date = f'*__{dt.strftime("%a, %d %b %y")}__*\n'
                    date_str += date
                    if i >= 7:
                        break
                    i += 1
                times += f'{dt.strftime("%H:%M")},'
            message_array.append(clinic_str if message_array[-1] else '')
            clinic_str = ''
        message_array.append(doctor_str if message_array[-1] else '')
        date_str = ''
    message = ''.join(reversed(message_array))
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
