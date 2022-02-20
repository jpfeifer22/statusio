#!/usr/bin/python3

import statusio
import requests
import json

STATUSPAGE_ID = '6210867bed6335053034e12d'

APPMANAGER = "http://10.89.132.128:5000/statusio/applications"

api = statusio.Api(api_id='c64514f9-7c8f-4966-80f4-a74ff785fa1d', api_key='qCXAVLXvBGdBF3xCPeji06apKwCRmng/Exk9htHnfbR52AgL2o4sxxP0+aO7nXWU7+fM8LjOk7lgoOpsO0+PDg==')

#summary = api.StatusSummary(STATUSPAGE_ID)
#print(summary)

#data = api.ComponentStatusUpdate(STATUSPAGE_ID, e8_operator, e8_operator_infra, 'Test status', 500)


payload={}
headers = {}

response = requests.request("GET", APPMANAGER, headers=headers, data=payload)

formed = json.loads(response.text) 
for app in formed['applications']:
    if app["statusio"] == "":
        continue
    d = api.ComponentStatusUpdate(STATUSPAGE_ID, app["statusio"], app["statusioapm"], 'apm', app["apmstatus"])
    #print(d)
    d = api.ComponentStatusUpdate(STATUSPAGE_ID, app["statusio"], app["statusiodigital"], 'digital', app["digitalstatus"])
    #print(d)
    d = api.ComponentStatusUpdate(STATUSPAGE_ID, app["statusio"], app["statusioinfra"], 'infra', app["infrastatus"])
    #print(d)
    print(app['name'] + ' apm ' + app['apmstatus'] + ' apmbterr ' + app['apmbterr'] + \
    ' digital ' + app['digitalstatus'] + \
    ' tealert ' + app['tealert'] + \
    ' infra ' + app['infrastatus'] + \
    ' appdmemhigh ' + app['appdmemhigh'] + \
    ' appdcpuhigh ' + app['appdcpuhigh'])




