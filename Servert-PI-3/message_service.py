
import paho.mqtt.client as mqtt
import threading

from my_logging.log_config import server_logger
from urllib.parse import urlparse, parse_qs
from config.config import server_ip, port


class MessageService:
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        self.client = mqtt.Client()
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
        self.client.connect(server_ip, port, keepalive=60)
        self.client.loop_start()
    
    
    def publish(self, topic: str, payload: str, qos: int = 0):
        pass
    
    
    def subscribe(self, callback, topic: str, qos: int = 1):
        self.client.subscribe(topic=topic, qos=qos)
        self.client.message_callback_add(topic=topic, callback=callback)
        server_logger.debug(f"Topic {topic} is subscribed with own callback function {callback.__name__}")
    
    
    def _on_connect(self):
        server_logger.debug(f"Connection ist established")
        
    
    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
        self._instance = None
        
        
    
    
    









