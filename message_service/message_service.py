import paho.mqtt.client as mqtt
import threading

class MessageService:
    """
    A messaging service for connecting to the MQTT broker Mosquitto.
    It is possible to publish and subscribe to messages.
    To publish a message, publish() must be called with a desired topic.
    When subscribing with subscribe(), the topic and a callback function must be specified.
    This callback function is called as soon as a message arrives.

    The class is designed as a singleton and will always return the same instance when an object
    is initialized or created several times. Create an object will always return the same instance.
    """

    _instance = None
    _lock = threading.Lock()
    
    def __init__(self, logging, user: str, password: str, server_ip: str, port: int, ):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._user = user
        self._password = password
        self._server_ip = server_ip
        self._port = port
        self.logging = logging

        self.client = mqtt.Client(protocol=mqtt.MQTTv5)
        self.client.username_pw_set(username=self._user, password=self._password)
        self.client.on_connect = self._on_connect
        self._init_connection()
        self._initialized = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def _init_connection(self):
        self.logging.info(f"Initialise the Connection to the MQTT-Broker {self._server_ip}:{self._port}")
        self.client.connect(self._server_ip, self._port, keepalive=60)
        self.client.loop_start()

    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
        """
        Publish sends a message with the desired topic.
        The message is sent to all registered subscribers who subscribe to the exact topic.

        Args:
            topic: MQTT topic for the message exchange (e.g "sensors/temperature")
            payload: the information to be sent
            qos: the Quality of Service with value {0, 1, 2}
            retain: When True, all messages that are sent are automatically delivered to a new subscriber.
                    False (the default) this is not done.
        """
        result = self.client.publish(topic, payload=payload, qos=qos, retain=retain)
        if result[0] == mqtt.MQTT_ERR_SUCCESS:
            self.logging.debug(f"Message sent to {topic}: {payload}")
        else:
            self.logging.error(f"Error when sending to {topic}: {result[0]}")

    def subscribe(self, callback, topic: str, qos: int = 1):
        """
        Subscribe to a MQTT topic and register a callback function.

        The function subscribes to an MQTT topic and links the callback function.
        As soon as a message arrives, the callback function is called for each individual message.

        Args:
            callback: signature of the callback function is "func(client, userdata, message)"
                      function is called when a message is received
            topic:  MQTT topic for the message exchange (e.g "sensors/temperature")
            qos:  the Quality of Service with value {0, 1, 2}
        """
        self.client.subscribe(topic=topic, qos=qos)
        self.client.message_callback_add(topic, callback)
        self.logging.debug(f"Topic '{topic}' is subscribed with a own callback function {callback.__name__}")

    def _on_connect(self, client, userdata, flags, reason_code, properties = None):
        """
        The function is called after a connection is attempted. The code “reason_code”
        returns the error. If the code is 0, the connection has not been
        successfully established, otherwise the connection failed.
        """
        if reason_code != 0:
            self.logging.debug(f"Connection failed")
        else:
            self.logging.debug(f"Connection ist established")

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
        self._instance = None
