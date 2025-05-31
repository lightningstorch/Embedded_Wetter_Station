# Embedded_Wetter_Station
This weather station is a small and simple integration of a weather 
station with two outdoor sensor points and one indoor server.
These communicate with an MQTT broker.

---
## Table of Contents
1. [Project Overview](#project-overview)
2. [Hardware Components](#hardware-components)
3. [Software Components](#software-components)
4. [Installation](#installation)
5. [Usage](#usage)
7. [License](#license)
8. [Contact and Contributors](#contact-and-contributors)

---

## Project Overview
This project is a weather station that collects data from various outdoor 
sensors and displays it on a UI. The system is designed to run on multible
Raspberry Pi devices, with one device acting as a server and MQTT-Broker.


## Hardware Components
| Modell/Typ                                 | Beschreibung                                                                                                                           | Anzahl |
|--------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|-------:|
| Raspberry PI 4                             | Outdoor Computer with sensor hat                                                                                                       |      1 |
| Raspberry PI Zero                          | Outdoor Computer with sensor hat2                                                                                                      |      1 |
| Raspberry PI 3 Model B                     | Server mit MQTT Broker and Server program                                                                                              |      1 |
| Raspberry PI Camera Boad v2 - 8 Megapixels | Transmission of a livestream https://www.adafruit.com/product/3099                                                                     |      1 |
| Raspberry Pi Sense HAT                     | Sensor Hat with LEDs, pressure, humidity, temperature  https://www.adafruit.com/product/2738                                           |      1 |
| Pimoroni Enviro pHAT for Raspberry Pi Zero | Sensor Hat with temperature, light level, color, 3-axis motion, compas heading and analog inputs https://www.adafruit.com/product/3194 |      1 |


## Software Components
| Betriebssystem                              | Beschreibung

|.............................................|..............................................................................................................................................................:
| Rasberry PI OS                               | 32-Bit, Lite oder Desktop
| Programmiersprache                            | Python 3.9+ 
| Bibliotheken                                 | paho-mqtt(Client), adafruit-circuitpython-dht, sense-                                                  hat (für Sense HAT), envirophat, streamlit (für das                                                     UI), pydantic (für Typen/Modelle im UI),sqlite3 für                                                     Datenbank
|MQTT                                          | Mosquitto (Broker, Version ≥ 2.0), Konfiguration                                                       erfolgt standardmäßig unter           
                                                 /etc/mosquitto/mosquitto.conf, sensor/outdoor1 (Sense                                                   HAT), sensor/outdoor2 (Enviro pHat),     
                                                   ui/sensor_data(gebündelt, für UI), 
                                                   sensors/light(Steurung für Licht) 


## Installation
Vorbereitung: 
Alle Raspberry Pis müssen mit Raspberry Pi OS aufgesetzt sein. Auf die Outdoor-Module (Pi 4 & Pi Zero) kommt dieselbe Python-Umgebung, das UI läuft idealerweise auf  Notebook/PC. Alle Geräte sollten im selben Netzwerk sein.

Das Repository klonen
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
cd Embedded_Wetter_Station

Update und Mosquitto installieren 
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv mosquitto -y

Virtuelle Umgebung und alles nötige Installieren

RPI 4 + Sense HAT
cd pi4
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

RPI Zero + Enviro pHAT
cd ../pi_zero
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

RPI Zero + Relais
cd ../light_control
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

Streamlit-U
cd ../ui
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../requirements.txt

Mosquitto-Broker konfigurieren
listener 1883
allow_anonymous true


Mosquitto aktivieren und starten
sudo systemctl enable mosquitto
sudo systemctl restart mosquitto


## Usage
Mosquitto-Broker starten
sudo systemctl start mosquitto
mosquitto -v

Outdoor-Sensoren starten
cd ~/Embedded_Wetterstation/pi4
source venv/bin/activate
python pi4_main.py

 Outdoor 2 (RPI Zero + Enviro pHAT
 cd ~/Embedded_Wetterstation/pi_zero
source venv/bin/activate
python zero_main.py

Lichtsteuerung (RPI Zero)
cd ~/Embedded_Wetterstation/light_control
source venv/bin/activate
python light_control.py

Streamlit-UI starten
cd ~/Embedded_Wetterstation

Streamlit-App starten
streamlit run main.py

## License
sind in https://github.com/lightningstorch/Embedded_Wetter_Station/licenses

## Contact and Contributors
Manuel Spiss - https://github.com/lightningstorch <br>
Daniel Rockenschaub - https://github.com/DanielRocky <br>
Mario Howegger - https://github.com/Marrchii
