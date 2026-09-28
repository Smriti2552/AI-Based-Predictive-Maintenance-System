import random
import time

from mqtt.producer import send_telemetry


while True:

    telemetry = {

        "node": "Node-2",

        "cpu_usage": round(random.uniform(55, 80), 2),

        "memory_usage": round(random.uniform(60, 85), 2),

        "network_traffic": round(random.uniform(40, 70), 2),

        "power_consumption": round(random.uniform(220, 280), 2),

        "num_executed_instructions": random.randint(50000, 90000),

        "execution_time": round(random.uniform(2, 4), 2),

        "energy_efficiency": round(random.uniform(0.65, 0.85), 2),

        "task_type": random.choice(
            ["Compute", "IO", "Network"]
        ),

        "task_priority": random.choice(
            ["Medium", "High"]
        ),

        "task_status": random.choice(
            ["Running", "Waiting"]
        )
    }


    print(telemetry)

    send_telemetry(telemetry)

    time.sleep(5)