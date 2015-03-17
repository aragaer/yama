#!/usr/bin/env python3

from itertools import chain

from yama.container import Container
from yama.message import Message


class Storage(object):

    _cache = None
    _storage = None

    def __init__(self, connection=None):
        self._cache = {}
        if connection is not None:
            self._storage = _MongoStorage(connection)

    def _cache(function):
        def wrapper(self, *args, **kwargs):
            result = function(self, *args, **kwargs)
            self._cache[result.id] = result
            return result
        return wrapper

    def _cached(function):
        def wrapper(self, item_id):
            try:
                return self._cache[item_id]
            except KeyError:
                self._cache[item_id] = function(self, item_id)
                return self._cache[item_id]
        return wrapper

    def _fill_in_id(self, item):
        record = _Record.from_item(item)
        item.id = self._storage.store_new_item(record)

    def _create_container(self, str_label):
        result = Container(label=str_label, storage=self)
        self._fill_in_id(result)
        return result

    def _make_root(self, container):
        self._storage.add_to_roots(container.id)

    @_cache
    def create_container(self, str_label):
        container = self._create_container(str_label)
        self._make_root(container)
        return container

    def _store_as_child_c(self, child, parent):
        self._storage.store_child_c(child.id, parent.id)

    def _store_as_child_m(self, child, parent):
        self._storage.store_child_m(child.id, parent.id)

    def store_container_child(self, child, parent):
        self._fill_in_id(child)
        self._store_as_child_c(child, parent)

    def post_message(self, message, container):
        self._fill_in_id(message)
        self._store_as_child_m(message, container)

    @_cached
    def get_container(self, container_id):
        return self._storage.load_container(container_id).inflate(self)

    def load_messages(self, mids):
        return (m.inflate(self) for m in self._storage.load_messages(mids))

    def get_root_containers(self):
        return (self.get_container(cid) for cid in self._storage.get_root_ids())


class _Record(object):
    @staticmethod
    def from_item(item):
        if isinstance(item, Container):
            return _ContainerRecord.from_item(item)
        elif isinstance(item, Message):
            return _MessageRecord.from_item(item)
        else:
            raise ValueError("Unknown class " + type(item))


class _ContainerRecord(object):

    def __init__(self, label, contents=None, children=None, _id=None):
        self._label = label
        self._contents = contents or []
        self._children = children or []
        self._id = _id

    @classmethod
    def from_item(cls, container):
        return cls(container.label, None, None, None)

    @property
    def document(self):
        return {'label': self._label,
                'contents': self._contents,
                'children': self._children}

    def inflate(self, storage):
        contents = chain(storage.load_messages(self._contents),
                         (storage.get_container(cid) for cid in self._children))
        return Container(_id=self._id,
                         label=self._label,
                         contents=contents,
                         storage=storage)

    @property
    def collection(self):
        return 'containers'


class _MessageRecord(object):

    def __init__(self, text, _id=None):
        self._text = text
        self._id = _id

    @classmethod
    def from_item(cls, message):
        return cls(text=message.text)

    @property
    def document(self):
        return {'text': self._text}

    def inflate(self, _):
        return Message(self._text, _id=self._id)

    @property
    def collection(self):
        return 'messages'


class _MongoStorage(object):

    _connection = None
    _root_id = None

    _CONTAINERS = None
    _MESSAGES = None
    _ROOTS = None

    def __init__(self, connection):
        self._connection = connection
        self._CONTAINERS = connection.containers
        self._MESSAGES = connection.messages
        self._ROOTS = connection.roots
        root_doc = self._ROOTS.find_one()
        if root_doc is None:
            self._root_id = self._ROOTS.save({'list': []})
        else:
            self._root_id = root_doc['_id']

    def add_to_roots(self, container_id):
        self._ROOTS.update({'_id': self._root_id},
                           {'$push': {'list': container_id}})

    def store_new_item(self, doc):
        """Save the new document and return the assigned _id."""
        return self._connection[doc.collection].save(doc.document)

    def _store_child(self, child_id, parent_id, list_name):
        self._CONTAINERS.update({'_id': parent_id},
                                {'$push': {list_name: child_id}})

    def store_child_c(self, child_id, parent_id):
        self._store_child(child_id, parent_id, 'children')

    def store_child_m(self, child_id, parent_id):
        self._store_child(child_id, parent_id, 'contents')

    def get_root_ids(self):
        return self._ROOTS.find_one(self._root_id)['list']

    def load_messages(self, mids):
        query = {'_id': {'$in': mids}}
        results = dict((d['_id'], _MessageRecord(**d))
                       for d in self._MESSAGES.find(query))
        return (results[i] for i in mids)

    def load_container(self, container_id):
        return _ContainerRecord(**self._CONTAINERS.find_one(container_id))
