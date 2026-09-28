import paho.mqtt.client as mqtt
import json
from datetime import datetime
import csv
import os

from src.predict import predict


# ==========================
# MQTT Configuration
# ==========================

BROKER = "localhost"
PORT = 1883

TOPIC = "factory/machines"


# ==========================
# Prediction Report File
# ==========================

REPORT_FILE = "reports/predictions.csv"


print("Current Working Directory:", os.getcwd())
print("Saving predictions to:", os.path.abspath(REPORT_FILE))


os.makedirs(
    "reports",
    exist_ok=True
)


# Create CSV file if it does not exist

if not os.path.exists(REPORT_FILE):

    with open(
        REPORT_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
    [
        "Time",
        "Node",
        "Status",
        "Risk Score",
        "Reasons",
        "CPU",
        "Memory",
        "Network",
        "Power"
    ]
)


# ==========================
# MQTT Message Handler
# ==========================

def on_message(
    client,
    userdata,
    msg
):

    # Convert JSON message

    data = json.loads(
        msg.payload.decode()
    )


    print("\n==============================")
    print("Received Telemetry")
    print("==============================")

    print(data)



    # ==========================
    # AI Prediction
    # ==========================

    result = predict(data)


    print("\nAI Prediction")
    print("------------------------------")

    print(
        "Node:",
        data["node"]
    )

    print(
        "Status:",
        result["status"]
    )

    print(
        "Risk Score:",
        result["risk_score"],
        "%"
    )

    print(
        "Reasons:",
        result["reasons"]
    )


    # ==========================
    # Save Prediction History
    # ==========================

    with open(
        REPORT_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)


        writer.writerow(
    [
        datetime.now(),
        data["node"],
        result["status"],
        result["risk_score"],
        ", ".join(result["reasons"]),

        data["cpu_usage"],
        data["memory_usage"],
        data["network_traffic"],
        data["power_consumption"]
    ]
)


    print(
        "Prediction saved."
    )



# ==========================
# MQTT Client
# ==========================

client = mqtt.Client()


client.on_message = on_message


client.connect(
    BROKER,
    PORT,
    60
)


client.subscribe(
    TOPIC
)


print(
    "MQTT Consumer Started..."
)

print(
    "Waiting for telemetry..."
)


client.loop_forever()