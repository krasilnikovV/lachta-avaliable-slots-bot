import logging

import telebot

import config

if config.bot_token is None:
    logging.error("telegram bot token is not specified!")
    exit(-2)

bot = None

try:
    bot = telebot.TeleBot(config.bot_token, parse_mode='MarkdownV2')
except Exception as ex:
    logging.exception("telegram bot token is incorrect", exc_info=ex, stack_info=False)
    exit(-2)


def send_schedule(user_id: int, schedule):
    bot.send_message(
        user_id,
        f"```"
        f"{str(schedule)}"
        f"```"
    )
