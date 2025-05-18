import configparser
from pathlib import Path

"""
This module reads the configuration from the 'config.ini' file and
provides important parameters.
"""

_config = configparser.ConfigParser()
_config.read(Path(__file__).parent / 'config.ini')

server_ip = _config['mqtt']['host']
port = _config['mqtt']['port']
user = _config['mqtt']['user']
password = _config['mqtt']['password']


