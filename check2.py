from pexpect import pxssh
import sys
try:
    s = pxssh.pxssh()
    s.login('172.30.105.204', 'root', 'JNPR.lab.1')
    s.sendline('virsh console 8 --devname serial1')
    s.sendline('\r')

    index = s.expect(['.login: ', s.TIMEOUT])
    if index == 0:
        print 'hit'
        s.sendline('root')
        s.expect('.Password: ')
        s.sendline('JNPR.lab.1')
        s.expect('.# ')
    elif  index == 1:
        print 'miss'
        s.sendline('logout')
        s.sendline('root')
        s.expect('.Password: ')
        s.sendline('JNPR.lab.1')
        s.expect('.# ')

#    s.expect('.login: ')
#    s.sendline('root')
#    s.expect('.Password: ')
#    s.sendline('JNPR.lab.1')
#    s.expect('.# ')
#    s.logfile = sys.stdout

    s.sendline('ping -w 3 172.30.105.200')
    index = s.expect(['.ms', '.100% packet loss'])
    if index == 1:
        print 'Failed'
    elif index == 0:
        print 'Success'
    else:
        print 'Missed'
    s.sendline('logout')

except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)
