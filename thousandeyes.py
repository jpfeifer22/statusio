import requests
import json
import constants

params = (
('output', 'JSON'),
)

class thousandeyes(object):
    def __init__(self):
        self.username = constants.thousandeyes_username
        self.password = constants.thousandeyes_password
        self.params = ('output', 'JSON')
        self.te_url = "https://api.thousandeyes.com/" 


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


    def alert_history(self, aid=None, type=None):
        """
        Returns a list of alerts for the past 7 days (window=7d).

        Response

        Sends back a collection of alerts.

        {
            "test": [
                {
                    "enabled": 1,
                    "testId": 817,
                    "savedEvent": 0,
                    "liveShare": 0,
                    "testName": "http://www.thousandeyes.com",
                    "type": "http-server",
                    "interval": 900,
                    "url": "http://www.thousandeyes.com",
                    "modifiedDate": "2013-05-11 02:02:21",
                    "networkMeasurements": 1,
                    "createdBy": "API Sandbox User (noreply@thousandeyes.com)",
                    "modifiedBy": "API Sandbox User (noreply@thousandeyes.com)",
                    "createdDate": "2012-06-28 19:33:12",
                    "apiLinks": [...]
                },
                        ...
            ]
        }
        """
        output_format = self._format_validation()
        aid = self._aid_validation(aid=aid)

        payload = {
                        'format': output_format,
                  }


        try:
            if not type:
                r = requests.get(self.te_url + 'alerts?window=7d', auth=(self.username, self.password), params=payload)
            elif type:
                r = requests.get(self.te_url + 'alerts/' + type + '?window=7d', auth=(self.username, self.password), params=payload)
            j = json.loads(r.text)
            return j
        except Exception:
            print("Failed to get alert_list: %s")
            return '{"errorMessage": "Unknown error from API"}'


    def active_alerts(self, aid=None, type=None):
        """
        Returns a list of active alerts 

        """
        output_format = self._format_validation()
        aid = self._aid_validation(aid=aid)

        payload = {
                        'format': output_format,
                  }

        try:
            r = requests.get(self.te_url + 'alerts', auth=(self.username, self.password), params=payload)
            return r.text
        except Exception:
            print("Failed to get active alerts: %s")
            return '{"errorMessage": "Unknown error from API"}'



    def active_alert_detail(self, alert_id=None, aid=None):
        """
        Receive the details of a specific Active Alert
        """
        alert_id = self._id_validation(id=alert_id)
        output_format = self._format_validation()
        aid = self._aid_validation(aid=aid)

        payload = {
                        'format': output_format,
                        'aid:': aid
                  }

        try:
            r = requests.get(self.THOUSANDEYES_API_URL() + 'alerts/' + alert_id, auth=(self.username, self.password), params=payload)
            j = json.loads(r.text)
            # print json.dumps(j, indent=4)
            return j
        except Exception:
            print("Failed to get alerts: %s")
            return '{"errorMessage": "Unknown error from API"}'



def get_alert_history():
    api = thousandeyes()
    return (api.alert_history())

def get_active_alerts():
    api = thousandeyes()
    return (api.active_alerts())






