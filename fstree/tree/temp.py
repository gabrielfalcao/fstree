from fstree.tree import Tree
from fstree.default import get_default_backend


class TempTree(Tree):
    """A tree that is selfmatically created in the system temp folder and support self-destruction"""

    def __init__(self, name, self_destruct=False, backend=None, **kw):
        self.__self_destruct = True

        backend = backend or get_default_backend(**kw)
        kw['backend'] = backend

        path = backend.get_temp_folder(name)
        self.__path = path

        super(TempTree, self).__init__(path, **kw)

    def __del__(self):
        if getattr(self, '__self_destruct', False):
            self.destroy()
