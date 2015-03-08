#!/usr/bin/env python3

from yama.container import Container


class Storage(object):

    _connection = None
    _containers = None

    def __init__(self, connection=None):
        self._connection = connection
        self._containers = {}

    def create_container(self, str_label):
        cid = self._connection.containers.save({'label': str_label,
                                                'contents': []})
        result = Container(label=str_label, _id=cid, storage=self)
        self._containers[cid] = result
        return result

    def get_container(self, container_id):
        try:
            return self._containers[container_id]
        except KeyError:
            label = None
            contents = None
            if self._connection is not None:
                document = self._connection.containers.find_one(container_id)
                label = document['label']
                contents = document['contents']
            self._containers[container_id] = Container(label=label,
                                                       _id=container_id,
                                                       contents=contents)
            return self._containers[container_id]

    def get_container_ids(self):
        for document in self._connection.containers.find():
            yield document['_id']

    def post_message(self, str_message, container_id):
        self._containers[container_id].messages.append(str_message)
        self._connection.containers.update(container_id,
                                           {'$push': {
                                               'contents': str_message}})
