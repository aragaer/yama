from yama import YamaObject


class Message(YamaObject):

    _contents = None

    def __init__(self, contents, _id=None):
        super().__init__(_id)
        self._contents = contents

    @property
    def text(self):
        return self._contents
