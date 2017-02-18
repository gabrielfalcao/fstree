from __future__ import unicode_literals

import io
import os
import stat
import time
import shutil
import tempfile

from os.path import join, exists, expanduser, abspath, isdir, isfile, dirname

from fstree.backends.base import Backend
from fstree.models import NodeInfo, AccessPolicy


# TODO: https://docs.python.org/2/library/pwd.html

__all__ = [
    'join',
    'exists',
    'expanduser',
    'abspath',
    'isdir',
    'isfile',
    'dirname',
    'Posix',
    'expand_path',
    'get_temp',
    'delete',
    'exists_and_is_file',
    'exists_and_is_folder',
]


def mode_to_bits(mode):
    bits = map(bool, map(int, bin(mode)[2:]))
    return bits


def rwx_bits_to_dict(bits):
    read, write, execute = bits[:3]
    return {
        'read': read,
        'write': write,
        'execute': execute,
    }


class PosixAccessPolicy(AccessPolicy):

    @classmethod
    def from_mode(cls, mode):
        bits = mode_to_bits(mode)
        owner = bits[:3]
        group = bits[3:-3]
        everyone = bits[-3:]

        return {
            'owner': rwx_bits_to_dict(owner),
            'group': rwx_bits_to_dict(group),
            'everyone': rwx_bits_to_dict(everyone),
        }

    @classmethod
    def from_st_mode(cls, st_mode):
        mode = stat.S_IMODE(st_mode)
        return cls.from_mode(mode)


