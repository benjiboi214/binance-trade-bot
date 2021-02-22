from adapters.state import StateAdapter
from adapters.config import ConfigAccessor


class StrategyAdapter(ConfigAccessor):
    """
    TODO - Update description of StrategyAdapter
    """

    # Strings
    CONFIG_SECTION_NAME = "strategy"

    BRIDGE_COIN = "bridge_coin"

    LOG_SUCCESS_MESSAGE = "StrategyAdapter successfully initialised"
    LOG_GENERATED_THRESHOLDS_MESSAGE = "Thresholds generated for {0} through {1}"
    LOG_ACTUAL_THRESHOLDS_MESSAGE = "Thresholds {0}:\n{1}"

    def __init__(self, config, logger, client):
        super().__init__()
        self._save_config(config)
        self.__logger = logger
        self.__client = client
        self.__state = StateAdapter(config, logger)

        self.__bridge_coin_symbol = self._get_config(StrategyAdapter.BRIDGE_COIN)

        if self.__state.default_state == True:
            self.get_trade_thresholds()

        self.__logger.debug(StrategyAdapter.LOG_SUCCESS_MESSAGE)

    def get_trade_thresholds(self):
        self.__state.all_tickers = self.__client.get_all_tickers()

        self.__state.coin_table = self.generate_price_matrix(
            self.__state.coin_table, self.__bridge_coin_symbol
        )

    def generate_price_matrix(self, table, bridge_coin_symbol, parent_ticker=None):
        """
        Basic steps are:
        - Get the altcoin symbols from the first level of the data structure already stored in the coin_table
        - Iterate over these symbols, add the bridge coin symbol and get the price of the pair from binance
        - For each of these symbols, we recursively call the same function this time with the parent ticker provided.
        - We run the same loop, add bridge coin, get price.
        - Now for each coin pair we have their respective prices, divide the parent price by the child price.
        - Store it in the table and return it.
        """
        output_table = table.copy()

        for symbol in table:
            ticker = self.__state.get_ticker_by_name(symbol + bridge_coin_symbol)
            if ticker is None:
                continue
            if parent_ticker is not None:
                if ticker != parent_ticker:
                    main_symbol = parent_ticker["symbol"].split(bridge_coin_symbol)[0]
                    output_table[main_symbol][symbol] = (
                        parent_ticker["price"] / ticker["price"]
                    )
            else:
                self.generate_price_matrix(
                    table, bridge_coin_symbol, parent_ticker=ticker
                )
                self.__logger.info(
                    StrategyAdapter.LOG_GENERATED_THRESHOLDS_MESSAGE.format(
                        symbol, bridge_coin_symbol
                    )
                )
                self.__logger.debug(
                    StrategyAdapter.LOG_ACTUAL_THRESHOLDS_MESSAGE.format(
                        symbol, output_table[symbol]
                    )
                )

        return output_table

    def scout(self):
        self.__logger.debug("Scouting!")
