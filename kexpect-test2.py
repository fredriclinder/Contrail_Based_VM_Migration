import pexpect
import sys
child = pexpect.spawn('ssh juniper@172.30.104.40')
child.logfile = sys.stdout
child.expect('.password:')
child.logfile = sys.stdout
child.sendline('JNPR.lab.1')
child.expect('.$')
child.sendline('ping 172.30.105.200')
child.expect('.Destination Host Unreachable')
try:
    index = p.expect(['.icmp_seq', '.Destination Host Unreachable'])
    if index == 0:
        print 'Success'
    elif index == 1:
        print 'Failed'
    else:
        print 'Missed'
