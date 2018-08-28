"""Appformix API module. Provides calls for appformix interaction"""
__author__ = "Zacharias El Banna"
__version__ = "1.0GA"
__status__ = "Production"
__add_globals__ = lambda x: globals().update(x)

from common.connector.appformix import Device

def authenticate(aDict):
 """Function docstring for authenticate TBD
 Args:
  - host (required)
 Output:
 """
 ret = {}
 controller = Device(SC['nodes'][aDict['node']])
 try:
  res = controller.auth({'username':SC['appformix']['username'], 'password':SC['appformix']['password'] })
  ret['auth'] = res['auth']
  ret['token'] = controller.get_token()
  ret['expires'] = controller.get_cookie_expire()
 except Exception as e: ret = e[0]
 return ret
