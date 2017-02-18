from types import NoneType
from collections import OrderedDict

from fstree._meta import ModelMeta


serializable_python_types = (
    int,
    dict,
    list,
    long,
    float,
    tuple,
    basestring,
    NoneType,
)


def extract_serializable_value(value):
    if isinstance(value, Model):
        value = value.to_dict()

    elif not isinstance(value, serializable_python_types):
        value = repr(value)

    return value


class Model(object):
    __metaclass__ = ModelMeta

    def __init__(self, **params):
        self.__data = OrderedDict([(k, v) for k, v in params.iteritems() if k in self.__fields__])

    @property
    def get_fieldnames(self):
        return self.__data.keys()

    @property
    def data(self):
        return self.__data.copy()

    def __getattr__(self, name):
        if name == 'data' or name.startswith('_'):
            return super(Model, self).__getattr__(name)

        if name in self.data:
            return self.data.get(name)

        raise AttributeError('{0} does not have attribute {1}'.format(self, name))

    def iter_fields(self):
        data = {}
        fields = self.__fields__ or dir(self)

        for name in fields:
            if name.endswith('_') or name.startswith('_'):
                continue

            raw = getattr(self, name, None)
            data[name] = extract_serializable_value(raw)

        return data

    def to_dict(self):
        data = {}
        for name in self.__fields__:
            data[name] = getattr(self, name, None)

        return data

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class AccessPolicy(Model):
    __fields__ = [
        'owner',
        'group',
        'everyone',
        'path',
    ]


class NodeInfo(Model):
    """
    .. note:: all dates are represented as unix timestamp (`int`)

    """
    __fields__ = [
        'uid',
        'gid',
        'size',
        'created_at',
        'last_accessed',
        'last_changed',
        'last_modified',
        'access_policy',
        'path',
        'basepath',
        'filename',
        'shortname',
        'extension',
    ]
