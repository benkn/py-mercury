import logging
from config.config import Config

from util.logger import get_logger


logger = get_logger("mercury", logging.DEBUG)

logger.info("Mercury rising!")
logger.info("Configuration: ")
logger.info("Configuration: %s", Config)


# logger.debug("debug message")
# logger.info("info message")
# logger.warning("warning message")
# logger.error("error message")
# logger.critical("critical message")
