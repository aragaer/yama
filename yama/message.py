class Message(object):

    _contents = None

    def __init__(self, contents):
        self._contents = contents

    @property
    def text(self):
        return self._contents
