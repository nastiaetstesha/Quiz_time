import os
import random
import logging
import redis
import vk_api
import json
from functools import partial

from vk_api.longpoll import VkLongPoll, VkEventType
from quiz_data import load_all_questions


logger = logging.getLogger(__name__)


def send_keyboard(vk, user_id, message):
    keyboard = {
        "one_time": False,
        "buttons": [
            [{"action":
              {"type": "text", "label": "Новый вопрос"},
              "color": "primary"}],
            [{"action":
              {"type": "text", "label": "Сдаться"},
              "color": "default"}],
            [{"action":
              {"type": "text", "label": "Мой счет"},
              "color": "default"}]
              ]
    }

    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 1_000_000),
        keyboard=json.dumps(keyboard, ensure_ascii=False))


def handle_message(event, vk, redis_conn, questions):
    user_id = str(event.user_id)
    text = event.text.strip()

    if text.lower() == "старт":
        send_keyboard(
            vk, user_id,
            "Привет! Я — бот-викторина.\n"
            "Нажми «Новый вопрос», чтобы начать игру.\n"
            "Если не знаешь ответ — нажми «Сдаться».\n"
            "Команда «Мой счет» пока не реализована."
        )
        return

    if text == "Новый вопрос":
        question = random.choice(list(questions.keys()))
        redis_conn.set(user_id, question)
        send_keyboard(vk, user_id, question)

    elif text == "Сдаться":
        question = redis_conn.get(user_id)
        if question:
            answer = questions.get(question)
            vk.messages.send(
                user_id=user_id,
                message=f"Правильный ответ: {answer}",
                random_id=random.randint(1, 1e9)
                )
        new_question = random.choice(list(questions.keys()))
        redis_conn.set(user_id, new_question)
        send_keyboard(vk, user_id, new_question)

    elif text == "Мой счет":
        vk.messages.send(
            user_id=user_id,
            message="Пока счёт не реализован :)",
            random_id=random.randint(1, 1e9)
        )

    else:
        question = redis_conn.get(user_id)
        if not question:
            vk.messages.send(
                user_id=user_id,
                message="Сначала нажмите «Новый вопрос»",
                random_id=random.randint(1, 1e9)
                )
            return

        correct_answer = questions.get(question)
        cleaned_correct = correct_answer.split('.')[0].split('(')[0].strip().lower()

        if text.lower() in cleaned_correct:
            vk.messages.send(
                user_id=user_id,
                message='''Правильно! Поздравляю!\n \
                "Нажми «Новый вопрос» для следующего.''',
                random_id=random.randint(1, 1e9)
            )
            redis_conn.delete(user_id)
        else:
            vk.messages.send(
                user_id=user_id,
                message="Неправильно… Попробуешь ещё раз?",
                random_id=random.randint(1, 1e9)
                )


if __name__ == "__main__":
    
    redis_conn = redis.StrictRedis(
        host=os.environ["REDIS_HOST"],
        port=19137,
        password=os.environ["REDIS_PASSWORD"],
        decode_responses=True
    )
    questions = load_all_questions(os.environ["PATH_TO_QUESTIONS"])

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )

    vk_token = os.environ["VK_API_KEY"]
    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    handler_new_message = partial(
        handle_message,
        redis_conn=redis_conn,
        questions=questions
        )
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handler_new_message(event, vk)
