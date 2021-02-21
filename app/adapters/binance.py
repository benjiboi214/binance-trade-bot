from binance.client import Client as BinanceClient


class ExchangeClientAdapter:
    """
    Abstraction to organise the calls to the binance client.
    TODO - Document the interface
    TODO - Make this an abstract class
    TODO - Move Binance implementation to a concrete class
    """

    CONFIG_SECTION_NAME = "binance-client"

    def __init__(self, config, logger):
        self.__logger = logger
        api_key = config.get(self.CONFIG_SECTION_NAME, "api_key")
        api_secret_key = config.get(self.CONFIG_SECTION_NAME, "api_secret_key")
        self.client = BinanceClient(api_key, api_secret_key)
        self.__logger.debug("ExchangeClient successfully initialised")

    def get_all_tickers(self):
        return self.client.get_all_tickers()
