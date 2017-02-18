from fnmatch import fnmatch
from itertools import chain
from fstree.node import File
from fstree.node import Folder
from fstree.models import NodeInfo


def expand_from_definition(parent, definition, TreeClass):
    result = []
    previous_node = parent
    for member in definition:
        if isinstance(member, basestring):
            result.append(TreeClass(parent.expand_path(member), parent=parent))
            previous_node = member

        elif isinstance(member, tuple):
            result.append(expand_from_definition(
                previous_node, member, TreeClass))

    return result


class BaseTree(Folder):
    """The base file-tree implementation, which is basically a
    :py:class:`~fstree.node.Folder` with node-traversal features.
    """

    def iter_files(self):
        """traverse all files recursively"""
        for path in self.backend.iter_files(self.path):
            yield File(path, latest=True)

    def iter_folders(self):
        """traverse all sub-folders recursively"""
        for path in self.backend.iter_files(self.path):
            yield Folder(path, latest=True)

    def iter_all(self):
        """traverse all sub-folders and files recursively"""
        return chain(self.iter_folders(), self.iter_files())


class Tree(BaseTree):
    """A file-tree  with bash-like features:
    - files
    - traverse all files
    - find files by fnmatch/glob
    - find files by regexp
    - find binary files by raw byte search
    - find text files by regexp search

    """

    def glob(self, pattern, sortby=NodeInfo.fields.created_at):
        """

        ::

            >>> tree.glob('./[0-9].*')
            [File(path='/home/user/giphy/1.gif'), File(path='/home/user/giphy/2.gif')]
            >>> tree.glob('*.gif')
            [File(path='/home/user/giphy/card.gif'), File(path='/home/user/giphy/2.gif')]
            >>> tree.glob('?.gif')
            File(path='/home/user/giphy/1.gif')
        """
        for item in self.iter_all():
            if fnmatch(item.name, pattern):
                yield item

    def destroy(self):
        """destroys a tree and optionally scrubs the data in every
        :py:class:`~fstree.node.FileNode` of the type
        `:py:class:fstree.node.types.FileType`.
        """
        for node in self.iter_files():
            node.destroy()

        super(Folder, self).destroy()


class HardCodedTree(Tree):

    def initialize(self, tree_definition=None, TreeClass=Tree):
        self.__definition = getattr(
            self, '__tree_definition__', tree_definition)
        self.__tree = expand_from_definition(self.__definition, TreeClass)

    @property
    def tree(self):
        return self.__tree


class ReadOnlyTree(Folder):
    """A Tree that cannot be destroyed"""

    def create(self, *args, **kw):
        msg = 'cannot create a ReadOnlyTree(path="{0}")'.format(self.path)
        raise RuntimeError(msg)

    def destroy(self):
        msg = 'cannot destroy the ReadOnlyTree(path="{0}")'.format(self.path)
        raise RuntimeError(msg)
