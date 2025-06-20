"""A bag of tokens emulator."""

import random

import db
from constants import TOKENS
from exceptions import (
    DontWantAddToken,
    DontWantDeleteToken,
    EmptyBag,
    UnexpectedToken
)


def get_token(id) -> None:
    """Get token from bag."""
    token_set = db.get_bag_from_db(id=id)
    if token_set:
        return random.choice(token_set)
    raise EmptyBag


def add_token(token, table, id) -> None:
    """Добавляет жетон в мешок."""
    if not isinstance(token, str):
        token = str(token)
    if token == 'Не хочу добавлять жетон':
        raise DontWantAddToken
    if token not in TOKENS:
        raise UnexpectedToken(
            'Такого жетона не существует. Попробуйте снова. '
            f'Список возможных жетонов: {TOKENS}')
    db.add_token(token=token, table=table, id=id)


def delete_token(token, table, id) -> None:
    """Удаляет жетоны из мешка."""
    if not isinstance(token, str):
        token = str(token)
    if token == 'Не хочу удалять жетоны':
        raise DontWantDeleteToken
    token_set = db.get_bag_from_db(id=id)
    if not token_set:
        raise EmptyBag
    if token not in token_set:
        raise UnexpectedToken(
            'Такого жетона нет в мешке. Попробуйте снова. '
            f'В мешке лежат жетоны: {token_set}')
    db.delete_token(token=token, table=table, id=id)


def what_in_bag(id):
    token_set = db.get_bag_from_db(id=id)
    if not token_set:
        return 'Мешок пуст'
    else:
        token_set = ' '.join(token_set)
        return f'В мешке лежат жетоны: {token_set}'


# def add_token_set(self, token_set: str) -> None:
#     """Add token set to the bag."""
#     if not isinstance(token_set, str):
#         token_set = str(token_set)
#     split_token_set = token_set.split(' ')
#     for token in split_token_set:
#         if token not in TOKENS:
#             print(f'Жетона {token} не существует. Попробуйте снова. '
#                     f'Список возможных жетонов: {TOKENS}')
#             return
#         self.token_set.append(token)
#     print(f'Набор жетонов {token_set} успешно добавлен в мешок.')

def main():
    """Main."""
    pass


if __name__ == '__main__':
    main()
