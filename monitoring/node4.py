import random
import time

from mqtt.producer import send_telemetry


while True:

    telemetry = {

        "node": "Node-4",

        "cpu_usage": round(random.uniform(20, 95), 2),

        "memory_usage": round(random.uniform(30, 95), 2),

        "network_traffic": round(random.uniform(20, 90), 2),

        "power_consumption": round(random.uniform(180, 350), 2),

        "num_executed_instructions": random.randint(
            30000, 120000
        ),

        "execution_time": round(
            random.uniform(1, 6), 2
        ),

        "energy_efficiency": round(
            random.uniform(0.40, 0.95), 2
        ),

        "task_type": random.choice(
            ["Compute", "IO", "Network"]
        ),

        "task_priority": random.choice(
            ["Low", "Medium", "High"]
        ),

        "task_status": random.choice(
            ["Running", "Waiting", "Completed"]
        )
    }


    print(telemetry)

    send_telemetry(telemetry)

    time.sleep(5)