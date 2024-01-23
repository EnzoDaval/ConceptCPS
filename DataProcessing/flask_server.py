import glob
import json
import os

from flask import Flask, request, jsonify, send_file, url_for
from flask import Flask, request, jsonify
from flask_cors import CORS
import paho.mqtt.client as mqtt

from DataProcessing.main import get_final_presence

MQTT_HOST = "192.168.80.177"
MQTT_PORT = 2883 #1884
app = Flask(__name__)
cors = CORS(app)

client = mqtt.Client("Server Flask")
client.connect(MQTT_HOST, MQTT_PORT)


@app.route("/get_image")
def get_image():
    # Utilisez la fonction glob pour rechercher le fichier commencant par "EIIN"
    image_files = glob.glob(os.path.join(os.getcwd(), 'EIIN*.png'))

    if image_files:
        # Utilisez le premier fichier correspondant trouvé
        image_path = image_files[0]
        return send_file(image_path, mimetype='image/png')
    else:
        return jsonify({'error': 'Image not found'})

@app.route("/calculate", methods=["POST"])
def recevoir_notification():
    # Traitez la notification ici
    data = request.get_json()

    if "classNumber" in data:
        class_number = data["classNumber"]
        print(f'Notification reçue pour la classe {class_number} !')
        # Utilisez class_number comme nécessaire dans votre logique

    get_final_presence()

    image_url = url_for('get_image', _external=True)
    return jsonify({'message': 'Notification reçue avec succès', 'image_url': image_url})


@app.route("/configs", methods=["POST"])
def recevoir_configs():
    configs = request.json  # Récupère les configurations depuis la requête POST en format JSON

    # Créer une liste de dictionnaires à partir de la structure de données
    config_list = [{"type_dispositif": key.capitalize(), "sampling": value} for key, value in configs.items()]
    print("Configs reçues :", config_list)

    # Écrire la liste dans un fichier JSON
    with open("Res/Sampling.json", 'w') as fichier:
        json.dump(config_list, fichier, indent=2)

    client.publish('sampling/update','Update')

    return jsonify({'message': 'Configs reçues avec succès'})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
    client.disconnect()
