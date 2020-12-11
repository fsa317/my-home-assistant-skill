from mycroft import MycroftSkill, intent_file_handler


class MyHomeAssistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('assistant.home.my.intent')
    def handle_assistant_home_my(self, message):
        self.speak_dialog('assistant.home.my')


def create_skill():
    return MyHomeAssistant()

