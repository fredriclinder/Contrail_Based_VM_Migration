#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
from urllib2 import urlopen, Request, URLError, HTTPError
from common import appformix
import os, sys
alarmpath = "./alarms"
servicealarmpath = "./alarms"

af_host = '172.30.105.207'
af_user = 'admin'
af_password = 'JNPR.lab.1'
af_authtype = 'openstack'

# Get AppFormix token
token = appformix.tokenrequest(af_host,af_user,af_password)

# Get current alarms
currentalarms = appformix.readalarms(af_host, token, af_authtype)
print json.dumps(currentalarms, indent=4, sort_keys=True)



# POST all alarms in directory ./alarms
dirs = os.listdir( alarmpath )



for file in dirs:
    print file
    with open(alarmpath+'/'+file) as json_file:
        alarm_def = json.load(json_file)
        postalarm = appformix.postalarm(af_host, token, af_authtype, json.dumps(alarm_def))
        print json.dumps(postalarm, indent=4, sort_keys=True)

for file in dirs:
    print file
    with open(servicealarmpath+'/'+file) as json_file:
        alarm_def = json.load(json_file)
        postalarm = appformix.postservicealarm(af_host, token, af_authtype, json.dumps(alarm_def))
        print json.dumps(postalarm, indent=4, sort_keys=True)
