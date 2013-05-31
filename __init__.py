
from logging.handlers import RotatingFileHandler
from pollster.conf import settings_local
import sys
import logging

LEVEL = logging.DEBUG

filename = None
filemode = None

filename = settings_local.LOG_FILE
filemode = 'w'
    
logger = logging.getLogger('')
logger.setLevel(LEVEL)
formatter = logging.Formatter("[%(asctime)s] %(name)s | %(levelname)s | %(message)s")
        
ch = logging.StreamHandler()
ch.setLevel(LEVEL)
# add formatter to ch
ch.setFormatter(formatter)
logger.addHandler(ch)

# Add the log message handler to the logger

ch = RotatingFileHandler(filename, maxBytes=25000000, backupCount=10)
#ch = logging.FileHandler(filename, filemode)

ch.setLevel(LEVEL)
ch.setFormatter(formatter)
# add ch to logger        
logger.addHandler(ch)
