import time

from message_service.message_service import MessageService
from pi_zero.config.config import user, password, server_ip, port
from pi_zero.dataclass.dataclass_models import SensorData
from pi_zero.zero_logging.log_config import zero_logger



def hat_data():

    temp = 25.5
    pressure = 1013.25
    light_level = 10

    values = SensorData(
        client="zero",
        temperature=temp,
        pressure=pressure,
        light_level=light_level
    )

    return values

def zero_main():
    message_service = MessageService(user=user, password=password, server_ip=server_ip, port=int(port), logging=zero_logger)

    try:
        while True:

            payload = hat_data()

            # Send sensor data
            message_service.publish(topic="sensors/pi4", payload=payload.model_dump_json(), qos=1)

            time.sleep(5)

    except KeyboardInterrupt:
        print("Shutdown the program")
    finally:
        message_service.close()





