#!/usr/bin/python3

import statusio
import requests
import json
import sched, time
import thousandeyes
import logicmonitor

STATUSPAGE_ID = '6211e1154cbc11052e574295'

api = statusio.Api(api_id='c64514f9-7c8f-4966-80f4-a74ff785fa1d', api_key='qCXAVLXvBGdBF3xCPeji06apKwCRmng/Exk9htHnfbR52AgL2o4sxxP0+aO7nXWU7+fM8LjOk7lgoOpsO0+PDg==')

#summary = api.StatusSummary(STATUSPAGE_ID)
#print(summary)

payload={}
headers = {}

NORMAL = str(100)
WARNING = str(300)
CRITICAL = str(500)

s = sched.scheduler(time.time, time.sleep)

def get_and_update(sc):

    # grab list of data from .json file.
    f = open('oper1_data.json')
    oper1data = json.load(f)
    f.close()

    # Get active thousandeyes alerts
    tedata = thousandeyes.get_active_alerts()

    #print(tedata)

    formed = json.loads(tedata) 

    for tier in oper1data['tiers']:
        if tier["statusio"] == "":
            continue
        for alert in formed['alert']:
            if alert['ruleName'] in tier['te_tests']:
                #print("found a te match", tier)
                d = api.ComponentStatusUpdate(STATUSPAGE_ID, tier["statusio"], tier["statusio_container"], 'digital', CRITICAL)
                continue
        d = api.ComponentStatusUpdate(STATUSPAGE_ID, tier["statusio"], tier["statusio_container"], 'digital', NORMAL)


    # Get active logicmonitor alerts
    lmdata = logicmonitor.get_active_alerts()

    formed = json.loads(lmdata) 

    for tier in oper1data['tiers']:
        if tier["statusio"] == "":
            continue
        for alert in formed['items']:
            if ('oper1' not in alert['monitorObjectName']):
                continue
            if alert['monitorObjectName'] == tier['name']:
                #print("found a match lmalert", alert)
                d = api.ComponentStatusUpdate(STATUSPAGE_ID, tier["statusio"], tier["statusio_container_infra"], 'infra', WARNING)
                continue
        d = api.ComponentStatusUpdate(STATUSPAGE_ID, tier["statusio"], tier["statusio_container_infra"], 'infra', NORMAL)

    s.enter(120, 1, get_and_update, (sc,))


#Main
s.enter(20, 1, get_and_update, (s,))
s.run()
