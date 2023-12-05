# This is a sample Python script.
# Importez la classe CameraManager depuis votre module (supposons que le module s'appelle camera_manager.py)
from CameraManager import CameraManager
import paho.mqtt.client as mqtt

class MqttManager:
    def __init__(self):
        client = mqtt.Client("digi_mqtt_test")  # Create instance of client with client ID “digi_mqtt_test”
        client.on_connect = self.on_connect  # Define callback function for successful connection
        client.on_message = self.on_message  # Define callback function for receipt of a message
        # client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
        client.connect('127.0.0.1', 2883)
        client.loop_forever()  # Start networking daemon
        # Créez une instance de la classe CameraManager
        # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

    def on_connect(self,client, userdata, flags, rc):  # The callback for when the client connects to the broker
        # Print result of connection attempt
        print("Connected with resultcode {0}".format(str(rc)))
        # Subscribe to the topic “digitest/test1”, receive any messages published on it
        client.subscribe("raspberry/bluetooth")
        client.subscribe("raspberry/wifi")

    def on_message(self,client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        print("Message received-> "+ msg.topic)  # Print a received msg
        match msg.topic:
            case "raspberry/bluetooth":
                self.on_message_bluetooth(msg.payload)
            case "raspberry/wifi":
                self.on_message_wifi(msg.payload)
            case _:
                exit()

    def on_message_bluetooth(self,msg):
        print("List of bluetooth addresses-> "+ str(msg))  # Print a received msg

    def on_message_wifi(self,msg):
        print("List of wifi addresses-> "+ str(msg))  # Print a received msg


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    camManager = CameraManager()# Press Maj+F10 to execute it or replace it with your code.
    mqttManager = MqttManager()

    #camManager.recuperation_images()
    #camManager.analyze_images_in_folder()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
