"""
utility components used across the fstree codebase

"""
import sys


class Sorter(object):
    def __init__(self, fields):
        for name in fields:
            setattr(self, name, lambda items: self._sorted(name, items))

    def _sorted(self, name, items):
        return sorted(items, key=lambda i: getattr(i, name, None))


def objectid(item):

    if not isinstance(item, type):
        return objectid(item.__class__)

    return ".".join((item.__module__, item.__name__))


def unpack_node_dict(path=None, info=None, **kw):
    return path, info


def iter_lifo(iterable):
    """
    :abbr:`LIFO (last-in, first-out)`.
    """
    for item in reversed(iterable):
        yield item


def unique(iterable):
    result = []

    for x in iterable:
        if x in result:
            continue

        result.append(x)

    return result


def import_from_objectid(objectid):
    parts = objectid.split('.')
    module_name = '.'.join(parts[:-1])
    name = parts[-1]
    module = sys.modules[module_name]
    return getattr(module, name)
