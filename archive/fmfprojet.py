import requests
import json

def generer_exercice_ollama(langue, type_exercice, niveau="débutant"):
    """
    Fonction pour générer un exercice via Ollama avec un prompt amélioré.
    """
    url = "http://localhost:11434/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
    }

    # Prompt amélioré avec plus de structure et de contraintes
    prompt = f"""En tant que professeur de {langue}, générez un exercice structuré comme suit:

1. CONSIGNE (en français):
- Écrivez une consigne claire et concise
- Maximum 2 phrases

2. EXERCICE (en {langue} uniquement):
- Type: {type_exercice}
- Niveau: {niveau}
- Format: 3-4 questions/phrases à compléter
- L'exercice doit être approprié pour le niveau indiqué
- Utilisez uniquement la langue cible ({langue})

Pour un exercice de grammaire, concentrez-vous sur une seule règle grammaticale.
Pour un exercice de vocabulaire, restez dans un seul champ lexical.
"""

    data = {
        "model": "qwen2",
        "messages": [
            {"role": "system", "content": "Vous êtes un professeur de langues expérimenté."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7  # Ajout d'un paramètre de température pour plus de contrôle
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion à Ollama : {str(e)}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"Erreur dans la réponse d'Ollama : {str(e)}"

def corriger_exercice_ollama(langue, reponse_utilisateur, exercice):
    """
    Fonction améliorée pour corriger l'exercice via Ollama.
    """
    url = "http://localhost:11434/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
    }

    prompt = f"""En tant que professeur de {langue}, corrigez la réponse suivante:

EXERCICE ORIGINAL:
{exercice}

RÉPONSE DE L'ÉLÈVE:
{reponse_utilisateur}

FORMAT DE CORRECTION DEMANDÉ:
1. Évaluation générale (1-2 phrases)
2. Corrections spécifiques (point par point)
3. Version corrigée
4. Conseils d'amélioration

Répondez en français."""

    data = {
        "model": "qwen2",
        "messages": [
            {"role": "system", "content": "Vous êtes un professeur de langues expérimenté."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3  # Température plus basse pour la correction
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion à Ollama : {str(e)}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"Erreur dans la réponse d'Ollama : {str(e)}"

def main():
    print("Bienvenue dans le générateur d'exercices linguistiques !")
    
    # Ajout de la gestion des langues supportées
    langues_supportees = ["anglais", "espagnol", "allemand", "italien", "polonais"]
    print(f"\nLangues disponibles : {', '.join(langues_supportees)}")
    
    while True:
        langue = input("\nQuelle langue voulez-vous apprendre ? : ").strip().lower()
        if langue in langues_supportees:
            break
        print(f"Désolé, cette langue n'est pas disponible. Veuillez choisir parmi : {', '.join(langues_supportees)}")

    # Ajout du niveau
    niveaux = ["débutant", "intermédiaire", "avancé"]
    print("\nNiveaux disponibles :")
    for i, niveau in enumerate(niveaux, 1):
        print(f"{i}. {niveau.capitalize()}")
    
    while True:
        choix_niveau = input("Choisissez votre niveau (1-3) : ").strip()
        if choix_niveau.isdigit() and 1 <= int(choix_niveau) <= 3:
            niveau = niveaux[int(choix_niveau) - 1]
            break
        print("Veuillez entrer un nombre entre 1 et 3.")

    print("\nTypes d'exercices disponibles :")
    print("1. Grammaire")
    print("2. Vocabulaire")
    print("3. Grammaire et Vocabulaire")

    while True:
        choix_type = input("Entrez le numéro correspondant à votre choix : ").strip()
        if choix_type in ["1", "2", "3"]:
            type_exercice = {
                "1": "grammaire",
                "2": "vocabulaire",
                "3": "grammaire et vocabulaire"
            }[choix_type]
            break
        print("Veuillez entrer un nombre entre 1 et 3.")

    # Génération des exercices avec gestion des erreurs
    print("\nGénération des exercices en cours...")
    exercices = []
    for i in range(3):
        print(f"Génération de l'exercice {i+1}...")
        exercice = generer_exercice_ollama(langue, type_exercice, niveau)
        if not exercice.startswith("Erreur"):
            exercices.append(exercice)
        else:
            print(f"⚠️ {exercice}")

    if not exercices:
        print("\nDésolé, impossible de générer des exercices. Veuillez vérifier que le service Ollama est bien lancé.")
        return

    # Affichage des exercices
    for i, exercice in enumerate(exercices, 1):
        print(f"\n{'='*50}")
        print(f"Exercice {i} :")
        print(exercice)
        print(f"{'='*50}")

    # Boucle de correction
    while True:
        action = input("\nAvez-vous terminé les exercices ? (oui/non) : ").strip().lower()
        if action == "oui":
            for i, exercice in enumerate(exercices, 1):
                print(f"\n--- Exercice {i} ---")
                print(exercice)
                reponse = input(f"\nVotre réponse pour l'exercice {i} : ").strip()
                correction = corriger_exercice_ollama(langue, reponse, exercice)
                print(f"\nCORRECTION :")
                print(correction)
            break
        elif action == "non":
            print("Prenez votre temps pour compléter les exercices.")
        else:
            print("Veuillez répondre par 'oui' ou 'non'.")

if __name__ == "__main__":
    main()