import sys

from config.config import Config
from config.accounts import accounts
from services.plaid import PlaidClient
from util.logger import get_logger

logger = get_logger("remove_item", Config["log_level"])


def find_account(name):
    matches = [a for a in accounts if a.name.lower() == name.lower()]
    if len(matches) == 1:
        return matches[0]
    return None


def main(argv):
    if len(argv) < 1:
        print("Usage: mise run remove-item -- <account name> [--yes]")
        print("Known accounts:")
        for account in accounts:
            print(f"  - {account.name}")
        return 1

    confirmed = "--yes" in argv or "-y" in argv
    name = " ".join(a for a in argv if a not in ("--yes", "-y"))

    account = find_account(name)
    if account is None:
        logger.error("No account found matching %r", name)
        return 1

    if not confirmed:
        answer = input(
            f"This will permanently unlink '{account.name}' (item_id={account.item_id}) "
            "from Plaid and invalidate its access token. Continue? [y/N] "
        )
        if answer.strip().lower() != "y":
            logger.info("Aborted.")
            return 1

    plaid_client = PlaidClient(Config)
    response = plaid_client.remove_item(account)

    if "error" in response:
        logger.error("Failed to remove '%s': %s", account.name, response["error"])
        return 1

    logger.info("Successfully removed '%s' from Plaid.", account.name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
