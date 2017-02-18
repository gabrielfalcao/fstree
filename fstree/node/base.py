from fstree._meta import NodeMeta
from fstree.utils import unpack_node_dict

from fstree.models import NodeInfo

from fstree.default import DEFAULT_LOGGER
from fstree.default import get_default_backend

from fstree.meta import node_from_path
from fstree.meta import backend_from_path
from fstree.meta import create_file_node
from fstree.meta import create_folder_node
from fstree.meta import node_by_type_name_and_path


class Node(object):
    """base class with common properties and methods among all types of
    Node:

    .. glossary::

       - :py:class:`fstree.node.File`
       - :py:class:`fstree.node.Folder`
       - :py:class:`fstree.tree.Tree`
       - :py:class:`fstree.tree.TempTree`

    """
    __metaclass__ = NodeMeta

    __repr_args__ = '(path={path})'

    # a safety flag to prevent child nodes to be destroyed and is
    # inherited by all the child node instances:
    __read_only__ = False

    def __init__(self, path, backend=None, parent=None, info=None, access_policy=None, logger=None, latest=False, *args, **kw):
        """
        :param path: `bytes` with the path to the file or folder, or a `~Node` from which the path will be extracted.
        :param backend: an instance of any :py:class:`~fstree.backends.Backend` subtype.
        :param parent: another instance of `~Node` (default: `None`)
        :param info: a :py:class:`~fstree.models.NodeInfo` - this argument is ignored when ``latest=True`` (defaults to an empty node info)
        :param access_policy: a :py:class:`~fstree.models.AccessPolicy` - this argument is ignored when ``latest=True`` (defaults to an empty access policy)
        :param logger: a logger instance. (defaults to ``logging.getLogger('fstree')``
        :param latest: when `True` the ``info`` and ``access_policy`` are freshly loaded with the backend.
        :raises IOError: if latest=True but the given ``path`` does not exist.
        """

        # fallback to the parent's backend first
        if parent:
            backend = backend or parent.backend

        # final fallback to default backend
        backend = backend or get_default_backend(**kw)

        logger = logger or DEFAULT_LOGGER

        self._latest = latest is True

        if isinstance(parent, Node):
            path = parent.expand_path(path)

        if latest:
            info = backend.load_info(path)
            access_policy = info.access_policy
        elif info:
            access_policy = access_policy or info.access_policy

        self._path = path
        self._info = info
        self._access_policy = access_policy
        self._backend = backend
        self._parent = parent
        self.log = logger
        self.initialize(*args, **kw)

    def initialize(self, *args, **kw):
        pass

    def get_path(self):
        return self._path

    path = property(fget=get_path)

    @property
    def relative_path(self):
        return self.backend.collapse_path(self.path)

    @property
    def name(self):
        """the file/folder name without the parent path (includes extension in case of files)"""
        return self.backend.get_file_name(self.path)

    @property
    def shortname(self):
        """same as `~Node.name` but without the extension"""
        return self.backend.remove_extension(self.name)

    @property
    def parent(self):
        if not self._parent:
            self._parent = node_by_type_name_and_path(
                'fstree.node.folder.Folder', self.path)

        return self._parent

    @property
    def backend(self):
        return self._backend

    @property
    def info(self):
        return self._info

    @property
    def size(self):
        return self.info.size

    @property
    def access_policy(self):
        return self._access_policy

    @property
    def heritage(self):
        """returns a dict with the kwargs necessary to create a child node"""
        child_kwargs = {}
        child_kwargs['parent'] = self
        child_kwargs['backend'] = self.backend
        child_kwargs['access_policy'] = self.access_policy
        child_kwargs['logger'] = self.log

        return child_kwargs

    @property
    def latest(self):
        return self.reloaded()

    def __str__(self):
        return self.path

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.__repr_args__.format(path=self.name)
        )

    def expand_path(self, *args):
        return self.backend.expand_path(self.path, *args)

    def expand_path_to_callback(self, path, callback, *args, **kw):
        return callback(self.expand_path(path), *args, **kw)

    def load_info(self):
        return self.backend.load_info(self.path)

    def load_access_policy(self):
        return self.backend.load_access_policy(self.path)

    def clone_params(self):
        return {
        }

    def reloaded(self):
        fresh = self.load_info()
        return self.__class__(self.path, backend=self.backend, info=fresh, logger=self.log, **self.clone_params())

    def does_exist(self):
        return self.backend.exists(self.path)

    # def child(self, *parts, **kw):
    #     path = self.expand_path(*parts)
    #     return node_from_path(path, backend=self.backend, **kw)

    def child_file(self, name, **kw):
        kw['parent'] = self
        return self.expand_path_to_callback(name, create_file_node, **kw)

    def child_folder(self, name, **kw):
        kw['parent'] = self
        return self.expand_path_to_callback(name, create_folder_node, **kw)

    def create_file(self, name, *args, **kw):
        return self.child_file(name).create(*args, **kw)

    def create_folder(self, name, *args, **kw):
        return self.child_folder(name).create(*args, **kw)

    # def ensure_access_policy(self, access_policy=None):
    #     access_policy = access_policy or self.access_policy
    #     self.backend.apply_access_policy(self.path, access_policy)

    def to_dict(self):
        data = self.clone_params()
        data['name'] = self.name
        data['shortname'] = self.shortname
        data['path'] = self.path
        data['relative_path'] = self.relative_path
        data['info'] = self.info and self.info.to_dict() or None
        return data

    # @classmethod
    # def from_dict(cls, data, backend=None, **kw):
    #     path, info = unpack_node_dict(**data)

    #     if not backend:
    #         backend = backend_from_path(path)

    #     info = NodeInfo.from_dict(info)
    #     return cls(path, backend=backend, info=info, **kw)

    @classmethod
    def supports_path(cls, path, backend=None):
        backend = backend or get_default_backend()
        return backend.supports_path(path)

    def destroy(self):
        if not self.does_exist():
            return False

        return self.backend.delete(self.path)
