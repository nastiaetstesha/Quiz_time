import os


def load_all_questions(folder_path, encoding='KOI8-R'):
    all_questions = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, 'r', encoding=encoding) as file:
                content = file.read()

            sections = content.split('\n\n')
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
                    all_questions[question_text] = answer_text

    return all_questions
