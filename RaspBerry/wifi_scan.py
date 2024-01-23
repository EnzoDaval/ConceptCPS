import time

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
        # client.subscribe("raspberry/wifi")

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
mac_ip_adresses_wifi = []


def arp_scan(ip_range):
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    ans, unans = srp(request, timeout=2, retry=1)

    for sent, received in ans:
        mac_ip_adresses_wifi.append({"MAC": received.hwsrc})

    return [{"MAC": received.hwsrc} for sent, received in ans]


'''def start_scanning(client):
    config_state = get_config()
    if config_state == 'boot':'''


def ask_config(client):
    id = get_id()
    client.publish('raspberry/config',id)

# arp_scan(ip_range)
# scan_available_bluetooth_devices()

if __name__ == '__main__':
    #ip_range = sys.argv[1]  # "172.20.10.1/24"
    id_dispositif = get_id()
    client = MqttManager(id_dispositif)

    while get_config() == 'boot':
        print('No config received, going to sleep for 10s...')
        time.sleep(10)

    creneaux = get_creneaux()
    horaire_actuelle = get_actual_date()
    timestamp_actuel_datetime = datetime.fromisoformat(horaire_actuelle)

    difference_minimale = timedelta.max
    creneau_le_plus_proche = None

    for creneau in creneaux:
        horaire_debut, horaire_fin = get_horaires(creneau)
        jour = get_jour(creneau)
        debut_datetime = datetime.fromisoformat(replace_date_with_reference_day(horaire_debut,jour))
        fin_datetime = datetime.fromisoformat(replace_date_with_reference_day(horaire_fin,jour))

        if debut_datetime <= timestamp_actuel_datetime <= fin_datetime:
            print("Le timestamp actuel est entre le début et la fin du créneau.")
        else:
            difference = debut_datetime - timestamp_actuel_datetime - timedelta(hours=1)
            if difference >= timedelta(0) and difference < difference_minimale:
                difference_minimale = difference
                creneau_le_plus_proche = creneau

    if creneau_le_plus_proche is not None:
        print(f"Le créneau le plus proche est {creneau_le_plus_proche}.")
        print(f"Il est séparé de l'heure actuelle par {difference_minimale}.")
        # Convertir la différence en secondes
        difference_en_secondes = int(difference_minimale.total_seconds())

        # Faire un time.sleep de la durée spécifiée
        print(f"En attente pendant {difference_en_secondes} secondes...")
        time.sleep(difference_en_secondes)
        print("Attente terminée.")
    else:
        print("Aucun créneau trouvé.")


# Scan et publication
    # print("Début du scan...")

    # REBOOT APRES LE PRESS CTRL+C
    client.disconnect()

