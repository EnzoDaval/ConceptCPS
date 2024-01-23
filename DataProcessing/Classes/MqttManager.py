import paho.mqtt.client as mqtt
import json

from DataProcessing.Utils.configUtils import *
from DataProcessing.main import update_configs
from InfluxDB.client import envoyer_donnes_data
from InfluxDB.data import Data

BLUETOOTH_ID = 150

WIFI_ID = 160

MQTT_HOST = "192.168.80.177"
MQTT_PORT = 2883 #1884


class MqttManager:
    # Charger le fichier JSON
    with open('DataProcessing/Res/Eleves.json', 'r') as fichier_json:
        list_eleves = json.load(fichier_json)

    list_presence = {}
    bluetooth_message_received = False
    wif_message_received = False
    client = None

    def __init__(self):
        self.client = mqtt.Client("Orchestrateur")  # Create instance of client with client ID “digi_mqtt_test”
        self.client.on_connect = self.on_connect  # Define callback function for successful connection
        self.client.on_message = self.on_message  # Define callback function for receipt of a message
        # client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
        self.client.connect(MQTT_HOST, MQTT_PORT)
        self.client.loop_forever()  # Start networking daemon
        #client.loop_start()
        # Créez une instance de la classe CameraManager
        # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

    def on_connect(self, client, userdata, flags, rc):  # The callback for when the client connects to the broker
        # Print result of connection attempt
        print("Connected with resultcode {0}".format(str(rc)))
        # Subscribe to the topic “digitest/test1”, receive any messages published on it
        for device_id in get_all_dispositifs():
            client.subscribe("raspberry/"+str(device_id)+"/config") # Pour ecouter la demande de config
            client.subscribe("raspberry/"+str(device_id)+"/data") # Pour ecouter l'envoi de données
            client.subscribe("sampling/update")

    def on_message(self, client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        print("Message received-> " + msg.topic)  # Print a received msg
        # Split du topic

        if msg.topic == "sampling/update": # Les données liées au sampling ont été mises a jour
            return update_configs(self.client)

        topic_parts = msg.topic.split('/')
        device_id = None
        # Récupération de l'ID
        if len(topic_parts) >= 2:
            device_id = int(topic_parts[-2])
            print(f"ID: {device_id}")

        type_dispositif = get_type_dispositif(device_id)

        # Vérification si la dernière partie du topic est "config"
        if len(topic_parts) >= 2 and topic_parts[-1] == "config":
            print("Message received on a 'config' topic")
            salle = get_salle_dispositif(device_id)
            creneaux = get_creneaux_par_salle(salle)
            sampling = get_sampling_for_device_type(type_dispositif)
            json_data = creer_json_config(device_id,type_dispositif,sampling,creneaux)
            # Vous pouvez utiliser la variable 'device_id' comme vous le souhaitez ici
            client.publish('raspberry/'+str(device_id)+"/setup",json_data)
        else:
            print("Message received on a 'data' topic")
            match type_dispositif:
                case "Bluetooth":
                    self.on_message_bluetooth(msg.payload)
                case "WiFi":
                    self.on_message_wifi(msg.payload)
                case _:
                    exit()

    def on_message_bluetooth(self, msg):
        try:
            # Transformer le payload en liste de dictionnaires
            mac_dicts = json.loads(msg.decode('utf-8'))
            # Extraire les valeurs MAC de chaque dictionnaire
            mac_addresses = [mac_dict['MAC'] for mac_dict in mac_dicts]

            # Créer et envoyer les données
            data = Data(BLUETOOTH_ID, mac_addresses)
            print(mac_addresses)
            envoyer_donnes_data(data)
        except json.JSONDecodeError:
            print("Erreur de décodage JSON.")
        except KeyError:
            print("Clé 'MAC' manquante dans les données reçues.")

    def on_message_wifi(self, msg):
        try:
            # Transformer le payload en liste de dictionnaires
            mac_dicts = json.loads(msg.decode('utf-8'))
            # Extraire les valeurs MAC de chaque dictionnaire
            mac_addresses = [mac_dict['MAC'] for mac_dict in mac_dicts]

            # Créer et envoyer les données
            data = Data(WIFI_ID, mac_addresses)
            envoyer_donnes_data(data)
        except json.JSONDecodeError:
            print("Erreur de décodage JSON.")
        except KeyError:
            print("Clé 'MAC' manquante dans les données reçues.")


    def loop_start(self):
        return self.client.loop_start()

    def loop_stop(self):
        return self.client.loop_stop()
