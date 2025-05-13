#v0.2
import telebot
from currency_converter import CurrencyConverter
from telebot import types
from datetime import datetime

bot = telebot.TeleBot('7999938977:AAH9jl0TlxB6_xQJ_Xpjxp6BgG4isagjYQ') #Токен бота
currency = CurrencyConverter()
amount = 0
user_data = {}

# Режимы работы(кнопки)
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Расчет доходов/расходов')
    btn2 = types.KeyboardButton('Конвертер валют')
    btn3 = types.KeyboardButton('История доходов/расходов')
    btn4 = types.KeyboardButton('Помощь')
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id,
        'Привет! Я бот для финансов. Выбери, что нужно:\n'
        '1. Расчет доходов/расходов\n'
        '2. Конвертер валют\n'
        '3. История доходов/расходов\n'
        '4. Помощь\n',
        reply_markup=markup)

# Обработка текста
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Расчет доходов/расходов':
        msg = bot.send_message(message.chat.id, 'Введи сумму дохода:', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_income)
    elif message.text == 'Конвертер валют':
        msg = bot.send_message(message.chat.id, 'Используется курс ЕЦБ, без комиссий\n  Введи сумму для конвертации:', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_amount)
    elif message.text == 'Помощь':
        msg = bot.send_message(message.chat.id, 'Напиши свой вопрос, и мы поможем! \n 🔧 Данный бот ещё в разработке и имеет ограниченный функционал. \n 🔧 Мы активно работаем над улучшениями, чтобы сделать его удобнее для вас! \n 🔧 Спасибо за понимание и терпение! \n 🔧 Если у вас есть пожелания или вопросы — пишите! \n 🔧 Скоро всё будет лучше!')
        bot.register_next_step_handler(msg, send_help)
    elif message.text == 'История доходов/расходов':
        show_totals_options(message)
    else:
        bot.send_message(message.chat.id, 'Я не понимаю. Нажми одну из кнопок.')
        start(message)

#Доходы и расходы
def get_income(message):
    try:
        income = float(message.text)
        msg = bot.send_message(message.chat.id, 'Теперь введи сумму расходов:')
        bot.register_next_step_handler(msg, lambda m: calculate_balance(m, income))
    except:
        bot.send_message(message.chat.id, 'Нужно ввести число. Попробуй снова.')
        start(message)

def calculate_balance(message, income):
    try:
        expenses = float(message.text)
        balance = income - expenses
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = message.chat.id

        if user_id not in user_data:
            user_data[user_id] = []

        user_data[user_id].append({
            'datetime': now,
            'income': income,
            'expenses': expenses,
            'balance': balance
        })

        bot.send_message(message.chat.id, f'Запись сохранена: {now}\nТвой баланс: {balance:.2f}')
        start(message)
    except:
        bot.send_message(message.chat.id, 'Нужно ввести число. Попробуй снова.')
        start(message)

# История расходом/доходов
def show_totals_options(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Общая история', callback_data='totals_general')
    btn2 = types.InlineKeyboardButton('Детальная история', callback_data='totals_detail')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Выбери тип историй:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('totals_'))
def handle_totals(call):
    user_id = call.message.chat.id
    if user_id not in user_data or not user_data[user_id]:
        bot.send_message(user_id, 'У тебя пока нет записей.')
        return

    if call.data == 'totals_general':
        total_income = sum(entry['income'] for entry in user_data[user_id])
        total_expenses = sum(entry['expenses'] for entry in user_data[user_id])
        total_balance = total_income - total_expenses

        bot.send_message(user_id,
            'История доходов/расходов:\n'
            f'Доходов: {total_income:.2f}\n'
            f'Расходов: {total_expenses:.2f}\n'
            f'Баланс: {total_balance:.2f}')
    elif call.data == 'totals_detail':
        detail_lines = [
            f"{entry['datetime']} — Доход: {entry['income']:.2f}, Расход: {entry['expenses']:.2f}"
            for entry in user_data[user_id]
        ]
        response = '\n'.join(detail_lines)
        bot.send_message(user_id, f'Детальная история:\n\n{response}')

# Конвертер валют
# Используется доступный конверт валюты, для других нужна платная подписка
def get_amount(message):
    global amount
    try:
        amount = float(message.text)
        if amount <= 0:
            bot.send_message(message.chat.id, 'Число должно быть больше нуля!')
            start(message)
            return

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('USD → EUR', callback_data='convert_usd/eur')
        btn2 = types.InlineKeyboardButton('EUR → USD', callback_data='convert_eur/usd')
        btn3 = types.InlineKeyboardButton('RUB → USD', callback_data='convert_rub/usd')
        btn4 = types.InlineKeyboardButton('Другая валюта', callback_data='convert_other')
        markup.add(btn1, btn2, btn3, btn4)

        bot.send_message(message.chat.id, 'Выбери валюты:', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, 'Нужно ввести число! Попробуй еще раз.')
        start(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('convert_'))
def callback_handler(call):
    data = call.data.replace('convert_', '')
    if data == 'other':
        msg = bot.send_message(call.message.chat.id, 'Введи пару валют через / (например USD/EUR):')
        bot.register_next_step_handler(msg, custom_currency)
    else:
        try:
            from_curr, to_curr = data.split('/')
            result = currency.convert(amount, from_curr.upper(), to_curr.upper())
            bot.send_message(call.message.chat.id, f'Результат: {round(result, 2)}')
            start(call.message)
        except:
            bot.send_message(call.message.chat.id, 'Ошибка конвертации. Попробуй еще раз.')
            start(call.message)

def custom_currency(message):
    try:
        from_curr, to_curr = message.text.upper().split('/')
        result = currency.convert(amount, from_curr, to_curr)
        bot.send_message(message.chat.id, f'Результат: {round(result, 2)}')
        start(message)
    except:
        bot.send_message(message.chat.id, 'Неверный формат. Попробуй еще раз.')
        start(message)

# Помощь
def send_help(message):
    bot.forward_message('@feedback_acc', message.chat.id, message.message_id) #Ссылка на группу для приема сообшений
    bot.send_message(message.chat.id, 'Твой вопрос отправлен! Скоро ответим.')
    start(message)

bot.polling(none_stop=True)
