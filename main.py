import importlib

import eel

import db
import exercise
import generate
import language
import lesson
import sentence
import topic

# Avoid code style removing imports
i = 3
if i % 2 == 0:
    importlib.reload(db)
    importlib.reload(exercise)
    importlib.reload(generate)
    importlib.reload(language)
    importlib.reload(lesson)
    importlib.reload(sentence)
    importlib.reload(topic)

db.initialize_database()

eel.init('web')
eel.start('main.html')
