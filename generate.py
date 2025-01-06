import re

import eel

from exercise import insert_exercise
from language import insert_language
from lesson import insert_lesson
from ollama import ask
from prompts import generate_prompt
from sentence import insert_sentence
from topic import insert_topic


@eel.expose
def generate_from_language(language):
    datas = {
        "topics": [
            {
                "name": "Vocabulary",
                "exercises": ["Beginner", "Intermediate", "Advanced"],
                "lesson": "Not implemented"
            },
            {
                "name": "Grammar",
                "exercises": ["Beginner", "Intermediate", "Advanced"],
                "lesson": "Not implemented"
            },
            {
                "name": "Conjugation",
                "exercises": ["Beginner", "Intermediate", "Advanced"],
                "lesson": "Not implemented"
            },
            {
                "name": "Expressions",
                "exercises": ["Beginner", "Intermediate", "Advanced"],
                "lesson": "Not implemented"
            }
        ]
    }

    language_id = insert_language(language)

    for i, e in enumerate(datas["topics"]):
        topic_id = insert_topic(e["name"], language_id)
        insert_lesson(e["lesson"], topic_id)
        for j, f in enumerate(e["exercises"]):
            exercise_id = insert_exercise(f, topic_id, j + 1)
            generate_sentences_of_exercise(exercise_id, language, e["name"], f)


@eel.expose
def generate_sentences_of_exercise(exercise_id, language, exercise_type, level):
    prompt = generate_prompt(language, exercise_type, level)
    content_gen = ask(prompt, "fast")
    try:
        sentences = parse_text_to_sentences(content_gen)

        for s in sentences:
            insert_sentence(s["content"], s["answer"], exercise_id)

    except Exception as e:  # Capturer toute exception venant de 'try'
        insert_sentence("error while generating, answer is 'error' to unlock the next", "error", exercise_id)
        print(f"An error occurred: {e}")


def parse_text_to_sentences(text):
    sentences = []

    # Divise le texte en deux parties : questions et réponses
    parts = text.split("Answers:")
    questions_part = parts[0].strip()
    answers_part = parts[1].strip()

    # Utilise une regex pour extraire uniquement les lignes qui commencent par un numéro
    questions = [q.strip() for q in questions_part.split("\n") if re.match(r"^\d+\.", q.strip())]
    answers = [a.strip() for a in answers_part.split("\n") if re.match(r"^\d+\.", a.strip())]

    # Création de la liste de dictionnaires
    for question, answer in zip(questions, answers):
        # Nettoie la réponse après le numéro et le point
        sentences.append({
            "content": question,
            "answer": answer.split(". ", 1)[-1]  # Extrait tout après "x. "
        })

    return sentences
