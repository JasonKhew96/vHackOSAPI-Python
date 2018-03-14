from utils import Utils
from user import User
from time import sleep
from time import time
from lxml import html
from distutils.version import StrictVersion
import requests
import logging

VERSION = '0.0.0.2' # major.minor.build.revision
APP_VER = '1.38'

def getappver():
    url = 'https://play.google.com/store/apps/details?id=cc.vhack.vhackxtmobile&hl=en'
    response = requests.get(url)
    html_content = html.fromstring(response.content)
    version = html_content.xpath('//div[@itemprop="softwareVersion"]')[0].text.strip()
    return version


def main():
    utils = Utils()
    user = User(utils)
    cd_timer = 0
    while True:
        user.update()
        user.attack()
        if time() - cd_timer > 600: # 5 minutes
            user.withdraw()
            cd_timer = time()
        user.update()
        user.upgrade()
        user.update()
        user.printuserinfo()
        logging.info('Sleep 1 minutes')
        sleep(60)



if __name__ == '__main__':
    try:
        FORMAT = '[%(asctime)s][%(module)s][%(funcName)8s][%(levelname)8s] %(message)s'
        formatter = logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%s")

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

        newappver = getappver()
        if StrictVersion(newappver) > StrictVersion(APP_VER):
            logger.error('\nNew vHackOS-app detected: {}\nSupported version: {}'.format(newappver, APP_VER))
            exit()

        logger.info('vHackOS-app: {}'.format(newappver))
        sleep(10)
        main()
    except KeyboardInterrupt:
        logging.info('Keyboard Interrupted')
        exit()
