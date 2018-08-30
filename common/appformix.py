#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

def tokenrequest(ip, user, password):
    url = 'http://' + ip + ':9000/appformix/controller/v2.0/auth_credentials'
    print url
    header = { 'Content-Type': 'application/json','Accept':'application/json' }
    data = '{"UserName":"' + user + '", "AuthType":"openstack", "Password":"' + password + '"}'
    print data
    req = requests.post(url, headers = header, data = data)
    resp = req.json()

    return resp['Token']['tokenId']

def readalarms(ip, token, authtype):
    url = 'http://' + ip + ':7000/appformix/controller/v2.0/alarms'
    header = { 'X-Auth-Token':token, 'X-Auth-Type':'openstack', 'Content-Type': 'application/json','Accept':'application/json'}
    req = requests.get(url, headers = header)
    resp = req.json()
    return resp


def postalarm(ip, token, authtype, alarm_def):
    url = 'http://' + ip + ':7000/appformix/controller/v2.0/alarms'
    header = { 'X-Auth-Token':token, 'X-Auth-Type':'openstack', 'Content-Type': 'application/json','Accept':'application/json'}
    req = requests.post(url, headers = header, data = alarm_def)
    resp = req.json()
    return resp

def postservicealarm(ip, token, authtype, alarm_def):
    url = 'http://' + ip + ':7000/appformix/controller/v1.0/service_alarm'
    header = { 'X-Auth-Token':token, 'X-Auth-Type':'openstack', 'Content-Type': 'application/json','Accept':'application/json'}
    req = requests.post(url, headers = header, data = alarm_def)
    resp = req.json()
    return resp
