#!/usr/bin/env python3

from itertools import chain

from yama.container import Container
from yama.message import Message


class Storage(object):

    _connection = None
    _containers = None
    _root_id = None

    def __init__(self, connection=None):
        self._connection = connection
        self._containers = {}
        if connection is not None:
            self._set_root_id(connection)

    def _set_root_id(self, connection):
        root_doc = connection.roots.find_one()
        if root_doc is None:
            self._root_id = connection.roots.save({'list': []})
        else:
            self._root_id = root_doc['_id']

    def _store_root_container(self, cid):
        self._connection.roots.update({'_id': self._root_id},
                                      {'$push': {'list': cid}})

    def create_container(self, str_label):
        cid = self._connection.containers.save({'label': str_label,
                                                'contents': [],
                                                'children': []})
        self._store_root_container(cid)
        self._containers[cid] = Container(label=str_label,
                                          _id=cid, storage=self)
        return self._containers[cid]

    def get_container(self, container_id):
        try:
            return self._containers[container_id]
        except KeyError:
            pass
        document = self._connection.containers.find_one(container_id)
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
        mid = self._connection.messages.save({'text': message.text})
        self._connection.containers.update({'_id': container.id},
                                           {'$push': {'contents': mid}})

    def _load_messages(self, mids):
        query = {'_id': {'$in': mids}}
        results = dict((d['_id'], Message(d['text']))
                       for d in self._connection.messages.find(query))
        return (results[i] for i in mids)

    def get_root_containers(self):
        roots = self._connection.roots.find_one()
        return (self.get_container(cid) for cid in roots['list'])

    def store_container_child(self, container, parent_id):
        cid = self._connection.containers.save({'label': container.label,
                                                'contents': [],
                                                'children': []})
        self._connection.containers.update({'_id': parent_id},
                                           {'$push': {
                                               'children': cid}})
        self._containers[cid] = Container(container.label, _id=cid,
                                          storage=self)
        return self._containers[cid]
