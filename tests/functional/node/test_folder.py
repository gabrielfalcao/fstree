# -*- coding: utf-8 -*-
from fstree.node.folder import Folder


def test_node_get_path():
    ('Folder.get_path() should return a string')

    Folder('/foo/bar.bin').get_path().should.equal('/foo/bar.bin')
