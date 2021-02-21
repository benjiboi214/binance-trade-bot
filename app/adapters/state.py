import json
import os

from adapters.config import ConfigAccessor
from utils import FileOperations


class StateBackupNotFound(Exception):
    pass


class SupportedCoinsFileNotFound(Exception):
    pass


class UnsupportedCoin(Exception):
    pass


class StateAdapter(ConfigAccessor):
    """
    TODO - Update description of State Adapter
    """

    # Strings
    CONFIG_SECTION_NAME = "state"
    CONFIG_BACKUP_DIRECTORY = "backup_directory"
    CONFIG_BACKUP_FILENAME = "backup_filename"
    CONFIG_START_COIN = "start_coin"
    CONFIG_SUPPORTED_COINS_FILENAME = "supported_coins_filename"

    BACKUP_COIN_TABLE = "coin_table"
    BACKUP_CURRENT_COIN = "current_coin"

    LOG_SUCCESS_MESSAGE = "State successfully initialised"
    LOG_INIT_FROM_BACKUP_MESSAGE = "Initialising state using backup file at %s"
    LOG_INIT_FROM_DEFAULTS_MESSAGE = "Initialising state using defaults"
    LOG_UNSUPPORTED_COIN_MESSAGE = (
        "'{0}' {1} not found in list of supported coins:\n {2}"
    )
    LOG_STATE_BACKUP_NOT_FOUND_MESSAGE = "State backup file does not exist at {0}."
    LOG_SUPPORTED_COINS_FILE_NOT_FOUND_MESSAGE = (
        "Unable to locate supported coins list at {}"
    )

    def __init__(self, config, logger):
        super().__init__()
        self._save_config(config)
        self.__logger = logger

        self.__supported_coins = self.__get_supported_coins_from_file()
        self.__backup_path = self.__get_backup_path()
        self.__default_state = False

        try:
            self.__load_state_from_backup()
        except StateBackupNotFound as e:
            self.__logger.warning("%s", e)
            self.__initialise_default_state()

        self.__logger.debug(StateAdapter.LOG_SUCCESS_MESSAGE)

    def __check_coin_supported(self, origin, coin):
        if not coin in self.__supported_coins:
            raise UnsupportedCoin(
                StateAdapter.LOG_UNSUPPORTED_COIN_MESSAGE.format(
                    origin, coin, self.__supported_coins
                )
            )

    @property
    def current_coin(self):
        return self.__current_coin

    @current_coin.setter
    def current_coin(self, current_coin):
        self.__check_coin_supported("@current_coin.setter", current_coin)
        self.__backup_state(current_coin=current_coin)
        self.__current_coin = current_coin

    @property
    def coin_table(self):
        return self.__coin_table

    @coin_table.setter
    def coin_table(self, coin_table):
        self.default_state = False
        self.__coin_table = coin_table
        self.__backup_state(coin_table=coin_table)

    @property
    def default_state(self):
        return self.__default_state

    def __backup_state(self, current_coin=None, coin_table=None):
        if current_coin is None:
            current_coin = self.current_coin

        if coin_table is None:
            coin_table = self.coin_table

        backup_data_structure = {
            StateAdapter.BACKUP_CURRENT_COIN: current_coin,
            StateAdapter.BACKUP_COIN_TABLE: coin_table,
        }

        FileOperations.write(
            self.__backup_path, backup_data_structure, FileOperations.write_json
        )

    def __load_state_from_backup(self):
        if not os.path.isfile(self.__backup_path):
            raise StateBackupNotFound(
                StateAdapter.LOG_STATE_BACKUP_NOT_FOUND_MESSAGE.format(
                    self.__backup_path
                )
            )

        self.__logger.info(
            StateAdapter.LOG_INIT_FROM_BACKUP_MESSAGE, self.__backup_path
        )

        backup_data = FileOperations.read(self.__backup_path, FileOperations.read_json)

        self.__current_coin = backup_data[StateAdapter.BACKUP_CURRENT_COIN]
        self.__coin_table = backup_data[StateAdapter.BACKUP_COIN_TABLE]

    def __initialise_default_state(self):
        self.__logger.info(StateAdapter.LOG_INIT_FROM_DEFAULTS_MESSAGE)

        start_coin = self._get_config(StateAdapter.CONFIG_START_COIN)
        self.__check_coin_supported(StateAdapter.CONFIG_START_COIN, start_coin)

        self.__current_coin = start_coin
        self.__coin_table = dict(
            (
                coin_entry,
                dict(
                    (coin, 0) for coin in self.__supported_coins if coin != coin_entry
                ),
            )
            for coin_entry in self.__supported_coins
        )
        self.default_state = True

        self.__backup_state()

    def __get_backup_path(self):
        backup_directory = self._get_config(StateAdapter.CONFIG_BACKUP_DIRECTORY)
        backup_filename = self._get_config(StateAdapter.CONFIG_BACKUP_FILENAME)
        return os.path.join(backup_directory, backup_filename)

    def __get_supported_coins_from_file(self):
        supported_coins_filename = self._get_config(
            StateAdapter.CONFIG_SUPPORTED_COINS_FILENAME
        )
        supported_coins_path = os.path.join(
            self._config.config_dir, supported_coins_filename
        )

        if not os.path.isfile(supported_coins_path):
            raise SupportedCoinsFileNotFound(
                StateAdapter.LOG_SUPPORTED_COINS_FILE_NOT_FOUND_MESSAGE.format(
                    supported_coins_path
                )
            )

        def read_function(open_file):
            return open_file.read().upper().splitlines()

        return FileOperations.read(supported_coins_path, read_function)
