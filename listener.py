#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
import sdcp.devices.appformix as applib
import json
import logging

logging.basicConfig(filename="listener.log", level=logging.DEBUG)

###########################
## V 0.1                 ##
###########################


OSuser = "admin"
OSpassword = "JNPR.lab.1"
OSproject = "demo"
RESThost = "http://172.30.105.201"

APPuser = "admin"
APPpassword = "JNPR.lab.1"
APPRESThost = "http://172.30.105.207"
APPauth = "openstack"

hostagg = []
mydict = {}
tester = False
targetinstance = []

###########################



app = Flask(__name__)

@app.route('/host/vrouter', methods=['POST'])
def vrouter_flow_count():
    entityId = request.json['status']['entityId']
#    print json.dumps(entityId, indent=4, sort_keys=True)

    hostagg = {}
    mydict = {}
    tester = False
    targetinstance = []

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
#        print json.dumps(hostagg, indent=4, sort_keys=True)
        if agg['Aggregate']['Type'] == 'instance':
            for myinstance in instlist['data']['VmProfile']:
#                print json.dumps(myinstance, indent=4, sort_keys=True)
                if myinstance['VirtualMachine']['VirtualMachineId'] in agg['Aggregate']['ObjectList']:
                    hostagg[myinstance['VirtualMachine']['Name']] = (agg['Aggregate']['Id'],  agg['Aggregate']['Name'], myinstance['VirtualMachine']['Name'], myinstance['VirtualMachine']['ServerId'])
#    print json.dumps(hostagg, indent=4, sort_keys=True)

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


#                    if innervalue[1] == local_aggregate:
#                        logging.info('Aggregate ' + innervalue[1] + ' found on server ' + innervalue[3])

    return jsonify(targetinstance)


app.run(
    debug=True,
    port=int("5563"),
    host="0.0.0.0"
    )
