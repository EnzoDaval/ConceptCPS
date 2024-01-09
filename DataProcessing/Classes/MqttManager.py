import paho.mqtt.client as mqtt
import json
from InfluxDB.client import envoyer_donnes_data
from InfluxDB.data import Data

BLUETOOTH_ID = 150

WIFI_ID = 160

MQTT_HOST = "127.0.0.1" #"192.168.195.81"
MQTT_PORT = 2883 #1884


class MqttManager:
    # Charger le fichier JSON
    with open('Res/Eleves.json', 'r') as fichier_json:
        list_eleves = json.load(fichier_json)

    list_presence = {}
    bluetooth_message_received = False
    wif_message_received = False

    def __init__(self):
        client = mqtt.Client("Orchestrateur")  # Create instance of client with client ID “digi_mqtt_test”
        client.on_connect = self.on_connect  # Define callback function for successful connection
        client.on_message = self.on_message  # Define callback function for receipt of a message
        # client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
        client.connect(MQTT_HOST, MQTT_PORT)
        client.loop_forever()  # Start networking daemon
        # Créez une instance de la classe CameraManager
        # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

    def on_connect(self, client, userdata, flags, rc):  # The callback for when the client connects to the broker
        # Print result of connection attempt
        print("Connected with resultcode {0}".format(str(rc)))
        # Subscribe to the topic “digitest/test1”, receive any messages published on it
        client.subscribe("raspberry/bluetooth")
        client.subscribe("raspberry/wifi")

    def on_message(self, client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        print("Message received-> " + msg.topic)  # Print a received msg
        match msg.topic:
            case "raspberry/bluetooth":
                self.on_message_bluetooth(msg.payload)
            case "raspberry/wifi":
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