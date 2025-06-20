from telebot import types
import db

# Buttons
button_plus_1 = types.KeyboardButton('+1')
button_0 = types.KeyboardButton('0')
button_minus_1 = types.KeyboardButton('-1')
button_minus_2 = types.KeyboardButton('-2')
button_minus_3 = types.KeyboardButton('-3')
button_minus_4 = types.KeyboardButton('-4')
button_minus_5 = types.KeyboardButton('-5')
button_minus_6 = types.KeyboardButton('-6')
button_minus_7 = types.KeyboardButton('-7')
button_minus_8 = types.KeyboardButton('-8')
button_star = types.KeyboardButton('⭐️')
button_tentacle = types.KeyboardButton('👹')
button_kthulhu = types.KeyboardButton('🐙')
button_hood = types.KeyboardButton('🥷')    
button_skull = types.KeyboardButton('💀')
button_tablet = types.KeyboardButton('🗿')

button_what_in_bag = types.KeyboardButton('Что в мешке?')
button_add_token = types.KeyboardButton('Добавить жетон')
button_delete_token = types.KeyboardButton('Удалить жетон')
button_dont_want_add_token = types.KeyboardButton('Не хочу добавлять жетон')
button_dont_want_delete_token = types.KeyboardButton('Не хочу удалять жетоны')
buttom_get_token = types.KeyboardButton('Достать жетон')

# TOKENS_BUTTONS = {
#     '+1': button_plus_1,
#     '0': button_0,
#     '-1': button_minus_1,
#     '-2': button_minus_2,
#     '-3': button_minus_3,
#     '-4': button_minus_4,
#     '-5': button_minus_5,
#     '-6': button_minus_6,
#     '-7': button_minus_7,
#     '-8': button_minus_8,
#     '⭐️': button_star,
#     '🥷': button_hood,
#     '🐙': button_kthulhu,
#     '💀': button_skull,
#     '🗿': button_tablet,
#     '👹': button_tentacle
# }

# Keyboards
keyboard_add_token = types.ReplyKeyboardMarkup(
    resize_keyboard=True
    ).row(
        button_minus_1,
        button_minus_2,
        button_minus_3,
        button_minus_4,
        button_minus_5,
        button_minus_6,
        button_minus_7,
        button_minus_8,
    ).row(
        button_plus_1,
        button_0,
        button_star,
        button_tentacle,
        button_kthulhu,
        button_hood,
        button_skull,
        button_tablet
    ).add(
        button_dont_want_add_token
    )


keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_what_in_bag
    ).add(
        button_add_token
    ).add(
        buttom_get_token
    ).add(
        button_delete_token
    )


def keyboard_delete_token(tokens):
    keyboard_delete_token = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=8)
    unique_tokens = list(dict.fromkeys(tokens))
    keyboard_delete_token.add(*unique_tokens).add(button_dont_want_delete_token)
    return keyboard_delete_token
