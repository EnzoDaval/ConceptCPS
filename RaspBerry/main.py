import bluetooth
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
import paho.mqtt.client as mqtt
from envparse import env

# Définition des listes pour les adresses MAC
mac_adresses_bluetooth = []
mac_adresses_wifi = []

def arp_scan(ip_range):
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    ans, unans = srp(request, timeout=2, retry=1)

    for sent, received in ans:
        mac_adresses_wifi.append(received.hwsrc)

    return [{'IP': received.psrc, 'MAC': received.hwsrc} for sent, received in ans]

def scan_available_bluetooth_devices():
    print("Scanning for available Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    for address, name in nearby_devices:
        mac_adresses_bluetooth.append(address)

    return [{"Adresse MAC": address, "Nom": name} for address, name in nearby_devices]

# Configuration MQTT
MQTT_HOST = env('MQTT_HOST', default='localhost')
MQTT_PORT = env.int('MQTT_PORT', default=1883)

# Connexion au broker MQTT
client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, 60)
print("Connecté au broker MQTT.")

# Scan et publication
print("Début du scan...")
ip_range = "172.20.10.1/24"
arp_scan(ip_range)
scan_available_bluetooth_devices()

print("Publication des adresses MAC sur MQTT...")
client.publish("mac_adresses/wifi", str(mac_adresses_wifi))
client.publish("mac_adresses/bluetooth", str(mac_adresses_bluetooth))

print("Adresses MAC WiFi:", mac_adresses_wifi)
print("Adresses MAC Bluetooth:", mac_adresses_bluetooth)
print("Données publiées avec succès.")

# Déconnexion du broker MQTT
client.disconnect()
print("Déconnecté du broker MQTT.")
