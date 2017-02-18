
from fstree.utils import objectid
from fstree.utils import unpack_node_dict
from fstree.utils import iter_lifo


class DummyDummy(object):
    pass


def test_objectid():
    ('fstree.utils.objectid() returns "module.classname" '
     'for either a class or instance')

    dummy = DummyDummy()

    objectid(dummy).should.equal('tests.unit.test_utils.DummyDummy')
    objectid(DummyDummy).should.equal('tests.unit.test_utils.DummyDummy')


def test_iter_lifo():
    'fstree.utils.iter_lifo()'

    items = ['a', 'b']
    list(iter_lifo(items)).should.equal(['b', 'a'])


def test_unpack_node_dict():
    'fstree.utils.unpack_node_dict()'

    result = unpack_node_dict(path='path', info='info', extra='discarded')
    result.should.equal(('path', 'info'))
