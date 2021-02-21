class StrategyAdapter(ConfigAccessor):
    """
    TODO - Update description of StrategyAdapter
    """

    # Strings
    CONFIG_SECTION_NAME = "strategy"

    LOG_SUCCESS_MESSAGE = "StrategyAdapter successfully initialised"

    def __init__(self, config, logger):
        super().__init__()
        self._save_config(config)
        self.__logger = logger

        self.__logger.debug(StrategyAdapter.LOG_SUCCESS_MESSAGE)