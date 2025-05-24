import json
import time
import streamlit as st
import paho.mqtt.client as mqtt

from message_service.message_service import MessageService
from ui.my_data.my_data import SensorData
from ui.my_logging.log_config import ui_logger
from ui.config.config import user, password, server_ip, port

sensor_data = SensorData()

def main():
    # init message_service
    #message_service = MessageService(user=user, password=password, server_ip=server_ip, port=int(port), logging=ui_logger)

    st.set_page_config("Smart Weather Station", layout="wide")
    st.title("🌦️ Smart Weather Station")

    temp_box      = st.empty()
    hum_box       = st.empty()
    light_box     = st.empty()
    img_box       = st.empty()
    button_col1, button_col2 = st.columns(2)


    if button_col1.button("💡 Lampe an/aus"):
        #message_service.publish(topic="sensors/pi4_light", payload="toggle_light", qos=1)
        st.info("Lampe toggeln…")


    while True:
        if sensor_data.temp is not None:
          temp_box.metric("🌡️ Temperatur", f"{sensor_data.temp:.1f} °C")
        if sensor_data.hum is not None:
           hum_box.metric("💧 Luftfeuchtigkeit", f"{sensor_data.hum:.1f} %")
        if sensor_data.brightness is not None:
           light_box.metric("🔆 Helligkeit", f"{sensor_data.brightness:.1f} %")
        #if sensor_data["camera_frame"] is not None:
           #img_box.image(sensor_data["camera_frame"], caption="Live-Bild", use_column_width=True)

        time.sleep(1)

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    sensor_data.temp = payload.get("temperatur")
    sensor_data.hum = payload.get("humidity")
    sensor_data.brightness = payload.get("brightness")


def app():
    main()