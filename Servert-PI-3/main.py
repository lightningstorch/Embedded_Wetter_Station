import time

from message_service.message_service import MessageService
from config.config import user, password, server_ip, port
from my_logging.log_config import server_logger


def on_message(client, userdata, message):
    print(f"it works: {message.payload.decode()}")

def text_connection(message_service):
    message_service.subscribe(on_message, topic="sensors/pi4", qos=1)
    message_service.subscribe(on_message, topic="sensors/zero", qos=1)

    time.sleep(0.5)

    message_service.publish(topic="sensors/pi4", payload="This is the channel for pi4", qos=1)
    message_service.publish(topic="sensors/zero", payload="This is the channel for zero", qos=1)

def main():
    
    # init MQTT client
    message_service = MessageService(server_logger, user=user, password=password, server_ip=server_ip, port=int(port))

    # for testing the message_service
    text_connection(message_service)



    try:
        # the server is running
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutdown the program")
    finally:
        message_service.close()

if __name__ == "__main__":
    main()
