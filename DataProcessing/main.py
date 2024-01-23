# This is a sample Python script.
# Importez la classe CameraManager depuis votre module (supposons que le module s'appelle camera_manager.py)
import datetime
import json
import sys
import os
import glob

from flask_cors import CORS
from flask import Flask, request, jsonify, send_file, url_for

from InfluxDB.client import get_data_in_horaire, envoyer_donnes_data
from DataProcessing.Utils.configUtils import *

# sys.path.insert(1, 'C:/Users/thoma/Documents/Devoirs/.POLY SOPHIA/S9/cyberphysique/proj/ConceptCPS/InfluxDB')

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
cors = CORS(app)

@app.route("/get_image")
def get_image():
    # Utilisez la fonction glob pour rechercher le fichier commencant par "EIIN"
    image_files = glob.glob(os.path.join(os.getcwd(), 'EIIN*.png'))

    if image_files:
        # Utilisez le premier fichier correspondant trouvé
        image_path = image_files[0]
        return send_file(image_path, mimetype='image/png')
    else:
        return jsonify({'error': 'Image not found'})

@app.route("/calculate", methods=["POST"])
def recevoir_notification():
    # Traitez la notification ici
    data = request.get_json()

    if "classNumber" in data:
        class_number = data["classNumber"]
        print(f'Notification reçue pour la classe {class_number} !')
        # Utilisez class_number comme nécessaire dans votre logique

    get_final_presence()

    image_url = url_for('get_image', _external=True)
    return jsonify({'message': 'Notification reçue avec succès', 'image_url': image_url})


@app.route("/configs", methods=["POST"])
def recevoir_configs():
    configs = request.json  # Récupère les configurations depuis la requête POST en format JSON
    print("Configs reçues :", configs)

    # Ajoutez ici le code pour effectuer des opérations supplémentaires avec les configurations si nécessaire

    return jsonify({'message': 'Configs reçues avec succès'})


# Fonction pour remplacer les clés dans le dictionnaire
def remplacer_cles_par_noms(mac_timestamp, adresse_type, chemin_fichier='DataProcessing/Res/Eleves.json'):
    new_dict = {}

    for mac_address, timestamps in mac_timestamp.items():
        if adresse_type == 'WiFi':
            packed_result = trouver_eleve_par_wifi(mac_address, chemin_fichier)
            if packed_result:
                prenom, nom = packed_result
        elif adresse_type == 'Bluetooth':
            packed_result = trouver_eleve_par_bluetooth(mac_address, chemin_fichier)
            if packed_result:
                prenom, nom = packed_result
        else:
            raise ValueError("Type d'adresse non valide. Utilisez 'Wifi' ou 'Bluetooth'.")

        if prenom and nom:
            nom_prenom = f"{prenom}_{nom}"
            new_dict[nom_prenom] = timestamps

    return new_dict


def get_dict_nom_addr(list_mac, type_dispositif):
    tz = pytz.timezone('Europe/Paris')

    mac_timestamp = {}

    for entry in list_mac:
        valeur_separee = entry['_value'].split(',')

        # Parcours de chaque valeur séparée
        for v in valeur_separee:
            # Si la clé existe déjà dans le dictionnaire, ajoutez le timestamp à la liste existante
            if v in mac_timestamp:
                mac_timestamp[v].append(entry['_time'].astimezone(tz))
            else:
                # Sinon, créez la clé et initialisez la liste avec le timestamp
                mac_timestamp[v] = [entry['_time'].astimezone(tz)]

    # À la fin, mac_timestamp contient les valeurs uniques en tant que clés,
    # et chaque valeur a une liste de timestamps associés
    print("Dictionnaire avec MAC: ", mac_timestamp)
    return remplacer_cles_par_noms(mac_timestamp, type_dispositif)


def draw_presence_per_dispositif(list_mac, type_dispositif, numero_cours):
    creneaux = get_creneaux(numero_cours)

    # Créez une seule figure pour tous les créneaux
    fig, axs = plt.subplots(len(creneaux), 1, figsize=(8, 4 * len(creneaux)))
    jour = None
    # Boucle sur chaque créneau
    for i, creneau in enumerate(creneaux):
        mac_timestamp = get_dict_nom_addr(list_mac, type_dispositif)
        print("Dictionnaire avec Noms: ", mac_timestamp)
        # print("Counter: ",get_number_of_detections(mac_timestamp))
        horaire_debut, horaire_fin = get_horaires(creneau)
        reference_day = get_reference_day(creneau)
        horaire_debut = replace_date_with_reference_day(horaire_debut, reference_day)
        horaire_fin = replace_date_with_reference_day(horaire_fin, reference_day)
        print(horaire_debut, horaire_fin)

        # Créez un sous-graphique pour chaque créneau
        ax = axs[i]

        for valeur, liste_timestamps in mac_timestamp.items():
            data_sorted = sorted(zip(liste_timestamps, [valeur] * len(liste_timestamps)), key=lambda x: x[0])
            timestamps_sorted, valeurs_sorted = zip(*data_sorted)
            ax.plot(timestamps_sorted, valeurs_sorted, marker='o', linestyle='-', markersize=5, label=valeur)

        horaire_debut_simple = datetime.strptime(horaire_debut, "%Y-%m-%dT%H:%M:%S.%fZ")
        horaire_fin_simple = datetime.strptime(horaire_fin, "%Y-%m-%dT%H:%M:%S.%fZ")
        horaire_debut_num = mdates.date2num(horaire_debut_simple)
        horaire_fin_num = mdates.date2num(horaire_fin_simple)
        ax.set_xlim(horaire_debut_num, horaire_fin_num)
        # Configuration de l'axe des abscisses avec le fuseau horaire
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis_date('Europe/Paris')
        ax.set_xlabel('Heures')
        ax.set_ylabel('Elèves')

        jour = horaire_debut_simple.strftime("%d/%m/%y")
        representation_horaire = f"{horaire_debut_simple.strftime('%Hh')}-{horaire_fin_simple.strftime('%Hh')}"

        ax.set_title(
            f'Présences pour le créneau {representation_horaire} du cours {numero_cours} du {reference_day} {jour}')
        ax.legend()

    # Ajustez l'espacement entre les sous-graphiques pour éviter les chevauchements
    plt.tight_layout()

    # Sauvegarder le tracé dans un fichier unique
    plt.savefig(numero_cours + "_" + type_dispositif + "_" + "-".join(jour.split('/')) + ".png")
    plt.show(block=True)


