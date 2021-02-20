import configparser, os, logging

def main():
    # Config consts
    CFG_FL_NAME = 'user.cfg'
    USER_CFG_SECTION = 'binance_user_config'

    # Init config
    config = configparser.ConfigParser()
    if not os.path.exists(CFG_FL_NAME):
        print('No configuration file (user.cfg) found! See README.')
        exit()
    config.read(CFG_FL_NAME)

    # Logger setup
    logger = logging.getLogger('crypto_trader_logger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler('crypto_trading.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # logging to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Started")

if __name__ == "__main__":
    main()