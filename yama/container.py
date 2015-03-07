class Container(object):

    _messages = None

    def __init__(self):
        self._messages = []

    def post(self, str_message):
        self._messages.append(str_message)

    @property
    def messages(self):
       return self._messages
