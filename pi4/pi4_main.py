from sense_hat import SenseHat
import json
import time

import pi4_logging
from pi4.dataclass.dataclass_models import SensorData
from message_service.message_service import MessageService
from pi4.config.config import user, password, server_ip, port

# Initialize the SenseHat
sense = SenseHat()

def sensor_data():
    while True:
        temp = round(sense.get_temperature(),2)
        humidity = round(sense.get_humidity(),2)
        pressure = round(sense.get_pressure(),2)

        payload = SensorData(
            temperature=temp,
            humidity=humidity,
            pressure=pressure
        )

        sense.clear()

        return payload


def light_level_callback(client, userdata, message):
    payload = message.payload.decode()

    sense.clear()
    if payload == "light on":
        sense.clear(255, 255, 0)
    elif payload == "light off":
        sense.clear(0, 0, 0)
    elif payload == "light on low":
        sense.clear(255, 255, 0)
        sense.low_light = True


def pi4_main():

    message_service = MessageService(user=user, password=password, server_ip=server_ip, port=int(port), logging=pi4_logging)

    # Subscribe for light level (light)
    message_service.subscribe(light_level_callback, topic="sensor/zero", qos=1)

    try:
        while True:
            # get sensor data
            payload = sensor_data()

            # Send sensor data
            message_service.publish(topic="sensor/pi4", payload=payload.model_dump_json(), qos=1)

            time.sleep(5)

    except KeyboardInterrupt:
        print("Shutdown the program")
    finally:
        message_service.close()
        sense.clear()


if __name__ == "__main__":
    main()