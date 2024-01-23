import json
import time
from datetime import datetime, timedelta

import pytz

fichier_config = "Config.json"#"RaspBerry/Config.json"


def read_config():
    with open(fichier_config, 'r') as fichier:
        json_data = fichier.read()
    return json.loads(json_data)


def get_creneaux():
    return read_config()[0]["creneaux"]


def get_sampling():
    return read_config()[0]["sampling"]


def get_horaires(creneau):
    return [creneau["heureDebut"],creneau["heureFin"]]


def get_jour(creneau):
    return creneau["jour"]


def get_id():
    return read_config()[0]["id"]


def get_type():
    return read_config()[0]["type"]


def get_config():
    return read_config()[0]["config"]


def update_config(json_data):
    with open(fichier_config, 'w') as fichier:
        fichier.write(json.dumps(json_data, indent=2))


def reboot():
    boot_config = [
        {
            "config": "boot",
            "id": 155,
            "type": "",
            "creneaux": [
                {
                    "heureDebut": "",
                    "heureFin": "",
                    "jour": ""
                }
            ]
        }
    ]

    update_config(boot_config)


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

def get_actual_date():
    timestamp_actuel = time.time()

    # Convertir le timestamp en objet datetime (fuseau horaire UTC)
    timestamp_actuel_utc = datetime.utcfromtimestamp(timestamp_actuel)

    # Ajouter le fuseau horaire de Paris
    paris_timezone = pytz.timezone('Europe/Paris')
    timestamp_actuel_paris = timestamp_actuel_utc.replace(tzinfo=pytz.utc).astimezone(paris_timezone)

    # Formater le timestamp actuel en ISO 8601 avec le fuseau horaire de Paris
    timestamp_actuel_iso_paris = timestamp_actuel_paris.isoformat()

    return timestamp_actuel_iso_paris
