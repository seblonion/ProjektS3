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

    def generate_vocabulary_prompt(self, language, level):
        level_specific_vocab = {
            "débutant": "objets quotidiens, couleurs, nombres, famille",
            "intermédiaire": "travail, loisirs, voyages, actualités",
            "avancé": "politique, économie, sciences, littérature"
        }
        
        vocab_themes = level_specific_vocab.get(level.lower(), level_specific_vocab["débutant"])
        
        return f"""
Générez un exercice de vocabulaire de niveau {level} en {language}.
Utilisez du vocabulaire sur les thèmes suivants : {vocab_themes}

Format requis :
1. Un espace par phrase marqué par _____ (soulignements correspondant à la longueur du mot)
2. Indice clair entre parenthèses
3. Toutes les phrases doivent être strictement en {language}

Exemple de format :
1. Le _______ (grand mammifère marin à peau grise) nageait gracieusement dans l'océan.
2. Les scientifiques utilisent un ________ (instrument optique pour observer les objets lointains) pour étudier les étoiles.

Réponses :
1. dauphin
2. télescope

IMPORTANT :
- Adaptez le vocabulaire au niveau {level}
- Donnez des indices clairs et sans ambiguïté
- Une réponse correcte par espace
- Le nombre de traits de soulignement doit correspondre à la longueur de la réponse
- Générez exactement 4 questions
"""

    def generate_grammar_prompt(self, language, level):
        grammar_points = {
            "débutant": "articles (le, la, les), prépositions simples (à, de, dans), accord simple adjectifs",
            "intermédiaire": "pronoms relatifs (qui, que, dont), temps simples, comparatifs",
            "avancé": "subjonctif, concordance des temps, pronoms complexes"
        }
        
        points = grammar_points.get(level.lower(), grammar_points["débutant"])
        
        return f"""
Générez un exercice de grammaire de niveau {level} en {language}.
Points grammaticaux à couvrir : {points}

Format requis :
1. Phrases à compléter avec un choix multiple entre parenthèses
2. Soulignez l'emplacement de la réponse avec _____
3. Toutes les phrases doivent être en {language}

Exemple de format :
1. Il _____ (a/est/à) allé au magasin hier.
2. Les enfants _____ (qui/que/dont) jouent dans le parc sont mes voisins.

Réponses :
1. est
2. qui

IMPORTANT :
- Adaptez la difficulté grammaticale au niveau {level}
- Donnez 3 options par question
- Les options doivent être clairement séparées par des /
- Générez exactement 4 questions
"""

    def generate_conjugation_prompt(self, language, level):
        tenses = {
            "débutant": "présent, futur proche",
            "intermédiaire": "passé composé, imparfait, futur simple",
            "avancé": "plus-que-parfait, subjonctif présent, conditionnel"
        }
        
        level_tenses = tenses.get(level.lower(), tenses["débutant"])
        
        return f"""
Générez un exercice de conjugaison de niveau {level} en {language}.
Temps à utiliser : {level_tenses}

Format requis :
1. Verbe à l'infinitif entre parenthèses et le temps demandé
2. Espace à remplir marqué par _____
3. Toutes les phrases doivent être en strictement en {language}

Exemple de format :
1. Je _____ (partir - présent) en vacances demain.
2. Hier, ils _____ (finir - passé composé) leur travail tôt.

Réponses :
1. pars
2. ont fini

IMPORTANT :
- Utilisez uniquement les temps correspondant au niveau {level}
- Spécifiez clairement le temps demandé entre parenthèses
- Générez exactement 4 questions
"""

    def generate_expressions_prompt(self, language, level):
        expression_types = {
            "débutant": "expressions très courantes et simples",
            "intermédiaire": "expressions usuelles avec contexte simple",
            "avancé": "expressions idiomatiques complexes et nuancées"
        }
        
        type_expr = expression_types.get(level.lower(), expression_types["débutant"])
        
        return f"""
Générez un exercice sur les expressions de niveau {level} en {language}.
Type d'expressions : {type_expr}

Format requis :
1. Expression à compléter avec _____ pour le mot manquant
2. Contexte et signification entre parenthèses
3. Toutes les phrases doivent être strictement en {language}
Exemple de format :
1. Avoir le _____ à l'envers. (sentiment de malaise - mot manquant décrit un organe)
2. Mettre les _____ dans le plat. (parler franchement - mot manquant décrit une partie du corps)

Réponses :
1. cœur
2. pieds

IMPORTANT :
- Adaptez les expressions au niveau {level}
- Fournissez un contexte clair et une explication
- Générez exactement 4 questions
"""

    def generate_prompt(self, language, exercise_type, level):
        prompt_generators = {
            "vocabulaire": self.generate_vocabulary_prompt,
            "grammaire": self.generate_grammar_prompt,
            "conjugaison": self.generate_conjugation_prompt,
            "expressions": self.generate_expressions_prompt
        }
        
        generator = prompt_generators.get(exercise_type.lower())
        if not generator:
            raise ValueError(f"Type d'exercice non supporté: {exercise_type}")
        
        return generator(language, level)

    def generate_exercise(self, language, exercise_type, level):
        try:
            # Générer le prompt approprié
            prompt = self.generate_prompt(language, exercise_type, level)
            
            # Vérifier que tous les paramètres sont valides
            if not all([language, exercise_type, level]):
                raise ValueError("Tous les paramètres doivent être spécifiés")
            
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
                    
                if line.lower().startswith('réponses'):
                    parsing_exercise = False
                elif parsing_exercise and '_____' in line:
                    if not line.startswith(str(current_question)):
                        line = f"{current_question}. {line}"
                    exercise_lines.append(line)
                    current_question += 1
                elif not parsing_exercise and line[0].isdigit():
                    try:
                        num, answer = line.split('.', 1)
                        answers[num.strip()] = answer.strip()
                    except ValueError:
                        continue
            
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
                self.console.print(f"\n[cyan]Question {i}:[/cyan]")
                self.console.print(line)
                response = Prompt.ask(f"Votre réponse")
                user_responses[str(i)] = response
        return user_responses

    def show_results(self, user_responses, correct_answers, score):
        table = Table(title="[bold]Résultats de l'exercice[/bold]")
        table.add_column("N°", style="cyan", justify="center")
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
                 if v.lower().strip() == correct_answers.get(k, "").lower().strip())
    return (correct / len(correct_answers)) * 100



def main():
    ui = ExerciseUI()
    ui.display_welcome()

    while True:
        # Demander d'abord la langue
        language = Prompt.ask(
            "Choisissez une langue",
            choices=["français", "anglais", "espagnol", "allemand"]
        ).lower()
        
        # Demander ensuite le type d'exercice
        exercise_type = Prompt.ask(
            "Choisissez un type d'exercice",
            choices=["grammaire", "vocabulaire", "conjugaison", "expressions"]
        ).lower()
        
        # Demander enfin le niveau
        level = Prompt.ask(
            "Choisissez un niveau",
            choices=["débutant", "intermédiaire", "avancé"]
        ).lower()
        
        # Générer l'exercice avec les paramètres dans le bon ordre
        result = ui.generator.generate_exercise(
            language=language,
            exercise_type=exercise_type,
            level=level
        )
        
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




