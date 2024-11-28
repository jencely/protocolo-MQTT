import paho.mqtt.client as mqtt
import json
from datetime import datetime

class RoomController:
    def __init__(self):
        
        self.light_thresholds = {
            "living_room": 45,
            "bedroom": 40,
            "kitchen": 50
        }
        
       
        self.devices_state = {
            "living_room": {"lights": False, "blinds": "DOWN"},
            "bedroom": {"lights": False, "blinds": "DOWN"},
            "kitchen": {"lights": False, "blinds": "DOWN"}
        }

    def control_lights(self, location, state):
        previous_state = self.devices_state[location]["lights"]
        self.devices_state[location]["lights"] = state == "ON"
        if previous_state != self.devices_state[location]["lights"]:
            print(f"🔆 Luces de {location}: {state}")

    def control_blinds(self, location, state):
        previous_state = self.devices_state[location]["blinds"]
        self.devices_state[location]["blinds"] = state
        if previous_state != state:
            if state == "UP":
                print(f"⬆️ Subiendo cortinas de {location}")
            else:
                print(f"⬇️ Bajando cortinas de {location}")

    def process_message(self, payload):
        try:
            location = payload['location']
            light_value = payload['value']
            accuracy = payload['accuracy']
            
            if accuracy > 0.9:  # Solo actuamos si la medición es precisa
                if light_value < self.light_thresholds[location]:
                    self.control_lights(location, "ON")
                    self.control_blinds(location, "UP")
                else:
                    self.control_lights(location, "OFF")
                    self.control_blinds(location, "DOWN")
        except KeyError as e:
            print(f"Error: Falta el campo {e} en el mensaje")

controller = RoomController()


def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        print(f"\nMensaje recibido en {message.topic}:")
        print(f"Device ID: {payload['device_id']}")
        print(f"Location: {payload['location']}")
        print(f"Valor de luz: {payload['value']}")
        print(f"Precisión: {payload['accuracy']}")
        
        controller.process_message(payload)
            
    except json.JSONDecodeError:
        print("Error: Mensaje recibido no es un JSON válido")
    except KeyError as e:
        print(f"Error: Falta el campo {e} en el mensaje")


client = mqtt.Client()
client.on_message = on_message

try:
    client.connect("localhost", 1883, 60)
    print("Conectado al broker MQTT")
except:
    print("Error al conectar al broker. Asegúrate que Mosquitto esté corriendo")
    exit(1)

client.subscribe("home/sensors/light/#")


print("Esperando mensajes... Presiona Ctrl+C para salir")
client.loop_forever()