import os

from http import HTTPStatus

import requests
from dotenv import load_dotenv

load_dotenv()

JWT_TOKEN = os.getenv('JWT_TOKEN')
HOST = 'http://127.0.0.1:8000/api/v1'
HEADERS = {'Authorization': f'Bearer {JWT_TOKEN}'}


def create_user(telegram_id: int) -> None:
    """Создаём пользователя."""
    requests.post(
        f'{HOST}/users/',
        data={
            'username': telegram_id,
            'telegram_id': telegram_id,
            'password': 'vjh@8@hbr1skv'
            }
    )

def get_token(telegram_id: int) -> str:
    """Получаем случайный токен."""
    response = requests.get(
        f'{HOST}/random/',
        headers=HEADERS,
        data={'owner': telegram_id},
    )
    if response.status_code == HTTPStatus.NOT_FOUND:
        return ''
    return response.json().get('token')

def get_tokens_from_bag(telegram_id: int) -> list[str]:
    """Получаем все токены."""
    response = requests.get(
        f'{HOST}/bag/',
        headers=HEADERS,
        data={'owner': telegram_id},
    )
    if not response.json():
        return ''
    text = [token.get('token') for token in response.json()]
    return text

def add_token_to_bag(telegram_id: int, token: str) -> str:
    """Добавляет токен в мешок."""
    response = requests.post(
        f'{HOST}/add/',
        headers=HEADERS,
        data={
            'owner': telegram_id,
            'token': token,
        },
    )
    if isinstance(response.json().get('token'), list):
        return ''
    token = response.json().get('token')
    return f'Жетон {token} добавлен.'

def delete_token_from_bag(telegram_id: int, token: str) -> str:
    """Удаляет токен из мешка."""
    response = requests.delete(
        f'{HOST}/delete/',
        headers=HEADERS,
        data={
            'owner': telegram_id,
            'token': token,
        },
    )
    if response.status_code != HTTPStatus.NO_CONTENT:
        return ''
    return f'Жетон {token} удалён.'