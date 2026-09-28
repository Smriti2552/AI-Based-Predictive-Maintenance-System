import random
import time

from mqtt.producer import send_telemetry


while True:

    telemetry = {

        "node": "Node-3",

        "cpu_usage": round(random.uniform(85, 100), 2),

        "memory_usage": round(random.uniform(85, 100), 2),

        "network_traffic": round(random.uniform(70, 100), 2),

        "power_consumption": round(random.uniform(300, 400), 2),

        "num_executed_instructions": random.randint(100000, 150000),

        "execution_time": round(random.uniform(4, 8), 2),

        "energy_efficiency": round(random.uniform(0.30, 0.60), 2),

        "task_type": random.choice(
            ["Compute", "Network"]
        ),

        "task_priority": "High",

        "task_status": random.choice(
            ["Running", "Waiting"]
        )
    }


    print(telemetry)

    send_telemetry(telemetry)

    time.sleep(5)