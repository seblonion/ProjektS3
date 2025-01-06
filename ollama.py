import json
import time

import requests

OLLAMA_URL = "http://ollama.primault.eu:15674/v1/chat/completions"


def ask(prompt, speed):
    model = "qwen2.5:14b"
    if speed == "fast":
        model = "qwen2.5:7b"
    elif speed == "normal":
        model = "qwen2.5:14b"
    elif speed == "precise":
        model = "qwen2.5:32b"
    elif speed == "ultrafast":
        model = "qwen2.5:3b"
    elif speed == "megafast":
        model = "qwen2.5:0.5b"

    print("START REQUEST OLLAMA")

    start_time = time.time()  # Démarre le chronométrage

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert language teacher."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5
        },
        headers={"Content-Type": "application/json"},
        timeout=600
    )

    if not response.ok:
        print("[red]Erreur de communication avec Ollama[/red]")
        return None

    end_time = time.time()  # Termine le chronométrage

    elapsed_time = end_time - start_time  # Calcule le temps écoulé

    content = response.json()['choices'][0]['message']['content']
    print("CONVERSATION========")
    print("TIME========")
    print(f"Request took {elapsed_time:.2f} seconds")  # Affiche le temps écoulé
    return content


def parse_exercise_response(content):
    try:
        lines = content.split('\n')
        exercise_lines = []
        answers = {}
        parsing_exercise = True
        current_question = 1

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.lower().startswith('réponses') or line.startswith('{'):
                parsing_exercise = False
                try:
                    json_start = line.find('{')
                    if json_start != -1:
                        answers = json.loads(line[json_start:])
                except json.JSONDecodeError:
                    continue
            elif parsing_exercise:
                if '_____' in line:
                    if not line.startswith(str(current_question)):
                        line = f"{current_question}. {line}"
                    current_question += 1
                exercise_lines.append(line)

        if not answers:
            answers = {str(i): "" for i in range(1, current_question)}

        return '\n'.join(exercise_lines), answers

    except Exception as e:
        print(f"[red]Erreur lors du parsing de la réponse: {str(e)}[/red]")
        return None, None
