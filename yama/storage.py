#!/usr/bin/env python3

from bson import ObjectId

from yama.container import Container
from yama.mongo import MongoStorage
from yama.record import Record


class Storage(object):

    _cached_objects = None
    _storage = None

    def __init__(self, connection=None):
        self._cached_objects = {}
        if connection is not None:
            self._storage = MongoStorage(connection)

    def _store_item(self, item):
        if item.id is None:
            item.id = ObjectId()
        self._storage.store_new_item(Record.from_item(item))

    def _create_container(self, str_label):
        result = Container(label=str_label, storage=self)
        self._store_item(result)
        self._cached_objects[result.id] = result
        return result

    def _make_root(self, container):
        self._storage.add_to_roots(container.id)

    def create_container(self, str_label):
        container = self._create_container(str_label)
        self._make_root(container)
        return container

    def _store_as_child(self, child, parent):
        self._storage.store_child(child.id, parent.id)

    def store_item(self, child, parent):
        self._store_item(child)
        self._store_as_child(child, parent)

    def get_container(self, container_id):
        try:
            return self._cached_objects[container_id]
        except KeyError:
            result = self._storage.load_one_item(container_id).inflate(self)
            self._cached_objects[container_id] = result
            return result

    def load_items(self, ids):
        return (m.inflate(self) for m in self._storage.load_many_items(ids))

    def get_root_containers(self):
        return (self.get_container(cid)
                for cid in self._storage.get_root_ids())
