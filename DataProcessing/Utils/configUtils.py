import json

def trouver_classe(chemin_fichier, numero_classe):
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for classe in data:
            if classe['numeroDeClasse'] == numero_classe:
                return classe

    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé.")
        return None
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier JSON.")
        return None

    return None

# Chemin vers votre fichier JSON
chemin_fichier_json = '../Res/config.json'

# Exemple d'utilisation de la fonction
numero_classe_recherche = "E209"
classe_trouvee = trouver_classe(chemin_fichier_json, numero_classe_recherche)

if classe_trouvee:
    print(f"Classe trouvée : {classe_trouvee}")
else:
    print("Classe non trouvée.")
