import os
import time
from utils import FileOperations
from adapters.config import ConfigAdapter
from adapters.log import LoggingAdapter

def main():
    # Config Initialisation
    CONFIG_DIR = os.getenv("CONFIG_DIR", default="/config")
    CONFIG_NAME = os.getenv("CONFIG_NAME", default="user.cfg")
    config = ConfigAdapter(CONFIG_DIR, CONFIG_NAME)

    # Logging Initialisation
    logger = LoggingAdapter(config)

    client = ExchangeClientAdapter(config)

    # file_name = "/state/.current_coin_sample"
    # current_coin_name = "TEST"
    # def write_coin_backup(file, content):
    #     file.write(content)

    # FileOperations.write(file_name, current_coin_name, write_coin_backup)
if __name__ == "__main__":
    main()
