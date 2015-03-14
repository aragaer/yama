class Container(object):

    _children = None
    _id = None
    _label = None
    _messages = None
    _storage = None

    def __init__(self, label=None, storage=None, _id=None,
                 contents=None, children=None):
        self._children = children or []
        self._id = _id
        self._label = label
        self._messages = contents or []
        self._storage = storage

    def post(self, str_message):
        if self._storage is not None:
            self._storage.post_message(str_message, self._id)
        self._messages.append(str_message)

    def create_child(self, child_name):
        child = Container(child_name)
        if self._storage is not None:
            child = self._storage.store_container_child(child, self._id)
        self._children.append(child)
        return child

    @property
    def messages(self):
        return self._messages

    @property
    def label(self):
        return self._label

    @property
    def children(self):
        return self._children
