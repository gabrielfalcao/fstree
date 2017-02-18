from socket import error as SocketError

from fstree._meta import ErrorMeta
from fstree._meta import get_node_error
from fstree.utils import objectid

FSErrors = (OSError, IOError, SocketError)


class UnsupportedPath(Exception):
    schema_prefix = None

    def __init__(self, path):
        template = " ".join([
            'Could not find a Node implementation that',
            'supports the path: {path}',
        ])
        context = {
            'path': path,
        }

        if self.schema_prefix:
            schema = '{0}://'.format(self.schema_prefix)
            context['schema'] = schema
            template.append('Should have matched the schema "{schema}"')

        message = template.format(**context)
        super(UnsupportedPath, self).__init__(message)


class InvalidSchema(Exception):
    def __init__(self, schema):
        pass


class InvalidNode(Exception):
    pass


class NodeError(Exception):
    """

    based on `posix errno <http://www.ioplex.com/~miallen/errcmp.html>`_
    """
    __metaclass__ = ErrorMeta
    __nodepath__ = 'fstree.node.base.Node'
    __template__ = 'Failed to perform operation with {node[path]}'

    def __init__(self, node, target_path=None, **context):
        context.update({
            'node': node.to_dict(),
            'target_path': target_path,
        })

        if node.parent:
            context['parent'] = node.parent.to_dict()

        msg = self.render(**context)
        super(NodeError, self).__init__(msg.format(node=node, path=node.path))

    def render(self, *args, **kw):
        excid = objectid(self)
        template = self.__template__
        try:
            return template.format(*args, **kw)
        except KeyError as e:
            key = bytes(e)
            raise RuntimeError('{excid} failed to render error message "{template}" because the missing context variable {key}'.format(**locals()))


class FileNodeError(NodeError):
    __nodepath__ = 'fstree.node.file.File'


class FolderNodeError(NodeError):
    __nodepath__ = 'fstree.node.folder.Folder'


class InvalidFileDescriptor(NodeError):
    __template__ = (
        'the node {node[name]} at {parent[relative_path]} '
        'has file-descriptor {node[fileno]} but you tried to {action} the fileno {fileno} at {target_path}'
    )


class OperationFailed(NodeError):
    __template__ = (
        'the node {node[name]} at {parent[relative_path]} '
        'already has an open file-descriptor'
    )


class FileAlreadyOpen(FileNodeError):
    __template__ = (
        'the node {node[name]} at {parent[relative_path]} '
        'already has an open file-descriptor'
    )


class FileAlreadyExists(FileNodeError):
    __errno__ = 17
    __template__ = (
        'the file {node[name]} at {parent[relative_path]} '
        'already exists'
    )


class FolderAlreadyExists(FolderNodeError):
    __nodepath__ = 'fstree.node.folder.Folder'
    __errno__ = 17
    __template__ = (
        'the folder {node[name]} at {parent[relative_path]} '
        'already exists'
    )


def fserror(node, errno, path):
    Exc = get_node_error(node, errno)
    raise Exc(node, path)
