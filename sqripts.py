
import chardet

# with open('quiz-questions/1vs1200.txt', 'rb') as raw_file:
#     raw_data = raw_file.read()
#     result = chardet.detect(raw_data)
#     print(result)
#     text = raw_data.decode(result['encoding'])
#     print(text[:1000])

# encodings_to_try = ['cp1251', 'koi8-r', 'utf-8', 'iso8859_5', 'mac_cyrillic']


# with open('quiz-questions/1vs1200.txt', 'rb') as raw_file:
#     raw_data = raw_file.read()

# for encoding in encodings_to_try:
#     try:
#         print(f'\nTrying {encoding}:')
#         text = raw_data.decode(encoding)
#         print(text[:500])  # покажи только часть
#         break  # если всё читаемо — выходим
#     except UnicodeDecodeError:
#         print(f'{encoding} — decode error.')

# def print_file_contents(file_path, encoding='KOI8-R'):
#     try:
#         with open(file_path, 'r', encoding=encoding) as file:
#             content = file.read()
#             print(content)
#     except FileNotFoundError:
#         print(f'Файл не найден: {file_path}')
#     except UnicodeDecodeError:
#         print(f'Ошибка декодирования файла {file_path}. Попробуй другую кодировку.')

# print_file_contents('quiz-questions/1vs1200.txt')

def parse_quiz_file(file_path):
    with open(file_path, 'r', encoding='KOI8-R') as file:
        content = file.read()

    sections = content.split('\n\n')
    qa_pairs = {}

    for section in sections:
        lines = section.strip().split('\n')
        question_text = ''
        answer_text = ''
        for line in lines:
            if line.lower().startswith('вопрос'):
                question_text = line.partition(':')[2].strip()
            elif line.lower().startswith('ответ'):
                answer_text = line.partition(':')[2].strip()

        if question_text and answer_text:
            qa_pairs[question_text] = answer_text

    return qa_pairs


if __name__ == '__main__':
    import os

    folder_path = '/Users/egorsemin/Practice/Quiz_time/quiz-questions'
    all_questions = {}

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            print(filename)
            full_path = os.path.join(folder_path, filename)
            qa = parse_quiz_file(full_path)
            all_questions.update(qa)

    print(f'Загружено {len(all_questions)} вопросов.')

