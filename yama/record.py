#!/usr/bin/env python3

"""This file handles conversion between objects and how they are stored."""

from yama.container import Container
from yama.message import Message


_RECORD_FROM_TYPE = {}
_RECORD_FOR_CLASS = {}


def _type(name):
    def wrapper(r_cls):
        _RECORD_FROM_TYPE[name] = r_cls
        return r_cls
    return wrapper


def _class(cls):
    def wrapper(r_cls):
        _RECORD_FOR_CLASS[cls] = r_cls
        return r_cls
    return wrapper


class Record(object):
    @staticmethod
    def from_item(item):
        return _RECORD_FOR_CLASS[type(item)].from_item(item)

    @staticmethod
    def from_document(document):
        return _RECORD_FROM_TYPE[document.pop('type')](**document)


@_type('container')
@_class(Container)
class _ContainerRecord(object):

    def __init__(self, label, contents, _id):
        self._label = label
        self._contents = contents or []
        self._id = _id

    @classmethod
    def from_item(cls, container):
        return cls(container.label, None, container.id)

    @property
    def document(self):
        return {'_id': self._id,
                'type': 'container',
                'label': self._label,
                'contents': self._contents}

    def inflate(self, context):
        return Container(_id=self._id,
                         label=self._label,
                         contents=context.load_items(self._contents),
                         storage=context)


@_type('message')
@_class(Message)
class _MessageRecord(object):

    def __init__(self, text, _id):
        self._text = text
        self._id = _id

    @classmethod
    def from_item(cls, message):
        return cls(message.text, message.id)

    @property
    def document(self):
        return {'_id': self._id,
                'type': 'message',
                'text': self._text}

    def inflate(self, _):
        return Message(self._text, _id=self._id)
