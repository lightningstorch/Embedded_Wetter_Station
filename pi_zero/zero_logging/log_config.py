import logging
import os

LOGS_DIR = '../logs'
os.makedirs(LOGS_DIR, exist_ok=True)

logging_format = app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --------------------------------
# Configuration of the Zero-Loggers
# --------------------------------
zero_logger = logging.getLogger('zero')
zero_logger.setLevel(logging.DEBUG)

if not zero_logger.handlers:
    zero_file_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'zero.log'))
    zero_file_handler.setLevel(logging.DEBUG)
    zero_file_handler.setFormatter(logging_format)

    zero_logger.addHandler(zero_file_handler)

