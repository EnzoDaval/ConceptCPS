import ipaddress
import json
import socket
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
            "sampling" : 0,
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


def replace_date_with_reference_day(timestamp_past, reference_day):
    ''''# Convertir le timestamp en objet datetime
    timestamp_ref = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # Remplacez la date dans le timestamp avec la date d'aujourd'hui
    new_ref = timestamp.replace(year=today.year, month=today.month, day=today.day)

    # Affichez le nouveau timestamp
    new_ref = new_ref.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Trouver le jour actuel de la semaine (0 pour lundi, 1 pour mardi, ..., 6 pour dimanche)
    current_weekday = timestamp_ref.weekday()

    # Trouver le jour de la semaine pour la référence
    reference_weekday = {'Lundi': 0, 'Mardi': 1, 'Mercredi': 2, 'Jeudi': 3, 'Vendredi': 4, 'Samedi': 5,
                         'Dimanche': 6}.get(reference_day)

    if reference_weekday is None:
        raise ValueError("Jour de référence invalide")

    # Calculer le nombre de jours à soustraire pour atteindre le dernier jour de la semaine
    #if current_weekday != reference_weekday:
    days_to_subtract = ((current_weekday - reference_weekday) % 7) #- 7
    #else: days_to_subtract = 0

    # Soustraire le nombre de jours nécessaire
    last_day_of_week = new_ref - timedelta(days=days_to_subtract)

    # Formater le résultat en chaîne de caractères
    result = last_day_of_week.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return result'''
    # Convertissez la chaîne en objet datetime
    timestamp = datetime.strptime(timestamp_past, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Obtenez la date d'aujourd'hui
    aujourdhui = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    reference_weekday = {'Lundi': 0, 'Mardi': 1, 'Mercredi': 2, 'Jeudi': 3, 'Vendredi': 4, 'Samedi': 5,
                         'Dimanche': 6}.get(reference_day)

    # Calculez la différence de jours entre aujourd'hui et le jour de référence passé
    difference_jours = (aujourdhui.weekday() - reference_weekday) % 7

    # Si aujourd'hui est le jour de référence, retournez le timestamp initial
    if difference_jours == 0:
        return aujourdhui.replace(hour=timestamp.hour, minute=timestamp.minute,
                                  second=timestamp.second, microsecond=timestamp.microsecond)

    # Calculez la nouvelle date en ajustant la date actuelle
    nouvelle_date = aujourdhui - timedelta(days=difference_jours)

    # Créez un nouveau timestamp avec la nouvelle date et les heures du timestamp initial
    nouveau_timestamp = nouvelle_date.replace(hour=timestamp.hour, minute=timestamp.minute,
                                              second=timestamp.second, microsecond=timestamp.microsecond)

    return nouveau_timestamp

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