import pathos
c = pathos.core.copy('/srv/project/check.py', destination='root@172.30.104.204:~/check.py')
s = pathos.core.execute('python check.py', host='172.30.105.204')
print s.response()
