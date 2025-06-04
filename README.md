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
8. [Third-Party-License](#third-party-license)
9. [Contact and Contributors](#contact-and-contributors)

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
| Betriebssystem        | Beschreibung                                                                                                                                                                                                                         |
| --------------------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Raspberry Pi OS       | 64/32-Bit, Lite oder Desktop                                                                                                                                                                                                         |
| Programmiersprache    | Python 3.13+                                                                                                                                                                                                                         |
| Bibliotheken          | paho-mqtt (Client)<br>adafruit-circuitpython-dht<br>sense-hat (für Sense HAT)<br>envirophat<br>streamlit (für das UI)<br>pydantic (für Typen/Modelle im UI)<br>sqlite3 (für Datenbank)                                               |
| MQTT                  | Mosquitto (Broker, Version ≥ 2.0)<br>Konfiguration unter `/etc/mosquitto/mosquitto.conf`<br>`sensor/pi4` (Sense HAT)<br>`sensor/zero` (Enviro pHAT)<br>`ui/sensor_data` (gebündelt, für UI)<br>`sensors/light` (Steuerung für Licht) |

---

## Installation
Vorbereitung: 
Alle Raspberry Pis müssen mit einem Kompatiblen Linux Betriebssystem (Raspberry Pi OS) aufgesetzt sein. <br>
Die Outdoor-Module (Pi 4 & Pi Zero) benötigen die aktuelle Python 3.13 Version. <br>
UI läuft idealerweise auf einem Notebook oder PC.  <br>
Damit alle Geräte miteinander kommunizieren können, müssen sie sich im selben Netzwerk befinden. <br>


### Installation Raspberry Server (RPI 3)
Für den Raspberry Pi Server wird ein MQTT-Broker (Mosquitto) benötigt,  <br>
um die Daten der Outdoor-Sensoren zu empfangen/senden und an die UI weiterzuleiten. <br>
Die Client-Software (Paho MQTT) müssen mit einem Usernamen und Passwort am Broker angemeldet werden. <br>
Link zu [Installation Mosquitto](https://mosquitto.org/download/)

Für pip muss eine virtuelle Umgebung erstellt werden, um die Abhängigkeiten zu installieren.
```text
sudo apt-get update
sudo apt-get install python3-venv
sudo apt-get install python3-pip
python3 -m venv --system-site-packages ~/server-venv
```
nun müssen wir die virtuelle Umgebung aktivieren
```text
source ~/server-venv/bin/activate
```

Nun können wir die Abhängigkeiten installieren.
```text
pip install --upgrade pip
pip install paho-mqtt
pip install pydantic
pip install systemtools
pip install SQLAlchemy
```

Nun kann das Reposiroty geklont werden
````text
sudo apt install git
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
````

Die Main-Datei muss bearbeitet werden und "program = "server_main"" aktiviert werden.
```text
sudo nano ~/Embedded_Wetter_Station/main.py
```
Bearbeiten und speichern (Strg + O, Enter, Strg + X)

Nun kann das Programm gestartet werden
```text
python3 ~/Embedded_Wetter_Station/main.py
```


### Installation Raspberry Sense-HAT (RPI 4)
Für den Raspberry Pi 4 wird der Sense HAT benötigt, um die Daten der Outdoor-Sensoren zu erfassen. <br>
Diese Software muss direkt auf dem OS installiert werden.
```text
sudo apt-get install sense-hat python3-sense-hat
```

Für pip muss eine virtuelle Umgebung erstellt werden, um die Abhängigkeiten zu installieren.
```text
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-venv
python3 -m venv --system-site-packages ~/sense-hat-venv
```
nun müssen wir die virtuelle Umgebung aktivieren
```text
source ~/sense-hat-venv/bin/activate
```

Nun können wir die Abhängigkeiten installieren
```text
pip install --upgrade pip
pip install paho-mqtt
pip install pydantic
pip install flask
pip install opencv-python
```

Nun kann das Reposiroty geklont werden
````text
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
cd Embedded_Wetter_Station
````

Die Main-Datei muss bearbeitet werden und "program = "pi4_main"" aktiviert werden.
```text
sudo nano ~/Embedded_Wetter_Station/main.py
```
Bearbeiten und speichern (Strg + O, Enter, Strg + X)

Nun kann das Programm gestartet werden
```text
python3 ~/Embedded_Wetter_Station/main.py
```


### Installation Raspberry Enviro pHAT (RPI Zero)
Für den Raspberry Pi Zero (V1) wird der Sense HAT benötigt, um die Daten der Outdoor-Sensoren zu erfassen. <br>
Diese Software muss direkt auf dem OS installiert werden.
```text
sudo apt-get install sense-hat python3-sense-hat
```

Für pip muss eine virtuelle Umgebung erstellt werden, um die Abhängigkeiten zu installieren.
```text
sudo apt-get update
sudo apt-get install python3-venv
sudo apt-get install python3-pip
sudo apt-get install python3-dev
sudo apt-get install i2c-tools
python3 -m venv --system-site-packages ~/envirophat-venv
```
nun müssen wir die virtuelle Umgebung aktivieren
```text
source ~/envirophat-venv/bin/activate
```

Nun können wir die Abhängigkeiten installieren. Der Raspberry pi Zero (V1) <br> 
schafft die installation von pydantic nicht, daher müssen alle pakete händisch installiert werden.
```text
pip install --upgrade pip
pip install paho-mqtt
pip install envirophat
```

Nun kann das Reposiroty geklont werden
````text
sudo apt install git
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
````

Die Main-Datei muss bearbeitet werden und "program = "zero_main"" aktiviert werden.
```text
sudo nano ~/Embedded_Wetter_Station/main.py
```
Bearbeiten und speichern (Strg + O, Enter, Strg + X)

Nun kann das Programm gestartet werden
```text
python3 ~/Embedded_Wetter_Station/main.py
```


### Installation UI (Streamlit)
Für die UI wird Streamlit benötigt, um die Daten der Outdoor-Sensoren anzuzeigen. <br>
Die benötigten Pakete müssen mit pip installiert werden. <br>
```text
pip install streamlit
pip install pydantic
pip install paho-mqtt
pip install flask
pip install opencv-python
```

Danach kann das Reposiroty geklont werden
````text
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
cd Embedded_Wetter_Station
````
Die Main-Datei muss bearbeitet werden und "program = "ui_main"" aktiviert werden.
Das Bearbeiten kann in einem Texteditor erfolgen.

Danach muss nur noch die Streamlit-App gestartet werden.
```text
streamlit run main.py
```

---

## Usage

### Start the MQTT Broker & Server 
```text
sudo systemctl start mosquitto
source ~/server-venv/bin/activate
python3 ~/Embedded_Wetter_Station/main.py
```

### Outdoor Sensors

#### Raspberry Pi 4 (Sense HAT)  
```text
source ~/sense-hat-venv/bin/activate
python3 ~/Embedded_Wetter_Station/main.py
```

#### Raspberry Pi Zero (Enviro pHAT)  
```text
source ~/envirophat-venv/bin/activate
python3 ~/Embedded_Wetter_Station/main.py
```

### Streamlit UI  
```text
cd ~/Embedded_Wetter_Station
streamlit run main.py
```
---

## License
© 2025 Manuel Spiss, Mario Howegger und Daniel Rockenschaub.  
This project is licensed under the [NAME DER LIZENZ] License. Further details on licensing can be found in the [LICENSE](LICENSE) file.

### Third-Party-License
This project uses libraries and dependencies that are each subject to their own licenses. In order to comply with these license conditions, the corresponding license texts must be provided. A complete overview of all third-party licenses can be found in [THIRD_PARTY_LICENSES.md](https://github.com/lightningstorch/Embedded_Wetter_Station/blob/main/THIRD_PARTY_LICENSES.md).

## Contact and Contributors
Manuel Spiss - https://github.com/lightningstorch <br>
Daniel Rockenschaub - https://github.com/DanielRocky <br>
Mario Howegger - https://github.com/Marrchii
