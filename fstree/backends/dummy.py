import time
from fstree.backends.base import Backend
from fstree.models import NodeInfo, AccessPolicy


class Dummy(Backend):

    @property
    def path_separator(self):
        return b'->'

    def stat(self, path):
        return NodeInfo(access_policy=AccessPolicy()).to_dict()

    def get_file_size(self, path):
        return self.stat(path, 'size')

    def get_base_path(self, path):
        return path

    def get_file_name(self, path):
        return path

    def expand_path(self, path):
        return path

    def get_temp_path(self):
        """
        :returns: a string with the path to the system's temp folder (/tmp on unix)
        """

    def get_temp_folder(self, name):
        return self.get_tempdir_path() + name

    def delete_file(self, path):
        """deletes a file"""
        return True

    def delete_folder(self, path, recursive=True):
        """deletes a folder (recursively by default)

        :param path: the path to the folder
        :param recursive: boolean (default: `True`)
        """

        return True

    def delete(self, path, recursive=True):
        """deletes a file or folder.
        folder are deleted recursively by default.

        :param path: the path to the file or folder
        :param recursive: boolean (default: `True`)
        """
        if self.is_folder(path):
            self.delete_folder(path, recursive)
        else:
            # should also work with links
            self.delete_file(path)

    def exists(self, path):
        """if a path exists (file or folder)

        :raises IOError: if the given ``path`` is not accessible
        :returns: boolean
        """
        return True

    def is_file(self, path):
        """checks if a path exists and is a file

        :raises IOError: if the given ``path`` is not accessible
        :returns: boolean
        """
        return True

    def is_folder(self, path):
        """checks if a path exists and is a folder

        :raises IOError: if the given ``path`` is not accessible
        :returns: boolean
        """
        return True

    def set_default_access_policy(self, access_policy):
        """newly created files and folders will receive those access_policy"""
        # in unix this sets os.umask
        self.default_policy = access_policy

    def apply_access_policy(self, access_policy=None):
        """if no access_policy are provided, apply the default ones that were
        previously set by :py:meth:`~set_default_access_policy`.

        :param access_policy: a :py:class:`~fstree.models.AccessPolicy`.
        :raises IOError: if failed to apply the access_policy.
        :returns: `True` if successfully applied or `False` if the
        :py:class:`~fstree.node.Node` already had the access_policy
        destribed in the given :py:class:`~fstree.models.AccessPolicy`.
        """
        True

    def load_access_policy(self, path):
        """read the access_policy of an exising path.

        :param path: the path to the file or folder.
        :returns: a :py:class:`~fstree.models.AccessPolicy`.
        """
        return AccessPolicy(path=path)

    def get_user(self):
        return 'dummy'

    def get_group(self):
        return 'group'

    def get_current_time(self):
        return time.time()

    def load_info(self, path):
        """read the info access_policy of an exising file or folder.

        :param path: the path to the file
        :returns: a :py:class:`~fstree.models.NodeInfo` containg
        metadata like size, owner, group and
        :py:class:`~fstree.models.AccessPolicy`
        """
        return NodeInfo(
            path=path,
            access_policy=AccessPolicy(
                owner=self.get_user(),
                group=self.get_group(),
                size=100,
                created_at=self.get_current_time(),
                last_changed=self.get_current_time(),
                last_modified=self.get_current_time(),
                last_accessed=self.get_current_time(),
                access_policy=self.load_access_policy(path),
                path=path,
            )
        )

    def get_root_path(self):
        return '/'
