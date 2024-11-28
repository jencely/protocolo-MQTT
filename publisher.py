import paho.mqtt.client as mqtt
import json
from datetime import datetime
import uuid
import time
import random

def generate_sensor_data():
    return {
        "device_id": str(uuid.uuid4()),
        "event_time": datetime.now().isoformat(),
        "value": random.uniform(0, 100),  # Valor de luz entre 0 y 100
        "accuracy": random.uniform(0.8, 1.0)  # Precisión entre 0.8 y 1.0
    }

# Configuración del cliente MQTT
client = mqtt.Client()

# Conectar al broker
try:
    client.connect("localhost", 1883, 60)
    print("Conectado al broker MQTT")
except:
    print("Error al conectar al broker. Asegúrate que Mosquitto esté corriendo")
    exit(1)

# Publicar datos cada 5 segundos
try:
    while True:
        data = generate_sensor_data()
        message = json.dumps(data)
        client.publish("home/sensors/light", message)
        print(f"Mensaje publicado: {message}")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nDeteniendo el publicador...")
    client.disconnect()