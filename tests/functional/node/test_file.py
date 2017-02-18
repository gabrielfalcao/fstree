# -*- coding: utf-8 -*-
from fstree.node.file import File


def test_node_get_path():
    ('File.get_path() should return a string')

    File('/foo/bar.bin').get_path().should.equal('/foo/bar.bin')
