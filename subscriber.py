import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Callback cuando se recibe un mensaje
def on_message(client, userdata, message):
    try:
        # Decodificar el mensaje JSON
        payload = json.loads(message.payload.decode())
        
        # Extraer valores
        light_value = payload['value']
        accuracy = payload['accuracy']
        device_id = payload['device_id']
        event_time = payload['event_time']
        
        print(f"\nMensaje recibido del dispositivo {device_id}")
        print(f"Tiempo: {event_time}")
        print(f"Valor de luz: {light_value}")
        print(f"Precisión: {accuracy}")
        
        # Lógica de control
        if light_value < 50 and accuracy > 0.9:
            print("🔆 Encendiendo las luces de la habitación")
        else:
            print("⬛ Apagando las luces de la habitación")
            
    except json.JSONDecodeError:
        print("Error: Mensaje recibido no es un JSON válido")
    except KeyError as e:
        print(f"Error: Falta el campo {e} en el mensaje")

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_message = on_message

# Conectar al broker
try:
    client.connect("localhost", 1883, 60)
    print("Conectado al broker MQTT")
except:
    print("Error al conectar al broker. Asegúrate que Mosquitto esté corriendo")
    exit(1)

# Suscribirse al tópico
client.subscribe("home/sensors/light")

# Iniciar el loop
print("Esperando mensajes... Presiona Ctrl+C para salir")
client.loop_forever()