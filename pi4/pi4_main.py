from sense_hat import SenseHat
import json
import time


from pi4.dataclass.dataclass_models import SensorData
from message_service.message_service import MessageService
from pi4.config.config import user, password, server_ip, port
from pi4.pi4_logging.log_config import pi4_logger

# Initialize the SenseHat
sense = SenseHat()

def sensor_data():
    while True:
        temp = round(sense.get_temperature(),2)
        humidity = round(sense.get_humidity(),2)
        pressure = round(sense.get_pressure(),2)

        payload = SensorData(
            client="pi4",
            temperature=temp,
            humidity=humidity,
            pressure=pressure
        )

        return payload


def light_level_callback(client, userdata, message):
    payload = message.payload.decode()

    if payload == "light on":
        sense.low_light = False
        sense.clear(255, 255, 255)
    elif payload == "light off":
        sense.low_light = False
        sense.clear(0, 0, 0)
    elif payload == "light on low":
        sense.low_light = True
        sense.clear(255, 255, 255)


def pi4_main():

    message_service = MessageService(user=user, password=password, server_ip=server_ip, port=int(port), logging=pi4_logger)

    # Subscribe for light level (light)
    message_service.subscribe(light_level_callback, topic="sensors/pi4_light", qos=1)

    try:
        while True:
            # get sensor data
            payload = sensor_data()

            # Send sensor data
            message_service.publish(topic="sensors/pi4", payload=payload.model_dump_json(), qos=1)

            time.sleep(5)

    except KeyboardInterrupt:
        print("Shutdown the program")
    finally:
        message_service.close()
        sense.clear()