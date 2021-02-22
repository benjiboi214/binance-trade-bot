from binance.client import Client as BinanceClient

from adapters.config import ConfigAccessor


class ExchangeClientAdapter(ConfigAccessor):
    """
    Abstraction to organise the calls to the binance client.
    TODO - Document the interface
    TODO - Make this an abstract class
    TODO - Move Binance implementation to a concrete class
    """

    # Strings
    CONFIG_SECTION_NAME = "binance-client"
    CONFIG_API_KEY = "api_key"
    CONFIG_API_SECRET_KEY = "api_secret_key"

    LOG_SUCCESS_MESSAGE = "ExchangeClient successfully initialised"

    def __init__(self, config, logger):
        super().__init__()
        self._save_config(config)
        self.__logger = logger

        api_key = self._get_config(ExchangeClientAdapter.CONFIG_API_KEY)
        api_secret_key = self._get_config(ExchangeClientAdapter.CONFIG_API_SECRET_KEY)
        self.__client = BinanceClient(api_key, api_secret_key)

        self.__logger.debug(ExchangeClientAdapter.LOG_SUCCESS_MESSAGE)

    def get_all_tickers(self):
        return self.__client.get_all_tickers()
