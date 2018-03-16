'''user.py'''
import logging
from random import uniform
from time import sleep
from terminaltables import SingleTable


logger = logging.getLogger(__name__)

class User:
    '''User'''
    def __init__(self, utils):
        self.utils = utils
        # game var
        self.update_obj = None
        self.network_obj = None
        self.init_update()

    def init_update(self):
        self.update()
        sleep(uniform(0.5, 2.0))
        self.update()

    def update(self, notify=True):
        if notify:
            self.update_obj = self.utils.call('update.php', lastread='0', notify='1')
        else:
            self.update_obj = self.utils.call('update.php', lastread='0', notify='0')
        sleep(uniform(0.5, 2.0))

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

    def mining(self, action=''):
        '''
        action -> 200 -> collect
        action -> 100 -> start

        running -> 0 -> idle
        running -> 1 -> running
        running -> 2 -> mined
        '''
        if action == '':
            self.mining_obj = self.utils.call('mining.php')
        else:
            self.mining_obj = self.utils.call('mining.php', action=action)


    # public function
    def attack(self):
        self.network()
        exploits_num = int(self.network_obj['exploits'])
        sleep(uniform(0.5, 2.0))
        for targetdetail in self.network_obj['ips']:
            targetip = targetdetail['ip']
            brute_level = int(self.update_obj['brute'])
            target_fw = int(targetdetail['fw'])
            if (brute_level > target_fw) and (exploits_num > 0):
                logger.info('Target fw {}'.format(target_fw))
                self.exploit(target=targetip)
                logger.info('Exploit {}'.format(targetip))
                sleep(uniform(0.5, 2.0))
                if self.exploit_obj['result'] == '0':
                    exploits_num = int(self.exploit_obj['exploits'])
                    self.remote(target=targetip)
                    sleep(uniform(0.5, 2.0))
                    if self.remote_obj['result'] == '0':
                        self.remotebanking(target=targetip)
                        logger.info('Remote banking {}'.format(targetip))
                        sleep(uniform(0.5, 2.0))
                        if self.remotebanking_obj['result'] == '0' and self.remotebanking_obj['open'] == '0':
                            self.startbruteforce(target=targetip)
                            exploits_num -= 1
                            logger.info('Start brute force {}'.format(targetip))
                            sleep(uniform(0.5, 2.0))
                        else:
                            logger.error('Remote banking failed...')
                        self.remotelog(target=targetip)
                        sleep(uniform(0.5, 2.0))
                        self.clearremotelog(target=targetip)
                        logger.info('Cleared remote log {}'.format(targetip))
                        sleep(uniform(0.5, 2.0))
                    else:
                        logger.error('Remote failed...')
                elif self.exploit_obj['result'] == '3':
                    logger.error('Exploit failed...')
                    exploits_num = int(self.exploit_obj['exploits'])
            elif (exploits_num == 0):
                logger.error('No exploits left...')
                break

    def withdraw(self):
        self.network()
        logger.info('Total connections: {}'.format(len(self.network_obj['cm'])))
        sleep(uniform(0.5, 2.0))
        for targetdetail in self.network_obj['cm']:
            if targetdetail['brute'] == '1':
                targetip = targetdetail['ip']
                self.remote(target=targetip)
                logger.info('Remote {}'.format(targetip))
                sleep(uniform(0.5, 2.0))
                if self.remote_obj['result'] == '0':
                    self.remotebanking(target=targetip)
                    logger.info('Remote banking {}'.format(targetip))
                    sleep(uniform(0.5, 2.0))
                    if self.remotebanking_obj['withdraw'] == '0' and self.remotebanking_obj['remotemoney'] != '0':
                        self.wdremotebanking(target=targetip)
                        if self.remotebanking_obj['result'] == '0':
                            level = int(self.remote_obj['remoteLevel'])
                            money = int(self.remotebanking_obj['remotemoney'])
                            username = self.remotebanking_obj['remoteusername']
                            logger.info('Withdraw {} from {}'.format(money, username))
                            self.utils.insert_db(targetip, level, username, money)
                        sleep(uniform(0.5, 2.0))
                    self.remotelog(target=targetip)
                    sleep(uniform(0.5, 2.0))
                    self.clearremotelog(target=targetip)
                    logger.info('Cleared remote log {}'.format(targetip))
                    sleep(uniform(0.5, 2.0))

    def upgradesingle(self):
        self.store()
        sleep(uniform(0.5, 2.0))
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
                logger.info('Upgrading {}'.format(app['appid']))
                sleep(uniform(0.5, 2.0))

    def collectmining(self):
        self.mining()
        running = self.mining_obj['running']
        sleep(uniform(0.5, 2.0))
        if running == '0':
            self.mining(action='100')
            logger.info('Started netcoins miner.')
            sleep(uniform(0.5, 2.0))
        elif running == '2':
            mined = int(self.mining_obj['mined'])
            self.mining(action='200')
            sleep(uniform(0.5, 2.0))
            result = self.mining_obj['result']
            if result == '0':
                logger.info('Collected {} netcoins'.format(mined))
                self.mining(action='100')
                sleep(uniform(0.5, 2.0))
                logger.info('Started netcoins miner.')
            else:
                logger.error('Collect netcoins failed.')
        else:
            logger.info('Netcoins miner still running.')

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
