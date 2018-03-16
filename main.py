import logging
from distutils.version import StrictVersion
from random import uniform
from time import sleep, time
from user import User

import requests
from lxml import html

from utils import Utils

VERSION = '0.0.0.4'  # major.minor.build.revision
APP_VER = '1.39'


def getappver():
    url = 'https://play.google.com/store/apps/details?id=cc.vhack.vhackxtmobile&hl=en'
    response = requests.get(url)
    html_content = html.fromstring(response.content)
    try:
        version = html_content.xpath('//div[@itemprop="softwareVersion"]')[
            0].text.strip()
    except IndexError:
        return getappver()
    return version


def main():
    utils = Utils()
    user = User(utils)
    cd_timer = 0
    while True:
        user.update()
        user.attack()
        user.update()
        if time() - cd_timer > 600: # 10 minutes
            user.withdraw()
            user.update()
            user.collectmining()
            user.update()
            cd_timer = time()
        user.upgradesingle()
        user.update()
        user.printuserinfo()
        mseconds = uniform(60.0, 600.0)
        logging.info('Sleep {} second(s)'.format(round(mseconds)))
        sleep(mseconds)


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
            logger.error(
                '\nNew vHackOS-app detected: {}\nSupported version: {}'.format(
                    newappver, APP_VER))
            exit()

        logger.info('vHackOS-app: {}'.format(newappver))
        sleep(10)
        main()
    except KeyboardInterrupt:
        logging.info('Keyboard Interrupted')
        exit()
