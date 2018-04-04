"""Network management"""
import json
import logging
import os
import sqlite3
from exceptions import CredentialsChangedException
from exceptions import CredentialsExpiredException
from time import sleep, time

import requests

import utils
from config import Config

ENDPOINT = "https://api.vhack.cc/mobile/15/"


class Network:
    """Network class handle all request before sending to vhack server."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = Config("config.yml")
        if not os.path.isfile('vhackos.db'):
            self._create_db()
        self.user_agent = utils.generate_ua(
            self.config.username + self.config.password)
        self.request = requests.Session()
        self.request.headers = {
            'User-Agent': self.user_agent,
            'Host': 'api.vhack.cc',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        self.request.timeout = 10
        if self.config.access_token == '' or self.config.uid == '':
            self._login()

    @staticmethod
    def _create_db():
        """Create sqlite3 database file."""

        conn = sqlite3.connect('vhackos.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            level TEXT,
            username TEXT,
            money INT,
            time INT
            )""")
        conn.commit()
        conn.close()

    @staticmethod
    def insert_db(ip_addr, level, username, money):
        """Insert data into sqlite3 database file.

        :param ip_addr: A string, player ip address.
        :param level: A string, player level.
        :param username: A string, player username.
        :param money: A string, money withdrew from player.
        """
        conn = sqlite3.connect('vhackos.db')
        cursor = conn.cursor()
        mtime = int(round(time()))
        cursor.execute("""INSERT INTO users(
            ip, level, username, money, time) VALUES (
            '{}', '{}', '{}', '{}', '{}')""".format(ip_addr, level, username,
                                                    money, mtime))
        conn.commit()
        conn.close()

    def _login(self):
        """Run login request."""
        logging.info('Logging in...')
        md5_password = utils.to_md5(self.config.password)
        json_str = {
            'lang': 'en',
            'username': self.config.username,
            'password': md5_password
        }
        json_str = json.dumps(json_str, separators=(',', ':'))
        param_user = utils.to_base64(json_str)
        param_pass = utils.to_md5("{}{}{}".format(json_str, json_str,
                                                  utils.to_md5(json_str)))
        url = "{}login.php?user={}&pass={}".format(ENDPOINT, param_user,
                                                   param_pass)
        response = self.request.get(url)
        response.encoding = 'UTF-8'
        logging.debug('\n%s\n', response.text)
        json_obj = response.json()
        self.config.access_token = json_obj['accesstoken']
        self.config.uid = json_obj['uid']
        self.config.save_config()
        return True

    @staticmethod
    def generate_url(php, lang, uid, accesstoken, **kwargs):
        """Generate url and parameters.

        :param php: A string, php endpoint.
        :param kwargs: A string, optional, others data to sent to server.
        :rtype: A string, full url.
        """
        json_str = {
            'lang': lang,
            'uid': uid,
            'accesstoken': accesstoken
        }
        json_str.update(kwargs)
        json_str = json.dumps(json_str, separators=(',', ':'))
        param_user = utils.to_base64(json_str)
        param_pass = utils.to_md5("{}{}{}".format(json_str, json_str,
                                                  utils.to_md5(json_str)))

        return "{}{}?user={}&pass={}".format(ENDPOINT, php, param_user,
                                             param_pass)

    def call(self, php, **kwargs):
        """Call the server!

        :param php: A string, php endpoint.
        :param kwargs: A string, optional, others data to sent to server.
        :rtype: A dictionary, an json object returned from server.
        """
        for i in range(1, 10):
            try:
                response = self.request.get(self.generate_url(php=php, lang='en', uid=self.config.uid, accesstoken=self.config.access_token, **kwargs))
                response.encoding = 'UTF-8'
                logging.debug('\n%s\n', response.text)
                json_obj = response.json()
                if json_obj['result'] == '36':
                    raise CredentialsChangedException
                if "expired" in json_obj:
                    if json_obj['expired'] == "1":
                        raise CredentialsExpiredException
                return json_obj
            except TimeoutError as e:
                self.logger.error('Retrying %i "%s"...', i, e)
                sleep(3)
            except CredentialsChangedException:
                self.logger.error('Credentials changed, re-login...')
                sleep(10)
                self._login()
                sleep(3)
            except CredentialsExpiredException:
                self.logger.warning("reCAPTCHAS forced...")
                exit(3)
            except json.decoder.JSONDecodeError:
                self.logger.error("json.decoder.JSONDecodeError\n%s\n", response)
                exit(2)
        self.logger.error('Please check your internet.')
        exit()
