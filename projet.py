import requests # type: ignore
import json
import sys
import time
def generer_exercice(langue_cible, type_exercice, domaine="vocabulaire"):
    url = "http://localhost:11434/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
    }
    
    if type_exercice == "traduction":
        prompt = (f"Crée un exercice de traduction pour pratiquer le {domaine} en {langue_cible}. "
                  f"L'utilisateur doit traduire cette phrase en {langue_cible} : 'Comment ça va ?'")
    elif type_exercice == "completions":
        prompt = (f"Crée un exercice de complétion de phrase pour pratiquer le {domaine} en {langue_cible}. "
                  f"Complétez la phrase suivante : 'I ___ a book.' (Choix : read, reads, reading)")
    elif type_exercice == "choix_multiples":
        prompt = (f"Crée un exercice de choix multiples pour pratiquer le {domaine} en {langue_cible}. "
                  f"Quelle est la traduction correcte de 'chien' en {langue_cible} ? Choix : [dog, cat, house].")
    elif type_exercice == "texte_a_trous":
        prompt = (f"Crée un exercice de texte à trous pour enseigner le {domaine} en {langue_cible}. "
                  f"Exemple : 'La ___ (cat) joue dans la ___ (house).'")
    else:
        return "Type d'exercice non reconnu."

    data = {
        "model": "llama3",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        message = result['choices'][0]['message']['content']
        return message
    else:
        return f"Erreur lors de la génération de l'exercice : {response.status_code} - {response.text}"

langues_cibles = ["anglais", "espagnol", "polonais", "allemand"]

for langue in langues_cibles:
    print(f"\n--- Exercice pour apprendre le {langue} ---")
    
    exercice_traduction = generer_exercice(langue, "traduction", "vocabulaire")
    print("\nExercice de traduction:")
    print(exercice_traduction)
    
    exercice_completions = generer_exercice(langue, "completions", "grammaire")
    print("\nExercice de complétion de phrase:")
    print(exercice_completions)
    
    exercice_choix_multiples = generer_exercice(langue, "choix_multiples", "vocabulaire")
    print("\nExercice de choix multiples:")
    print(exercice_choix_multiples)
    
    exercice_texte_a_trous = generer_exercice(langue, "texte_a_trous", "mixte")
    print("\nExercice de texte à trous:")
    print(exercice_texte_a_trous)


def generer_cours(langue_cible, domaine="vocabulaire"):
    url = "http://localhost:11434/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
    }
    
    prompt = (f"Crée un cours complet sur le {domaine} pour apprendre le {langue_cible}. "
              f"Le cours doit inclure une introduction théorique, des règles importantes, et des exemples pratiques "
              f"adaptés aux débutants.")
    
    data = {
        "model": "llama2",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        message = result['choices'][0]['message']['content']
        return message
    else:
        return f"Erreur lors de la génération du cours : {response.status_code} - {response.text}"

langues_cibles = ["anglais", "espagnol", "polonais", "allemand"]

for langue in langues_cibles:
    print(f"\n--- Cours pour apprendre le {langue} ---")
    
    cours_vocabulaire = generer_cours(langue, "vocabulaire")
    print("\nCours sur le vocabulaire:")
    print(cours_vocabulaire)
    
    cours_grammaire = generer_cours(langue, "grammaire")
    print("\nCours sur la grammaire:")
    print(cours_grammaire)


# def barre_progression_decroissante(duree_totale):
#     increments = 100
#     intervalle = duree_totale / increments
#     progression = increments

#     print("Début du compte à rebours :")
#     while progression >= 0:
#         pourcentage = (progression / increments) * 10
#         barre = "█" * progression + " " * (increments - progression)
#         sys.stdout.write(f"\rProgression : |{barre}| {pourcentage:.2f}")
#         sys.stdout.flush()
#         time.sleep(intervalle)
#         progression -= 1

#     print("\nTemps écoulé !")

# barre_progression_decroissante(10)

