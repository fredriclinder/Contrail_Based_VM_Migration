#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
import sdcp.devices.appformix as applib
import json
import logging

logging.basicConfig(filename="listener.log", level=logging.DEBUG)

###########################
## V 0.2                 ##
###########################

OSuser = "admin"
OSpassword = "JNPR.lab.1"
OSproject = "demo"
RESThost = "http://172.30.105.201"

APPuser = "admin"
APPpassword = "JNPR.lab.1"
APPRESThost = "http://172.30.105.207"
APPauth = "openstack"

targethosts = []
###########################

app = Flask(__name__)

@app.route('/host/vrouter', methods=['POST'])
def vrouter_flow_count():
    entityId = request.json['status']['entityId']
    alarmstate = request.json['status']['state']

    if alarmstate == 'active':

        hostagg = {}



    # Get AppFormix token
        app = applib.Device(APPRESThost)
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

        ###########################

        ## Create dict with hostid, vmid, aggid

        for agg in agglist['data']['Aggregates']:
            if agg['Aggregate']['Type'] == 'instance':
                for myinstance in instlist['data']['VmProfile']:
                    if myinstance['VirtualMachine']['VirtualMachineId'] in agg['Aggregate']['ObjectList']:
                        print json.dumps(myinstance)
                        hostagg[myinstance['VirtualMachine']['Name']] = (agg['Aggregate']['Id'],  agg['Aggregate']['Name'], myinstance['VirtualMachine']['Name'], myinstance['VirtualMachine']['ServerId'])


        ## Find Agg in target host
        ## Search for Agg with mambers on different hosts
        ## Reture False, True

        for key, value in hostagg.items():
            if value[3] == entityId:
                local_aggregate = value[1]
                logging.info('Alarm from server ' + entityId + '. Target aggregate is ' + local_aggregate)
                print 'Alarm from server ' + entityId + '. Target aggregate is ' + local_aggregate
                for innerkey, innervalue in hostagg.items():
                    if innervalue[3] != entityId and innervalue[1] == local_aggregate:
                        print 'server ' + innervalue[3] + ' is not local for aggregate ' + local_aggregate
                        targethosts.append(innervalue[3])
        print json.dumps(targethosts)
        return json.dumps(targethosts)
    elif alarmstate == 'inactive':



        print 'Alarm from server ' + entityId + ' is set to  ' + alarmstate
        return jsonify(entityId)

    else:
        print 'test'
        return jsonify('test')


app.run(
    debug=True,
    port=int("5560"),
    host="0.0.0.0"
    )
