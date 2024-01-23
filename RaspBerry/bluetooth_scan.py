# -*- coding: utf-8 -*-

import time
import bluetooth

from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
from Utils.utils import *
import paho.mqtt.client as mqtt
import sys
import json

# Configuration MQTT
MQTT_HOST = "192.168.80.177"  # env('MQTT_HOST', default='localhost')
MQTT_PORT = 2883  # env.int('MQTT_PORT', default=1884)


class MqttManager:
    # Charger le fichier JSON
    """with open('DataProcessing/Res/Eleves.json', 'r') as fichier_json:
        list_eleves = json.load(fichier_json)"""

    dispositif_id = -1
    client = None

    def __init__(self, dispositif_id):
        self.client = mqtt.Client("Raspberry_" + str(dispositif_id))  # Create instance of client with client ID “digi_mqtt_test”
        self.client.on_connect = self.on_connect  # Define callback function for successful connection
        self.client.on_message = self.on_message  # Define callback function for receipt of a message
        # client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
        self.client.connect(MQTT_HOST, MQTT_PORT)
        self.dispositif_id = dispositif_id
        #self.client.loop_forever()  # Start networking daemon
        # Créez une instance de la classe CameraManager
        # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

    def on_connect(self, client, userdata, flags, rc):  # The callback for when the client connects to the broker
        # Print result of connection attempt
        print("Connected with resultcode {0}".format(str(rc)))
        # Subscribe to the topic “digitest/test1”, receive any messages published on it
        client.subscribe("raspberry/" + str(self.dispositif_id))

    def on_message(self, client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        print("Message received-> " + msg.topic)  # Print a received msg
        if msg.topic == "raspberry/" + str(self.dispositif_id):
            update_config(msg.payload)

    def publish_data(self, topic, msg):
        return self.client.publish(topic, json.dumps(msg))

    def loop_start(self):
        return self.client.loop_start()

    def loop_stop(self):
        return self.client.loop_stop()

    def disconnect(self):
        return self.client.disconnect()


# Définition des listes pour les adresses MAC et IP
mac_ip_adresses_bluetooth = []

def scan_bluetooth(debut,fin,sampling):
    horaire_act = get_actual_date()
    timestamp_act_datetime = datetime.fromisoformat(horaire_act)
    while debut <= timestamp_act_datetime <= fin:
        scan = scan_available_bluetooth_devices()
        print("données: ",scan)
        client.publish_data("raspberry/bluetooth", scan)
        print(f"Attente de {sampling} minutes pour un autre scan")
        time.sleep(sampling*60)

def scan_available_bluetooth_devices():
    print("Scanning for available Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True, flush_cache=True, lookup_class=False)

    for address, name in nearby_devices:
        mac_ip_adresses_bluetooth.append({"MAC": address})

    return [{"MAC": address} for address, name in nearby_devices]


'''def start_scanning(client):
    config_state = get_config()
    if config_state == 'boot':'''


def ask_config(client):
    id = get_id()
    client.publish('raspberry/config',id)

# arp_scan(ip_range)
# scan_available_bluetooth_devices()

if __name__ == '__main__':
    id_dispositif = get_id()
    client = MqttManager(id_dispositif)

    while get_config() == 'boot':
        print('No config received, going to sleep for 10s...')
        time.sleep(10)

    timezone_1_hour = pytz.timezone("Europe/Paris")  # Remplacez "Europe/Paris" par le fuseau horaire souhaité

    try:
        while True:
            creneaux = get_creneaux()
            horaire_actuelle = get_actual_date()
            timestamp_actuel_datetime = datetime.fromisoformat(horaire_actuelle)

            difference_minimale = timedelta.max
            creneau_le_plus_proche = None

            for creneau in creneaux:
                horaire_debut, horaire_fin = get_horaires(creneau)
                jour = get_jour(creneau)
                debut_datetime = replace_date_with_reference_day(horaire_debut,jour)
                fin_datetime = replace_date_with_reference_day(horaire_fin,jour)
                # Ajoutez le décalage horaire +1 heure
                debut_datetime = debut_datetime.replace(tzinfo=timezone_1_hour)
                fin_datetime = fin_datetime.replace(tzinfo=timezone_1_hour)

                if debut_datetime <= timestamp_actuel_datetime <= fin_datetime:
                    print("Le timestamp actuel est entre le debut et la fin du creneau. Debut du sampling...")
                    sampling = get_sampling()
                    scan_bluetooth(debut_datetime,fin_datetime,sampling)
                else:
                    difference = debut_datetime - timestamp_actuel_datetime - timedelta(hours=1)
                    if difference >= timedelta(0) and difference < difference_minimale:
                        difference_minimale = difference
                        creneau_le_plus_proche = creneau

            if creneau_le_plus_proche is not None:
                print(f"Le creneau le plus proche est {creneau_le_plus_proche}.")
                print(f"Il est separe de l'heure actuelle par {difference_minimale}.")
                # Convertir la différence en secondes
                difference_en_secondes = int(difference_minimale.total_seconds())

                # Faire un time.sleep de la durée spécifiée
                print(f"En attente pendant {difference_en_secondes} secondes...")
                time.sleep(difference_en_secondes)
                print("Attente terminee.")
                sampling = get_sampling()
                scan_bluetooth(debut_datetime,fin_datetime,sampling)

            else:
                print("Aucun creneau trouve.")

    except KeyboardInterrupt:
        print("\nSortie par Ctrl+C. Arret du programme.")
        client.disconnect()
        reboot()


# Scan et publication
# print("Début du scan...")

# REBOOT APRES LE PRESS CTRL+C


