import bluetooth
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp

# Listes pour stocker les adresses MAC
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

# Exemple d'utilisation
ip_range = "172.20.10.1/24"
arp_scan(ip_range)
print("Adresses MAC des appareils WiFi :", mac_adresses_wifi)

scan_available_bluetooth_devices()
print("Adresses MAC des appareils Bluetooth :", mac_adresses_bluetooth)

# Envoi des données via MQTT (à implémenter)
# mqtt_send(mac_adresses_wifi, mac_adresses_bluetooth)