def evaluate_presence_per_creneau(creneau):
    horaire_debut, horaire_fin = get_horaires(creneau)
    reference_day = get_reference_day(creneau)
    horaire_debut = replace_date_with_reference_day(horaire_debut, reference_day)
    horaire_fin = replace_date_with_reference_day(horaire_fin, reference_day)
    print(horaire_debut, horaire_fin)
    # On récupère la salle du créneau, ensuite, on récupère les id des dispositifs de cette salle
    salle = get_salle(creneau)
    dispositif_ids = get_dispositif_salle(salle)
    # Pour chaque dispositif, (s'il y en a plusieurs pour une même salle), on appel get_data_in_horaire
    # Si plusieurs dispositifs dans une salle,
    presence_temp = {}
    ponderation = 0
    presence_finale = {}

    for dispositif in dispositif_ids:
        data = get_data_in_horaire(horaire_debut, horaire_fin, dispositif, range=7)
        print("Data en lien avec cet horaire: ", data)
        type_dispositif = get_type_dispositif(dispositif)
        list_mac = get_dict_nom_addr(data, type_dispositif)
        presence_dispositif = get_number_of_detections(list_mac)
        number_of_samples = get_number_of_samples(horaire_debut, horaire_fin, type_dispositif)
        ponderation += number_of_samples

        for personne, nombre_timestamps in presence_dispositif:
            print(f"{personne} a {nombre_timestamps} timestamps.")
            if personne in presence_temp:
                presence_temp[personne].append(nombre_timestamps)
            else:
                # Sinon, créez la clé et initialisez la liste avec le timestamp
                presence_temp[personne] = [nombre_timestamps]

    for personne, valeurs in presence_temp.items():
        somme_valeurs = sum(valeurs)
        presence_finale[personne] = somme_valeurs / ponderation

    print("Presence avec calcul des moyennes pondérées: ", presence_finale)
    return presence_finale


def get_final_presence():
    print("Evaluation des présences en cours...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from Classes.CameraManager import CameraManager
    from Classes.MqttManager import MqttManager

    # camManager = CameraManager()  # Press Maj+F10 to execute it or replace it with your code.
    # mqttManager = MqttManager()

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

    # data = Data(155, ["AA:BB:CC:DD:EE:FF", "5F:37:6E:8D:1C:A2","3D:7F:8A:2E:56:91"])
    # envoyer_donnes_data(data)

    # horaires = get_creneaux("155")
    # print("Horaires reçues: ", horaires)
    # tz = pytz.timezone('Europe/Paris')
    # horaire_debut, horaire_fin = horaires.split('_')
    # horaire_debut = datetime.strptime(horaire_debut, '%Y-%m-%d %H:%M').astimezone(tz)
    # horaire_fin = datetime.strptime(horaire_fin, '%Y-%m-%d %H:%M').astimezone(tz)

    """current_time = datetime.utcnow()
    timezone = pytz.utc
    influxdb_timestamp_max = pd.to_datetime(current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')).replace(tzinfo=timezone)
    influxdb_timestamp_min = pd.to_datetime((current_time - timedelta(hours=2)).strftime("'%Y-%m-%dT%H:%M:%S.%fZ'")).replace(tzinfo=timezone)
    data = get_data_in_horaire(influxdb_timestamp_min, influxdb_timestamp_max, "155")
    print("Data en lien avec cet horaire: ", data)
    evaluate_presence(data, 'Wifi',"EIIN905")"""

    """creneaux = get_creneaux('EIIN905')
    horaire_debut, horaire_fin = get_horaires(creneaux[1])
    reference_day = get_reference_day(creneaux[1])
    horaire_debut = replace_date_with_reference_day(horaire_debut, reference_day)
    horaire_fin = replace_date_with_reference_day(horaire_fin, reference_day)
    print(horaire_debut, horaire_fin)
    data = get_data_in_horaire(horaire_debut, horaire_fin, "155", range=7)
    print("Data en lien avec cet horaire: ", data)

    draw_presence_per_dispositif(data, 'Wifi', "EIIN905")"""

    creneaux = get_creneaux('EIIN905')
    evaluate_presence_per_creneau(creneaux[1])
    # get_number_of_samples("2024-01-16T14:00:00.104000Z","2024-01-16T18:00:00.104000Z","Bluetooth")

    app.run(host="0.0.0.0",port=5000,debug=True)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
