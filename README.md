Универсальный Telegram Бот (v0.1)
Многофункциональный бот для финансовых расчетов и конвертации валют

📌 Основные функции:
   
    💰 Расчет баланса (доходы минус расходы)
    💱 Конвертер валют с поддержкой популярных пар

⚙️ Технические требования:

    Python 3.6+

Установленные библиотеки:

1

      pyTelegramBotAPI

2

      CurrencyConverter

🛠 Установка:
Установите зависимости:
    
    pip install pyTelegramBotAPI CurrencyConverter

Замените токен бота в коде:

    bot = telebot.TeleBot('ВАШ_ТОКЕН')
    
Запустите бота:

    python bot.py
    
🎮 Как пользоваться:

        Отправьте команду /start
        
        Выберите режим работы:
        
        Финансовый расчет:
        
        Введите сумму дохода
        
        Введите сумму расходов
        
        Получите расчет баланса


        Конвертер валют:
        
        Введите сумму для конвертации
        
        Выберите валютную пару из предложенных или введите свою
        
        Получите результат конвертации


⚠️ Примечания:

Все суммы должны быть положительными числами
Для валютной конвертации используйте общепринятые коды валют
Точность расчетов зависит от актуальности курсов валют

Universal Telegram Bot (v0.1)
Multifunctional bot for financial calculations and currency conversion

📌 Key Features:
💰 Balance calculation (income minus expenses)

💱 Currency converter with popular pairs support

⚙️ Requirements:
Python 3.6+

Required libraries:

    pyTelegramBotAPI
    
    CurrencyConverter

🛠 Installation:
Install dependencies:

    pip install pyTelegramBotAPI CurrencyConverter

Replace bot token in code:

    bot = telebot.TeleBot('YOUR_BOT_TOKEN')
    
Run the bot:

    python bot.py

🎮 How to use:
Send /start command

        Select mode:
        
        Financial calculator:
        
        Enter income amount
        
        Enter expenses amount
        
        Get balance calculation
        
        Currency converter:
        
        Enter amount to convert
        
        Select currency pair or enter custom one
        
        Get conversion result

⚠️ Notes:

All amounts must be positive numbers
Use standard currency codes for conversion
Calculation accuracy depends on current exchange rates
