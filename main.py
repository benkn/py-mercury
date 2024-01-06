from config.config import Config
from config.accounts import accounts
from services.plaid import PlaidClient

from util.logger import get_logger

logger = get_logger("mercury", Config["log_level"])

logger.info("Mercury rising!")
logger.debug("Processing %d Accounts", len(accounts))

plaidClient = PlaidClient(Config)

allTransactions = []
for account in accounts:
    transactions = plaidClient.get_transactions(
        account, Config["start_date"], Config["end_date"]
    )
    allTransactions.append(transactions)
    logger.info("Total transactions found so far: %d", len(allTransactions))

# logger.debug("debug message")
# logger.info("info message")
# logger.warning("warning message")
# logger.error("error message")
# logger.critical("critical message")
