import logging
import os

LOGS_DIR = '../logs'
os.makedirs(LOGS_DIR, exist_ok=True)

logging_format = app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --------------------------------
# Configuration of the App-Loggers
# --------------------------------
server_logger = logging.getLogger('server')
server_logger.setLevel(logging.DEBUG)

if not server_logger.handlers:
    server_file_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'server.log'))
    server_file_handler.setLevel(logging.DEBUG)
    server_file_handler.setFormatter(logging_format)

    server_logger.addHandler(server_file_handler)

