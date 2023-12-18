# This is a sample Python script.
# Importez la classe CameraManager depuis votre module (supposons que le module s'appelle camera_manager.py)

from Classes.Eleve import *
from API.InfluxDB import envoyer_donnees

NUMBER_OF_SENSORS = 2  # Bluetooth & Wifi
BLUETOOTH_CONFIDENCE = 0.4  # Donné par l'utilisateur
WIFI_CONFIDENCE = 0.6  # Donné par l'utilisateur


def evaluate_presence(presences):
    final_presence = {}
    precision = 0
    for presence in presences.values():
        nom = presence.get('Nom')
        prenom = presence.get('Prenom')
        presenceWifi = presence.get('PresenceWifi')
        presenceBluetooth = presence.get('PresenceBluetooth')
        presence_value = presenceWifi == 'True' or presenceBluetooth == 'True'
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
    post_final_presence(final_presence)


def post_final_presence(final_presence):
    final_presence_eleve = []
    for person in final_presence.values():
        nom = person.get('Nom')
        prenom = person.get('Prenom')
        presence = True if person.get('Presence') == 'True' else False
        certitude = round(float(person.get('Precision')))
        final_presence_eleve.append(Eleve(nom, prenom, presence, certitude))
    envoyer_donnees(final_presence_eleve,"Cours A")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from Classes.CameraManager import CameraManager
    from Classes.MqttManager import MqttManager

    camManager = CameraManager()  # Press Maj+F10 to execute it or replace it with your code.
    mqttManager = MqttManager()

    # camManager.recuperation_images()
    # camManager.analyze_images_in_folder()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
