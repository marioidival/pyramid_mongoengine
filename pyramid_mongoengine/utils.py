from __future__ import unicode_literals
from bson import json_util

from mongoengine.base import BaseDocument

try:
    from mongoengine.base import BaseQuerySet
except ImportError as ie: # support mongoengine < 0.7
    from mongoengine.queryset import QuerySet as BaseQuerySet


def basedocument_adapter(obj, request):
    if isinstance(obj, BaseDocument):
        return json_util._json_convert(obj.to_mongo())


def basequeryset_adapter(obj, request):
    if isinstance(obj, BaseQuerySet):
        return json_util._json_convert(obj.as_pymongo())

new_adapters = (
    (BaseDocument, basedocument_adapter),
    (BaseQuerySet, basequeryset_adapter)
)
