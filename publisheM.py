import paho.mqtt.client as mqtt
import json
from datetime import datetime
import uuid
import time
import random

class LightSensor:
    def __init__(self, sensor_id, location):
        self.sensor_id = sensor_id
        self.location = location
        self.topic = f"home/sensors/light/{location}"

    def generate_data(self):
        return {
            "device_id": self.sensor_id,
            "location": self.location,
            "event_time": datetime.now().isoformat(),
            "value": random.uniform(0, 100),
            "accuracy": random.uniform(0.8, 1.0)
        }

def main():
    
    sensors = [
        LightSensor("sensor-001", "living_room"),
        LightSensor("sensor-002", "bedroom"),
        LightSensor("sensor-003", "kitchen")
    ]

   
    client = mqtt.Client()

    # Conectar al broker
    try:
        client.connect("localhost", 1883, 60)
        print("Conectado al broker MQTT")
    except:
        print("Error al conectar al broker. Asegúrate que Mosquitto esté corriendo")
        exit(1)

    try:
        while True:
            for sensor in sensors:
                data = sensor.generate_data()
                message = json.dumps(data)
                client.publish(sensor.topic, message)
                print(f"Mensaje publicado en {sensor.topic}: {message}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nDeteniendo el publicador...")
        client.disconnect()

if __name__ == "__main__":
    main()