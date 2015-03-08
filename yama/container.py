class Container(object):

    _id = None
    _label = None
    _messages = None
    _storage = None

    def __init__(self, label=None, storage=None, _id=None,
                 contents=None):
        self._id = _id
        self._label = label
        self._messages = contents or []
        self._storage = storage

    def post(self, str_message):
        if self._storage is not None:
            self._storage.post_message(str_message, self._id)
        self._messages.append(str_message)

    @property
    def messages(self):
        return self._messages

    @property
    def label(self):
        return self._label
