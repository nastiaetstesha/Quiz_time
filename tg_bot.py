import os
import logging
import random

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler
)
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram_logs import TelegramLogsHandler
from quiz_data import load_all_questions
import redis
from enum import Enum


class BotState(Enum):
    WAITING_FOR_ANSWER = 1


logger = logging.getLogger(__name__)


def handle_new_question_request(update: Update, context: CallbackContext) -> BotState:
    user_id = str(update.effective_user.id)
    question = random.choice(list(questions.keys()))
    redis_conn.set(user_id, question)
    update.message.reply_text(question)
    return BotState.WAITING_FOR_ANSWER


def handle_solution_attempt(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    question = redis_conn.get(user_id)

    if not question:
        update.message.reply_text("Сначала запросите вопрос.")
        return BotState.WAITING_FOR_ANSWER

    correct_answer = questions.get(question)
    user_answer = update.message.text.lower()
    cleaned_correct = correct_answer.split('.')[0].split('(')[0].strip().lower()

    if user_answer in cleaned_correct:
        update.message.reply_text(
            '''Правильно! Поздравляю!
            Для следующего вопроса нажми «Новый вопрос».'''
        )
        return ConversationHandler.END
    else:
        update.message.reply_text('Неправильно… Попробуешь ещё раз?')
        return BotState.WAITING_FOR_ANSWER


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("До встречи!")
    return ConversationHandler.END


def handle_give_up(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    question = redis_conn.get(user_id)

    if question:
        answer = questions.get(question)
        update.message.reply_text(f'Правильный ответ: {answer}')
    else:
        update.message.reply_text('Сначала запросите вопрос.')

    new_question = random.choice(list(questions.keys()))
    redis_conn.set(user_id, new_question)
    update.message.reply_text(new_question)

    return BotState.WAITING_FOR_ANSWER


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text(
        "Привет! \n"
        "Я — бот-викторина 🎓. Я буду задавать тебе вопросы.\n\n"
        "Нажми «Новый вопрос», чтобы начать!\n"
        "Если не знаешь — нажми «Сдаться», чтобы узнать ответ.\n"
        "Потом можешь попробовать следующий вопрос.\n\n"
        "Удачи! 🍀",
        reply_markup=reply_markup
    )


if __name__ == "__main__":

    redis_host = os.environ["REDIS_HOST"]
    path_to_questions = os.environ["PATH_TO_QUESTIONS"]
    tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
    admin_chat_id = os.environ["TG_ADMIN_CHAT_ID"]

    redis_conn = redis.StrictRedis(
        host=redis_host,
        port=19137,
        password=os.environ["REDIS_PASSWORD"],
        decode_responses=True
    )
    
    questions = load_all_questions(path_to_questions)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bot = Bot(tg_token)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    logger.addHandler(TelegramLogsHandler(bot, chat_id=admin_chat_id))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(
            Filters.regex('^(Новый вопрос)$'), handle_new_question_request
            )],
        states={
             BotState.WAITING_FOR_ANSWER: [
                MessageHandler(Filters.regex('^(Сдаться)$'), handle_give_up),
                MessageHandler(
                    Filters.text & ~Filters.command, handle_solution_attempt
                    ),
                ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()