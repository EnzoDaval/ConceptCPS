# This is a sample Python script.
# Importez la classe CameraManager depuis votre module (supposons que le module s'appelle camera_manager.py)
from CameraManager import CameraManager
import paho.mqtt.client as mqtt
import json

NUMBER_OF_SENSORS = 2  # Bluetooth & Wifi
BLUETOOTH_CONFIDENCE = 0.4  # Donné par l'utilisateur
WIFI_CONFIDENCE = 0.6  # Donné par l'utilisateur


class MqttManager:
    # Charger le fichier JSON
    with open('Res/Eleves.json', 'r') as fichier_json:
        list_eleves = json.load(fichier_json)

    list_presence = {}
    bluetooth_message_received = False
    wif_message_received = False

    def __init__(self):
        client = mqtt.Client("digi_mqtt_test")  # Create instance of client with client ID “digi_mqtt_test”
        client.on_connect = self.on_connect  # Define callback function for successful connection
        client.on_message = self.on_message  # Define callback function for receipt of a message
        # client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
        client.connect('127.0.0.1', 2883)
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
        print("List of bluetooth addresses-> " + str(msg))  # Print a received msg
        for eleve in self.list_eleves:  # La liste de tous les eleves
            nom = eleve['Nom']
            prenom = eleve['Prenom']
            adresse_mac_bluetooth = eleve['Adresse_MAC_Bluetooth']
            presence_bool = False
            for presence in json.loads(msg):  # La liste des eleves detectes
                adresse_mac_bluetooth_detected = presence['Adresse_MAC_Bluetooth']
                if adresse_mac_bluetooth_detected == adresse_mac_bluetooth:
                    presence_bool = True
            cle = f'{nom}-{prenom}'
            valeurs = {'Nom': f'{nom}', 'Prenom': f'{prenom}', 'PresenceBluetooth': f'{presence_bool}'}
            if self.list_presence.get(cle):
                self.list_presence[cle].update(valeurs)
            else:
                self.list_presence[cle] = valeurs
        # print(self.list_presence)
        if self.wif_message_received:
            evaluate_presence(self.list_eleves, self.list_presence)
            self.bluetooth_message_received = False
            self.wif_message_received = False
        else:
            self.bluetooth_message_received = True

    def on_message_wifi(self, msg):
        print("List of wifi addresses-> " + str(msg))  # Print a received msg
        for eleve in self.list_eleves:  # La liste de tous les eleves
            nom = eleve['Nom']
            prenom = eleve['Prenom']
            adresse_mac_wifi = eleve['Adresse_MAC_Wifi']
            presence_bool = False
            for presence in json.loads(msg):  # La liste des eleves detectes
                adresse_mac_wifi_detected = presence['Adresse_MAC_Wifi']
                if adresse_mac_wifi_detected == adresse_mac_wifi:
                    presence_bool = True
            cle = f'{nom}-{prenom}'
            valeurs = {'Nom': f'{nom}', 'Prenom': f'{prenom}', 'PresenceWifi': f'{presence_bool}'}
            if self.list_presence.get(cle):
                self.list_presence[cle].update(valeurs)
            else:
                self.list_presence[cle] = valeurs
        # print(self.list_presence)
        if self.bluetooth_message_received:
            evaluate_presence(self.list_eleves, self.list_presence)
            self.bluetooth_message_received = False
            self.wif_message_received = False
        else:
            self.wif_message_received = True


def evaluate_presence(eleves, presences):
    final_presence = {}
    for eleve in eleves:
        nom = eleve['Nom']
        prenom = eleve['Prenom']
        precision = 0
        presence_value = False
        for presence in presences.values():
            presenceWifi = presence.get('PresenceWifi')
            presenceBluetooth = presence.get('PresenceBluetooth')
            if nom == presence['Nom'] and prenom == presence['Prenom']:
                presence_value = True
                if presenceWifi == 'True':
                    precision += 100 * WIFI_CONFIDENCE
                if presenceBluetooth == 'True':
                    precision += 100 * BLUETOOTH_CONFIDENCE
                if presenceBluetooth == 'False' and presenceWifi == 'False':
                    precision = 100
        cle = f'{nom}-{prenom}'
        valeurs = {'Nom': f'{nom}', 'Prenom': f'{prenom}', 'Presence': f'{presence_value}', 'Precision': f'{precision}'}
        final_presence[cle] = valeurs
    print(final_presence)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    camManager = CameraManager()  # Press Maj+F10 to execute it or replace it with your code.
    mqttManager = MqttManager()

    # camManager.recuperation_images()
    # camManager.analyze_images_in_folder()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
