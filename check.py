import pexpect
import sys
import time

child = pexpect.spawn('virsh console 8 --devname serial1')
time.sleep(1)
child.sendline('\r')
time.sleep(1)
child.logfile = sys.stdout
child.expect('.login: ')
child.logfile = sys.stdout
child.sendline('root')
child.logfile = sys.stdout
child.expect('.Password: ')
child.logfile = sys.stdout
child.sendline('JNPR.lab.1')
child.logfile = sys.stdout
child.expect('.# ')
child.logfile = sys.stdout


child.sendline('ping -w 3 172.30.105.200')
index = child.expect(['.ms', '.100% packet loss'])
print index
if index == 1:
  print 'Failed'
elif index == 0:
  print 'Success'
else:
  print 'Missed'

child.sendline('logout')
child.sendline('\^]')