class Posix(Backend):

    def __init__(self, root_path='/'):
        self.__root_path = root_path

    @classmethod
    def supports_path(cls, path):
        return path.startswith(os.sep) or path.startswith('file://')

    def get_root_path(self):
        return self.__root_path

    def stat(self, path, key=None):
        st = os.stat(path)
        raw = dict([(attr, getattr(st, attr))
                    for attr in dir(st) if attr.startswith('st_')])
        data = {
            'permissions': PosixAccessPolicy.from_st_mode(st.st_mode),
            'uid': raw['st_uid'],
            'gid': raw['st_gid'],
            'size': raw['st_size'],
            'created_at': raw['st_birthtime'],
            'last_accessed': raw['st_atime'],
            'last_changed': raw['st_ctime'],
            'last_modified': raw['st_mtime'],
        }

        if key:
            return data[key]

        return data

    def get_file_size(self, path):
        return self.stat(path, 'size')

    # def get_base_path(self, path):
    #     return os.path.split(path)[0]

    def get_file_name(self, path):
        return os.path.split(path)[1]

    def remove_extension(self, path):
        return os.path.splitext(path)[0]

    def expand_path(self, *path):
        return expand_path(*path)

    def collapse_path(self, path):
        home_path = self.get_home_path()

        if not abspath(path):
            relative = path
        else:
            relative = os.path.relpath(path)

        if path.startswith(home_path):
            relative = path.replace(home_path, '~', 1)

        return relative

    def get_temp_path(self):
        """
        :returns: a string with the path to the system's temp folder (/tmp on unix)
        """
        return get_temp()

    def get_home_path(self):
        return os.getenv('HOME')

    def create_folder(self, path):
        """
        :param path: the path to be created
        :return: `True` if succeeded
        """
        os.makedirs(path)
        return True

    def get_temp_folder(self, name):
        return get_temp(name)

    def delete_file(self, path):
        """
        :param path: the path to be file to deleted
        :return: `True` if succeeded
        """
        if not self.is_file(path):
            return False

        os.unlink(path)
        return True

    def open_fd(self, path, mode='wb+', *args, **kw):
        """:returns: a `~FileDescriptor`"""
        return io.open(path, mode, *args, **kw)

    def sync_fd(self, fd):
        """flushes the file-destriptor then forces an ``os.fsync`` on its _``_fileno``_

        :param fd: a `~FileDescriptor`
        :returns: `True`
        """
        fd.flush()
        os.fsync(fd.fileno())
        return True

    def seek_fd(self, fd, position):
        """
        :param fd: a `
        :returns: an `int` with the current position (result from `~file.tell`)."""
        position = position or 0

        if not isinstance(position, int):
            raise ValueError(
                'position must be an `int` not a {0}'.format(type(position)))

        args = []
        if position < 0:
            args = [os.SEEK_END]

        fd.seek(position, *args)
        return fd.tell()

    def write_fd(self, fd, data, offset=None, sync=True):
        """writes bytes in the given file-destriptor

        :param fd: a `~FileDescriptor`
        :returns: `int` - how many bytes were written
        """
        self.seek_fd(fd, offset)

        count = fd.write(data)
        if sync:
            self.sync_fd(fd)

        return count

    def read_fd(self, fd, count=None, offset=None):
        """read bytes from the file-destriptor
        :param fd: the file-descriptor instance
        :param count: how many bytes to read (defaults to ``None``: read all bytes)
        :param offset: skip this many bytes
        :returns: ``bytes`` if mode contains **b**, ``unicode`` otherwise
        """
        self.seek_fd(fd, offset)

        return fd.read(count)

    def erase_fd(self, fd, rounds=1):
        """erases a file by performing the 2 steps below repeatedly by
        indicated number of _rounds_:

        - replace each of its bytes with random bytes
        - replace each of its bytes with

        :param fd: a `~FileDescriptor`
        :param rounds: repeat the steps mentioned above. Must be a positive `int` (default: **1**)
        :returns: `True`

        """
        rounds = rounds or 1
        for level in range(rounds):
            self.scrub_fd(fd)
            self.void_fd(fd)

        return True

    def void_fd(self, fd):
        """replace every byte of the file-destriptor with a null-byte ``\\0``

        :param fd: a `~FileDescriptor`
        :returns: `True`
        """
        size = self.get_file_size(fd.name)
        fd.seek(size)
        fd.write('\0')
        self.sync_fd(fd)

    def scrub_fd(self, fd):
        """replace every byte of the file-destriptor with a random byte from :py:func``os.urandom(1)``

        :param fd: a `~FileDescriptor`
        :returns: `True`
        """
        for position in range(self.get_file_size(fd.name)):
            fd.seek(position)
            fd.write(os.urandom(1))

        self.sync_fd(fd)

    def close_fd(self, fd):
        """closes the file-destriptor
        :param fd: a `~FileDescriptor`
        :returns: `True`
        """
        self.sync_fd(fd)
        fd.close()
        return True

    def write_to_file(self, path, data, mode='wb'):
        """writes to a file in the given path and closes it

        :param path: the path to the file
        :param data: the bytes to be written
        :param mode: defaults to ``'wb'``

        :returns: `int` - how many bytes were written
        """
        fd = self.open_fd(path, mode)
        count = self.write_fd(fd, data)
        self.close_fd(fd)
        return count

    def read_from_file(self, path, mode='rb'):
        """reads all bytes from a file

        :param path: the path to the file
        :param mode: defaults to ``'wb'``

        :returns: ``bytes`` if mode contains **b**, ``unicode`` otherwise
        """
        fd = self.open_fd(path, mode)
        result = fd.read()
        self.close_fd(fd)
        return result

    def delete_folder(self, path, recursive=True):
        """deletes a folder (recursively by default)

        :param path: the path to the folder
        :param recursive: boolean (default: `True`)
        """
        if not self.is_folder(path):
            return False

        shutil.rmtree(path)
        return True

    def delete(self, path, recursive=True):
        """deletes a file or folder.
        folder are deleted recursively by default.

        :param path: the path to the file or folder
        :param recursive: boolean (default: `True`)
        """
        if self.is_folder(path):
            return self.delete_folder(path, recursive)
        else:
            # should also work with links
            return self.delete_file(path)

    def exists(self, path):
        """if a path exists (file or folder)

        :raises IOError: if the given ``path`` is not accessible
        :returns: boolean
        """
        return exists(path)

    def is_file(self, path):
        """checks if a path exists and is a file

        :raises IOError: if the given ``path`` is not accessible
        :returns: boolean
        """
        return exists_and_is_file(path)

    def is_folder(self, path):
        """checks if a path exists and is a folder

        :raises IOError: if the given ``path`` is not accessible
        :returns: boolean
        """
        return exists_and_is_folder(path)

    def get_metadata(self, key):
        return os.getenv(key)

    def get_uid(self):
        return os.getuid()

    def get_gid(self):
        return os.getgid()

    def get_username(self):
        return os.getlogin()

    def get_current_time(self):
        return time.time()

    def get_default_access_policy(self):
        default = os.umask(0)
        os.umask(default)
        return AccessPolicy(**PosixAccessPolicy.from_mode(default ^ 0777))

    def load_info(self, path):
        return NodeInfo(
            uid=self.get_uid(),
            gid=self.get_gid(),
            size=self.get_file_size(path),
            created_at=self.get_current_time(),
            last_changed=self.get_current_time(),
            last_modified=self.get_current_time(),
            last_accessed=self.get_current_time(),
            access_policy=self.load_access_policy(path),
            path=path,
        )

    def set_default_access_policy(self, access_policy):
        """newly created files and folders will receive those access_policy"""
        # in unix this sets os.umask
        pass

    def load_access_policy(self, path):
        """read the access_policy of an exising path.

        :param path: the path to the file or folder.
        :returns: a :py:class:`~fstree.models.AccessPolicy`.
        """
        params = self.stat(path, 'permissions')
        params['path'] = path
        return AccessPolicy(**params)

    def iter_files(self, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                yield self.expand_path(root, name)


def expand_path(*path):
    """join all the given ``*args`` as elements of a path in the file-system.

    :param path: _(optional)_ will be concatenated to the system's tempdir. Otherwise returns the path to the tempdir
    :returns: an absolute path
    """
    return abspath(expanduser(join(*path)))


def get_temp(*path):
    """returns the path to a temporary folder.

    :param path: _(optional)_ will be concatenated to the system's tempdir. Otherwise returns the path to the tempdir
    :returns: `bytes` the full path to the temporary folder
    """
    return join(tempfile.gettempdir(), *path)


def delete(path):
    """
    :param path: `bytes` pointing to a physical file or folder in the local file-system
    :returns: `bool` - `True` of the path was successfully deleted
    """

    if not exists(path):
        return False

    if isdir(path):
        shutil.rmtree(path)
    else:
        os.unlink(path)

    return True


def exists_and_is_file(path):
    """
    :param path: `bytes` pointing to a physical file in the local file-system
    :returns: `bool` - `True` of the path exists and is a `~FileType`
    """

    expanded = expand_path(path)
    return exists(expanded) and isfile(expanded)


def exists_and_is_folder(path):
    """
    :param path: `bytes` pointing to a physical file in the local file-system
    :returns: `bool`
    """
    expanded = expand_path(path)
    return exists(expanded) and isdir(expanded)


def path_to_folder(path):
    """takes the path to an existing file or folder and returns the
    absolute path to the folder.

    - if the path is a file the return value will point to its parent folder
    - if the path is already a folder the return value will simply be its own absolute path

    The initial motivation to this is to help prevent code duplication
    in scripts or any situation like this:

    ::

      #!/usr/bin/env python

      import os

      local_path = os.path.join(os.path.abspath(os.path.dirname(__file__))

      with open(os.path.join(local_path, 'hello-world.txt')) as fd:
          fd.write('Hello World!\n')

    Which could be replaced by this:

    ::

      #!/usr/bin/env python

      from fstree import Folder
      from fstree.backends.local import path_to_folder

      local_path = path_to_folder(__file__)

      Folder(local_path) \
          .create_file('hello-world.txt') \
          .write_bytes('Hello World!\n')

    Or even better; this:

      #!/usr/bin/env python

      from fstree import Folder

      Folder(__file__).parent \
           .create_file('hello-world.txt') \
           .write_bytes('Hello World!\n')


    :param path: the path to a file or folder
    :returns: `bytes` - an absolute path

    """
    if exists_and_is_folder(path):
        return path

    return abspath(dirname(path))
