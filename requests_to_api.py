import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv

from constants import TOKENS_STR, TOKENS_STAT

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
            'password': os.getenv('USER_PASSWORD')
            }
    )


def get_token(telegram_id: int) -> str:
    """Получаем случайный токен."""
    try:
        response = requests.get(
            f'{HOST}/random/',
            headers=HEADERS,
            data={'owner': telegram_id},
        )
    except Exception:
        answer = 'Ой, кажется сервис временно не работает, попробуйте позже.'
    else:
        if response.status_code == HTTPStatus.NOT_FOUND:
            answer = 'Мешок пуст.'
        else:
            answer = response.json().get('token')
    return answer


def get_tokens_from_bag(telegram_id: int) -> list[str]:
    """Получаем все токены."""
    try:
        response = requests.get(
            f'{HOST}/bag/',
            headers=HEADERS,
            data={'owner': telegram_id},
        )
    except Exception:
        answer = 'Ой, кажется сервис временно не работает, попробуйте позже.'
    else:
        if not response.json():
            answer = 'Мешок пуст.'
        else:
            answer = [token.get('token') for token in response.json()]
    return answer


def add_token_to_bag(telegram_id: int, token: str) -> str:
    """Добавляет токен в мешок."""
    try:
        response = requests.post(
            f'{HOST}/add/',
            headers=HEADERS,
            data={
                'owner': telegram_id,
                'token': token,
            },
        )
    except Exception:
        answer = 'Ой, кажется сервис временно не работает, попробуйте позже.'
    else:
        if response.status_code == HTTPStatus.BAD_REQUEST:
            answer = (
                'Такого жетона не существует.\n'
                'Выберите один из предложеных жетонов.\n'
                f'Список возможных жетонов:\n{TOKENS_STR}'
            )
        else:
            answer = f'Жетон {response.json().get("token")} добавлен.'
    return answer


def delete_token_from_bag(telegram_id: int, token: str) -> str:
    """Удаляет токен из мешка."""
    try:
        response = requests.delete(
            f'{HOST}/delete/',
            headers=HEADERS,
            data={
                'owner': telegram_id,
                'token': token,
            },
        )
    except Exception:
        answer = 'Ой, кажется сервис временно не работает, попробуйте позже.'
    else:
        if response.status_code == HTTPStatus.NO_CONTENT:
            answer = f'Жетон {token} удалён.'
        else:
            answer = 'Ой, что-то пошло не так, проверьте мешок.'
    return answer


def get_statistic(telegram_id: int) -> str:
    """Получение статистики пользователя."""
    try:
        response = requests.get(
            f'{HOST}/statistic/',
            headers=HEADERS,
            data={'owner': telegram_id},
        )
    except Exception:
        answer = 'Ой, кажется сервис временно не работает, попробуйте позже.'
    else:
        answer = get_beautiful_statistic(response.json())
    return answer


def get_beautiful_statistic(statistic: dict) -> str:
    statistic_values = statistic.values()
    maximum_value = max(statistic_values) or 1
    beautiful_statistic = 'Статистика\n'
    for char, stat in zip(TOKENS_STAT, statistic_values):
        n = 4 - len(str(stat))
        v = round(stat / maximum_value * 15)
        beautiful_statistic += f'{char}: {stat}{" " * n}▐{"█" * v}\n'
    return '`' + beautiful_statistic + '`'
