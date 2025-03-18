import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('7999938977:AAFLMYMmBRxO_crNSX9nMtRSb5sgqVs9ww8')  # токен API
Currency = CurrencyConverter()
amount = 0

# Хранилище текущего режима
current_mode = ''

@bot.message_handler(commands=['start'])
def start(message):
    global current_mode
    current_mode = ''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Расчет доходов/расходов')
    btn2 = types.KeyboardButton('Конвертер валют')
    markup.add(btn1, btn2)
    bot.send_message(
        message.chat.id,
        'Здравствуйте! Я универсальный бот. Выберите режим работы:',
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def select_mode(message):
    global current_mode

    if message.text == 'Расчет доходов/расходов':
        current_mode = 'budget'
        bot.send_message(
            message.chat.id,
            'Вы выбрали режим расчета доходов/расходов. Введите сумму дохода:'
        )
        bot.register_next_step_handler(message, calculate_budget)
    elif message.text == 'Конвертер валют':
        current_mode = 'currency'
        bot.send_message(
            message.chat.id,
            'Вы выбрали режим конвертера валют. Введите сумму для конвертации:'
        )
        bot.register_next_step_handler(message, summa)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из доступных режимов.')

# Режим расчета доходов/расходов
def calculate_budget(message):
    try:
        income = float(message.text.strip())
        bot.send_message(message.chat.id, 'Введите сумму расходов:')
        bot.register_next_step_handler(message, lambda msg: calculate_result(msg, income))
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите числовое значение дохода.')
        bot.register_next_step_handler(message, calculate_budget)

def calculate_result(message, income):
    try:
        expenses = float(message.text.strip())
        balance = income - expenses
        bot.send_message(
            message.chat.id,
            f'Ваш баланс: {balance:.2f}. Введите новую сумму дохода для расчета или выберите другой режим.'
        )
        bot.register_next_step_handler(message, calculate_budget)
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите числовое значение расходов.')
        bot.register_next_step_handler(message, lambda msg: calculate_result(msg, income))

# Режим конвертера валют
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
        bot.send_message(call.message.chat.id, 'Введите пару значений через \"/\".')
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
        bot.send_message(message.chat.id, f'Что-то пошло не так: {e}. Впишите значение через \"/\".')
        bot.register_next_step_handler(message, mycurrency)

bot.polling(none_stop=True)
