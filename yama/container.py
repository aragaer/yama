from yama import YamaObject
from yama.message import Message


class Container(YamaObject):

    _contents = None
    _label = None
    _storage = None

    def __init__(self, label=None, storage=None, _id=None, contents=None):
        super().__init__(_id)
        self._label = label
        self._contents = list(contents or [])
        self._storage = storage

    def post(self, str_message):
        message = Message(str_message)
        if self._storage is not None:
            self._storage.post_message(message, self)
        self._contents.append(message)

    def create_child(self, child_name):
        child = Container(child_name, storage=self._storage)
        if self._storage is not None:
            child = self._storage.store_container_child(child, self.id)
        self._contents.append(child)
        return child

    @property
    def children(self):
        return (item for item in self._contents
                if isinstance(item, Container))

    @property
    def messages(self):
        return (item.text for item in self._contents
                if isinstance(item, Message))

    @property
    def label(self):
        return self._label
