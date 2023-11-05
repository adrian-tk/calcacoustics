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
# .env file for ugly way to change kivy log level
# for all project
from dotenv import load_dotenv
load_dotenv()
from kivy.logger import Logger, LOG_LEVELS
# main logger
# all child logger will have this same level
logger = logging.getLogger('calac')
# log for communication, a lot of data
# all child logger will have this same level
logcom = logging.getLogger('calac.com')

def setlog(verbose='standard'):
    match verbose:
        case 'debug':
            logging.basicConfig(level=logging.INFO)
            logger.setLevel(logging.DEBUG)
            logcom.setLevel(logging.ERROR)
            Logger.setLevel(LOG_LEVELS["warning"])
        case 'silent':
            logging.basicConfig(level=logging.CRITICAL)
            logger.setLevel(logging.CRITICAL)
            logcom.setLevel(logging.CRITICAL)
            Logger.setLevel(LOG_LEVELS["critical"])
        case 'standard':
            logging.basicConfig(level=logging.INFO)
            logger.setLevel(logging.INFO)
            logcom.setLevel(logging.CRITICAL)
            Logger.setLevel(LOG_LEVELS["critical"])

if __name__ == '__main__':
    # set config level of kivy
    # run twice
    from kivy.config import Config
    Config.set('kivy', 'log_level', 'error')
    #Config.set('kivy', 'log_level', 'debug')
    Config.write()
