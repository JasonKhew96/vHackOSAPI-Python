"""Main entry point"""
import logging
from distutils.version import StrictVersion
from random import uniform
from time import sleep, time

import requests
from lxml import html

from network import Network
from vhackosapi import VHackOSAPI

VERSION = "0.0.0.6"  # major.minor.build.revision
APP_VER = "1.39"


def getappver():
    """Get vHackOS version from play store."""
    url = 'https://play.google.com/store/apps/details?id=cc.vhack.vhackxtmobile&hl=en'
    response = requests.get(url)
    html_content = html.fromstring(response.content)
    try:
        version = html_content.xpath('//div[@itemprop="softwareVersion"]')[
            0].text.strip()
    except IndexError:
        return getappver()
    return version


def mainloop():
    """Main bot loop."""
    network = Network()
    api = VHackOSAPI(network)
    cd_timer = 0
    while True:
        api.update()
        api.attack()
        api.update()
        if time() - cd_timer > 600:  # 10 minutes
            api.withdraw()
            api.update()
            api.collectmining()
            api.update()
            cd_timer = time()
        api.upgradesingle()
        api.update()
        api.printuserinfo()
        mseconds = uniform(60.0, 600.0)
        logging.info('Sleep %i second(s)', round(mseconds))
        sleep(mseconds)


def main():
    """Main entry point."""
    try:
        log_format = "[%(asctime)s][%(module)s][%(funcName)8s][%(levelname)8s] %(message)s"
        # FORMATTER = logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%s")

        logging.basicConfig(format=log_format, level=logging.INFO)
        logger = logging.getLogger(__name__)

        # fh = logging.FileHandler('debug.log')
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)

        # logger.debug('debug message')
        # logger.info('info message')
        # logger.warn('warn message')
        # logger.error('error message')
        # logger.critical('critical message')
        logger.info('vHackOS-Bot: %s', VERSION)

        newappver = getappver()
        if StrictVersion(newappver) > StrictVersion(APP_VER):
            logger.error(
                '\nNew vHackOS-app detected: %s\nSupported version: %s',
                newappver, APP_VER)
            exit()

        logger.info('vHackOS-app: %s', newappver)
        sleep(10)
        mainloop()
    except KeyboardInterrupt:
        logging.info('Keyboard Interrupted')
        exit()


if __name__ == '__main__':
    main()
