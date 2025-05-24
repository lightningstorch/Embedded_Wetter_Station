import json
import queue
import time
from datetime import datetime

from server_pi3.database.database import init_db, store_data
from server_pi3.dataclass.dataclass_models import MeasuredData
from message_service.message_service import MessageService
from server_pi3.config.config import user, password, server_ip, port
from server_pi3.my_logging.log_config import server_logger

message_service_queue = queue.Queue()

def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    message_service_queue.put(payload)
    server_logger.info(f"Received message: {payload}")
    print(f"Received message: {payload}")

def subscribe_pis(message_service):
    message_service.subscribe(on_message, topic="sensors/pi4", qos=1)
    message_service.subscribe(on_message, topic="sensors/zero", qos=1)
    message_service.subscribe(on_message, topic="sensors/light", qos=1)

def light(message_service, payload):
    message_service.publish(topic="sensors/pi4_light", payload=payload, qos=1)


def server_main():
    print("Starting the server...")

    # init MQTT client
    message_service = MessageService(server_logger, user=user, password=password, server_ip=server_ip, port=int(port))

    # subscribe to the sensors
    subscribe_pis(message_service)

    # init Database
    init_db()

    # variables
    light_on = False
    switch_from_ui = False

    try:
        while True:
            # look in the queue
            if message_service_queue.empty():
                time.sleep(1)
                continue

            # get the message from the queue
            payload = json.loads(message_service_queue.get())

            values = None
            if payload.get("client") == "ui":
                if light_on:
                    # turn light off
                    switch_from_ui = False
                    light_on = False
                    light(message_service, "light off")
                else:
                    # turn light on
                    switch_from_ui = True
                    light_on = True
                    light(message_service, "light on")
                continue

            elif payload.get("client") == "pi4":
                # process the message
                values = MeasuredData(
                    client=payload.get("client"),
                    time=datetime.now(),
                    temperature=payload.get("temperature"),
                    humidity=payload.get("humidity"),
                    pressure=payload.get("pressure"),
                )

            elif payload.get("client") == "zero":
                # process the message
                values = MeasuredData(
                    client=payload.get("client"),
                    time=datetime.now(),
                    brightness=payload.get("brightness"),
                )

                if values.brightness >= 50 and not switch_from_ui:
                    light(message_service, "light off")
                elif values.brightness < 50 and not switch_from_ui:
                    light(message_service, "light on")


            # save the my_data in DB
            store_data(values)

            # send it to the MQTT broker for ui visualization
            send_values = values.model_dump_json()
            message_service.publish(topic="ui/sensor_data", payload=send_values, qos=1)

    except KeyboardInterrupt:
        print("Shutdown the program")
    finally:
        message_service.close()
