def generate_vocabulary_prompt(language, level):
    level_specific_vocab = {
        "beginner": "everyday objects, colors, numbers, family",
        "intermediate": "work, hobbies, travel, current events",
        "advanced": "politics, economics, science, literature"
    }

    vocab_themes = level_specific_vocab.get(level.lower(), level_specific_vocab["beginner"])

    return f"""
Generate a {level} level vocabulary exercise in {language}.
Use vocabulary on the following themes: {vocab_themes}

Required format:
1. One space per sentence marked by _____ (underscores corresponding to the length of the word)
2. Clear hint in parentheses
3. All sentences must be strictly in {language}

Example format:
1. The _______ (large marine mammal with gray skin) swam gracefully in the ocean.
2. Scientists use a ________ (optical instrument to observe distant objects) to study the stars.

Answers:
1. dolphin
2. telescope

IMPORTANT:
- Adapt the vocabulary to the {level} level
- Provide clear and unambiguous hints
- One correct answer per blank
- The number of underscores must match the length of the answer
- Generate exactly 4 questions
"""


def generate_grammar_prompt(language, level):
    grammar_points = {
        "beginner": "articles (the, a, an), simple prepositions (at, to, in), simple adjective agreement",
        "intermediate": "relative pronouns (who, that, whose), simple tenses, comparatives",
        "advanced": "subjunctive, tense agreement, complex pronouns"
    }

    points = grammar_points.get(level.lower(), grammar_points["beginner"])

    return f"""
Generate a {level} level grammar exercise in {language}.
Grammar points to cover: {points}

Required format:
1. Sentences to be completed with multiple-choice options in parentheses
2. Underline the space for the answer with _____
3. All sentences must be in {language}

Example format:
1. He _____ (has/is/at) gone to the store yesterday.
2. The children _____ (who/that/whose) are playing in the park are my neighbors.
Answers:
1. is
2. who

IMPORTANT:
- Adapt the grammatical difficulty to the {level} level
- Provide 3 options per question
- Options must be clearly separated by /
- Generate exactly 4 questions
- Don't forget to generate answers in {language}
"""


def generate_conjugation_prompt(language, level):
    tenses = {
        "beginner": "present, near future",
        "intermediate": "past perfect, imperfect, simple future",
        "advanced": "pluperfect, present subjunctive, conditional"
    }

    level_tenses = tenses.get(level.lower(), tenses["beginner"])

    return f"""
Generate a {level} level conjugation exercise in {language}.
Tenses to use: {level_tenses}

Required format:
1. Verb in the infinitive in parentheses with the requested tense
2. Blank space marked by _____
3. All sentences must be strictly in {language}

Example format:
1. I _____ (to leave - present) for vacation tomorrow.
2. Yesterday, they _____ (to finish - past perfect) their work early.
Answers:
1. leave
2. finished

IMPORTANT:
- Use only tenses corresponding to the {level} level (or tenses which are similar)
- Clearly specify the requested tense in parentheses
- Generate exactly 4 questions
- Don't forget to generate answers in {language}
"""


def generate_expressions_prompt(language, level):
    expression_types = {
        "beginner": "very common and simple expressions",
        "intermediate": "everyday expressions with simple context",
        "advanced": "complex and nuanced idiomatic expressions"
    }

    type_expr = expression_types.get(level.lower(), expression_types["beginner"])

    return f"""
Generate a {level} level expressions exercise in {language}.
Type of expressions: {type_expr}

Required format:
1. Expression to be completed with _____ for the missing word
2. Context and meaning in parentheses
3. All sentences must be strictly in {language}

Example format:
1. To have the _____ upside down. (feeling of discomfort - the missing word describes an organ)
2. To put the _____ in the dish. (to speak frankly - the missing word describes a part of the body)
Answers:
1. heart
2. feet

IMPORTANT:
- Adapt the expressions to the {level} level
- Provide clear context and an explanation
- Generate exactly 4 questions
- Don't forget to generate answers in {language}
"""


def generate_prompt(language, exercise_type, level):
    language = language.capitalize()
    level = level.lower()

    prompt_generators = {
        "vocabulary": generate_vocabulary_prompt,
        "grammar": generate_grammar_prompt,
        "conjugation": generate_conjugation_prompt,
        "expressions": generate_expressions_prompt
    }

    generator = prompt_generators.get(exercise_type.lower())
    if not generator:
        raise ValueError(f"Type d'exercice non supporté: {exercise_type}")

    return generator(language, level)
