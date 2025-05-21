import logging
import os

LOGS_DIR = '../logs'
os.makedirs(LOGS_DIR, exist_ok=True)

logging_format = app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --------------------------------
# Configuration of the Server-Loggers
# --------------------------------
server_logger = logging.getLogger('server')
server_logger.setLevel(logging.DEBUG)

if not server_logger.handlers:
    server_file_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'server.log'))
    server_file_handler.setLevel(logging.DEBUG)
    server_file_handler.setFormatter(logging_format)

    server_logger.addHandler(server_file_handler)

# --------------------------------
# Configuration of the PI4-Loggers
# --------------------------------
# pi4_logger = logging.getLogger('pi4')
# pi4_logger.setLevel(logging.DEBUG)
#
# if not pi4_logger.handlers:
#     pi4_file_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'pi4.log'))
#     pi4_file_handler.setLevel(logging.DEBUG)
#     pi4_file_handler.setFormatter(logging_format)
#
#     pi4_logger.addHandler(pi4_file_handler)

# --------------------------------
# Configuration of the Zero-Loggers
# --------------------------------

# zero_logger = logging.getLogger('zero')
# zero_logger.setLevel(logging.DEBUG)
#
# if not zero_logger.handlers:
#     zero_file_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'zero.log'))
#     zero_file_handler.setLevel(logging.DEBUG)
#     zero_file_handler.setFormatter(logging_format)
#
#     zero_logger.addHandler(zero_file_handler)

