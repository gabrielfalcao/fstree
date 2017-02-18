
from fstree.node import Node
from fstree.default import logger
from fstree.default import get_default_backend


def test_empty_heritage():
    ('fstree.node.Node("path") with an bleak heritage')

    instance = Node('path')
    instance.path.should.equal('path')

    instance.heritage.should.equal({
        'access_policy': None,
        'backend': get_default_backend(),
        'parent': instance,
        'logger': logger,
    })
