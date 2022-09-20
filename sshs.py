#!/usr/bin/python3

##########################################################################################################
#
#	Utility script to automate ssh connections
#
#
#
#
#
#
#
#
#
#
#
##########################################################################################################

import sys

sys.path.append('/usr/lib/python3/dist-packages/')

from pexpect import pxssh
import time
import getpass


class classSSHClient:

    def __init__(self, ip_node, username, password):
        self.ssh = pxssh.pxssh()
        self.ip_node = ip_node
        self.username = username
        self.password = password

    def login(self):
        try:
            self.ssh.login(self.ip_node, self.username, self.password)
        except:
            print('SSH login error')

    def command(self, command):
        try:
            self.ssh.sendline(command)
            self.ssh.prompt()
            res = self.ssh.before

            return res.decode()
        except:
            print('SSH command error: ' + command)
            return 'Error'

    def logout(self):
        self.ssh.logout()

    def __del__(self):
        # if you forget it
        try:
            self.ssh.logout()
        except:
            pass

        self.ssh = None


######			testing
'''	
host = '192.168.1.61'
username = input("Enter username: ")
password = getpass.getpass()

sshClient = classSSHClient(host, username, password)

sshClient.login()
sshClient.command('cd /root/')

res = sshClient.command('ls')
print(res)

sshClient.logout()
'''

