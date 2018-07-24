#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
import sdcp.devices.appformix as applib
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

targethosts = []

vRouter_not_reachable = "vRouter_not-reachable"
vrouter_no_flow = "no_flow"
print 'Current state'
print '--------------'
print '--   START  --'
print '--------------'

###########################

app = Flask(__name__)

@app.route('/host/isolate', methods=['POST'])
def vrouter_flow_count():
    entityId = request.json['status']['entityId']
    alarmstate = request.json['status']['state']
    description = request.json['spec']['name']

    if alarmstate == 'active':
        print 'Current state: for alarms : alarmstate == active:'
        print '--------------'
        print 'Redis value for vRouter_not-reachable alarm is set to ' + str(redis_db.hmget(entityId, "vRouter_not_reachable"))
        print 'Redis value for no_flow alarm is set to ' + str(redis_db.hmget(entityId, "no_flow"))
        print '--------------'

        if description == vRouter_not_reachable:
            setvalues = {"vRouter_not_reachable":"yes"}
            redis_db.hmset(entityId, setvalues)

            print '--------------'
            print 'Alarm from server ' + entityId + ' is set to  ' + alarmstate
            print 'New state for key vRouter_not-reachable alarm is set to ' + str(redis_db.hmget(entityId, "vRouter_not_reachable"))
            print 'New state for key no_flow alarm is set to ' + str(redis_db.hmget(entityId, "no_flow"))
            print '--------------'

        elif description == vrouter_no_flow:
            setvalues = {"no_flow":"yes"}
            redis_db.hmset(entityId, setvalues)

            print '--------------'
            print 'Alarm from server ' + entityId + ' is set to  ' + alarmstate
            print 'New state for key vRouter_not-reachable alarm is set to ' + str(redis_db.hmget(entityId, "vRouter_not_reachable"))
            print 'New state for key no_flow alarm is set to ' + str(redis_db.hmget(entityId, "no_flow"))
            print '--------------'

    elif alarmstate == 'inactive':
        print 'Current state: for alarms : alarmstate == inactive:'
        print '--------------'
        print 'Redis value for vRouter_not-reachable alarm is set to ' + str(redis_db.hmget(entityId, "vRouter_not_reachable"))
        print 'Redis value for no_flow alarm is set to ' + str(redis_db.hmget(entityId, "no_flow"))
        print '--------------'


        if description == vRouter_not_reachable:
            setvalues = {"vRouter_not_reachable":"no"}
            redis_db.hmset(entityId, setvalues)
            
            print 'Alarm from server ' + entityId + ' is set to  ' + alarmstate
            print 'New state for key vRouter_not-reachable alarm is set to ' + str(redis_db.hmget(entityId, "vRouter_not_reachable"))
            print 'New state for key no_flow alarm is set to ' + str(redis_db.hmget(entityId, "no_flow"))

        elif description == vrouter_no_flow:
            setvalues = {"no_flow":"no"}
            redis_db.hmset(entityId, setvalues)
            
            print 'Alarm from server ' + entityId + ' is set to  ' + alarmstate
            print 'New state for key vRouter_not-reachable alarm is set to ' + str(redis_db.hmget(entityId, "vRouter_not_reachable"))
            print 'New state for key no_flow alarm is set to ' + str(redis_db.hmget(entityId, "no_flow"))

        logging.info('Alarm from server ' + entityId + ' is set to  ' + alarmstate)


    return ("entityId")

app.run(
    debug=True,
    port=int("5560"),
    host="0.0.0.0"
    )
