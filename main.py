# import asyncio
import os

from dotenv import load_dotenv
from telebot import TeleBot

import keyboard
from constants import TOKENS_STIKERS, TOKENS
from keyboard import keyboard_add_token, keyboard_main
import requests_to_api as api

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = TeleBot(token=TELEGRAM_TOKEN)


@bot.message_handler(regexp='Что в мешке?')
def get_tokens_from_bag(message):
    chat_id = message.chat.id
    tokens = api.get_tokens_from_bag(telegram_id=chat_id)
    if isinstance(tokens, str):
        bot.send_message(
            chat_id=chat_id,
            text=tokens
        )
    else:
        tokens_str = ', '.join(tokens)
        bot.send_message(
            chat_id=chat_id,
            text=f'В мешке лежат жетоны: {tokens_str}'
        )


@bot.message_handler(regexp='Добавить жетон')
def add_token(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Какой жетон добавить?',
        reply_markup=keyboard_add_token
    )
    bot.register_next_step_handler(message, add_token_input)


def add_token_input(message):
    if message.text == 'Не хочу добавлять жетон':
        start_message(message)
        return
    chat_id = message.chat.id
    answer = api.add_token_to_bag(
        token=message.text,
        telegram_id=chat_id,
    )
    if answer.startswith('Такого'):
        bot.send_message(
            chat_id=chat_id,
            text=answer,
        )
        bot.register_next_step_handler(message, add_token_input)
    else:
        bot.send_message(
            chat_id=chat_id,
            text=answer,
            reply_markup=keyboard_main
        )


@bot.message_handler(regexp='Удалить жетон')
def delete_token(message):
    chat_id = message.chat.id
    answer = api.get_tokens_from_bag(telegram_id=chat_id)
    if isinstance(answer, str):
        bot.send_message(
            chat_id=chat_id,
            text=answer,
            reply_markup=keyboard_main
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text='Какой жетон удалить?',
            reply_markup=keyboard.keyboard_delete_token(answer),
        )
        bot.register_next_step_handler(
            message,
            delete_token_input,
            answer,
        )


def delete_token_input(message, tokens):
    if message.text == 'Не хочу удалять жетоны':
        start_message(message)
        return
    chat_id = message.chat.id
    if message.text not in tokens:
        tokens_str = ', '.join(tokens)
        bot.send_message(
            chat_id=chat_id,
            text='Такого жетона нет в мешке. Попробуйте снова. '
                 f'В мешке лежат жетоны: {tokens_str}'
        )
        bot.register_next_step_handler(
            message,
            delete_token_input,
            tokens,
        )
    else:
        answer = api.delete_token_from_bag(
            telegram_id=chat_id,
            token=message.text,
        )
        bot.send_message(
            chat_id=chat_id,
            text=answer,
            reply_markup=keyboard_main,
        )


@bot.message_handler(regexp='Достать жетон')
def get_token(message):
    chat_id = message.chat.id
    answer = api.get_token(telegram_id=chat_id)
    if answer in TOKENS:
        sticker = TOKENS_STIKERS.get(answer)
        bot.send_sticker(
            chat_id=chat_id,
            sticker=sticker,
            reply_markup=keyboard_main
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=answer,
            reply_markup=keyboard_main
        )


@bot.message_handler(regexp='Статистика')
def get_statistic(message):
    chat_id = message.chat.id
    statistic = api.get_statistic(telegram_id=chat_id)
    bot.send_message(
        chat_id=chat_id,
        text=statistic,
        reply_markup=keyboard_main,
        parse_mode='MarkdownV2',
    )


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    api.create_user(telegram_id=chat_id)
    start_message(message)


@bot.message_handler(commands=['home'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Я мешок, я мешок. Вот что я могу.',
        reply_markup=keyboard_main
    )


@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Извините, я не знаю такой команды. Вот что я могу.',
        reply_markup=keyboard_main
    )


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
