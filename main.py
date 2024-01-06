from config.config import Config
from config.accounts import accounts

from util.logger import get_logger

logger = get_logger("mercury", Config["log_level"])

logger.info("Mercury rising!")
logger.debug("Processing %d Accounts", accounts.__len__())

# logger.debug("debug message")
# logger.info("info message")
# logger.warning("warning message")
# logger.error("error message")
# logger.critical("critical message")
