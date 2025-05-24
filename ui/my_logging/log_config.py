import logging
import os

LOGS_DIR = '../logs'
os.makedirs(LOGS_DIR, exist_ok=True)

logging_format = app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --------------------------------
# Configuration of the Server-Loggers
# --------------------------------
ui_logger = logging.getLogger('ui')
ui_logger.setLevel(logging.DEBUG)

if not ui_logger.handlers:
    ui_file_handler = logging.FileHandler(os.path.join(LOGS_DIR, 'ui.log'))
    ui_file_handler.setLevel(logging.DEBUG)
    ui_file_handler.setFormatter(logging_format)

    ui_logger.addHandler(ui_file_handler)


