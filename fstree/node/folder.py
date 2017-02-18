from fstree.node.base import Node
from fstree.exceptions import FSErrors, fserror


class Folder(Node):
    """Has all the features of a
    regular `~Node` except for 2 differences:

    - the `~Folder.create` method creates a folder
    - the `~Folder.destroy` method removes the folder recursively if it exists
    """

    def create(self, name=None, force=False):
        """creates a folder or returns an exising one with pre-loaded
        `~fstree.models.NodeInfo`.

        :param name: if provided must be `bytes`
        :param force: if `True` removes any existing contents before creating
        :returns: a `~Folder`
        """
        if name:
            path = self.expand_path(name)
        else:
            path = self.path

        if force:
            self.destroy()

        try:
            self.backend.create_folder(path)
        except FSErrors as e:
            raise fserror(self, e.errno, path)

        return Folder(path, latest=True)

    def destroy(self):
        return self.backend.delete_folder(self.path)
