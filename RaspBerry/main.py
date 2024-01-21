import bluetooth
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
import paho.mqtt.client as mqtt
import sys
import json

# Définition des listes pour les adresses MAC et IP
mac_ip_adresses_bluetooth = []
mac_ip_adresses_wifi = []

def arp_scan(ip_range):
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    ans, unans = srp(request, timeout=2, retry=1)

    for sent, received in ans:
        mac_ip_adresses_wifi.append({"MAC": received.hwsrc})

    return [{"MAC": received.hwsrc} for sent, received in ans]

def scan_available_bluetooth_devices():
    print("Scanning for available Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    for address, name in nearby_devices:
        mac_ip_adresses_bluetooth.append({"MAC": address})

    return [{"MAC": address} for address, name in nearby_devices]

# Configuration MQTT
MQTT_HOST = "192.168.80.177"#env('MQTT_HOST', default='localhost')
MQTT_PORT = 2884#env.int('MQTT_PORT', default=1884)

# Connexion au broker MQTT
client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, 60)
print("Connection au broker MQTT: ",MQTT_HOST,MQTT_PORT)

# Scan et publication
print("Début du scan...")
ip_range = sys.argv[1] # "172.20.10.1/24"
#arp_scan(ip_range)
#scan_available_bluetooth_devices()

print("Publication des adresses MAC et IP sur MQTT...")
client.publish("raspberry/wifi", json.dumps(arp_scan(ip_range)))
client.publish("raspberry/bluetooth", json.dumps(scan_available_bluetooth_devices()))

print("Adresses MAC et IP WiFi:", mac_ip_adresses_wifi)
print("Adresses MAC Bluetooth:", mac_ip_adresses_bluetooth)
print("Données publiées avec succès.")

# Déconnexion du broker MQTT
client.disconnect()
print("Déconnecté du broker MQTT.")

