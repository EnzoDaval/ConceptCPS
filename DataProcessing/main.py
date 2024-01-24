# This is a sample Python script.
# Importez la classe CameraManager depuis votre module (supposons que le module s'appelle camera_manager.py)
import datetime
import json
import sys
import os
import glob

import numpy as np
from PIL import Image
from flask_cors import CORS

from InfluxDB.client import get_data_in_horaire, envoyer_donnes_data
from DataProcessing.Utils.configUtils import *

# sys.path.insert(1, 'C:/Users/thoma/Documents/Devoirs/.POLY SOPHIA/S9/cyberphysique/proj/ConceptCPS/InfluxDB')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pytz
# from flask_cors import CORS  # Import CORS
# from InfluxDB.client import *
from InfluxDB.dispositif import Dispositif
from InfluxDB.data import Data


def update_configs(client):
    print("Mise à jour des configs")
    with open("DataProcessing/Res/Dispositifs.json", 'r') as file:
        devices_data = json.load(file)

    with open("DataProcessing/Res/Sampling.json", 'r') as file:
        sampling_data = json.load(file)

    # Créer un dictionnaire de type_dispositif vers sampling
    sampling_dict = {entry["type_dispositif"].capitalize(): entry["sampling"] for entry in sampling_data}

    # Parcourir les dispositifs et mettre à jour en fonction du type_dispositif
    for device in devices_data:
        device_id = device["id"]
        device_type = device["type_dispositif"][0].capitalize() if isinstance(device["type_dispositif"], list) else \
        device["type_dispositif"].capitalize()
        salle = device["salle"]

        # Vérifier si le type_dispositif est présent dans le fichier sampling
        if device_type in sampling_dict:
            sampling_value = sampling_dict[device_type]
            # Appeler la fonction 'update' avec les paramètres nécessaires
            creneaux = get_creneaux_par_salle(salle)
            print("publication sur le device: " + str(device_id))
            client.publish("raspberry/" + str(device_id) + "/setup",
                           creer_json_config(device_id, device_type, sampling_value, creneaux))

    return None


# Fonction pour remplacer les clés dans le dictionnaire
def remplacer_cles_par_noms(mac_timestamp, adresse_type, chemin_fichier='Res/Eleves.json'):
    new_dict = {}
    nom, prenom = None, None
    for mac_address, timestamps in mac_timestamp.items():
        if adresse_type == 'Wifi':
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


'''
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

        # horaire_debut_simple = datetime.strptime(horaire_debut, "%Y-%m-%dT%H:%M:%S.%fZ")
        # horaire_fin_simple = datetime.strptime(horaire_fin, "%Y-%m-%dT%H:%M:%S.%fZ")
        horaire_debut_num = mdates.date2num(horaire_debut)
        horaire_fin_num = mdates.date2num(horaire_fin)
        ax.set_xlim(horaire_debut_num, horaire_fin_num)
        # Configuration de l'axe des abscisses avec le fuseau horaire
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis_date('Europe/Paris')
        ax.set_xlabel('Heures')
        ax.set_ylabel('Elèves')

        jour = horaire_debut.strftime("%d/%m/%y")
        representation_horaire = f"{horaire_debut.strftime('%Hh')}-{horaire_fin.strftime('%Hh')}"

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
    list_eleves = get_eleves(creneau)

    for dispositif in dispositif_ids:
        data = get_data_in_horaire(horaire_debut, horaire_fin, dispositif, range=20)
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

    for eleve in list_eleves:
        eleve_key = f"{eleve['prenom']}_{eleve['nom']}"
        if eleve_key not in presence_finale:
            presence_finale[eleve_key] = 0

    print("Presence avec calcul des moyennes pondérées: ", presence_finale)
    return presence_finale
'''


