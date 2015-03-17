#!/usr/bin/env python3

from itertools import chain

from yama.container import Container
from yama.message import Message


class Storage(object):

    _containers = None
    _storage = None

    def __init__(self, connection=None):
        self._containers = {}
        if connection is not None:
            self._storage = _MongoStorage(connection)

    def _create_container_id(self, label):
        return self._storage.store_new_container(label)

    def _create_message_id(self, text):
        return self._storage.store_new_message(text)

    def _create_container(self, str_label):
        cid = self._create_container_id(str_label)
        self._containers[cid] = Container(label=str_label,
                                          _id=cid, storage=self)
        return self._containers[cid]

    def _make_root(self, container):
        self._storage.add_to_roots(container.id)

    def create_container(self, str_label):
        container = self._create_container(str_label)
        self._make_root(container)
        return container

    def _store_as_child(self, child, parent_id):
        self._storage.store_child(child.id, parent_id)

    def _store_as_child_m(self, child, parent_id):
        self._storage.store_child_m(child.id, parent_id)

    def store_container_child(self, container, parent_id):
        container.id = self._create_container_id(container.label)
        self._containers[container.id] = container
        self._store_as_child(container, parent_id)
        return container

    def get_container(self, container_id):
        try:
            return self._containers[container_id]
        except KeyError:
            pass
        document = self._storage.load_container(container_id)
        contents = chain(self._load_messages(document['contents']),
                         (self.get_container(cid)
                          for cid in document['children']))
        self._containers[container_id] = Container(label=document['label'],
                                                   _id=container_id,
                                                   contents=contents,
                                                   storage=self)
        return self._containers[container_id]

    def post_message(self, message, container):
        self._store_message(container, message)

    def _store_message(self, container, message):
        message.id = self._create_message_id(message.text)
        self._store_as_child_m(message, container.id)

    def _load_messages(self, mids):
        return (Message(m) for m in self._storage.load_messages(mids))

    def get_root_containers(self):
        return (self.get_container(cid) for cid in self._storage.get_root_ids())


class _MongoStorage(object):

    _root_id = None

    _CONTAINERS = None
    _MESSAGES = None
    _ROOTS = None

    def __init__(self, connection):
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

    def store_new_container(self, str_label):
        return self._CONTAINERS.save({'label': str_label,
                                      'contents': [], 'children': []})

    def store_new_message(self, str_text):
        return self._MESSAGES.save({'text': str_text})

    def _store_child(self, child_id, parent_id, list_name):
        self._CONTAINERS.update({'_id': parent_id},
                                {'$push': {list_name: child_id}})

    def store_child(self, child_id, parent_id):
        self._store_child(child_id, parent_id, 'children')

    def store_child_m(self, child_id, parent_id):
        self._store_child(child_id, parent_id, 'contents')

    def get_root_ids(self):
        return self._ROOTS.find_one(self._root_id)['list']

    def load_messages(self, mids):
        query = {'_id': {'$in': mids}}
        results = dict((d['_id'], d['text']) for d in self._MESSAGES.find(query))
        return (results[i] for i in mids)

    def load_container(self, container_id):
        return self._CONTAINERS.find_one(container_id)
