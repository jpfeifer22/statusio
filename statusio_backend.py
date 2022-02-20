import requests
import json
import constants
import thousandeyes
import appd

params = (
('output', 'JSON'),
)

SUCCESS = str(100)
WARNING = str(300)
DANGER = str(500)

def setappcolor(currentvalue, newvalue):
    if currentvalue == SUCCESS:
        return newvalue
    if currentvalue == WARNING:
        if newvalue != DANGER:
            return newvalue
    return currentvalue

class statusio(object):
    def __init__(self):
        self.username = constants.appd_username + "@" + constants.appd_account
        self.password = constants.appd_password
        self.params = ('output', 'JSON'),
        self.appd_url = "https://cdw.saas.appdynamics.com/controller/rest/"



    def application_data(self):
 
        # Opening JSON file
        f = open('app_data.json',)
 
        # returns JSON object as a dictionary
        formed = json.load(f)
 
        # Closing file
        f.close()
                        
        cpu_high_threshold = 80
        mem_high_threshold = 80

        #Precheck for Te tests
        apps_with_te_test = 0
        for i in formed["applications"]:
            if not i['te_tests']:
                continue 
            apps_with_te_test = apps_with_te_test + 1
        
        # Determine ThousandEyes Information
        if apps_with_te_test > 0:
            tedata = thousandeyes.get_active_alerts()

        s = '{"applications" : [\n'
        for app in formed["applications"]:
            letter = app['name'][0]
            statusio = app['statusio']
            statusioapm = app['statusio_apm']
            statusiodigital = app['statusio_digital']
            statusioinfra = app['statusio_infra']
            appcolor = "100"
            appdbtcolor = appdcpucolor = appdmemcolor = tecolor = iwocolor = SUCCESS 
            bpcolor = lmcpucolor = lmmemcolor = slcpucolor = slmemcolor = SUCCESS

            # Determine AppDynamics Information
            if app['appd_name'] == "":
                appdbterr = "" 
            else: 
                #720 = 12 hours #4320 = 3 days
                mins = str(4320)

                formed = json.loads(appd.get_bt_errors(app['name'], mins))
                appdbterr = 0 
                for metric in formed:
                    if not metric["metricValues"]:
                        continue
                    for mv in metric["metricValues"]: 
                        appdbterr = appdbterr + mv['sum']

                if appdbterr > 0:
                    appdbtcolor = WARNING
                    appcolor = setappcolor(appcolor, WARNING)
                if appdbterr > 10:
                    appdbtcolor = DANGER
                    appcolor = setappcolor(appcolor, DANGER)


                #Number of BTs 
                formed = json.loads(appd.get_num_bts(app['name'], mins))
                appdbtnum = 0 
                for metric in formed:
                    if not metric["metricValues"]:
                        continue
                    for mv in metric["metricValues"]: 
                        appdbtnum = appdbtnum + mv['sum']

                # CPU High
                formed = json.loads(appd.get_cpu_busy(app['name'], mins))
                appdcpuhigh = 0
                for metric in formed:
                    if not metric["metricValues"]:
                        continue
                    for mv in metric["metricValues"]: 
                        if mv['current'] > cpu_high_threshold:
                            appdcpuhigh = appdcpuhigh + 1
                if appdcpuhigh > 0:
                    appdcpucolor = WARNING
                    appcolor = setappcolor(appcolor, WARNING)
                if appdcpuhigh >= 1:
                    appdcpucolor = DANGER
                    appcolor = setappcolor(appcolor, DANGER)


                formed = json.loads(appd.get_mem_usage(app['name'], mins))
                appdmemhigh = 0
                for metric in formed:
                    if not metric["metricValues"]:
                        continue
                    for mv in metric["metricValues"]: 
                        if mv['current'] > mem_high_threshold:
                            appdmemhigh = appdmemhigh + 1
                if appdmemhigh > 0:
                    appdmemcolor = WARNING
                    appcolor = setappcolor(appcolor, WARNING)
                if appdmemhigh >= 1:
                    appdmemcolor = DANGER
                    appcolor = setappcolor(appcolor, DANGER)

            tealert = 0
            if app['te_tests']:
                teformed = json.loads(tedata)
                for alert in teformed['alert']:
                    if alert['testName'] in app['te_tests']:
                        tealert = tealert + 1
                if tealert > 0:
                    tecolor = DANGER
                    appcolor = setappcolor(appcolor, DANGER)
        
            s += '    {"name": "' + app['name'] + \
                       '", "statusio": "' + str(statusio) + \
                       '", "statusioapm": "' + str(statusioapm) + \
                       '", "statusiodigital": "' + str(statusiodigital) + \
                       '", "statusioinfra": "' + str(statusioinfra) + \
                       '", "mins": "' + mins + \
                       '", "apmbtnum": "' + str(appdbtnum) + \
                       '", "apmbterr": "' + str(appdbterr) + \
                       '", "apmstatus": "' + str(appdbtcolor) + \
                       '", "appdcpuhigh": "' + str(appdcpuhigh) + \
                       '", "appdcpucolor": "' + str(appdcpucolor) + \
                       '", "appdmemhigh": "' + str(appdmemhigh) + \
                       '", "infrastatus": "' + str(appdmemcolor) + \
                       '", "tealert": "' + str(tealert) + \
                       '", "digitalstatus": "' + str(tecolor) + \
                       '", "infra2status": "' + str(lmcpucolor) + \
                       '", "lmmemcolor": "' + str(lmmemcolor) + \
                       '", "slcpucolor": "' + str(slcpucolor) + \
                       '", "slmemcolor": "' + str(slmemcolor) + \
                       '"},\n' 


        s = s[:-2] + '\n'
        s += "]}\n"
        return s
 
def get_application_data():
    api = statusio()
    return (api.application_data())
