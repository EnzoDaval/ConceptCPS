import json
import time
from collections import Counter
from datetime import datetime, timedelta

import pytz

fichier_config = "DataProcessing/Res/Hyperplanning.json"


def _get_info_cours(numero_cours):
    try:
        with open(fichier_config, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for cours in data:
            if cours['numeroDuCours'] == numero_cours:
                return cours

    except FileNotFoundError:
        print("Le fichier n'a pas été trouvé.")
        return None
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier JSON.")
        return None

    return None


'''
Retourne tous les objets 'horaire' d'un cours
'''


def get_creneaux(numero_cours):
    cours = _get_info_cours(numero_cours)
    return [horaires for horaires in cours.get('creneaux', [])]


'''
Retourne uniquement les objets heureDebut et heureFin d'un objet creneau donné
'''


def get_horaires(creneau):
    total_horaires = []
    # for horaires in creneau:
    # total_horaires += [[horaires.get('heureDebut'), horaires.get('heureFin')]]

    return [creneau.get('heureDebut'), creneau.get('heureFin')]


'''
Recupère l'objet 'jour' d'un objet 'horaires' donné
'''


def get_reference_day(creneau):
    return creneau.get("jour", [])


"""
Retourne la salle du creneau donné
"""


def get_salle(creneau):
    return creneau.get("salle", [])


"""
Retourne la liste des élèves censé être présents au creneau donné
"""


def get_eleves(creneau):
    return creneau.get("eleves", [])


'''
Retourne le timestamp donné à la bonne date
'''


def replace_date_with_reference_day(timestamp, reference_day):
    # Convertir le timestamp en objet datetime
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Trouver le jour actuel de la semaine (0 pour lundi, 1 pour mardi, ..., 6 pour dimanche)
    current_weekday = dt.weekday()

    # Trouver le jour de la semaine pour la référence
    reference_weekday = {'Lundi': 0, 'Mardi': 1, 'Mercredi': 2, 'Jeudi': 3, 'Vendredi': 4, 'Samedi': 5,
                         'Dimanche': 6}.get(reference_day)

    if reference_weekday is None:
        raise ValueError("Jour de référence invalide")

    # Calculer le nombre de jours à soustraire pour atteindre le dernier jour de la semaine
    days_to_subtract = ((current_weekday - reference_weekday) % 7) - 7

    # Soustraire le nombre de jours nécessaire
    last_day_of_week = dt - timedelta(days=days_to_subtract)

    # Formater le résultat en chaîne de caractères
    result = last_day_of_week.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return result



def trouver_eleve_par_wifi(adresse_mac_wifi, chemin_fichier='DataProcessing/Res/Eleves.json'):
    try:
        with open(chemin_fichier, 'r') as fichier:
            eleves = json.load(fichier)
            for eleve in eleves:
                if eleve['Adresse_MAC_Wifi'].lower() == adresse_mac_wifi.lower():
                    return eleve['Prenom'], eleve['Nom']
    except FileNotFoundError:
        print("Fichier non trouvé.")
    except json.JSONDecodeError:
        print("Erreur de formatage du fichier JSON.")

    return None


def trouver_eleve_par_bluetooth(adresse_mac_bluetooth, chemin_fichier='DataProcessing/Res/Eleves.json'):
    try:
        with open(chemin_fichier, 'r') as fichier:
            eleves = json.load(fichier)
            for eleve in eleves:
                if eleve['Adresse_MAC_Bluetooth'].lower() == adresse_mac_bluetooth.lower():
                    return eleve['Prenom'], eleve['Nom']
    except FileNotFoundError:
        print("Fichier non trouvé.")
    except json.JSONDecodeError:
        print("Erreur de formatage du fichier JSON.")


def get_type_dispositif(id, chemin_fichier='DataProcessing/Res/Dispositifs.json'):
    try:
        with open(chemin_fichier, 'r') as fichier:
            dispositifs = json.load(fichier)
            for dispositif in dispositifs:
                if dispositif['id'] == id:
                    return dispositif['type_dispositif']
    except FileNotFoundError:
        print("Fichier non trouvé.")
    except json.JSONDecodeError:
        print("Erreur de formatage du fichier JSON.")


def get_salle_dispositif(id, chemin_fichier='DataProcessing/Res/Dispositifs.json'):
    try:
        with open(chemin_fichier, 'r') as fichier:
            dispositifs = json.load(fichier)
            for dispositif in dispositifs:
                if dispositif['id'] == id:
                    return dispositif['salle']
    except FileNotFoundError:
        print("Fichier non trouvé.")
    except json.JSONDecodeError:
        print("Erreur de formatage du fichier JSON.")


"""
Retourne tous les dispositifs d'une salle donnée
"""
def get_dispositif_salle(salle_recherche,nom_fichier_json="Dataprocessing/Res/Dispositifs.json"):
    resultats = []

    with open(nom_fichier_json, 'r') as fichier:
        data = json.load(fichier)

        for dispositif in data:
            if dispositif["salle"] == salle_recherche:
                resultats.append(dispositif["id"])

    return resultats

def get_number_of_samples(horaire_debut,horaire_fin,type_dispositif):
    from DataProcessing.main import WIFI_SAMPLES,BLUETOOTH_SAMPLES
    sampling = None
    if type_dispositif == 'Bluetooth': sampling = BLUETOOTH_SAMPLES
    else: sampling = WIFI_SAMPLES

    heure1_obj = datetime.fromisoformat(horaire_debut.rstrip("Z"))
    heure2_obj = datetime.fromisoformat(horaire_fin.rstrip("Z"))

    # Calcul de la différence en minutes
    difference_en_minutes = (heure2_obj - heure1_obj).total_seconds() / 60

    # Calcul du nombre de quarts d'heure
    quarts_d_heure = difference_en_minutes / sampling

    print(f"Il y a {quarts_d_heure} quarts d'heure entre {horaire_debut} et {horaire_fin}.")
    return quarts_d_heure


def get_number_of_detections(dict):
    compteur_timestamps_par_personne = Counter()

    # Parcourir le dictionnaire et compter les timestamps par personne
    for personne, timestamps in dict.items():
        compteur_timestamps_par_personne[personne] = len(timestamps)

    # Afficher les résultats
    for personne, nombre_timestamps in compteur_timestamps_par_personne.items():
        print(f"{personne} a {nombre_timestamps} timestamps.")

    return compteur_timestamps_par_personne.items()


# Chemin vers votre fichier JSON

# Exemple d'utilisation de la fonction
'''numero_classe_recherche = "E209"
classe_trouvee = trouver_cours(chemin_fichier_json, numero_classe_recherche)

if classe_trouvee:
    print(f"Classe trouvée : {classe_trouvee}")
else:
    print("Classe non trouvée.")'''
