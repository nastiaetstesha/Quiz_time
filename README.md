# Quiz_Time
#### Python 3.11.11  
`Quiz_Time` — это Telegram- и VK-боты для викторины. Пользователь может получать вопросы, отвечать на них, сдаваться, видеть новый вопрос и накапливать очки (в будущем).  

📌 Примеры:
- Telegram: [t.me/bot_Quiz_quiz_bot](https://t.me/bot_Quiz_quiz_bot)
- VK: [vk.com/club75514542](https://vk.com/club75514542)

---

## 🚀 Функциональность

- Викторина по готовым вопросам
- Кнопки управления (Новый вопрос, Сдаться, Мой счёт)
- Поддержка Telegram и ВКонтакте
- Хранение состояния и статистики в Redis
- Логирование ошибок в Telegram-чат

---

## 🛠️ Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/Quiz_Time.git
cd Quiz_Time
```

### Установка зависимостей

`pip install -r requirements.txt`
### Переменные окружения
Создайте .env файл в корне проекта со следующим содержимым:

```
VK_API_KEY=токен от группы в вконтакте
TELEGRAM_BOT_TOKEN=токен телеграм от бота
TG_ADMIN_CHAT_ID=чат айди администратора в телеграмм
REDIS_PASSWORD=redis пароль
REDIS_HOST=redis хост
PATH_TO_QUESTIONS=путь до директории с вопросами для квиза
```
### 📁 Структура проекта
```
Quiz_Time/
├── quiz_data.py            # Загрузка и парсинг текстов с вопросами
├── telegram_logs.py        # Логирование ошибок в Telegram
├── tg_bot.py               # Telegram-бот
├── vk_bot.py               # ВКонтакте-бот
├── test.py                 # Тесты (или временные функции)
├── .env                    # Переменные окружения
├── requirements.txt        # Зависимости
├── README.md               # Документация
```
### 🔧 Запуск
#### Telegram бот:

`python tg_bot.py`
#### VK бот:


`python vk_bot.py`
### 📡 Логирование
Все ошибки и события отправляются в Telegram-чат, указанный в TG_ADMIN_CHAT_ID.

```
from telegram import Bot
from telegram_logs import TelegramLogsHandler

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
logger.addHandler(TelegramLogsHandler(bot, chat_id=os.getenv("TG_ADMIN_CHAT_ID")))
```

### 📌 Основные зависимости
`python-telegram-bot` — Telegram API

`vk_api` — VK API

`redis` — хранение состояния пользователей

`python-dotenv` — подгрузка переменных окружения из .env

`logging` — логирование ошибок
