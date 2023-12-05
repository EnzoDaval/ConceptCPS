import bluetooth
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp


def arp_scan(ip_range):
    """
    Scan for devices connected to the WiFi network.

    Args:
    - ip_range (str): The IP range to scan, in CIDR notation.

    Returns:
    - list: A list of dictionaries containing the IP and MAC addresses of the connected WiFi devices.
    """
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    ans, unans = srp(request, timeout=2, retry=1)
    wifi_devices = []

    for sent, received in ans:
        wifi_devices.append({'IP': received.psrc, 'MAC': received.hwsrc})

    return wifi_devices

def scan_available_bluetooth_devices():
    """
    Scan for available Bluetooth devices in the vicinity.

    Returns:
    - list: A list of dictionaries containing the MAC addresses and names of the available Bluetooth devices.
    """
    print("Scanning for available Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
    available_devices = []

    for address, name in nearby_devices:
        device_info = {"Adresse MAC": address, "Nom": name}
        available_devices.append(device_info)

    return available_devices

# Exemple d'utilisation :
# Remplacez par votre plage d'adresses IP pour le scan WiFi
ip_range = "192.168.1.1/24"
wifi_devices = arp_scan(ip_range)
print("Appareils WiFi connectés :")
for device in wifi_devices:
    print(device)

print("\nAppareils Bluetooth disponibles à proximité :")
bluetooth_devices = scan_available_bluetooth_devices()
for device in bluetooth_devices:
    print(device)


print(arp_scan("172.20.10.1/24"))
