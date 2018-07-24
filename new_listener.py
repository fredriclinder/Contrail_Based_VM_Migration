from paramiko import SSHClient
host="172.30.105.204"
user="root"
client = SSHClient()
client.load_system_host_keys()
client.connect(host, username=user)
stdin, stdout, stderr = client.exec_command('ls -la install.sh')
print "stderr: ", stderr.readlines()
print "pwd: ", stdout.readlines()
