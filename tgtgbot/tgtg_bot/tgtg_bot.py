import datetime as dt
import os
import time
from random import SystemRandom

import requests
from tgtg import TgtgClient


class TgtgBot:  # pylint:disable=unused-variable
    """Class for our Too Good To Go bot"""

    def __init__(
        self, item_id: int = 678105, message: str = "FRICHTIIII", scan_period: int = 120
    ) -> None:
        """Initializes the Bot

        Parameters
        ----------
        item_id: int
            Item ID of the Too Good To Go product you want to catch
        message: str
            Message sent by the Telegram Bot
        scan_period: int
            The period during which you want the bot to refresh the item availability in minutes
        """
        self.client = TgtgClient(
            access_token=os.environ["TGTG_ACCESS_TOKEN"],
            refresh_token=os.environ["TGTG_REFRESH_TOKEN"],
            user_id=os.environ["TGTG_USER_ID"],
            cookie=os.environ["TGTG_COOKIE"],
        )
        self.item_id = item_id
        self.message = message
        self.end_time = dt.datetime.now() + dt.timedelta(seconds=scan_period * 60)

    def is_item_available(self) -> bool:
        """Check if the item is available

        Returns
        -------
        bool
            If the item is available
        """
        item = self.client.get_item(item_id=self.item_id)
        return int(item["items_available"]) > 0

    def send_message(self) -> None:
        """Sends the message"""
        url = (
            f"https://api.telegram.org/bot{os.environ['TGTG_TELEGRAMBOT_TOKEN']}/sendMessage?"
            f"chat_id={os.environ['TGTG_TELEGRAMBOT_CHAT_ID']}&text={self.message}"
        )
        requests.get(url=url, timeout=5).json()

    def run(self) -> None:
        """Run the bot: refresh and send message when item available or scan period elapsed"""
        refresh = True

        while refresh:
            now = dt.datetime.now()
            try:
                frichti_available = self.is_item_available()
            except requests.exceptions.ReadTimeout:
                frichti_available = False

            if frichti_available:
                self.send_message()
                refresh = False
            else:
                refresh = now < self.end_time

            time.sleep(SystemRandom().randrange(30, 60))
