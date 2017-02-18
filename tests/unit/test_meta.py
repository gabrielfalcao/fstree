
from fstree._meta import list_nodes
from fstree._meta import list_backends
from fstree._meta import list_file_types

from fstree import backends

from fstree.node import Node
from fstree.node import File
from fstree.node import Folder
from fstree.tree import Tree
from fstree.tree import TempTree
from fstree.tree.base import BaseTree
from fstree.tree.base import HardCodedTree
from fstree.tree.base import ReadOnlyTree

from fstree.node import types as file_types


def test_list_nodes():
    ("list_nodes() returns all known types of nodes")

    list_nodes().should.equal([
        (TempTree, ('fstree.tree.temp', 'TempTree'), None),
        (ReadOnlyTree, ('fstree.tree.base', 'ReadOnlyTree'), None),
        (HardCodedTree, ('fstree.tree.base', 'HardCodedTree'), None),
        (Tree, ('fstree.tree.base', 'Tree'), None),
        (BaseTree, ('fstree.tree.base', 'BaseTree'), None),
        (Folder, ('fstree.node.folder', 'Folder'), None),
        (File, ('fstree.node.file', 'File'), None),
        (Node, ('fstree.node.base', 'Node'), None)
    ])


def test_list_file_types():
    ("list_file_types() returns all known types of file types")

    list_file_types().should.equal([
        (file_types.SocketType, ('fstree.node.types', 'SocketType'), 'SOCKET'),
        (file_types.PipeType, ('fstree.node.types', 'PipeType'), 'PIPE'),
        (file_types.HardlinkType, ('fstree.node.types', 'HardlinkType'), 'HARDLINK'),
        (file_types.SymlinkType, ('fstree.node.types', 'SymlinkType'), 'SYMLINK'),
        (file_types.DeviceType, ('fstree.node.types', 'DeviceType'), 'DEVICE'),
        (file_types.FolderType, ('fstree.node.types', 'FolderType'), 'FOLDER'),
        (file_types.FileType, ('fstree.node.types', 'FileType'), 'FILE')
    ])


def test_list_backends():
    ("list_backends() returns all known types of backends")

    list_backends().should.equal([
        (backends.DreamObjects, ('fstree.backends.dreamhost', 'DreamObjects'), None),
        (backends.DropBox, ('fstree.backends.dropbox', 'DropBox'), None),
        (backends.Box, ('fstree.backends.box', 'Box'), None),
        (backends.ElasticFileSystem, ('fstree.backends.aws', 'ElasticFileSystem'), 'efs://'),
        (backends.S3, ('fstree.backends.aws', 'S3'), 's3://'),
        (backends.SecureFTP, ('fstree.backends.ssh', 'SecureFTP'), None),
        (backends.FTP, ('fstree.backends.ftp', 'FTP'), None),
        (backends.Dummy, ('fstree.backends.dummy', 'Dummy'), None),
        (backends.Local, ('fstree.backends.local', 'Local'), None),
        (backends.Windows, ('fstree.backends.nt', 'Windows'), None),
        (backends.Posix, ('fstree.backends.posix', 'Posix'), None),
        (backends.Backend, ('fstree.backends.base', 'Backend'), None)
    ])
