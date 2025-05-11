import os
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
from telegram import Update, ForceReply, Bot, ReplyKeyboardMarkup
from telegram_logs import TelegramLogsHandler


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Отправка приветствия и клавиатуры с кнопками."""
    user = update.effective_user

    keyboard = [
        ['Новый вопрос', 'Сдаться'],
        ['Мой счёт']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text(
        f'Привет, {user.first_name}! Я бот для викторины.',
        reply_markup=reply_markup
    )



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


if __name__ == "__main__":

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
    # chat_id = os.environ["TELEGRAM_CHAT_ID"]
    admin_chat_id = os.environ["TG_ADMIN_CHAT_ID"]

    bot = Bot(tg_token)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    logger.addHandler(TelegramLogsHandler(bot, chat_id=admin_chat_id))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # dispatcher.add_handler(
    #     MessageHandler(Filters.text & ~Filters.command, )
    #     )

    updater.start_polling()

    updater.idle()