'''config.py'''
import yaml


class Config:
    '''Config class'''

    def __init__(self):
        try:
            with open("config.yml", 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
        except FileNotFoundError:
            self.create_config()
        try:
            self.username = cfg['user']['username']
            self.password = cfg['user']['password']
            self.access_token = cfg['access_token']
            self.uid = cfg['uid']
        except (KeyError, TypeError):
            self.create_config()

    def save_config(self):
        '''save_config'''
        with open("config.yml", 'w') as ymlfile:
            cfg = {
                'access_token': self.access_token,
                'uid': self.uid,
                'user': {
                    'username': self.username,
                    'password': self.password
                }
            }
            ymlfile.write(yaml.dump(cfg, default_flow_style=False))

    @staticmethod
    def create_config():
        '''create_config'''
        with open("config.yml", 'w') as ymlfile:
            cfg = {
                'access_token': '',
                'uid': '',
                'user': {
                    'username': '',
                    'password': ''
                }
            }
            ymlfile.write(yaml.dump(cfg, default_flow_style=False))
            exit()


if __name__ == '__main__':
    CONFIG = Config()
