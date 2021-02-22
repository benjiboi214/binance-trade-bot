import os
import time
from adapters.config import ConfigAccessor, ConfigAdapter
from adapters.log import LoggingAdapter
from adapters.binance import ExchangeClientAdapter
from adapters.strategy import StrategyAdapter


class TradeBot(ConfigAccessor):
    """
    TODO - Update description of the Trade Bot
    """

    # Strings
    CONFIG_SECTION_NAME = "bot"

    BOT_SLEEP_PERIOD = "sleep_period"
    MAX_SCOUT_LOOPS = "max_scout_loops"

    LOG_INIT_SUCCESS_MESSAGE = "Successfully initialised TradeBot"
    LOG_START_BOT_MESSAGE = "Starting TradeBot"

    def __init__(self, config, logger, strategy):
        super().__init__()
        self._save_config(config)
        self.__logger = logger
        self.__strategy = strategy

        self.__logger.debug(TradeBot.LOG_INIT_SUCCESS_MESSAGE)

    def start(self):
        self.__logger.info(TradeBot.LOG_START_BOT_MESSAGE)

        # Test / Example Loop
        sleep_period = self._get_int_config(TradeBot.BOT_SLEEP_PERIOD)
        max_scout_loops = self._get_int_config(TradeBot.MAX_SCOUT_LOOPS)
        count = 0
        while count <= max_scout_loops:
            time.sleep(sleep_period)
            count += 1
            self.__strategy.scout()


def main():
    # Config Initialisation
    CONFIG_DIR = os.getenv("CONFIG_DIR", default="/config")
    CONFIG_NAME = os.getenv("CONFIG_NAME", default="user.cfg")
    config = ConfigAdapter(CONFIG_DIR, CONFIG_NAME)

    # Logging Initialisation
    logger = LoggingAdapter(config)

    # ExchangeClient Initialisation
    client = ExchangeClientAdapter(config, logger)

    # Strategy
    strategy = StrategyAdapter(config, logger, client)

    # Start Bot
    bot = TradeBot(config, logger, strategy)

    try:
        bot.start()
    except Exception as e:
        logger.exception("Fatal error in the bot runtime")


if __name__ == "__main__":
    main()
