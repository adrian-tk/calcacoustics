"""module for working with loggers
format loggers, turn on or off some modules ie. kivy
set levels and other stuff to ensure consistent logging
for all app
"""

import logging

# format for logging
LOGFORMAT="%(levelname)-8s[%(name)s]\
     [%(filename)s][%(funcName)s] %(message)s"
LOGFILEFORMAT="%(asctime)s - %(levelname)-8s\
        [%(name)s][%(filename)s:%(lineno)d]\
        [%(funcName)s] %(message)s"
#logging.basicConfig(level=logging.DEBUG, format=LOGFORMAT)
# root logger, every module will have this unless 
# specified another below
logging.basicConfig(level=logging.INFO)
# .env file for ugly way to change kivy log level
# for all project
from dotenv import load_dotenv
load_dotenv()
from kivy.logger import Logger, LOG_LEVELS
Logger.setLevel(LOG_LEVELS["warning"])
# main logger
# all child logger will have this same level
logger = logging.getLogger('calac')
logger.setLevel(logging.DEBUG)
# log for communication, a lot of data
# all child logger will have this same level
logcom = logging.getLogger('calac.com')
logcom.setLevel(logging.ERROR)
