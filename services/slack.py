import requests

from util.logger import get_logger


class SlackClient:
    def __init__(self, config):
        self.webhook_url = config.get("slack_webhook_url")
        self.logger = get_logger("slack", config["log_level"])

    def send_alert(self, message):
        """Post a message to Slack via an incoming webhook, if one is configured."""
        if not self.webhook_url:
            return

        try:
            response = requests.post(self.webhook_url, json={"text": message}, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error("Failed to send Slack alert: %s", e)
