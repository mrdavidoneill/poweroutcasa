import logging
import logging.handlers
import time

######### DEBUG LEVELS ##########
CONSOLE_LEVEL = logging.DEBUG
FILE_LEVEL = logging.INFO
#################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter.converter = time.gmtime

# Log to console
ch = logging.StreamHandler()
ch.setLevel(CONSOLE_LEVEL)
ch.setFormatter(formatter)
logger.addHandler(ch)

# Log to file
fh = logging.handlers.RotatingFileHandler(
    'emailchecker.log', maxBytes=1024*2, backupCount=1)
fh.setLevel(FILE_LEVEL)
fh.setFormatter(formatter)
logger.addHandler(fh)
