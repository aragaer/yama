#!/usr/bin/env python3

from yama.container import Container


class Storage(object):

    _connection = None
    _containers = None

    def __init__(self, connection=None):
        self._connection = connection
        self._containers = {}

    def _store_root_container(self, cid):
        root_doc = self._connection.roots.find_one()
        if root_doc is None:
            self._connection.roots.save({'list': [cid]})
        else:
            self._connection.roots.update(root_doc['_id'],
                                          {'$push': {'list': cid}})

    def create_container(self, str_label):
        cid = self._connection.containers.save({'label': str_label,
                                                'contents': [],
                                                'children': []})
        self._store_root_container(cid)
        result = Container(label=str_label, _id=cid, storage=self)
        self._containers[cid] = result
        return result

    def get_container(self, container_id):
        try:
            return self._containers[container_id]
        except KeyError:
            pass
        label = None
        contents = None
        children = None
        if self._connection is not None:
            document = self._connection.containers.find_one(container_id)
            label = document['label']
            contents = [self._load_message(mid)
                        for mid in document['contents']]
            children = [self.get_container(cid)
                        for cid in document['children']]
        self._containers[container_id] = Container(label=label,
                                                   _id=container_id,
                                                   contents=contents,
                                                   children=children,
                                                   storage=self)
        return self._containers[container_id]

    def get_container_ids(self):
        for document in self._connection.containers.find():
            yield document['_id']

    def post_message(self, str_message, container_id):
        self._store_message(container_id, str_message)

    def _store_message(self, container_id, str_message):
        message_id = self._connection.messages.save({'text': str_message})
        self._connection.containers.update({'_id': container_id},
                                           {'$push': {
                                               'contents': message_id}})

    def _load_message(self, message_id):
        return self._connection.messages.find_one(message_id)['text']

    def get_root_containers(self):
        roots = self._connection.roots.find_one()
        if roots is not None:
            for cid in roots['list']:
                yield self.get_container(cid)

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