def draw_presence_per_creneau(all_data, horaire_debut, horaire_fin, reference_day, creneau, id_graph):
    # Créez une seule figure pour tous les créneaux
    # fig, axs = plt.subplots(len(creneaux), 1, figsize=(8, 4 * len(creneaux)))
    # fig, ax = plt.subplots(figsize=(8, 4))
    # plt.figure(figsize=(8, 4))
    jour = None

    # Boucle sur chaque créneau
    # for i, creneau in enumerate(creneaux):
    mac_timestamps = {}  # Un seul dictionnaire pour tous les dispositifs
    print("Dictionnaire avec Noms: ", mac_timestamps)

    # Rassemblez les données de tous les dispositifs dans mac_timestamps
    for nom, timestamp in all_data.items():
        # type_dispositif = get_type_dispositif(dispositif)
        # mac_timestamp = get_dict_nom_addr(data, type_dispositif)
        if nom == 'Presence': break

        # Mettez à jour le dictionnaire global mac_timestamps
        if nom in mac_timestamps:
            mac_timestamps[nom].append(timestamp)
        else:
            mac_timestamps[nom] = timestamp

    taux_presence = all_data['Presence']
    # Créez un seul graphique
    fig, ax = plt.subplots(figsize=(8, 4))

    # Utilisez la fonction scatter pour afficher les points de chaque personne en fonction de son taux de présence
    '''for personne, timestamps in mac_timestamps.items():
        taux = taux_presence.get(personne, 0.0)  * 100 # Obtenez le taux de présence, par défaut à 0 si non présent
        data_sorted = sorted(zip(timestamps, [personne] * len(timestamps)), key=lambda x: x[0])
        timestamps_sorted, valeurs_sorted = zip(*data_sorted)
        # timestamps_num = mdates.date2num(timestamps_sorted)  # Convertissez les objets datetime en valeurs numériques
        plt.plot(timestamps_sorted, valeurs_sorted, marker='o', linestyle='-', markersize=5, label=personne)
        #plt.scatter(timestamps_num, valeurs_sorted, marker='o', label=personne)'''

    # Utilisez le dictionnaire global mac_timestamps pour le tracé
    for personne, liste_timestamps in mac_timestamps.items():
        taux = taux_presence.get(personne, 0.0) * 100  # Obtenez le taux de présence, par défaut à 0 si non présent
        data_sorted = sorted(zip(liste_timestamps, [personne] * len(liste_timestamps)), key=lambda x: x[0])
        timestamps_sorted, valeurs_sorted = zip(*data_sorted)
        # plt.plot(timestamps_sorted, valeurs_sorted, marker='o', linestyle='-', markersize=5, label=valeur)
        # plt.scatter(timestamps_sorted, [taux] * len(timestamps_sorted), marker='o', label=personne)
        plt.plot(timestamps_sorted, [taux] * len(timestamps_sorted), marker='o', linestyle='-', markersize=5,
                 label=personne)

    # Configuration de l'axe des abscisses avec le fuseau horaire
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis_date('Europe/Paris')
    ax.set_xlabel('Heures')
    ax.set_ylabel('Taux de présence (en %)')
    horaire_debut_num = mdates.date2num(horaire_debut)
    horaire_fin_num = mdates.date2num(horaire_fin)
    plt.xlim(horaire_debut_num, horaire_fin_num)
    plt.ylim(0, 100)

    jour = horaire_debut.strftime("%d/%m/%y")
    representation_horaire = f"{horaire_debut.strftime('%Hh')}-{horaire_fin.strftime('%Hh')}"

    plt.title(
        f'Présences pour le créneau {representation_horaire} du cours {get_numero_cours(creneau)} du {reference_day} {jour}')
    plt.legend()

    # Ajustez l'espacement entre les sous-graphiques pour éviter les chevauchements
    # plt.tight_layout()

    # Sauvegarder le tracé dans un fichier unique
    plt.savefig(get_numero_cours(creneau) + "_" + str(id_graph) + ".png")
    plt.show(block=True)


