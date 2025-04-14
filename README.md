Многофункциональный бот для финансовых расчетов и конвертации валют

📌 Основные функции:

💰 Расчет баланса (доходы минус расходы)
💱 Конвертер валют с поддержкой популярных валютных пар

⚙️ Технические требования
    Python 3.6+

Библиотеки:
    pyTelegramBotAPI
    CurrencyConverter
    
🛠 Установка и запуск
Установите необходимые зависимости:
    
    pip install pyTelegramBotAPI CurrencyConverter

Замените токен бота в строке:
    
    bot = telebot.TeleBot('TELEGRAM_BOT_TOKEN')
    
Запустите бота:
    
    python bot.py

🎮 Как пользоваться

Отправьте команду /start

    Выберите режим работы:
        Расчет доходов/расходов:
            Введите сумму дохода
                Введите сумму расходов
                    Получите расчет баланса
                    
Конвертер валют:

    Введите сумму для конвертации
        Выберите валютную пару или введите свою
            Получите результат конвертации

📜 Лицензия
Свободное использование. Автор не несет ответственности за точность финансовых расчетов.

v0.1
