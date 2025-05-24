import time

from message_service.message_service import MessageService
from pi_zero.config.config import user, password, server_ip, port
from pi_zero.dataclass.dataclass_models import SensorData
from pi_zero.zero_logging.log_config import zero_logger

from envirophat import weather, light



def hat_data():
    brightness = light.light()

    values = SensorData(
        client="zero",
        brightness=brightness
    )

    return values

def zero_main():
    message_service = MessageService(user=user, password=password, server_ip=server_ip, port=int(port), logging=zero_logger)

    try:
        while True:

            payload = hat_data()

            # Send sensor data
            message_service.publish(topic="sensors/zero", payload=payload.to_json(), qos=1)

            time.sleep(5)

    except KeyboardInterrupt:
        print("Shutdown the program")
    finally:
        message_service.close()





