# import asyncio
import os

from dotenv import load_dotenv
from telebot import TeleBot

import bag_of_tokens
import db
import keyboard
from constants import TOKENS_STIKERS, TOKENS_STR
from exceptions import DontWantAddToken, DontWantDeleteToken, EmptyBag, UnexpectedToken
from keyboard import keyboard_add_token, keyboard_main
import requests_to_api as api

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = TeleBot(token=TELEGRAM_TOKEN)


@bot.message_handler(regexp='Что в мешке?')
def get_tokens_from_bag(message):
    chat_id = message.chat.id
    tokens = api.get_tokens_from_bag(telegram_id=chat_id)
    if not tokens:
        bot.send_message(
        chat_id=chat_id,
        text=f'Мешок пуст.'
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
    text = api.add_token_to_bag(
        token=message.text,
        telegram_id=chat_id
    )
    if not text:
        bot.send_message(
            chat_id=chat_id,
            text='Такого жетона не существует.\n'
                 'Выберите один из предложеных жетонов.\n'
                 f'Список возможных жетонов:\n{TOKENS_STR}'
        )
        bot.register_next_step_handler(message, add_token_input)
    else:
        bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard_main
        )


@bot.message_handler(regexp='Удалить жетон')
def delete_token(message):
    chat_id = message.chat.id
    tokens = api.get_tokens_from_bag(telegram_id=chat_id)
    if not tokens:
        bot.send_message(
            chat_id=chat_id,
            text='Мешок пуст.',
            reply_markup=keyboard_main
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text='Какой жетон удалить?',
            reply_markup=keyboard.keyboard_delete_token(tokens),
        )
        bot.register_next_step_handler(
            message,
            delete_token_input,
            tokens,
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
        api.delete_token_from_bag(
        telegram_id=chat_id,
        token=message.text,
    )
        bot.send_message(
            chat_id=chat_id,
            text=f'Жетон {message.text} удалён.',
            reply_markup=keyboard_main,
        )


@bot.message_handler(regexp='Достать жетон')
def get_token(message):
    chat_id = message.chat.id
    token = api.get_token(telegram_id=chat_id)
    if not token:
        bot.send_message(
            chat_id=chat_id,
            text='Мешок пуст.',
            reply_markup=keyboard_main
        )
    else:
        sticker = TOKENS_STIKERS.get(token)
        bot.send_sticker(
            chat_id=chat_id,
            sticker=sticker,
            reply_markup=keyboard_main
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
        text='Я мешок, я мешок. Вот что я могу',
        reply_markup=keyboard_main
    )

def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
