# Copyright (c) 2015 Idival, Mario <marioidival@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import unicode_literals
import mongoengine

from mongoengine.base import ValidationError
from mongoengine.queryset import (
    MultipleObjectsReturned,
    DoesNotExist,
    QuerySet
)

from pyramid.httpexceptions import exception_response
from pyramid.renderers import JSON

from .utils import new_adapters


def _include_mongoengine(obj):
    for module in mongoengine, mongoengine.fields:
        for key in module.__all__:
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))


def _connect_database(config):
    """Create simple connection with Mongodb

    config comes with settings from .ini file.
    """
    settings = config.registry.settings

    mongo_uri = "mongodb://localhost"
    mongodb_name = "test"

    if settings.get("mongo_url"):
        mongo_uri = settings["mongo_url"]

    if settings.get("mongodb_name"):
        mongodb_name = settings["mongodb_name"]

    return mongoengine.connect(mongodb_name, host=mongo_uri)


class MongoEngine(object):
    """ MongoEngine class based on flask-mongoengine """

    def __init__(self, config=None):

        _include_mongoengine(self)

        self.Document = Document
        self.DynamicDocument = DynamicDocument

        if config:
            _connect_database(config)


class BaseQuerySet(QuerySet):
    """
    A base queryset with handy extras.

    BaseQuerySet based on flask-mongoengine
    """

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            raise exception_response(404)

    def first_or_404(self):

        obj = self.first()
        if obj is None:
            raise exception_response(404)

        return obj


class Document(mongoengine.Document):
    """Abstract document with extra helpers in the queryset class.

    Document class based on flask-mongoengine
    """

    meta = {"abstract": True, "queryset_class": BaseQuerySet}


class DynamicDocument(mongoengine.DynamicDocument):
    """Abstract Dynamic document with extra helpers in the queryset class.

    DynamicDocument class based on flask-mongoengine
    """

    meta = {"abstract": True, "queryset_class": BaseQuerySet}


def includeme(config):

    # How to connect: config.add_connection_database()
    config.add_directive("add_connection_database", _connect_database)

    # Modify default JSON renderer
    json_adapter = JSON(adapters=new_adapters)

    config.add_renderer("json", json_adapter)
