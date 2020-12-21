from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger


# Timeout time for HA requests
TIMEOUT = 10

class MyHomeAssistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        token = "abceyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhZjA1NmY5Mzc4NTI0NWY4YmUzYTUwMGMzYzgxNGY0NCIsImlhdCI6MTYwODUyMjQ4MCwiZXhwIjoxOTIzODgyNDgwfQ.CXEuvGcKw6ZkDohYvYqkXYDz0Ja4d7gMyDzxgqncRfUdef"
        self.ha_url = 'https://fulton.duckdns.org'
        self.headers = {
            'Authorization': "Bearer {}".format(token),
            'Content-Type': 'application/json'
        }

    @intent_file_handler('home.status.intent')
    def handle_home_status_intent(self, message):
        #self.speak_dialog('assistant.home.my')
        resp = getState('sensor.jarvis_temps')
        self.speak(resp)


def create_skill():
    return MyHomeAssistant()

def getState(entity):
    response = callApi('/states/{}'.format(entity))
    if response:
        state = response['state']
        self.log.info("Response state {}".format(state))
        return state
    return None

def callApi(api):
    fullurl = "{}/api{}".format(self.url,api)
    self.log.info("Calling {}".format(fullurl))
    req = get(fullurl, headers=self.headers, verify=False, timeout=TIMEOUT)
    req.raise_for_status()
    return req.json()