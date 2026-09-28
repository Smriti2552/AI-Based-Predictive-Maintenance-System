import paho.mqtt.client as mqtt
import json


BROKER = "localhost"
PORT = 1883

TOPIC = "factory/machines"


client = mqtt.Client()


client.connect(
    BROKER,
    PORT,
    60
)


def send_telemetry(data):

    message = json.dumps(data)

    client.publish(
        TOPIC,
        message
    )

    print("\nMQTT Published:")
    print(message)