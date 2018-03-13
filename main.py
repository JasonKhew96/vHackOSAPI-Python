from utils import Utils
from user import User
from time import sleep
from time import time
import logging

VERSION = '0.0.0.1' # major.minor.build.revision

def main():
    utils = Utils()
    user = User(utils)
    cd_timer = 0
    while True:
        user.update()
        user.attack()
        if time() - cd_timer > 300: # 5 minutes
            user.withdraw()
            cd_timer = time()
        user.update()
        user.upgrade()
        logging.info('Sleep 1 minutes')
        sleep(60)



if __name__ == '__main__':
    try:
        FORMAT = '[%(asctime)s][%(module)s][%(funcName)8s][%(levelname)8s] %(message)s'
        formatter = logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%S")

        logging.basicConfig(format=FORMAT, level=logging.INFO)
        logger = logging.getLogger(__name__)

        # fh = logging.FileHandler('debug.log')
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)

        # logger.debug('debug message')
        # logger.info('info message')
        # logger.warn('warn message')
        # logger.error('error message')
        # logger.critical('critical message')
        logger.info('vHackOS-Bot: {}'.format(VERSION))
        sleep(10)
        main()
    except KeyboardInterrupt:
        logging.info('Keyboard Interrupted')
        exit()
