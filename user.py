'''user.py'''
import logging
from random import uniform
from time import sleep
from terminaltables import SingleTable

class User:
    '''User'''
    def __init__(self, utils):
        self.utils = utils
        # game var
        self.update_obj = None
        self.network_obj = None
        self.init_update()

    def init_update(self):
        self.update(notify=False)
        sleep(uniform(1.0, 2.0))
        self.update()

    def update(self, notify=True):
        if notify:
            self.update_obj = self.utils.call('update.php', lastread='0', notify='1')
        else:
            self.update_obj = self.utils.call('update.php', lastread='0')
        sleep(uniform(1.0, 2.0))

    def network(self):
        self.network_obj = self.utils.call('network.php')

    def exploit(self, target):
        ''' target="123.123.123.123" '''
        self.exploit_obj = self.utils.call('exploit.php', target=target)

    def remote(self, target):
        ''' target="123.123.123.123" '''
        self.remote_obj = self.utils.call('remote.php', target=target)

    def remotebanking(self, target):
        ''' target="123.123.123.123" '''
        self.remotebanking_obj = self.utils.call('remotebanking.php', target=target)

    def wdremotebanking(self, target, action='100'):
        self.wdremotebanking_obj = self.utils.call('remotebanking.php', target=target, action=action)

    def startbruteforce(self, target):
        ''' target="123.123.123.123" '''
        self.startbruteforce_obj = self.utils.call('startbruteforce.php', target=target)

    def remotelog(self, target):
        ''' target="123.123.123.123" '''
        self.remotelog_obj = self.utils.call('remotelog.php', target=target)

    def clearremotelog(self, target, action='100', log=''):
        self.clearremotelog_obj = self.utils.call('remotelog.php', action=action, target=target, log=log)

    def tasks(self):
        self.tasks_obj = self.utils.call('tasks.php')

    def removebrute(self, updateid, action='10000'):
        self.removebrute_obj = self.utils.call('tasks.php', action=action, updateid=updateid)

    def store(self):
        self.store_obj = self.utils.call('store.php')

    def upgradestore(self, appcode, action='100'):
        '''
        action -> 100  -> upgrade 1
        action -> 5500 -> fill task
        '''
        self.store_obj = self.utils.call('store.php', appcode=appcode, action=action)

    # public function
    def attack(self):
        self.network()
        sleep(uniform(1.0, 2.0))
        for targetdetail in self.network_obj['ips']:
            targetip = targetdetail['ip']
            sdk_level = int(self.update_obj['sdk'])
            target_fw = int(targetdetail['fw'])
            exploits_num = int(self.network_obj['exploits'])
            if (sdk_level > target_fw) and (sdk_level - target_fw < 20) and (exploits_num > 0):
                logging.info('Target fw {}'.format(target_fw))
                self.exploit(target=targetip)
                logging.info('Exploit {}'.format(targetip))
                sleep(uniform(1.0, 2.0))
                if self.exploit_obj['result'] == '0':
                    self.remote(target=targetip)
                    # logging.info('Remote {}'.format(targetip))
                    sleep(uniform(1.0, 2.0))
                    if self.remote_obj['result'] == '0':
                        self.remotebanking(target=targetip)
                        logging.info('Remote banking {}'.format(targetip))
                        sleep(uniform(1.0, 2.0))
                        if self.remotebanking_obj['result'] == '0' and self.remotebanking_obj['open'] == '0':
                            self.startbruteforce(target=targetip)
                            logging.info('Start brute force {}'.format(targetip))
                            sleep(uniform(1.0, 2.0))
                        else:
                            logging.error('Remote banking failed...')
                        self.remotelog(target=targetip)
                        sleep(uniform(1.0, 2.0))
                        self.clearremotelog(target=targetip)
                        logging.info('Cleared remote log {}'.format(targetip))
                        sleep(uniform(1.0, 2.0))
                    else:
                        logging.error('Remote failed...')
                else:
                    logging.error('Exploit failed...')
            elif (exploits_num == 0):
                logging.error('No exploits left...')
                break
            # else:
            #     logging.error('FW too high...')

    def withdraw(self):
        self.network()
        logging.info('Total connections: {}'.format(len(self.network_obj['cm'])))
        sleep(uniform(1.0, 2.0))
        for targetdetail in self.network_obj['cm']:
            if targetdetail['brute'] == '1':
                targetip = targetdetail['ip']
                self.remote(target=targetip)
                logging.info('Remote {}'.format(targetip))
                sleep(uniform(1.0, 2.0))
                if self.remote_obj['result'] == '0':
                    self.remotebanking(target=targetip)
                    logging.info('Remote banking {}'.format(targetip))
                    sleep(uniform(1.0, 2.0))
                    if self.remotebanking_obj['withdraw'] == '0' and self.remotebanking_obj['remotemoney'] != '0':
                        self.wdremotebanking(target=targetip)
                        money = self.remotebanking_obj['remotemoney']
                        username = self.remotebanking_obj['remoteusername']
                        logging.info('Withdraw {} from {}'.format(money, username))
                        sleep(uniform(1.0, 2.0))
                    self.remotelog(target=targetip)
                    sleep(uniform(1.0, 2.0))
                    self.clearremotelog(target=targetip)
                    logging.info('Cleared remote log {}'.format(targetip))
                    sleep(uniform(1.0, 2.0))

    def upgrade(self):
        self.store()
        sleep(uniform(1.0, 2.0))
        while True:
            apps = self.store_obj['apps']
            apps = [x for x in apps if x['price'] != '0']
            apps = [x for x in apps if x['level'] != '0']
            apps = [x for x in apps if x['maxlvl'] != '1']
            apps = sorted(apps, key=lambda k: int(k['level']))

            total_running = 0
            for app in apps:
                try:
                    total_running += int(app['running'])
                except KeyError:
                    pass
            if total_running >= 10:
                break

            app = apps[0]
            if int(app['price']) < int(self.store_obj['money']):
                self.upgradestore(appcode=app['appid'])
                logging.info('Upgrading {}'.format(app['appid']))
                sleep(uniform(1.0, 2.0))

    def printuserinfo(self):
        data = []
        data.append(['Exploits', self.update_obj['exploits'], 'Level', self.update_obj['level']])
        data.append(['Netcoins', self.update_obj['netcoins'], 'Money', self.update_obj['money']])
        table = SingleTable(data)
        table.title = 'User info'
        table.inner_heading_row_border = False
        print(table.table)

        data = []
        data.append(['Firewall', self.update_obj['fw'], 'Antivirus', self.update_obj['av']])
        data.append(['SDK', self.update_obj['sdk'], 'BruteF', self.update_obj['brute']])
        data.append(['Spam', self.update_obj['spam']])
        table = SingleTable(data)
        table.title = 'Software info'
        table.inner_heading_row_border = False
        print(table.table)





if __name__ == '__main__':
    from utils import Utils
    UTILS = Utils()
    USER = User(UTILS)
