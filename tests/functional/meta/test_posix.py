# -*- coding: utf-8 -*-

"\033[0;33m@posix\n======\n\n\033[0;32mfstree.meta\033[0m"

from fstree.meta import node_from_path

from tests.functional.scenarios import posix, SubScenario


@posix
def test_node_from_path(context):
    ("fstree.meta.node_from_path()")

    SubScenario('detect file')
    finode = node_from_path(context.files[0], context.backend)
    finode.should.be.a('fstree.node.file.File')

    SubScenario('detect folder')
    fonode = node_from_path(context.path, context.backend)
    fonode.should.be.a('fstree.node.folder.Folder')
