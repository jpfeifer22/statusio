#!/usr/bin/python3

import statusio
import requests
import json
import sched, time

STATUSPAGE_ID = '6210867bed6335053034e12d'

APPMANAGER = "http://10.89.132.128:5000/statusio/applications"

api = statusio.Api(api_id='c64514f9-7c8f-4966-80f4-a74ff785fa1d', api_key='qCXAVLXvBGdBF3xCPeji06apKwCRmng/Exk9htHnfbR52AgL2o4sxxP0+aO7nXWU7+fM8LjOk7lgoOpsO0+PDg==')

#summary = api.StatusSummary(STATUSPAGE_ID)
#print(summary)

payload={}
headers = {}

s = sched.scheduler(time.time, time.sleep)

def get_and_update(sc):
    response = requests.request("GET", APPMANAGER, headers=headers, data=payload)
    formed = json.loads(response.text) 
    for app in formed['applications']:
        if app["statusio"] == "":
            continue
        d = api.ComponentStatusUpdate(STATUSPAGE_ID, app["statusio"], app["statusioapm"], 'apm', app["apmstatus"])
        d = api.ComponentStatusUpdate(STATUSPAGE_ID, app["statusio"], app["statusiodigital"], 'digital', app["digitalstatus"])
        d = api.ComponentStatusUpdate(STATUSPAGE_ID, app["statusio"], app["statusioinfra"], 'infra', app["infrastatus"])
        print(app['name'] + ' apm ' + app['apmstatus'] + ' apmbterr ' + app['apmbterr'] + \
        ' digital ' + app['digitalstatus'] + \
        ' tealert ' + app['tealert'] + \
        ' infra ' + app['infrastatus'] + \
        ' appdmemhigh ' + app['appdmemhigh'] + \
        ' appdcpuhigh ' + app['appdcpuhigh'])
    s.enter(120, 1, get_and_update, (sc,))


#Main
s.enter(20, 1, get_and_update, (s,))
s.run()
