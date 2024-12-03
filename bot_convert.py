import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('') #токенAPI
Currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        'Здравствуйте, я универсальный бот.\n'
        'На данный момент могу конвертировать валюту.\n'
        'Введите число, которое хотите конвертировать в нужную пару\n'
        'P.S. Вводите целые числа\n'
        'P.S.S Обновление курса происходит с задержкой'
    ) 
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try: 
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите целое число.')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть > 0. Впишите сумму.')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        try:
            res = Currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму.')
        except Exception as e:
            bot.send_message(call.message.chat.id, f'Ошибка конвертации: {e}. Попробуйте снова.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через "/".')
        bot.register_next_step_handler(call.message, mycurrency)

def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        if len(values) != 2:
            raise ValueError("Некорректный формат. Укажите пару в формате XXX/YYY.")
        res = Currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму.')
        bot.register_next_step_handler(message, summa)
    except Exception as e:
        bot.send_message(message.chat.id, f'Что-то пошло не так: {e}. Впишите значение через "/".')
        bot.register_next_step_handler(message, mycurrency)

bot.polling(none_stop=True)
