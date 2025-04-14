import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot(' ')  # токен бота
currency = CurrencyConverter()
amount = 0

# Главное меню
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Расчет доходов/расходов')
    btn2 = types.KeyboardButton('Конвертер валют')
    btn3 = types.KeyboardButton('Помощь')
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, 
                    'Привет! Я бот для финансов. Выбери что нужно:\n'
                    '1. Расчет доходов/расходов\n'
                    '2. Конвертер валют\n'
                    '3. Помощь\n'
                    'Курс валют может немного отличаться от реального',
                    reply_markup=markup)

# Обработка всех сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Расчет доходов/расходов':
        msg = bot.send_message(message.chat.id, 'Введи сумму дохода:', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_income)
    elif message.text == 'Конвертер валют':
        msg = bot.send_message(message.chat.id, 'Введи сумму для конвертации:', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_amount)
    elif message.text == 'Помощь':
        msg = bot.send_message(message.chat.id, 'Напиши свой вопрос, и мы поможем! \n 🔧 Данный бот ещё в разработке и имеет ограниченный функционал. \n 🔧 Мы активно работаем над улучшениями, чтобы сделать его удобнее для вас! \n 🔧 Спасибо за понимание и терпение! \n 🔧 Если у вас есть пожелания или вопросы — пишите! \n 🔧 Скоро всё будет лучше!')
        bot.register_next_step_handler(msg, send_help)
    else:
        bot.send_message(message.chat.id, 'Я не понимаю. Нажми одну из кнопок!')
        start(message)

# Функции для расчета бюджета
def get_income(message):
    try:
        income = float(message.text)
        msg = bot.send_message(message.chat.id, 'Теперь введи сумму расходов:')
        bot.register_next_step_handler(msg, lambda m: calculate_balance(m, income))
    except:
        bot.send_message(message.chat.id, 'Нужно ввести число! Попробуй еще раз.')
        start(message)

def calculate_balance(message, income):
    try:
        expenses = float(message.text)
        balance = income - expenses
        bot.send_message(message.chat.id, f'Твой баланс: {balance:.2f}')
        start(message)
    except:
        bot.send_message(message.chat.id, 'Нужно ввести число! Попробуй еще раз.')
        start(message)

# Функции для конвертера валют
def get_amount(message):
    global amount
    try:
        amount = float(message.text)
        if amount <= 0:
            bot.send_message(message.chat.id, 'Число должно быть больше нуля!')
            start(message)
            return
            
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('USD → EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR → USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('RUB → USD', callback_data='rub/usd')
        btn4 = types.InlineKeyboardButton('Другая валюта', callback_data='other')
        markup.add(btn1, btn2, btn3, btn4)
        
        bot.send_message(message.chat.id, 'Выбери валюты:', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, 'Нужно ввести число! Попробуй еще раз.')
        start(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'other':
        msg = bot.send_message(call.message.chat.id, 'Введи пару валют через / (например USD/EUR):')
        bot.register_next_step_handler(msg, custom_currency)
    else:
        try:
            from_curr, to_curr = call.data.split('/')
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

# Функция для помощи
def send_help(message):
    bot.forward_message('@', message.chat.id, message.message_id)  # Канал для приема через "@"
    bot.send_message(message.chat.id, 'Твой вопрос отправлен! Скоро ответим.')
    start(message)

bot.polling(none_stop=True)
