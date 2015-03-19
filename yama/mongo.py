from yama.record import Record


class MongoStorage(object):

    _collection = None
    _connection = None
    _root_id = None

    _roots = None

    def __init__(self, connection):
        self._connection = connection
        self._collection = connection.objects
        self._roots = connection.roots
        root_doc = self._roots.find_one()
        if root_doc is None:
            self._root_id = self._roots.save({'list': []})
        else:
            self._root_id = root_doc['_id']

    def add_to_roots(self, container_id):
        self._roots.update({'_id': self._root_id},
                           {'$push': {'list': container_id}})

    def store_new_item(self, doc):
        """Save the new document."""
        self._collection.save(doc.document)

    def store_child(self, child_id, parent_id):
        self._collection.update({'_id': parent_id},
                                {'$push': {'contents': child_id}})

    def get_root_ids(self):
        return self._roots.find_one(self._root_id)['list']

    def load_one_item(self, item_id):
        return Record.from_document(self._collection.find_one(item_id))

    def load_many_items(self, item_ids):
        query = {'_id': {'$in': item_ids}}
        results = dict((d['_id'], Record.from_document(d))
                       for d in self._collection.find(query))
        return (results[i] for i in item_ids)
