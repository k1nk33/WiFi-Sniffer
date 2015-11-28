import os
import re
import csv
import time
import shelve
from subprocess import getoutput
from wifi import Cell


class NetUtil:

    '''
    Class object that provides various network analysis methods
    '''

    def __init__(self):
        '''
        Constructor method
        '''

        # Default directory & interface
        self.cwd = os.getcwd()
        self.iface = 'wlan0'

        # Try to get wireless gateway details,
        # unless there's no active connection
        try:
            self.ping_ip, self.gw_mac = self.getGateway()
        except:
            self.ping_ip = self.gw_mac = None
            print('Error! \nCheck your connection!')
        finally:
            pass

        # Get the Gateway SSID
        try:
            cell = Cell.all(self.iface)
            x, y = str(list(cell)[0]).split('=')
            self.ssid = y.strip(')')
        except:
            self.ssid = 'Offline'

    def __str__(self):
        '''
        Implements a string descriptor for the NetUtil class object
        '''

        return (('NetUtil\n'
                 '- CWD : %s\n'
                 '- GW IP : %s\n'
                 '- GW MAC : %s\n'
                 '- SSID : %s\n'
                 '- IFACE : %s') %
                (self.cwd,
                 self.ping_ip,
                 self.gw_mac,
                 self.ssid,
                 self.iface)
                )

    def getGateway(self):
        '''
        Returns the current Gateway IP & MAC Address in string format
        '''

        # Will have to try catch import error on netifaces
        try:
            import netifaces
            gw_dict = netifaces.gateways()
            self.gw_ip = ((gw_dict['default'])[2][0])
            self.iface = ((gw_dict['default'])[2][1])

        except:
            gw_line = getoutput('route | grep default')
            gw_pattern = re.compile('default (.*) 0.0.0.0 ')
            gw_match = gw_pattern.search(gw_line)
            self.gw_ip = (gw_match.group(1).strip())

        self.gw_mac = getoutput(("iwconfig wlan0 | grep Access"
                                 "| cut -d ' ' -f18"))

        return self.gw_ip, self.gw_mac

    def signalTest(self):
        '''
        Method to check and return Signal Strenght
        '''

        try:
            sig = getoutput('iwconfig %s | grep -e "Signal"' % self.iface)
            sig = sig.strip()
            sig_pattern = re.compile('=(.*)/70  Signal level=(.*) dBm')
            sig_match = sig_pattern.search(sig)
            self.quality, self.level = sig_match.group(1), sig_match.group(2)
            return self.quality, self.level
        except:
            return str(0), str(0)

    def pingTest(self, switch):
        '''
        Runs type of ping command depending on switch argument value :
        Returns either Delay, Throughput, Loss or a List of Response times
        '''

        count = 0
        if switch == 'delay':
            self.rtt = 0.0
            while count < 2:
                self.rtt += self.delay()
                count += 1
            return str((round((self.rtt / 2), 3)))

        elif switch == 'tput':
            self.t_tput = 0
            while count < 2:
                self.t_tput += self.throughPut()
                count += 1
            self.t_tput = round((self.t_tput / 2), 3)
            return self.t_tput

        elif switch == 'loss':
            self.t_loss = 0
            while count < 2:
                self.t_loss += self.packetLoss()
                count += 1
            try:
                self.t_loss = (self.t_loss / 2)
                return self.t_loss
            except:
                return 0

        elif switch == 'ping':
            self.values = []
            while count < 5:
                self.pingValues()
                count += 1
            return self.values

        else:
            return ('Error, %s not a valid argument' % str(switch))

    def packetLoss(self):
        '''
        Returns the percentage of lost packets
        '''

        try:
            loss_line = getoutput("ping -c 1 " + self.ping_ip)
            loss_pattern = re.compile("received, (.*)% packet loss")
            loss_match = loss_pattern.search(loss_line)
            self.loss = int(loss_match.group(1))
            return self.loss
        except:
            return 0

    def delay(self):
        '''
        Returns avgerage round trip time of a packet
        '''

        try:
            avg_time_line = getoutput(("ping -c 1 " + self.ping_ip +
                                       "| grep rtt"))
            avg_time_pattern = re.compile('= (.*)/(.*)/')
            avg_time_match = avg_time_pattern.search(avg_time_line)
            self.average_time = float(avg_time_match.group(2))
            return self.average_time
        except:
            return 0

    def throughPut(self):
        '''
        Returns the current network speed (throughput)
        '''

        try:
            rtime_line = getoutput(("ping -s 65507 -c 1 %s"
                                    "| grep rtt") %
                                    self.ping_ip)
            rtime_pattern = re.compile('= (.*)/(.*)/')
            rtime_match = rtime_pattern.search(rtime_line)
            rtime = rtime_match.group(2)
            self.tput = round(2 * 65515 / float(rtime) * 0.008, 2)
            return self.tput
        except:
            return 0

    def pingValues(self):
        '''
        Runs a number of Pings to the gateway and appends to a list of values
        '''
        try:
            ping_line = getoutput('ping -c 1 ' + self.ping_ip)
            ping_pattern = re.compile('time=(.*)ms')
            ping_match = ping_pattern.search(ping_line)
            self.values.append(ping_match.group(1))
        except:
            self.values.append('0,')
            pass

    def saveFile(self, fname, res_dicts, switch):
        '''
        Method to save various types of files
        '''

        def dbSave():
            # Creates shelve database file
            with shelve.open(self.cwd + '/' + fname + '.db') as db:
                for d in res_dicts:
                    db.update(d)

        def logSave():
            # Creates a results log file
            with open(self.cwd + '/' + fname + '.log', 'a') as fn:

                t_now = time.strftime("%H:%M:%S - %d/%m/%Y")

                # Writes Results section to logfile
                for d in res_dicts:
                    fn.write(("#\t\tWiFi Sweep\t"
                              "SSID : " + self.ssid +
                              " - " + t_now + "\n"))

                    for k, v in d.items():
                        fn.write('# {} = {}\n'.format(k, v))

                # Writes Ping section to logfile
                str_list = [("\n#\t\tPing Results\t"
                             "SSID : " + self.ssid +
                             " - " + t_now + "\n"),
                            '#' + str(self.values).replace(',', ' :: '),
                            '-' * 70
                            ]

                for s in str_list:
                    fn.write(s + '\n')

        def csvSave():
            # List of csv Headings
            headings = ['GatewayIP',
                        'GatewayMac',
                        'Throughput Mbps',
                        'Delay ms',
                        'PacketLoss %',
                        'Quality /70',
                        'Level dBms'
                        ]

            # Creates Excel type file of Headings, Tests & Values
            with open(self.cwd + '/' + fname + '.csv', 'w') as csv_f:
                w = csv.DictWriter(csv_f, fieldnames=headings, dialect='excel')
                w.writeheader()
                # For each dictionary in the list, write to file
                for d in res_dicts:
                    w.writerow(d)

        if switch == 0:
            dbSave()
        elif switch == 1:
            logSave()
        elif switch == 2:
            csvSave()
        else:
            dbSave()
            logSave()
            csvSave()


def main():
    nt = NetUtil()
    print(nt)
    print('Signal Quality %s\nSignal Level %s' % nt.signalTest())
    print('Delay %s' % nt.pingTest('delay'))
    print('Throughput %s' % nt.pingTest('tput'))
    print('Loss %i' % nt.pingTest('loss'))
    print('Responses \n%s' % nt.pingTest('ping'))


if __name__ == '__main__':
    main()
