#!/usr/bin/python3

import statusio
api = statusio.Api(api_id='c64514f9-7c8f-4966-80f4-a74ff785fa1d', api_key='qCXAVLXvBGdBF3xCPeji06apKwCRmng/Exk9htHnfbR52AgL2o4sxxP0+aO7nXWU7+fM8LjOk7lgoOpsO0+PDg==')

STATUSPAGE_ID = '6210867bed6335053034e12d'
summary = api.StatusSummary(STATUSPAGE_ID)
print(summary)

e8_operator = '6210867bed6335053034e13d'
e8_operator_apm = '6210867bed6335053034e13c'
e8_operator_digital = '621086ebc6a9830534d3792f'
e8_operator_infra = '621086f63625a5052e32a245'
data = api.ComponentStatusUpdate(STATUSPAGE_ID, e8_operator, e8_operator_infra, 'Test status', 500)


