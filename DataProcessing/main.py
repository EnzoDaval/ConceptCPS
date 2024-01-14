# This is a sample Python script.
# Importez la classe CameraManager depuis votre module (supposons que le module s'appelle camera_manager.py)
import datetime
import json
import sys

from InfluxDB.client import get_data_in_horaire, get_horaires

#sys.path.insert(1, 'C:/Users/thoma/Documents/Devoirs/.POLY SOPHIA/S9/cyberphysique/proj/ConceptCPS/InfluxDB')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pytz
from flask import Flask, request, jsonify
# from flask_cors import CORS  # Import CORS
# from InfluxDB.client import *
from InfluxDB.dispositif import Dispositif
from InfluxDB.data import Data

NUMBER_OF_SENSORS = 2  # Bluetooth & Wifi

BLUETOOTH_SAMPLES = 15  # en minutes

WIFI_SAMPLES = 15  # en minutes

app = Flask(__name__)
# cors = CORS(app)

# Pour l'instant ça marche pas le print, j'arrive pas à installer cors pour changer lol
@app.route('/calculate', methods=['POST'])
def recevoir_notification():
    # Traitez la notification ici
    print('Notification reçue !')
    return jsonify({'message': 'Notification reçue avec succès'})
def trouver_eleve_par_wifi(adresse_mac_wifi, chemin_fichier='Res/Eleves.json'):
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

def trouver_eleve_par_bluetooth(adresse_mac_bluetooth, chemin_fichier='Res/Eleves.json'):
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


def evaluate_presence(list_mac, id_dispositif):
    current_time = datetime.utcnow()
    timezone = pytz.utc
    # influxdb_timestamp_max = pd.to_datetime((current_time + timedelta(hours=5)).strftime("'%Y-%m-%dT%H:%M:%S.%fZ'")).replace(tzinfo=timezone)
    # influxdb_timestamp_min = pd.to_datetime((current_time - timedelta(hours=5)).strftime("'%Y-%m-%dT%H:%M:%S.%fZ'")).replace(tzinfo=timezone)

    horaires = get_horaires(id_dispositif)
    horaire_debut, horaire_fin = horaires.split('_')
    horaire_debut = datetime.strptime(horaire_debut, '%Y-%m-%d %H:%M')
    horaire_fin = datetime.strptime(horaire_fin, '%Y-%m-%d %H:%M')

    dictionnaire_valeurs = {}

    for entry in list_mac:
        valeur_separee = entry['_value'].split(',')

        # Parcours de chaque valeur séparée
        for v in valeur_separee:
            # Si la clé existe déjà dans le dictionnaire, ajoutez le timestamp à la liste existante
            if v in dictionnaire_valeurs:
                dictionnaire_valeurs[v].append(entry['_time'])
            else:
                # Sinon, créez la clé et initialisez la liste avec le timestamp
                dictionnaire_valeurs[v] = [entry['_time']]

    # À la fin, dictionnaire_valeurs contient les valeurs uniques en tant que clés,
    # et chaque valeur a une liste de timestamps associés
    print(dictionnaire_valeurs)

    # Créez un tracé pour chaque valeur
    for valeur, liste_timestamps in dictionnaire_valeurs.items():
        # Triez les données par timestamp
        data_sorted = sorted(zip(liste_timestamps, [valeur] * len(liste_timestamps)), key=lambda x: x[0])

        timestamps_sorted, valeurs_sorted = zip(*data_sorted)

        # Tracez les données triées pour cette valeur spécifique
        plt.plot(timestamps_sorted, valeurs_sorted, marker='o', linestyle='-', markersize=5, label=valeur)

    # Limitez l'axe des abscisses entre les valeurs spécifiées
    plt.xlim(horaire_debut, horaire_fin)

    # Formattez l'axe des abscisses pour afficher uniquement l'heure et la minute
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Ajoutez des étiquettes et un titre
    plt.xlabel('Timestamps')
    plt.ylabel('Valeurs')
    plt.title('Visualisation des valeurs avec timestamps')
    plt.legend()  # Ajoutez une légende pour indiquer quelle ligne correspond à quelle valeur

    # Affichez le tracé
    plt.savefig("test")
    plt.show(block=True)


def post_final_presence(final_presence):
    '''final_presence_eleve = []
    for person in final_presence.values():
        nom = person.get('Nom')
        prenom = person.get('Prenom')
        presence = True if person.get('Presence') == 'True' else False
        certitude = round(float(person.get('Precision')))
        final_presence_eleve.append(Eleve(nom, prenom, presence, certitude))
    envoyer_donnees(final_presence_eleve,"Cours A")'''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from Classes.CameraManager import CameraManager
    from Classes.MqttManager import MqttManager

    # camManager = CameraManager()  # Press Maj+F10 to execute it or replace it with your code.
    mqttManager = MqttManager()

    # camManager.recuperation_images()
    # camManager.analyze_images_in_folder()

    # Date fictive
    # date_fictive = datetime.today()

    # Création des dates fictives à 13h30 et 15h30
    # date_13h30 = date_fictive.replace(hour=13, minute=30)
    # date_15h30 = date_fictive.replace(hour=15, minute=30)
    # date_range_string = f'{date_13h30.strftime("%Y-%m-%d %H:%M")}_{date_15h30.strftime("%Y-%m-%d %H:%M")}'

    # Mock de l'envoi des données
    # dispositif = Dispositif(155, "Raspberry", "E303", date_range_string, "Enzo, Morgane, Emilien")
    # envoyer_donnees_dispositif(dispositif)

    # data = Data(155, ["MAC1", "MAC2", "MAC3", "MAC4"])
    # envoyer_donnes_data(data)

    horaires = get_horaires("155")
    print("Horaires reçues: ", horaires)
    tz = pytz.timezone('Europe/Paris')
    horaire_debut, horaire_fin = horaires.split('_')
    horaire_debut = datetime.strptime(horaire_debut, '%Y-%m-%d %H:%M').astimezone(tz)
    horaire_fin = datetime.strptime(horaire_fin, '%Y-%m-%d %H:%M').astimezone(tz)

    # current_time = datetime.utcnow()
    # timezone = pytz.utc
    # influxdb_timestamp_max = pd.to_datetime(current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')).replace(tzinfo=timezone)
    # influxdb_timestamp_min = pd.to_datetime((current_time - timedelta(hours=5)).strftime("'%Y-%m-%dT%H:%M:%S.%fZ'")).replace(tzinfo=timezone)

    data = get_data_in_horaire(horaire_debut, horaire_fin, "155")
    print("Data en lien avec cet horaire: ", data)

    evaluate_presence(data, "155")

    app.run(port=5000)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
