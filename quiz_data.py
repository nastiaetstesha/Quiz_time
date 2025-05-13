import os
import re


def load_all_questions(folder_path, encoding='KOI8-R'):
    all_questions = {}

    for filename in os.listdir(folder_path):
        if not filename.endswith('.txt'):
            continue

        full_path = os.path.join(folder_path, filename)
        with open(full_path, 'r', encoding=encoding) as file:
            content = file.read()

        pattern = re.compile(
            r'Вопрос\s*\d*:?\s*([\s\S]*?)\nОтвет\s*:?\s*([\s\S]*?)(?=\n(?:Зачет|Комментарий|Источник|Автор|Вопрос|\Z))',
            re.IGNORECASE
        )

        matches = pattern.findall(content)

        for question_raw, answer_raw in matches:
            question = clean_text(question_raw)
            answer = clean_text(answer_raw.split('.')[0])

            if question and answer:
                all_questions[question] = answer

    return all_questions


def clean_text(text):
    text = re.sub(r'\(pic:[^)]+\)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
