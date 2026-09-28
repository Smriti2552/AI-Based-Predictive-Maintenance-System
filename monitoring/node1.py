import random
import time

from mqtt.producer import send_telemetry


while True:

    telemetry = {

        "node": "Node-1",

        "cpu_usage": round(random.uniform(20, 50), 2),

        "memory_usage": round(random.uniform(30, 55), 2),

        "network_traffic": round(random.uniform(10, 40), 2),

        "power_consumption": round(random.uniform(180, 220), 2),

        "num_executed_instructions": random.randint(20000, 50000),

        "execution_time": round(random.uniform(1, 2), 2),

        "energy_efficiency": round(random.uniform(0.85, 1.00), 2),

        "task_type": random.choice(
            ["Compute", "IO", "Network"]
        ),

        "task_priority": "Low",

        "task_status": random.choice(
            ["Running", "Completed"]
        )
    }


    print(telemetry)

    send_telemetry(telemetry)

    time.sleep(5)