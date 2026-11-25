"""
Reads the MQTT settings from 'config.ini' next to this file.
Copy 'config.example.ini' to 'config.ini' and fill in your values first.
"""
import configparser
from pathlib import Path

_config_file = Path(__file__).parent / 'config.ini'
if not _config_file.is_file():
    raise FileNotFoundError(
        f"{_config_file} not found. Copy config.example.ini to config.ini and adjust it."
    )

_config = configparser.ConfigParser()
_config.read(_config_file)

server_ip = _config['mqtt']['host']
port = _config['mqtt']['port']
user = _config['mqtt']['user']
password = _config['mqtt']['password']

database_type = _config['database']['type']
database_connection = _config['database']['connection_string']
