'''Utils.py'''
import base64
import hashlib
import json

import requests

from config import Config as config

USER_AGENT = [
    'Dalvik/2.1.0 (Linux; U; Android 5.0.1; GT-I9508V Build/LRX22C)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.1; MX4 Build/LRX22C)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; D5322 Build/19.3.A.0.472)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; D816w Build/LRX22G)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC D816v Build/LRX22G)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC E9pw Build/LRX22G)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC M8t Build/LRX22G)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC One M8s Build/LRX22G)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; LG-F320L Build/LRX22G)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Letv X500 Build/DBXCNOP5500912251S)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Nexus 5 Build/LRX22G)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0.2; SM-N9005 Build/LRX22G)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0; ASUS_Z00ADB Build/LRX21V)',
    'Dalvik/2.1.0 (Linux; U; Android 5.0; Nexus 5 Build/LPX13D)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1 Build/LYZ28N)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; 2014811 MIUI/6.1.26)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY47V)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY48Y)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; D5833 Build/23.4.A.1.232)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; GT-I9152 Build/LMY48Y)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; LG-D802 Build/LMY48W)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 2 Build/LMY48B)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 2SC Build/LMY47V)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 3 Build/LMY48Y)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Mi-4c MIUI/6.1.14)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; NX403A Build/LMY48Y)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; ONE A2001 Build/LMY47V)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; R7Plusm Build/LMY47V)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Redmi Note 2 Build/LMY48Y)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-J3109 Build/LMY47X)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N9200 Build/LMY47X)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Sparkle V Build/LMY47V)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Xperia Z2 Build/LMY48Y)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1.1; titan Build/LMY48W)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; HTC M9w Build/LMY47O)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; HTC One M9 Build/LMY47O)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; LG-H818 Build/LMY47D)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; MX5 Build/LMY47I)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; XT1060 Build/LPA23.12-39.7)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; XT1085 Build/LPE23.32-53)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; m1 note Build/LMY47D)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; m2 Build/LMY47D)',
    'Dalvik/2.1.0 (Linux; U; Android 5.1; m2 note Build/LMY47D)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; 2014813 Build/MMB29U)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; A0001 Build/MMB29M)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; ASUS_Z00A Build/MMB29T)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 4LTE Build/MMB29M)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Mi-4c Build/MMB29U)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Moto G 2014 Build/MMB29M)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Moto G 2014 LTE Build/MMB29T)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 4 Build/MMB29M)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5 Build/MMB29K)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Sensation Build/MMB29U)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Z1 Build/MMB29T)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 2 Build/MRA58K)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 2A Build/MRA58K)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0; Moto G 2014 Build/MDB08M)',
    'Dalvik/2.1.0 (Linux; U; Android 6.0; XT1097 Build/MPE24.49-18)'
]


class Utils:
    '''Utils Class'''

    def __init__(self):
        self.config = config()
        self.endpoint = "https://api.vhack.cc/mobile/6/"
        self.user_agent = self._generate_ua(
            self.config.username + self.config.password)
        self.request = requests.Session()
        self.request.headers = {
            'User-Agent': self.user_agent,
            'Host': 'api.vhack.cc',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        if self.config.access_token == '' or self.config.uid == '':
            self._login()

    def _generate_ua(self, identifier):
        pick = int(self._to_md5(identifier), 16)
        user_agents = tuple(USER_AGENT)
        return user_agents[pick % len(user_agents)]

    @staticmethod
    def _to_md5(txt):
        md5 = hashlib.md5()
        md5.update(txt.encode('utf-8'))
        return md5.hexdigest()

    @staticmethod
    def _to_base64(string):
        b64 = base64.urlsafe_b64encode(string.encode('UTF-8')).decode('ascii')
        return b64.replace("=", "")

    def _login(self):
        md5_password = self._to_md5(self.config.password)
        json_str = {'username': self.config.username, 'password': md5_password}
        json_str = json.dumps(json_str, separators=(',', ':'))
        param_user = self._to_base64(json_str)
        param_pass = self._to_md5("{}{}{}".format(json_str, json_str,
                                                  self._to_md5(json_str)))
        url = "{}login.php?user={}&pass={}".format(self.endpoint, param_user,
                                                   param_pass)
        response = self.request.get(url)
        response.encoding = 'UTF-8'

        json_obj = response.json()
        self.config.access_token = json_obj['accesstoken']
        self.config.uid = json_obj['uid']
        self.config.save_config()
        return True

    def _generate_url(self, php, **kwargs):
        json_str = {
            'uid': self.config.uid,
            'accesstoken': self.config.access_token
        }
        json_str.update(kwargs)
        json_str = json.dumps(json_str, separators=(',', ':'))
        param_user = self._to_base64(json_str)
        param_pass = self._to_md5("{}{}{}".format(json_str, json_str,
                                                  self._to_md5(json_str)))

        return "{}{}?user={}&pass={}".format(self.endpoint, php, param_user,
                                             param_pass)

    def call(self, php, **kwargs):
        '''call'''
        for i in range(10):
            try:
                response = self.request.get(self._generate_url(php, **kwargs))
                response.encoding = 'UTF-8'
                json_obj = response.json()
                return json_obj
            except requests.exceptions.Timeout:
                print('Retrying {} times...'.format(i))
            print('Please check your internet.')
            exit(0)


if __name__ == '__main__':
    UTILS = Utils()
