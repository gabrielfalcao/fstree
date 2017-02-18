import _io
from io import BufferedIOBase
from abc import ABCMeta

from StringIO import StringIO

from fstree.exceptions import InvalidNode
from fstree.exceptions import UnsupportedPath
from fstree._meta import list_nodes
from fstree._meta import list_backends
from fstree._meta import list_file_types
from fstree._meta import get_node_error


__all__ = [
    'FileDescriptor',
    'node_from_path',
    'backend_from_path',
    'node_by_type_name_and_path',
    'list_nodes',
    'list_backends',
    'list_file_types',
    'get_node_error',
]


class FileDescriptor(object):
    __metaclass__ = ABCMeta

    @classmethod
    def ack_paternity(cls, child):
        return child is not None and isinstance(child, cls) or type(child) in (
            BufferedIOBase,
            _io.BufferedReader,
            _io.BufferedWriter,
        ) or callable(getattr(child, 'fileno', None))


FileDescriptor.register(file)
FileDescriptor.register(StringIO)
FileDescriptor.register(BufferedIOBase)
FileDescriptor.register(_io.BufferedReader)
FileDescriptor.register(_io.BufferedWriter)


def node_from_path(path, backend=None, latest=False, **kw):
    """returns an appropriate Node instance to handle the given path

    :param path: a string
    :param backend: ensure the resulting node supports this backend instance
    :param latest: whether to latest the node (default: `False`)
    :raises UnsupportedPath: if no suitable nodes were found.
    :returns: an instance of some :py:class:`~Node` subclass.
    """

    kw['latest'] = latest
    kw['backend'] = backend

    for NodeClass, (modulename, classname), FileType in list_nodes():
        if NodeClass.supports_path(path):
            return NodeClass(path, **kw)

    raise UnsupportedPath(path)


def backend_from_path(path, **kw):
    """returns an appropriate Backend instance to handle the given path

    :param path: a string
    :raises UnsupportedPath: if no suitable nodes were found.
    :returns: an instance of some :py:class:`~Backend` subclass.
    """

    for BackendClass, (modulename, classname), schema in list_backends():
        if BackendClass.supports_path(path):
            return BackendClass(**kw)

    raise UnsupportedPath(path)


def node_by_type_name_and_path(name, path, backend=None, latest=False, **kw):
    """returns a new Node instance matching the given name and pointing to the indicated path

    :param name: a string with <class-name> or <module-name>.<class-name>
    :param path: a string
    :param backend: ensure the resulting node supports this backend instance
    :param latest: whether to latest the node (default: `False`)
    :raises InvalidNode: if there are no Node implementations matching the given name
    :returns: an instance of the specified class
    """
    kw['latest'] = latest
    kw['backend'] = backend

    for NodeClass, (modulename, classname), FileType in list_nodes():
        objectid = ".".join([modulename, classname])

        if objectid.endswith(name):
            return NodeClass(path, **kw)

    raise InvalidNode(name)


def create_file_node(*args, **kw):
    """shortcut to create an instance of `~fstree.node.file.File`

    :param *args: forwarded to the constructor method
    :param *kw: forwarded to the constructor method
    :returns: `~fstree.node.file.File`
    """
    return node_by_type_name_and_path('fstree.node.file.File', *args, **kw)


def create_folder_node(*args, **kw):
    """shortcut to create an instance of `~fstree.node.folder.Folder`

    :param *args: forwarded to the constructor method
    :param *kw: forwarded to the constructor method
    :returns: `~fstree.node.folder.Folder`
    """
    return node_by_type_name_and_path('fstree.node.folder.Folder', *args, **kw)
