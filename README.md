# Práctica MQTT - Sistema de Control de Iluminación
Este proyecto implementa un sistema de control de iluminación usando MQTT, que incluye sensores de luz y controladores para luces y cortinas.
Requisitos Previos

Ubuntu (o cualquier distribución Linux)
Python 3.x
pip3
Mosquitto broker

# Instalación

Instalar Mosquitto:

bashCopysudo apt update
sudo apt install mosquitto
sudo apt install mosquitto-clients

Crear y activar entorno virtual:

bashCopypython3 -m venv venv
source venv/bin/activate

Instalar dependencias:

bashCopypip install paho-mqtt
Estructura del Proyecto
Copymqtt_project/
├── mosquitto.conf
├── publisher.py
├── subscriber.py
├── README.md

# Configuración

Crear archivo mosquitto.conf:

Copylistener 1883
protocol mqtt
allow_anonymous true
persistence false
log_type all
Ejecución

Iniciar el broker Mosquitto (Terminal 1):

bashCopymosquitto -c mosquitto.conf

Iniciar el subscriber (Terminal 2):

bashCopypython subscriber.py

Iniciar el publisher (Terminal 3):

bashCopypython publisher.py
Verificación
El sistema está funcionando correctamente si:

El publisher muestra mensajes enviados cada 5 segundos
El subscriber muestra mensajes recibidos y decisiones de control
Se observan cambios en el estado de luces y cortinas según los valores de luz

Detener el Sistema

Detener publisher y subscriber: Ctrl+C en cada terminal
Detener Mosquitto: Ctrl+C en su terminal