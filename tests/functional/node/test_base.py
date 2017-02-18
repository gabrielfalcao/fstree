# -*- coding: utf-8 -*-
from fstree.node.base import Node


def test_node_get_path():
    ('Node.get_path() should return a string')

    Node('/foo/bar').get_path().should.equal('/foo/bar')
