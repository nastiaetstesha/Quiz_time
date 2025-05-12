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

        # print(f'📄 Читаем: {filename}')

        pattern = re.compile(
            r'Вопрос\s*\d*:?\s*([\s\S]*?)\nОтвет\s*:?\s*([\s\S]*?)(?=\n(?:Зачет|Комментарий|Источник|Автор|Вопрос|\Z))',
            re.IGNORECASE
        )

        matches = pattern.findall(content)
        # print(f'   Найдено вопросов: {len(matches)}')

        for question_raw, answer_raw in matches:
            question = clean_text(question_raw)
            answer = clean_text(answer_raw.split('.')[0])  # ответ до первой точки

            if question and answer:
                all_questions[question] = answer
                # print(f"✔ Вопрос: {question[:50]}... → Ответ: {answer[:30]}")

        # print(f'✅ Загружено вопросов: {len(all_questions)}\n')

    return all_questions


def clean_text(text):
    text = re.sub(r'\(pic:[^)]+\)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# def extract_following_lines(text, start_pattern, stopwords=None):
#     """Вспомогательная функция: достаёт строки после ключевого слова, пока не наткнётся на стоп-слово."""
#     lines = text.strip().split('\n')
#     start_idx = None
#     result_lines = []
#     stopwords = stopwords or []

#     for i, line in enumerate(lines):
#         if re.match(start_pattern, line, flags=re.IGNORECASE):
#             start_idx = i + 1
#             break

#     if start_idx is not None:
#         for line in lines[start_idx:]:
#             if any(sw.lower() in line.lower() for sw in stopwords):
#                 break
#             result_lines.append(line.strip())

#     return ' '.join(result_lines).strip()
