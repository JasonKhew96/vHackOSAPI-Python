"""vHackOS unofficial API"""
import logging
from random import uniform
from time import sleep

from terminaltables import SingleTable


class VHackOSAPI:
    """vHackOSAPI class

    :param network: A :class:`network`
    """

    def __init__(self, network):
        self.utils = network
        self.logger = logging.getLogger(__name__)
        # Game return object
        self.update_obj = None
        self.network_obj = None
        self.exploit_obj = None
        self.remote_obj = None
        self.remotebanking_obj = None
        self.startbruteforce_obj = None
        self.remotelog_obj = None
        self.tasks_obj = None
        self.removebrute_obj = None
        self.store_obj = None
        self.mining_obj = None
        self.wdremotebanking_obj = None
        self.missions_obj = None
        self.server_obj = None

    def update(self, notify=True):
        """Update player details

        :param notify: A boolean, notify player when got exploited by other player.
        """
        if notify:
            self.update_obj = self.utils.call(
                'update.php', lastread='0', notify='1')
        else:
            self.update_obj = self.utils.call(
                'update.php', lastread='0', notify='0')

    def network(self):
        """Get network ip address and connection manager."""
        self.network_obj = self.utils.call('network.php')

    def exploit(self, target):
        """Exploit a target ip address.

        :param target: A string, ip address.
        """
        self.exploit_obj = self.utils.call('exploit.php', target=target)

    def remote(self, target):
        """Remote a target ip address.

        :param target: A string, ip address.
        """
        self.remote_obj = self.utils.call('remote.php', target=target)

    def remotebanking(self, target):
        """Remote banking a target ip address.

        :param target: A string, ip address.
        """
        self.remotebanking_obj = self.utils.call(
            'remotebanking.php', target=target)

    def wdremotebanking(self, target, amount, action="100"):
        """Withdraw money from target ip address.

        :param target: A string, ip address.
        :param action: A string, 100 means withdraw.
        """
        self.wdremotebanking_obj = self.utils.call(
            'remotebanking.php', target=target, action=action, amount=amount)

    def startbruteforce(self, target):
        """Bruteforce a target ip address.

        :param target: A string, ip address.
        """
        self.startbruteforce_obj = self.utils.call(
            'startbruteforce.php', target=target)

    def remotelog(self, target):
        """Fetch remote log from target ip address.

        :param target: A string, ip address.
        """
        self.remotelog_obj = self.utils.call('remotelog.php', target=target)

    def clearremotelog(self, target, action="100", log=''):
        """Save remote log to target ip address.

        :param target: A string, ip address.
        :param action: A string, 100 means save.
        :param log: A string, string to save to remote log.
        """
        self.remotelog_obj = self.utils.call(
            'remotelog.php', action=action, target=target, log=log)

    def tasks(self, action='', updateid=''):
        """Get a list of tasks including bruteforce list

        888 -> boost
        500 -> finish
        10000 -> removebrute
        """
        if action == '':
            self.tasks_obj = self.utils.call('tasks.php')
        else:
            self.tasks_obj = self.utils.call(
                'tasks.php', action=action, updateid=updateid)

    def store(self):
        """Get app list"""
        self.store_obj = self.utils.call('store.php')

    def upgradestore(self, appcode, action='100'):
        """Upgrade an app

        :param appcode: A string, app code.
        :param action: A string, action code.

        action -> 100  -> upgrade 1
        action -> 5500 -> fill task
        """
        self.store_obj = self.utils.call(
            'store.php', appcode=appcode, action=action)

    def mining(self, action=''):
        """Get netcoins mining state.

        :param action: A string, action code

        action -> 200 -> collect
        action -> 100 -> start

        running -> 0 -> idle
        running -> 1 -> running
        running -> 2 -> mined
        """
        if action == '':
            self.mining_obj = self.utils.call('mining.php')
        else:
            self.mining_obj = self.utils.call('mining.php', action=action)

    def missions(self, action='', dailyid=''):
        """Get missions list or collect finish missions.

        :param action: A string, action code
        :param dailyid: A string, daily id

        action -> 200 -> collect
        dailyid -> 0, 1, 2, 3

        finished -> 1 -> can collect
        """
        if action == '':
            self.missions_obj = self.utils.call('missions.php')
        else:
            self.missions_obj = self.utils.call(
                'missions.php', action=action, dailyid=dailyid)

    def server(self, action='', node_type='', node_number=''):
        """Get server details or make server action.

        :param action: A string, action code
        :param node_type: A string, node type
        :param node_number: A string, node number

        action -> 500 -> ?
        action -> 600 -> ?
        action -> 1000 -> open 1 package
        action -> 2000 -> open all packages
        """
        if action == '':
            self.server_obj = self.utils.call('server.php')
        elif action == "1000" or action == "2000":
            self.server_obj = self.utils.call('server.php', action=action)

    def attack(self):
        """Attack loop"""
        self.network()
        exploits_num = int(self.network_obj['exploits'])
        self.logger.info("Refresh network, you have %i exploit(s)",
                         exploits_num)
        sleep(uniform(0.5, 1.5))

        if exploits_num < 1:
            self.logger.error('No exploits left...')
            return

        for targetdetail in self.network_obj['ips']:
            if exploits_num < 1:
                self.logger.error('No exploits left...')
                break
            targetip = targetdetail['ip']
            brute_level = int(self.update_obj['brute'])
            target_fw = int(targetdetail['fw'])
            if (brute_level >
                    target_fw) and (targetdetail['open'] == "0"):  # and (brute_level - target_fw < 200):
                self.logger.info('Target fw %i', target_fw)
                self.exploit(target=targetip)
                self.logger.info('Exploit %s', targetip)
                sleep(uniform(0.5, 1.5))
                if self.exploit_obj['result'] == '0':
                    exploits_num = int(self.exploit_obj['exploits'])
                    self.remote(target=targetip)
                    sleep(uniform(0.5, 1.5))
                    if self.remote_obj['result'] == '0':
                        self.remotebanking(target=targetip)
                        self.logger.info('Remote banking %s', targetip)
                        sleep(uniform(0.5, 1.5))
                        if (self.remotebanking_obj['result'] == '0'
                                and self.remotebanking_obj['open'] == '0'):
                            self.startbruteforce(target=targetip)
                            if self.startbruteforce_obj['result'] == '0':
                                self.logger.info('Start brute force %s',
                                                 targetip)
                            else:
                                self.logger.error('Brute force error %s',
                                                  targetip)
                            sleep(uniform(0.5, 1.5))
                        else:
                            self.logger.error('Remote banking failed...')
                        self.remotelog(target=targetip)
                        sleep(uniform(0.5, 1.5))
                        self.clearremotelog(target=targetip)
                        self.logger.info('Cleared remote log %s', targetip)
                        sleep(uniform(0.5, 1.5))
                    else:
                        self.logger.error('Remote failed...')
                elif self.exploit_obj['result'] == '3':
                    self.logger.error('Exploit failed...')
                    exploits_num = int(self.exploit_obj['exploits'])

        if exploits_num > 0:
            sleep(uniform(5.0, 10.0))
            self.attack()

    def withdraw(self):
        """Withdraw loop"""
        self.tasks()
        self.logger.info('Total connections: %i',
                         len(self.tasks_obj['brutes']))
        sleep(uniform(0.5, 1.5))
        mymoney = int(self.update_obj['money'])
        if mymoney >= 999999999:
            self.logger.info("Maximum capacity reached: {:,}".format(mymoney))
            return
        for targetdetail in self.tasks_obj['brutes']:
            if targetdetail['result'] == '1':
                targetip = targetdetail['user_ip']
                self.remote(target=targetip)
                self.logger.info('Remote %s', targetip)
                sleep(uniform(0.5, 1.5))
                if self.remote_obj['result'] == '0':
                    self.remotebanking(target=targetip)
                    self.logger.info('Remote banking %s', targetip)
                    sleep(uniform(0.5, 1.5))
                    if (self.remotebanking_obj['withdraw'] == '0'
                            and self.remotebanking_obj['remotemoney'] != '0'
                            and self.remotebanking_obj['aatt'] == '0'):
                        amount = round(
                            int(self.remotebanking_obj['remotemoney']) * 10 /
                            100)
                        self.wdremotebanking(
                            target=targetip, amount=str(amount))
                        if self.remotebanking_obj['result'] == '0':
                            level = int(self.remote_obj['remoteLevel'])
                            money = int(self.remotebanking_obj['remotemoney'])
                            username = self.remotebanking_obj['remoteusername']
                            self.logger.info('Withdraw {:,} from {}'.format(
                                amount, username))
                            self.utils.insert_db(targetip, level, username,
                                                 money)
                        sleep(uniform(0.5, 1.5))
                    self.remotelog(target=targetip)
                    sleep(uniform(0.5, 1.5))
                    self.clearremotelog(target=targetip)
                    self.logger.info('Cleared remote log %s', targetip)
                    sleep(uniform(0.5, 1.5))
                # else:
                #     self.logger.error(self.remote_obj['result'])

    def upgradesingle(self):
        """Upgrade single app loop"""
        self.store()
        sleep(uniform(0.5, 1.5))
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
                self.logger.info('Upgrading %s', app['appid'])
                sleep(uniform(0.5, 1.5))
        self.boostupgrade()

    def boostupgrade(self):
        self.update()
        sleep(uniform(0.5, 1.5))
        self.tasks()
        sleep(uniform(0.5, 1.5))
        boosters = int(self.tasks_obj['boosters'])
        if boosters > 0 and int(self.tasks_obj['updateCount']) > 0:
            updateid = self.tasks_obj['updates'][0]['id']
            self.tasks(action="888", updateid=updateid)
            sleep(uniform(0.5, 1.5))
            boosted = self.tasks_obj['boosted']
            if boosted == "1":
                self.logger.info("Boosted")
            else:
                self.logger.error("Boost ERROR")
        else:
            self.logger.error("No more booster...")

    def finishall(self):
        self.tasks()
        sleep(uniform(0.5, 1.5))
        self.logger.info('Total updates: %i', len(self.tasks_obj['updates']))
        netcoins = int(self.tasks_obj['netcoins'])
        finishallcosts = int(self.tasks_obj['finishallcosts'])
        if netcoins > finishallcosts and (
                netcoins - finishallcosts > 6000) and int(
                    self.tasks_obj['updateCount']) > 0:
            updateid = self.tasks_obj['updates'][0]['id']
            self.tasks(action="500", updateid=updateid)
            sleep(uniform(0.5, 1.5))
            finishall = self.tasks_obj['finishall']
            if finishall == "1":
                self.logger.info("Used netcoins to finish all tasks")
            else:
                self.logger.error("Use netcoins ERROR")
        else:
            self.logger.error("No more netcoins...")

    def collectmining(self):
        """Collect netcoins and keep it running"""
        self.mining()
        running = self.mining_obj['running']
        sleep(uniform(0.5, 1.5))
        if running == '0':
            self.mining(action='100')
            self.logger.info('Started netcoins miner.')
            sleep(uniform(0.5, 1.5))
        elif running == '2':
            mined = int(self.mining_obj['mined'])
            self.mining(action='200')
            sleep(uniform(0.5, 1.5))
            result = self.mining_obj['result']
            if result == '0':
                self.logger.info('Collected %i netcoins', mined)
                self.mining(action='100')
                sleep(uniform(0.5, 1.5))
                self.logger.info('Started netcoins miner.')
            else:
                self.logger.error('Collect netcoins failed.')
        else:
            self.logger.info('Netcoins miner still running.')

    def missions_job(self):
        """Colect missions rewards."""
        self.missions()
        sleep(uniform(0.5, 1.5))
        for daily in self.missions_obj['daily']:
            if daily['finished'] == "1":
                dailyid = str(self.missions_obj['daily'].index(daily))
                self.missions(action="200", dailyid=dailyid)
                if self.missions_obj['claimed'] == "1":
                    self.logger.info("Claimed missions %i: %i %s, %i EXP",
                                     dailyid, daily['rewAmount'],
                                     daily['rewType'], daily['exp'])
                else:
                    self.logger.error("Claim missions error...")
                sleep(uniform(0.5, 1.5))
        self.logger.info("Missions checked")

    def server_job(self):
        """Do server job."""
        self.server()
        sleep(uniform(0.5, 1.5))
        packages = int(self.server_obj['packs'])
        if packages > 0:
            self.server(action="2000")
            if self.server_obj['sPackOpenAll'] == "1":
                self.logger.info("Collected %i packages.", packages)
            else:
                self.logger.error("Collect packages error.")
            sleep(uniform(0.5, 1.5))
        self.logger.info("Server checked.")

    def printuserinfo(self):
        """Print player details"""
        exp = int(self.update_obj["exp"]) / int(self.update_obj["expreq"])
        exp = round((exp * 100), 2)
        money = '{:,}'.format(int(self.update_obj['money']))
        level = "{} ({}%)".format(self.update_obj['level'], exp)

        data = []
        data.append(['Exploits', self.update_obj['exploits'], 'Level', level])
        data.append(['Netcoins', self.update_obj['netcoins'], 'Money', money])
        table = SingleTable(data)
        table.title = 'User info'
        table.inner_heading_row_border = False
        print(table.table)

        data = []
        data.append([
            'Firewall', self.update_obj['fw'], 'Antivirus',
            self.update_obj['av']
        ])
        data.append([
            'SDK', self.update_obj['sdk'], 'BruteF', self.update_obj['brute']
        ])
        data.append(['Spam', self.update_obj['spam']])
        table = SingleTable(data)
        table.title = 'Software info'
        table.inner_heading_row_border = False
        print(table.table)
