import requests
import json
import constants
import hashlib
import base64
import time
import hmac


class logicmonitor(object):
    def __init__(self):
        self.accessid = constants.lm_accessid
        self.accesskey = constants.lm_accesskey
        self.company = constants.lm_company
        self.url = "https://" + self.company + ".logicmonitor.com/santaba/rest" 


    def _format_validation(self, output_format="json"):
        """
        format=json|xml optional, specifies the format of output requested
        """
        format_list = ['json', 'xml']
        if output_format not in format_list:
            raise ValueError('Output Format must be set to "json" or "xml", default is "json"')
        return output_format


    def _aid_validation(self, aid=None):
        """
        aid=x optional, changes the account group context of the current user.
        # If an invalid account ID is specified as a parameter, the response
        # will come back as an HTTP/400 error
        """
        if not isinstance(aid, int) and aid is not None:
            raise ValueError('Required Integer or None')
        return aid


    def _id_validation(self, id=None):
        """
        id is required to be a integer.
        """
        if not isinstance(id, int) and id is not None:
            raise ValueError('Required Integer or None')
        return str(id)



    def active_alerts(self, aid=None, type=None):
        """
        Returns a list of active alerts 

        """
        output_format = self._format_validation()
        aid = self._aid_validation(aid=aid)

        httpVerb ='GET'
        resourcePath = '/alert/alerts'
        data=''
        #queryParams ='?customColumns=%2523%2523externalticketid%2523%2523'
        queryParams ='?size=100'
        callurl = self.url + resourcePath + queryParams
        epoch = str(int(time.time() * 1000))
        requestVars = httpVerb + epoch + data + resourcePath
        hmac1 = hmac.new(self.accesskey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
        signature = base64.b64encode(hmac1.encode())
        auth = 'LMv1 ' + self.accessid + ':' + signature.decode() + ':' + epoch
        headers = {'Content-Type':'application/json','Authorization':auth, 'X-version':'2'}

        try:
            r = requests.get(callurl, data=data, headers=headers)
            return r.text
        except Exception:
            print("Failed to get active alerts: %s")
            return '{"errorMessage": "Unknown error from API"}'




def get_active_alerts():
    api = logicmonitor()
    return (api.active_alerts())