def evaluate_presence_per_creneau(creneau, id_graph):
    horaire_debut, horaire_fin = get_horaires(creneau)
    reference_day = get_reference_day(creneau)
    horaire_debut = replace_date_with_reference_day(horaire_debut, reference_day)
    horaire_fin = replace_date_with_reference_day(horaire_fin, reference_day)
    print(horaire_debut, horaire_fin)

    # On récupère la salle du créneau, ensuite, on récupère les id des dispositifs de cette salle
    salle = get_salle(creneau)
    dispositif_ids = get_dispositif_salle(salle)

    # Rassemblez les données de tous les dispositifs dans un seul dictionnaire
    all_data = {}
    all_data_to_draw = {}
    for dispositif in dispositif_ids:
        data = get_data_in_horaire(horaire_debut, horaire_fin, dispositif, range=20)
        print("Data en lien avec cet horaire: ", data)
        type_dispositif = get_type_dispositif(dispositif)
        list_mac = get_dict_nom_addr(data, type_dispositif)
        all_data[dispositif] = list_mac

        for personne in list_mac:
            if personne in all_data_to_draw:
                all_data_to_draw[personne] += list_mac.get(personne)
            else:
                all_data_to_draw[personne] = list_mac.get(personne)

    # Appelez la fonction de tracé avec toutes les données de dispositifs
    #    draw_presence_per_dispositif(all_data, horaire_debut,horaire_fin,reference_day,creneau)

    # Le reste de votre code pour le calcul des présences moyennées reste inchangé
    presence_temp = {}
    ponderation = 0
    presence_finale = {}
    list_eleves = get_eleves(creneau)

    for dispositif, mac_timestamp in all_data.items():
        presence_dispositif = get_number_of_detections(mac_timestamp)
        number_of_samples = get_number_of_samples(horaire_debut, horaire_fin, get_type_dispositif(dispositif))
        ponderation += number_of_samples

        for personne, nombre_timestamps in presence_dispositif:
            print(f"{personne} a {nombre_timestamps} timestamps {get_type_dispositif(dispositif)}.")
            if personne in presence_temp:
                presence_temp[personne].append(nombre_timestamps)
            else:
                presence_temp[personne] = [nombre_timestamps]

    all_data_to_draw['Presence'] = {personne: sum(valeurs) / ponderation for personne, valeurs in presence_temp.items()}

    for personne, valeurs in presence_temp.items():
        somme_valeurs = sum(valeurs)
        presence_finale[personne] = somme_valeurs / ponderation

    for eleve in list_eleves:
        eleve_key = f"{eleve['prenom']}_{eleve['nom']}"
        if eleve_key not in presence_finale:
            presence_finale[eleve_key] = 0

    print("Presence avec calcul des moyennes pondérées: ", presence_finale)
    draw_presence_per_creneau(all_data_to_draw, horaire_debut, horaire_fin, reference_day, creneau, id_graph)

    return presence_finale


def get_final_presence(cours,fichier):
    print("Evaluation des présences en cours...")
    creneaux = get_creneaux(cours,fichier)
    i = 0
    for creneau in creneaux:
        evaluate_presence_per_creneau(creneau, i)
        i += 1

    image1 = cours+"_0.png"
    if i > 1 : image2 = cours+"_1.png"

    write_final_image(image1,image2,cours)


def write_final_image(image1, image2, cours):
    image1 = Image.open(image1)
    if not image2 :
        width1, height1 = image1.size
        new_image = Image.new('RGB', (width1, height1), (255, 255, 255))
        new_image.paste(image1, (0, 0))
        new_image.save(cours + '.png')
    else :
        image2 = Image.open(image2)

        # Obtenir les dimensions des images
        width1, height1 = image1.size
        width2, height2 = image2.size

        # Créer une nouvelle image avec la largeur maximale et la somme des hauteurs
        new_width = max(width1, width2)
        new_height = height1 + height2 #+ 400
        new_image = Image.new('RGB', (new_width, new_height), (255, 255, 255))

        y_position_image1 = (new_height // 2) - height1
        y_position_image2 = y_position_image1 + height1

        # Superposer les deux images verticalement
        new_image.paste(image1, (0, y_position_image1))
        new_image.paste(image2, (0, y_position_image2))  # La deuxième image commence après la première

        # Sauvegarder l'image fusionnée
        new_image.save(cours + '.png')

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

    # data = Data(1000, ["AA:BB:CC:DD:EE:FF", "5F:37:6E:8D:1C:A2","3D:7F:8A:2E:56:91"])
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

    # creneaux = get_creneaux('EIIN905')
    # evaluate_presence_per_creneau(creneaux[1])

    '''horaire_debut, horaire_fin = get_horaires(creneaux[1])
    reference_day = get_reference_day(creneaux[1])
    horaire_debut = replace_date_with_reference_day(horaire_debut, reference_day)
    horaire_fin = replace_date_with_reference_day(horaire_fin, reference_day)
    data = get_data_in_horaire(horaire_debut, horaire_fin, "155", range=7)
    draw_presence_per_dispositif(data, 'Wifi', "EIIN905")'''
    # get_number_of_samples("2024-01-16T14:00:00.104000Z","2024-01-16T18:00:00.104000Z","Bluetooth")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
