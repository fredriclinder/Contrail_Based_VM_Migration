"""Openstack REST module. Provides all REST functions to interwork with an Openstack controller for different services"""
__author__ = "Zacharias El Banna"
__version__ = "1.0GA"
__status__ = "Production"
__add_globals__ = lambda x: globals().update(x)

from common.connector.openstack import Device
from common.common import rest_call

#
#
def application(aDict):
 """Function docstring for application. Delivers the information for SDCP login to redirect to the openstack App.
 Args:
  - node (required)
  - appformix (optional)
  - name (optional)
  - token (optional)
 Output:
 """
 from datetime import datetime,timedelta
 ret = {'title':"%s 2 Cloud"%(aDict.get('name','iaas')),'choices':[],'message':"Welcome to the '%s' Cloud Portal"%(aDict.get('name','iaas')),'portal':'openstack' }
 try:
  if aDict.get('token'):
   controller = Device(SC['nodes'][aDict['node']],aDict.get('token'))
  else:
   controller = Device(SC['nodes'][aDict['node']],None)
   res = controller.auth({'project':SC['openstack']['project'], 'username':SC['openstack']['username'],'password':SC['openstack']['password']})
  auth = controller.call("5000","v3/projects")
  if auth['code'] == 200:
   projects = []
   for project in auth['data']['projects']:
    projects.append({'name':project['name'], 'id':"%s_%s"%(project['id'],project['name'])})
   ret['choices'] = [{'display':'Customer', 'id':'project', 'data':projects}]
 except Exception as e:
  ret['exception'] = str(e)
 ret['parameters'] = [{'display':'Username', 'id':'username', 'data':'text'},{'display':'Password', 'id':'password', 'data':'password'}]
 cookie = {'name':aDict.get('name','iaas'),'node':aDict['node'],'portal':'openstack'}
 if aDict.get('appformix'):
  cookie['appformix'] = aDict.get('appformix')
 ret['cookie'] = ",".join(["%s=%s"%(k,v) for k,v in cookie.iteritems()])
 ret['expires'] = (datetime.utcnow() + timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
 return ret

#
#
def authenticate(aDict):
 """Function docstring for authenticate TBD
 Args:
  - node (required)
  - username (required)
  - project_id (required)
  - password (required)
  - project_name (required)
 Output:
 """
 from common.logger import log
 ret = {}
 controller = Device(SC['nodes'][aDict['node']],None)
 res = controller.auth({'project':aDict['project_name'], 'username':aDict['username'],'password':aDict['password'] })
 ret = {'authenticated':res['auth']}
 if res['auth'] == 'OK':
  with DB() as db:
   ret.update({'project_name':aDict['project_name'],'project_id':aDict['project_id'],'username':aDict['username'],'token':controller.get_token(),'expires':controller.get_cookie_expire()})
   db.do("INSERT INTO openstack_tokens(token,expires,project_id,username,node) VALUES('%s','%s','%s','%s','%s')"%(controller.get_token(),controller.get_token_expire(),aDict['project_id'],aDict['username'],SC['nodes'][aDict['node']]))
   token_id = db.get_last_id()
   for service in ['heat','nova','neutron','glance']:
    svc = controller.get_service(service,'public')
    if len(svc['path']) > 0:
     svc['path'] = svc['path'] + '/'
    db.do("INSERT INTO openstack_services(id,service,service_port,service_url,service_id) VALUES('%s','%s','%s','%s','%s')"%(token_id,service,svc['port'],svc['path'],svc['id']))
   db.do("INSERT INTO openstack_services(id,service,service_port,service_url,service_id) VALUES('%s','%s','%s','%s','%s')"%(token_id,"contrail",8082,'',''))
  log("openstack_authenticate - successful login and catalog init for %s@%s"%(aDict['username'],aDict['node']))
 else:
  log("openstack_authenticate - error logging in for  %s@%s"%(aDict['username'],ctrl))
 return ret

#
#
def services(aDict):
 """Function docstring for services. Produces a list of services attached to token, services can be filtered on project names as a string list
 Args:
  - token (required)
  - filter (optional)
 Output:
 """
 ret = {}
 with DB() as db:
  db.do("SELECT id FROM openstack_tokens WHERE token = '%s'"%aDict['token'])
  id = db.get_val('id')
  ret['count']    = db.do("SELECT %s FROM openstack_services WHERE id = '%s'"%("*" if not aDict.get('filter') else aDict.get('filter'), id))
  ret['services'] = db.get_rows()
 return ret

#
#
def rest(aDict):
 """Function docstring for rest TBD
 Args:
  - token (required)
  - service (optional)
  - call (optional)
  - href (optional)
  - arguments (optional)
  - method (optional)
 Output:
 """
 try:
  if aDict.get('href'):
   ret = rest_call(aDict.get('href'), aDict.get('arguments'), aDict.get('method','GET'), { 'X-Auth-Token':aDict['token'] })
  else:
   with DB() as db:
    db.do("SELECT node, service_port, service_url FROM openstack_tokens LEFT JOIN openstack_services ON openstack_tokens.id = openstack_services.id WHERE openstack_tokens.token = '%s' AND service = '%s'"%(aDict['token'],aDict.get('service')))
    data = db.get_row()
   controller = Device(data['node'],aDict['token'])
   ret = controller.call(data['service_port'], data['service_url'] + aDict['call'], aDict.get('arguments'), aDict.get('method','GET'))
  ret['result'] = 'OK' if not ret.get('result') else ret.get('result')
 except Exception as e: ret = e[0]
 return ret

#
#
def call(aDict):
 """Function docstring for call. Basically creates a controller instance and send a (nested) rest_call.
 Args:
  - node (required)
  - token (required)
  - service (required)
  - call (required)
  - arguments (optional)
  - method (optional)
 Output:
 """
 with DB() as db:
  db.do("SELECT node, service_port, service_url FROM openstack_tokens LEFT JOIN openstack_services ON openstack_tokens.id = openstack_services.id WHERE openstack_tokens.token = '%s' AND service = '%s'"%(aDict['token'], aDict['service']))
  data = db.get_row()
 controller = Device(data['node'],aDict['token'])
 try:
  ret = controller.call(data['service_port'], data['service_url'] + aDict.get('call',''), aDict.get('arguments'), aDict.get('method'))
  ret['result'] = 'OK' if not ret.get('result') else ret.get('result')
 except Exception as e: ret = e[0]
 return ret

def href(aDict):
 """Function docstring for call. Basically creates a controller instance and send a (nested) rest_call
 Args:
  - href (required)
  - token (required)
  - arguments (optional)
  - method (optional)
 Output:
 """
 try: ret = rest_call(aDict.get('href'), aDict.get('arguments'), aDict.get('method','GET'), { 'X-Auth-Token':aDict['token'] })
 except Exception as e: ret = e[0]
 return ret

#
#
def info(aDict):
 """Function docstring for info. Returns a list of Internal to Openstack tokens for user X
 Args:
  - username (required)
 Output:
 """
 from datetime import datetime
 ret = {}
 with DB() as db:
  ret['found'] = (db.do("SELECT id, token, node, CAST(FROM_UNIXTIME(expires) AS CHAR(50)) AS expires, (UNIX_TIMESTAMP() < expires) AS valid FROM openstack_tokens WHERE username = '%s'"%aDict['username']) > 0)
  ret['data'] = db.get_rows()
 return ret

#
#
def token_info(aDict):
 """Function docstring for info. Returns detailed list of Openstack token given token
 Args:
  - token (required)
 Output:
 """
 from datetime import datetime
 ret = {}
 with DB() as db:
  ret['found'] = (db.do("node, SELECT CAST(NOW() AS CHAR(50)) AS time, INET_NTOA(controller) AS controller, id, CAST(FROM_UNIXTIME(expires) AS CHAR(50)) AS expires FROM openstack_tokens WHERE token = '%s'"%aDict['token']) > 0)
  ret['data'] = db.get_row()
 return ret
