from sense_hat import SenseHat
import json
import time
from message_service.message_service import MessageService

sense = SenseHat()

def send_sensor_data(message_service):
    while True:
        temp = round(sense.get_temperature(),2)
        humidity = round(sense.get_humidity(),2)

        payload = json.dumps({
            "temp": temp,
            "humidity": humidity
        })

        message_service.publish(topic="sensor/pi4", payload=payload, qos=1)
        time.sleep(10)

        