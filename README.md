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
| Model/Type                                 | Description                                                                                                                           | Amount |
|--------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|-------:|
| Raspberry PI 4                             | Outdoor Computer with sensor hat                                                                                                       |      1 |
| Raspberry PI Zero                          | Outdoor Computer with enviro hat                                                                                                     |      1 |
| Raspberry PI 3 Model B                     | Server mit MQTT Broker and Server program                                                                                              |      1 |
| Raspberry PI Camera Boad v2 - 8 Megapixels | Transmission of a livestream https://www.adafruit.com/product/3099                                                                     |      1 |
| Raspberry Pi Sense HAT                     | Sensor Hat with LEDs, pressure, humidity, temperature  https://www.adafruit.com/product/2738                                           |      1 |
| Pimoroni Enviro pHAT for Raspberry Pi Zero | Sensor Hat with temperature, light level, color, 3-axis motion, compas heading and analog inputs https://www.adafruit.com/product/3194 |      1 |


## Software Components
| Topic                | Description                                                                                                                                                                                                                                        |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Raspberry Pi OS      | 64/32-Bit, Lite or Desktop                                                                                                                                                                                                                         |
| Programming Language | Python 3.13+                                                                                                                                                                                                                                       |
| Library's            | paho-mqtt (Client)<br>adafruit-circuitpython-dht<br>sense-hat (for Sense HAT)<br>envirophat<br>streamlit (for the UI)<br>pydantic (for data classes (excluding PI Zero v1)<br>sqlite3 (for Database) <br> Flask and opencv-python (for Camera API) |
| MQTT                 | Mosquitto (Broker, Version ≥ 2.0)<br>Configuration under `/etc/mosquitto/mosquitto.conf`<br>`sensor/pi4` (Sense HAT)<br>`sensor/zero` (Enviro pHAT)<br>`ui/sensor_data` (bundled, for UI)<br>`sensors/light` (for light control)                 |

---

## Installation
Preparation: 
All Raspberry Pis must be set up with a compatible Linux operating system (Raspberry Pi OS). <br>
The outdoor modules (Pi 4 & Pi Zero) require the latest Python 3.13 version. <br>
UI ideally runs on a notebook or PC.  <br>
In order for all devices to communicate with each other, they must be in the same network. <br>


### Installation Raspberry Server (RPI 3)
An MQTT broker (Mosquitto) is required for the Raspberry Pi server, <br>
to receive/send the data from the outdoor sensors and forward it to the UI. <br>
The client software (Paho MQTT) must be logged into the broker with a username and password. <br>
Link to [Installation Mosquitto](https://mosquitto.org/download/)

A virtual environment must be created for pip to install the dependencies.
```text
sudo apt-get update
sudo apt-get install python3-venv
sudo apt-get install python3-pip
python3 -m venv --system-site-packages ~/server-venv
```
Now we need to activate the virtual environment
```text
source ~/server-venv/bin/activate
```

Now we can install the dependencies.
```text
pip install --upgrade pip
pip install paho-mqtt
pip install pydantic
pip install systemtools
pip install SQLAlchemy
```

Now the reposiroty can be cloned
````text
sudo apt install git
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
````

The main file must be edited and “program = ”server_main“” must be activated.
```text
sudo nano ~/Embedded_Wetter_Station/main.py
```
Edit and save (Ctrl + O, Enter, Ctrl + X)

The program can now be started
```text
cd Embedded_Wetter_Station
python3 main.py
```


### Installation Raspberry Sense-HAT (RPI 4)
The Sense HAT is required for the Raspberry Pi 4 to record the data from the outdoor sensors. <br>
This software must be installed directly on the OS.
```text
sudo apt-get install sense-hat python3-sense-hat
```

A virtual environment must be created for pip in order to install the dependencies.
```text
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-venv
python3 -m venv --system-site-packages ~/sense-hat-venv
```
Now we need to activate the virtual environment
```text
source ~/sense-hat-venv/bin/activate
```

Now we can install the dependencies
```text
pip install --upgrade pip
pip install paho-mqtt
pip install pydantic
pip install flask
pip install opencv-python
```

Now the reposiroty can be cloned
````text
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
cd Embedded_Wetter_Station
````

The main file must be edited and “program = ”pi4_main“” must be activated.
```text
sudo nano ~/Embedded_Wetter_Station/main.py
```
Edit and save (Ctrl + O, Enter, Ctrl + X)

The program can now be started
```text
cd Embedded_Wetter_Station
python3 main.py
```


### Installation Raspberry Enviro pHAT (RPI Zero)
The Sense HAT is required for the Raspberry Pi Zero (V1) in order to record the data from the outdoor sensors. <br>
This software must be installed directly on the OS.
```text
sudo apt-get install sense-hat python3-sense-hat
```

A virtual environment must be created for pip in order to install the dependencies.
```text
sudo apt-get update
sudo apt-get install python3-venv
sudo apt-get install python3-pip
sudo apt-get install python3-dev
sudo apt-get install i2c-tools
python3 -m venv --system-site-packages ~/envirophat-venv
```
Now we need to activate the virtual environment
```text
source ~/envirophat-venv/bin/activate
```

Now we can install the dependencies. The Raspberry pi Zero (V1) <br> 
does not manage the installation of pydantic, so all packages must be installed manually.
```text
pip install --upgrade pip
pip install paho-mqtt
pip install envirophat
```

Now the reposiroty can be cloned
````text
sudo apt install git
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
````

The main file must be edited and “program = ”zero_main“” must be activated.
```text
sudo nano ~/Embedded_Wetter_Station/main.py
```
Edit and save (Ctrl + O, Enter, Ctrl + X)

The program can now be started
```text
cd Embedded_Wetter_Station
python3 main.py
```


### Installation UI (Streamlit)
Streamlit is required for the UI to display the data from the outdoor sensors. <br>
The required packages must be installed with pip. <br>
```text
pip install streamlit
pip install pydantic
pip install paho-mqtt
pip install flask
pip install opencv-python
```

The reposiroty can then be cloned
````text
git clone https://github.com/DeinGitHubUsername/Embedded_Wetter_Station.git
cd Embedded_Wetter_Station
````
The main file must be edited and “program = ”ui_main“” must be activated.
Editing can be done in a text editor.

Then all you have to do is start the Streamlit app.
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
This project is licensed under the GPLv3 License. Further details on licensing can be found in the [LICENSE](LICENSE) file.

### Third-Party-License
This project uses libraries and dependencies that are each subject to their own licenses. In order to comply with these license conditions, the corresponding license texts must be provided. A complete overview of all third-party licenses can be found in [THIRD_PARTY_LICENSES.md](https://github.com/lightningstorch/Embedded_Wetter_Station/blob/main/THIRD_PARTY_LICENSES.md).

## Contact and Contributors
Manuel Spiss - https://github.com/lightningstorch <br>
Daniel Rockenschaub - https://github.com/DanielRocky <br>
Mario Howegger - https://github.com/Marrchii
