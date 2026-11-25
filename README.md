# Embedded Weather Station

A small weather station built from three Raspberry Pis that talk to each other over MQTT. Two outdoor nodes measure the weather, an indoor Raspberry Pi runs the MQTT broker and stores the readings, and a Streamlit dashboard shows them live. It was built as a team project for the course Embedded and Pervasive Systems.

## How it works

```
 Pi 4 + Sense HAT ──── sensors/pi4 ────┐
 (temp, humidity, pressure, camera)    │
                                       ▼
 Pi Zero + Enviro pHAT ─ sensors/zero ─▶  Pi 3: Mosquitto + server  ── ui/sensor_data ──▶  Streamlit UI
 (brightness)                          │  (stores readings in SQLite)  ◀── sensors/light ───  (light toggle)
                                       │
 Pi 4 LED matrix ◀── sensors/pi4_light ┘
```

- The Pi 4 reads temperature, humidity and pressure from its Sense HAT every 5 seconds and publishes them on `sensors/pi4`. It also serves a camera livestream (Flask, port 5000, `/video_feed`).
- The Pi Zero reads the light level from its Enviro pHAT every 5 seconds and publishes it on `sensors/zero`.
- The server on the Pi 3 stores every reading in SQLite and forwards it to the UI on `ui/sensor_data`. When it gets dark, it switches on the Sense HAT's LED matrix through `sensors/pi4_light`.
- The UI shows the readings and can switch the light by hand via `sensors/light`.

## Hardware

| Part | Used for |
|---|---|
| Raspberry Pi 4 with [Sense HAT](https://www.adafruit.com/product/2738) | outdoor node: temperature, humidity, pressure, LED light |
| [Raspberry Pi Camera Board v2](https://www.adafruit.com/product/3099) (8 MP) | livestream from the Pi 4 |
| Raspberry Pi Zero with [Pimoroni Enviro pHAT](https://www.adafruit.com/product/3194) | outdoor node: light level |
| Raspberry Pi 3 Model B | MQTT broker (Mosquitto) and server |
| Notebook or PC | Streamlit UI |

## Software

- Raspberry Pi OS (32 or 64 bit, Lite or Desktop)
- Python 3.13
- Mosquitto 2.0 or newer as MQTT broker
- Python packages: paho-mqtt, pydantic, SQLAlchemy, Streamlit, Flask, opencv-python, sense-hat, envirophat. Which device needs which package is listed under Installation.

All devices have to be in the same network.

## Installation

Each part runs from the same repository. Clone it on every device:

```bash
git clone https://github.com/lightningstorch/Embedded_Wetter_Station.git
cd Embedded_Wetter_Station
```

Every part reads its MQTT settings from a `config.ini` that is not part of the repository. Copy the example file of the part you install and enter the broker's IP address, the MQTT user and its password:

```bash
cp server_pi3/config/config.example.ini server_pi3/config/config.ini   # Pi 3
cp pi4/config/config.example.ini pi4/config/config.ini                 # Pi 4
cp pi_zero/config/config.example.ini pi_zero/config/config.ini         # Pi Zero
cp ui/config/config.example.ini ui/config/config.ini                   # UI
```

### Server (Pi 3)

Install Mosquitto (see the [Mosquitto download page](https://mosquitto.org/download/)) and turn on password authentication in `/etc/mosquitto/mosquitto.conf` with one user per client (`mosquitto_passwd`). The user names in the example configs are `server`, `PI4`, `Zero` and `ui`. Then set up a virtual environment:

```bash
sudo apt-get update
sudo apt-get install python3-venv python3-pip
python3 -m venv --system-site-packages ~/server-venv
source ~/server-venv/bin/activate
pip install --upgrade pip
pip install paho-mqtt pydantic SQLAlchemy
```

### Outdoor node with Sense HAT (Pi 4)

The Sense HAT library is installed through the system package manager:

```bash
sudo apt-get update
sudo apt-get install sense-hat python3-sense-hat python3-venv python3-pip
python3 -m venv --system-site-packages ~/sense-hat-venv
source ~/sense-hat-venv/bin/activate
pip install --upgrade pip
pip install paho-mqtt pydantic flask opencv-python
```

### Outdoor node with Enviro pHAT (Pi Zero)

The first Pi Zero cannot install pydantic, so this node only uses paho-mqtt and envirophat:

```bash
sudo apt-get update
sudo apt-get install python3-venv python3-pip python3-dev i2c-tools
python3 -m venv --system-site-packages ~/envirophat-venv
source ~/envirophat-venv/bin/activate
pip install --upgrade pip
pip install paho-mqtt envirophat
```

### UI (notebook or PC)

```bash
pip install streamlit pydantic paho-mqtt
```

## Usage

`main.py` starts one part of the system. The part is chosen with the first argument: `server`, `pi4`, `zero` or `ui`.

```bash
# Pi 3
sudo systemctl start mosquitto
source ~/server-venv/bin/activate
python3 main.py server

# Pi 4
source ~/sense-hat-venv/bin/activate
python3 main.py pi4

# Pi Zero
source ~/envirophat-venv/bin/activate
python3 main.py zero

# UI
streamlit run main.py
```

Logs are written to `../logs` relative to the working directory.

## Authors

- Manuel Spiss ([lightningstorch](https://github.com/lightningstorch))
- Daniel Rockenschaub ([DanielRocky](https://github.com/DanielRocky))
- Mario Howegger ([Marrchii](https://github.com/Marrchii))

## License

© 2025 Manuel Spiss, Mario Howegger and Daniel Rockenschaub. Licensed under the GPLv3, see [LICENSE.txt](LICENSE.txt). The licenses of the libraries used are collected in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
