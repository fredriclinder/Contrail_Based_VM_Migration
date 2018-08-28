#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request
import common.connector.appformix as applib
import json
import logging
import redis

###########################
## V 0.3                 ##
###########################

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

logging.basicConfig(filename="listener.log", level=logging.DEBUG)

OSuser = "admin"
OSpassword = "JNPR.lab.1"
OSproject = "demo"
RESThost = "http://172.30.105.201"

APPuser = "admin"
APPpassword = "JNPR.lab.1"
APPRESThost = "http://172.30.105.207"
APPauth = "openstack"


# Get AppFormix token
app = applib.connector(APPRESThost)
appresponse = app.auth({'username': APPuser, 'password': APPpassword, 'AuthType': APPauth})

###########################
def gethosts(APPRESThost):
## Get  hosts
    hosts = APPRESThost + ':7000/appformix/controller/v2.0/' + 'hosts'
    hostlist = app.href(hosts)
    return hostlist

def getaggregates(APPRESThost):
## Get  aggregates
    aggregates = APPRESThost + ':7000/appformix/controller/v2.0/' + 'aggregates'
    agglist = app.href(aggregates)
    return agglist

def getinstances(APPRESThost):
## Get  instances
    instances = APPRESThost + ':7000/appformix/controller/v2.0/' + 'instances'
    instlist = app.href(instances)
    return instlist

hostlist = gethosts(APPRESThost)
instlist = getinstances(APPRESThost)
agglist = getaggregates(APPRESThost)
