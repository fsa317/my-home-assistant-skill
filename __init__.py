from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
from requests import get, post


# Timeout time for HA requests
TIMEOUT = 10

class MyHomeAssistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        token = self.settings.get('hasecret')
        self.ha_url = self.settings.get('hahost')
        self.log.info("Starting MyHomeAssistant v0.11")
        self.headers = {
            'Authorization': "Bearer {}".format(token),
            'Content-Type': 'application/json'
        }

    @intent_file_handler('home.status.intent')
    def handle_home_status_intent(self, message):
        #self.speak_dialog('assistant.home.my')
        resp = self.getState('sensor.jarvis_temps')
        self.speak(resp)
    
    @intent_file_handler('temp.check.intent')
    def handle_temp_check_intent(self, message):
        resp = self.getState('sensor.jarvis_temps')
        self.speak(resp)

    @intent_file_handler('everyone.intent')
    def handle_everyone_intent(self, message):
        # self.speak("Checking, please hold.")
        resp1 = self.getState('sensor.jarvis_sal_status')
        resp2 = self.getState('sensor.jarvis_vincent_status')
        resp3 = self.getState('sensor.jarvis_tiffany_status')
        resp4 = self.getState('sensor.jarvis_frank_status')
        self.speak(resp1)
        self.speak(resp2)
        self.speak(resp3)
        self.speak(resp4)

    @intent_file_handler('whereis.intent')
    def handle_whereis_intent(self, message):
        self.log.info("Whereis - "+str(message))
        pers = message.data["person"]
        resp = self.getState('sensor.jarvis_'+pers+'_status')
        self.speak(resp)
    
    @intent_file_handler('energy.intent')
    def handle_energy_intent(self, message):
        self.log.info("energy intent")
        solarnow = self.getState('sensor.powerwall_solar_now')
        gridnow = float(self.getState('sensor.powerwall_site_now'))
        net7 = float(self.getState('sensor.net_usage_7d'))
        net30 = float(self.getState('sensor.net_usage_30d'))
        
        ha_data = {'value': solarnow} 
        self.speak_dialog('solar',data=ha_data)
        
        ha_data = {'value': abs(gridnow)}
        if (gridnow>0):
            self.speak_dialog('gridnow.deficit',data=ha_data)
        else:
            self.speak_dialog('gridnow.surplus',data=ha_data)
        
        ha_data = {'value': abs(net7), 'days':7}
        if (net7>0):
            self.speak_dialog('grid.deficit',data=ha_data)
        else:
            self.speak_dialog('grid.surplus',data=ha_data)
        
        ha_data = {'value': abs(net30), 'days':30}
        if (net30>0):
            self.speak_dialog('grid.deficit',data=ha_data)
        else:
            self.speak_dialog('grid.surplus',data=ha_data)
    
    def getState(self,entity):
        response = self.callApi('/states/{}'.format(entity))
        if response:
            state = response['state']
            self.log.info("Response state {}".format(state))
            return state
        return None

    def callApi(self,api): 
        fullurl = "{}/api{}".format(self.ha_url,api)
        self.log.info("Calling {}".format(fullurl))
        req = get(fullurl, headers=self.headers, verify=False, timeout=TIMEOUT)
        req.raise_for_status()
        return req.json()


def create_skill():
    return MyHomeAssistant()

