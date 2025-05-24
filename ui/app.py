import json
import time
from queue import Queue

import streamlit as st
import paho.mqtt.client as mqtt
from streamlit.testing.v1.element_tree import Toggle

from message_service.message_service import MessageService
from ui.my_data.my_data import SensorData, ToggleLight
from ui.my_logging.log_config import ui_logger
from ui.config.config import user, password, server_ip, port

message_queue = Queue()

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    SensorData(
        temperature=payload.get("temperature"),
        humidity=payload.get("humidity"),
        pressure=payload.get("pressure"),
        brightness=payload.get("brightness"),
    )
    message_queue.put(payload)

def app():
    if "sensor_data" not in st.session_state:
        st.session_state.sensor_data = SensorData()

    if "message_service" not in st.session_state:
        st.session_state.message_service = MessageService(
            user=user, password=password, server_ip=server_ip, port=int(port), logging=ui_logger
        )
        time.sleep(1)
        st.session_state.message_service.subscribe(on_message, topic="ui/sensor_data", qos=1)

    st.set_page_config("Smart Weather Station", layout="wide")
    st.title("🌦️ Smart Weather Station")

    button_col1, _ = st.columns(2)
    temperature_box = st.empty()
    humidity_box = st.empty()
    pressure_box = st.empty()
    light_box = st.empty()
    img_box = st.empty()


    if button_col1.button("💡 Lampe an/aus"):
        print("Lampe an/aus")
        payload = ToggleLight(client="ui", toggle=True)
        st.session_state.message_service.publish(
            topic="sensors/light", payload=payload.model_dump_json(), qos=1
        )

    while True:
        if not message_queue.empty():
            payload = message_queue.get()
            st.session_state.sensor_data.temperature = payload.get("temperature")
            st.session_state.sensor_data.humidity = payload.get("humidity")
            st.session_state.sensor_data.pressure = payload.get("pressure")
            st.session_state.sensor_data.brightness = payload.get("brightness")

        data = st.session_state.sensor_data
        if data.temperature is not None:
            temperature_box.metric("🌡️ Temperatur", f"{data.temperature:.1f} °C")
        if data.humidity is not None:
            humidity_box.metric("💧 Luftfeuchtigkeit", f"{data.humidity:.1f} %")
        if data.pressure is not None:
            pressure_box.metric("🌪️ Luftdruck", f"{data.pressure:.1f} PA")
        if data.brightness is not None:
            light_box.metric("🔆 Helligkeit", f"{data.brightness:.1f} lux")