import queue
import time
from datetime import datetime

from database.database import init_db, store_data
from dataclasses.dataclass_models import MeasuredData
from message_service.message_service import MessageService
from config.config import user, password, server_ip, port
from my_logging.log_config import server_logger

message_service_queue = queue.Queue()

def on_message(client, userdata, message):
    payload = message.payload.decode()
    message_service_queue.put(payload)

def subscribe_pis(message_service):
    message_service.subscribe(on_message, topic="sensors/pi4", qos=1)
    message_service.subscribe(on_message, topic="sensors/zero", qos=1)

def main():
    
    # init MQTT client
    message_service = MessageService(server_logger, user=user, password=password, server_ip=server_ip, port=int(port))

    # subscribe to the sensors
    subscribe_pis(message_service)

    # init Database
    init_db()

    try:
        while True:
            # look in the queue
            if message_service_queue.empty():
                time.sleep(1)
                continue

            # get the message from the queue
            payload = message_service_queue.get()

            # process the message
            values = MeasuredData(
                time=datetime.now(),
                temperature=payload.get("temperature"),
                humidity=payload.get("humidity"),
                pressure=payload.get("pressure"),
                light_level=payload.get("light_level", None),
            )

            # save the data in DB
            store_data(values)

            # send it to the MQTT broker for UI visualization
            message_service.publish(topic="ui/sensor_data", payload=payload.model_dump_json(), qos=1)

    except KeyboardInterrupt:
        print("Shutdown the program")
    finally:
        message_service.close()

if __name__ == "__main__":
    main()
