import requests
import json
import sqlite3
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
import os

# Configuration
DATABASE_PATH = "language_exercises.db"
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"

# Initialisation de Rich
console = Console()

class LanguageExerciseDB:
    def __init__(self):
        self.init_database()

    def init_database(self):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    language TEXT,
                    level TEXT,
                    exercise_type TEXT,
                    content TEXT,
                    correct_answers TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exercise_id INTEGER,
                    response TEXT,
                    score REAL,
                    date TEXT,
                    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
                )
            ''')

    def save_exercise(self, language, level, exercise_type, content, correct_answers):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO exercises (date, language, level, exercise_type, content, correct_answers)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), language, level, exercise_type, content, correct_answers))
            return cursor.lastrowid

    def save_user_response(self, exercise_id, response, score):
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_responses (exercise_id, response, score, date)
                VALUES (?, ?, ?, ?)
            ''', (exercise_id, json.dumps(response), score, datetime.now().isoformat()))

class ExerciseGenerator:
    def __init__(self):
        self.db = LanguageExerciseDB()

    def generate_prompt(self, language, exercise_type, level):
       return f"""
    Generate a {level} level {exercise_type} exercise in {language}.
    
    For a vocabulary exercise in English, focus on:
    - Specific vocabulary fields (business, nature, technology, etc.)
    - Context-based usage
    - Clear hints with definitions or synonyms
    
    Format required:
    1. One gap per sentence marked with _____ (underscores matching word length)
    2. Clear hint in parentheses
    3. All sentences must be in English
    4. Focus only on vocabulary (no grammar or conjugation)
    
    Example format:
    1. The _______ (large sea mammal with grey skin) swam gracefully in the ocean.
    2. Scientists use a ________ (optical instrument for viewing distant objects) to study stars.
    3. The company's _______ (person responsible for financial decisions - CFO) presented the annual report.
    4. She bought a new ________ (portable computing device) for her studies.
    
    Answers:
    1. dolphin
    2. telescope
    3. treasurer
    4. laptop
    
    IMPORTANT:
    - All sentences must be in English
    - Focus only on vocabulary appropriate for {level} level
    - Provide clear, unambiguous hints
    - One correct answer per gap
    - Number of underscores should match the length of the answer
    """

    def generate_exercise(self, language, exercise_type, level):
        try:
            prompt = self.generate_prompt(language, exercise_type, level)
            
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": "qwen2",
                    "messages": [
                        {"role": "system", "content": "Vous êtes un professeur de langues expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if not response.ok:
                console.print("[red]Erreur de communication avec Ollama[/red]")
                return None
            
            content = response.json()['choices'][0]['message']['content']
            exercise_content, answers = self.parse_exercise_response(content)
            
            if not exercise_content or not answers:
                console.print("[red]Erreur dans le format de réponse d'Ollama[/red]")
                return None
            
            exercise_id = self.db.save_exercise(
                language=language,
                level=level,
                exercise_type=exercise_type,
                content=exercise_content,
                correct_answers=json.dumps(answers)
            )
            
            return {
                'id': exercise_id,
                'content': exercise_content,
                'answers': answers
            }
            
        except Exception as e:
            console.print(f"[red]Erreur lors de la génération de l'exercice: {str(e)}[/red]")
            return None

    def parse_exercise_response(self, content):
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
            console.print(f"[red]Erreur lors du parsing de la réponse: {str(e)}[/red]")
            return None, None

class ExerciseUI:
    def __init__(self):
        self.console = Console()
        self.generator = ExerciseGenerator()

    def display_welcome(self):
        self.console.print(Panel.fit(
            "[bold blue]Bienvenue dans l'Assistant d'Apprentissage des Langues[/bold blue]\n"
            "[italic]Un outil interactif pour améliorer vos compétences linguistiques[/italic]",
            border_style="blue"
        ))

    def display_exercise(self, content, answers):
        self.console.print("\n[bold green]Exercice:[/bold green]")
        self.console.print(Panel(content, border_style="green"))
        
        user_responses = {}
        for i, line in enumerate(content.split('\n'), 1):
            if '_____' in line:
                self.console.print(f"\n[cyan]Phrase {i}:[/cyan]")
                self.console.print(line)
                response = Prompt.ask(f"Votre réponse")
                user_responses[str(i)] = response
                self.console.print()  # Ligne vide pour la lisibilité
        return user_responses

    def show_results(self, user_responses, correct_answers, score):
        table = Table(title="[bold]Résultats de l'exercice[/bold]")
        table.add_column("N°", style="cyan", justify="center")
        table.add_column("Phrase", style="blue")
        table.add_column("Votre réponse", style="yellow")
        table.add_column("Réponse correcte", style="green")
        table.add_column("Résultat", justify="center")

        for q_num, user_answer in user_responses.items():
            correct = correct_answers.get(q_num, "")
            is_correct = user_answer.lower().strip() == correct.lower().strip()
            result = "✓" if is_correct else "✗"
            result_style = "green" if is_correct else "red"
            
            table.add_row(
                q_num,
                f"Phrase {q_num}",
                user_answer,
                correct,
                f"[{result_style}]{result}[/{result_style}]"
            )

        self.console.print(table)
        self.console.print(f"\n[bold]Score final: {score:.1f}%[/bold]")

def calculate_score(user_responses, correct_answers):
    if not correct_answers:
        return 0
    correct = sum(1 for k, v in user_responses.items() 
                 if v.lower() == correct_answers.get(k, "").lower())
    return (correct / len(correct_answers)) * 100

def main():
    ui = ExerciseUI()
    ui.display_welcome()

    while True:
        language = Prompt.ask(
            "Choisissez une langue",
            choices=["français", "anglais", "espagnol", "allemand"]
        )
        
        level = Prompt.ask(
            "Choisissez un niveau",
            choices=["débutant", "intermédiaire", "avancé"]
        )
        
        exercise_type = Prompt.ask(
            "Choisissez un type d'exercice",
            choices=["grammaire", "vocabulaire", "conjugaison", "expressions"]
        )
        
        result = ui.generator.generate_exercise(language, level, exercise_type)
        
        if result is None:
            console.print("[red]Impossible de générer l'exercice. Voulez-vous réessayer?[/red]")
            if not Prompt.ask("Réessayer?", choices=["oui", "non"]) == "oui":
                break
            continue
        
        user_responses = ui.display_exercise(result['content'], result['answers'])
        score = calculate_score(user_responses, result['answers'])
        ui.generator.db.save_user_response(result['id'], user_responses, score)
        ui.show_results(user_responses, result['answers'], score)
        
        if not Prompt.ask("\nVoulez-vous faire un autre exercice?", choices=["oui", "non"]) == "oui":
            break

    ui.console.print("[bold blue]Merci d'avoir utilisé l'Assistant d'Apprentissage des Langues![/bold blue]")

if __name__ == "__main__":
    main()