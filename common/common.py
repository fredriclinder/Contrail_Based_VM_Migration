"""Module docstring.
DB module
"""
__author__ = "Zacharias El Banna"
__version__ = "1.0GA"
__status__ = "Production"


######################################### REST ########################################
#
#
def rest_call(aURL, aArgs = None, aMethod = None, aHeader = None, aVerify = None, aTimeout = 20):
 """ Rest call function
  Args:
   - aURL (required)
   - aArgs (optional)
   - ... (optional)
  Output:
   - de-json:ed data structure that function returns and all status codes
 """
 from json import loads, dumps
 from urllib2 import urlopen, Request, URLError, HTTPError
 try:
  head = { 'Content-Type': 'application/json','Accept':'application/json' }
  try:    head.update(aHeader)
  except: pass
  try:    from logger import log
  except: pass
  else:   log("rest_call -> %s '%s'"%(aURL,dumps(aArgs)))
  req = Request(aURL, headers = head, data = dumps(aArgs) if aArgs else None)
  if aMethod:
   req.get_method = lambda: aMethod
  if aVerify is None or aVerify is True:
   sock = urlopen(req, timeout = aTimeout)
  else:
   from ssl import _create_unverified_context
   sock = urlopen(req,context=_create_unverified_context(), timeout = aTimeout)
  output = {'info':dict(sock.info()), 'code':sock.code }
  output['node'] = output['info'].pop('x-api-node','_no_node_')
  try:    output['data'] = loads(sock.read())
  except: output['data'] = None
  if (output['info'].get('x-api-res','OK') == 'ERROR'):
   output['info'].pop('server',None)
   output['info'].pop('connection',None)
   output['info'].pop('transfer-encoding',None)
   output['info'].pop('content-type',None)
   output['exception'] = 'RESTError'
  sock.close()
 except HTTPError as h:
  raw = h.read()
  try:    data = loads(raw)
  except: data = raw
  output = { 'result':'ERROR', 'exception':'HTTPError', 'code':h.code, 'info':dict(h.info()), 'data':data }
 except URLError as e:  output = { 'result':'ERROR', 'exception':'URLError',  'code':590, 'info':{'error':str(e)}}
 except Exception as e: output = { 'result':'ERROR', 'exception':type(e).__name__, 'code':591, 'info':{'error':str(e)}}
 output['info']['x-api-code'] = code_to_string(output['code'])
 if output.get('exception'):
  raise Exception(output)
 return output

#
# Basic Auth header generator for base64 authentication
#
def basic_auth(aUsername,aPassword):
 return {'Authorization':'Basic ' + (("%s:%s"%(aUsername,aPassword)).encode('base64')).replace('\n','') }

#
# HTML Code translator
#
def code_to_string(aCode):
 return {200:'OK',201:'Created',204:'No Content',304:'Not Modified',400:'Bad Request',401:'Unauthorized',403:'Forbidden',404:'Not Found',500:'Internal Server Error',591:'Z-Exception'}.get(aCode,'%s Code Not Encoded'%aCode)
