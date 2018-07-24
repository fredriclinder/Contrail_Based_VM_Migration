import pexpect
import sys
import time
child = pexpect.spawn('ssh juniper@172.30.104.40')
child.logfile = sys.stdout
child.expect('.password:')
child.logfile = sys.stdout
child.sendline('JNPR.lab.1')
child.expect('.$')
child.logfile = sys.stdout

time.sleep(5)
child.sendline('ping 172.30.105.200')
child.expect('.Destination Host Unreachable')
index = child.expect(['.ms', '.Unreachable'])
print index
if index == 1:
  print 'Failed'
elif index == 0:
  print 'Success'
else:
  print 'Missed'
