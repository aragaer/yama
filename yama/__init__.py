class YamaObject(object):

    _id = None

    def __init__(self, _id):
        self._id = _id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
