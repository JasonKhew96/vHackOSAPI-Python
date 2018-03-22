"""Config management"""
import logging

import yaml


class Config:
    """Config class

    :param filename: A string, file name of config file
    """

    def __init__(self, filename):
        self.config_file = filename
        self.logger = logging.getLogger(__name__)
        try:
            with open(self.config_file, "r") as ymlfile:
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
        """Save config to configuration file."""
        with open(self.config_file, "w") as ymlfile:
            cfg = {
                'access_token': self.access_token,
                'uid': self.uid,
                'user': {
                    'username': self.username,
                    'password': self.password
                }
            }
            ymlfile.write(yaml.dump(cfg, default_flow_style=False))

    def create_config(self):
        """Create a default configuration file."""
        with open(self.config_file, 'w') as ymlfile:
            cfg = {
                'access_token': '',
                'uid': '',
                'user': {
                    'username': '',
                    'password': ''
                }
            }
            ymlfile.write(yaml.dump(cfg, default_flow_style=False))
            self.logger.info(
                "Config file created, please edit your credentials in %s",
                self.config_file)
            exit()
