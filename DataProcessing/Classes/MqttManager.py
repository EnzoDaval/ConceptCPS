import paho.mqtt.client as mqtt
import json

MQTT_HOST = "192.168.195.81" #"127.0.0.1" #192.168.195.81"
MQTT_PORT = 1884 #2883 #1884


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
        from main import evaluate_presence

        print("List of bluetooth addresses-> " + str(msg))  # Print a received msg
        for eleve in self.list_eleves:  # La liste de tous les eleves
            nom = eleve['Nom']
            prenom = eleve['Prenom']
            adresse_mac_bluetooth = eleve['Adresse_MAC_Bluetooth']
            presence_bool = False
            for presence in json.loads(msg):  # La liste des eleves detectes
                adresse_mac_bluetooth_detected = presence['MAC']
                if adresse_mac_bluetooth_detected.lower() == adresse_mac_bluetooth.lower():
                    presence_bool = True
            cle = f'{nom}-{prenom}'
            valeurs = {'Nom': f'{nom}', 'Prenom': f'{prenom}', 'PresenceBluetooth': f'{presence_bool}'}
            if self.list_presence.get(cle):
                self.list_presence[cle].update(valeurs)
            else:
                self.list_presence[cle] = valeurs
        # print(self.list_presence)
        if self.wif_message_received:
            evaluate_presence(self.list_presence)
            self.bluetooth_message_received = False
            self.wif_message_received = False
        else:
            self.bluetooth_message_received = True

    def on_message_wifi(self, msg):
        from main import evaluate_presence

        print("List of wifi addresses-> " + str(msg))  # Print a received msg
        for eleve in self.list_eleves:  # La liste de tous les eleves
            nom = eleve['Nom']
            prenom = eleve['Prenom']
            adresse_mac_wifi = eleve['Adresse_MAC_Wifi']
            presence_bool = False
            for presence in json.loads(msg):  # La liste des eleves detectes
                adresse_mac_wifi_detected = presence['MAC']
                if adresse_mac_wifi_detected.lower() == adresse_mac_wifi.lower():
                    presence_bool = True
            cle = f'{nom}-{prenom}'
            valeurs = {'Nom': f'{nom}', 'Prenom': f'{prenom}', 'PresenceWifi': f'{presence_bool}'}
            if self.list_presence.get(cle):
                self.list_presence[cle].update(valeurs)
            else:
                self.list_presence[cle] = valeurs
        # print(self.list_presence)
        if self.bluetooth_message_received:
            evaluate_presence(self.list_presence)
            self.bluetooth_message_received = False
            self.wif_message_received = False
        else:
            self.wif_message_received = True
