import pexpect
from pexpect import pxssh
import sys
import time
import getpass
try:


    s = pxssh.pxssh()
    s.login('172.30.105.204', 'root', 'JNPR.lab.1')
    s.sendline('\r')
    s.sendline('virsh console 8 --devname serial1')
    time.sleep(1)
    s.sendline('\r')
    time.sleep(1)
    s.expect('.login: ')
    s.sendline('root')
    s.expect('.Password: ')
    s.sendline('JNPR.lab.1')
    s.expect('.# ')
    s.logfile = sys.stdout
    s.sendline('ping -w 3 172.30.105.200')
    index = s.expect(['.100% packet loss'])
    print index
    if index == 0:
        print 'Failed'
    else:
        print 'Connected'
    s.sendline('logout')
    s.sendline('\^]')
    time.sleep(5)
    s.logout()

except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)
