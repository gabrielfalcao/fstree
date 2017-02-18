from fstree.meta import FileDescriptor
from fstree.utils import objectid
from fstree.node.base import Node
from fstree.exceptions import FileAlreadyOpen
from fstree.exceptions import InvalidFileDescriptor


class File(Node):
    """Node with extra methods that can manipulate file contents

    .. glossary::

       - ***internal fd:*** a `~FileDescriptor` internally stored in a `~File` after a `~File.open` call.
    """

    def initialize(self, fd=None, fileno=None):
        self._fd = fd
        self.__fileno = fileno

    def clone_params(self):
        return {
            'fd': self._fd,
            'fileno': self.__fileno,
        }

    @property
    def fd(self):
        """
        .. note:: this property has a side-effect in the internal state of the node instance.

        :returns: a `~FileDescriptor` or `None`
        """
        if not self._fd or self._fd.closed:
            self._fd = None
            self.__fileno = None
            return None

        return self._fd

    @property
    def fileno(self):
        """
        :returns: `int` with _internal fd_ or `None`
        """

        if FileDescriptor.ack_paternity(self.fd):
            self.__fileno = self.fd.fileno()

        return self.__fileno

    def write_bytes(self, data, autoclose=None):
        """write the given bytes to the file

        :param data: the bytes
        :param autoclose: when `True` closes the file at the end
        :returns: a _reloaded_ version instance of :py:class:`~File`
        """
        if autoclose is None:
            autoclose = len(data) > 0

        if autoclose:
            mode = 'wb'
        else:
            mode = 'wb+'

        fd = self.open(mode=mode, reuse_if_open=True)

        self.backend.write_fd(fd, data)

        if autoclose:
            self.close(fd)

        return self.latest

    def append_bytes(self, data, autoclose=None):
        """append the given bytes to the file
        :param data: the bytes
        :param autoclose: when `True` closes the file at the end
        :returns: a _reloaded_ version instance of :py:class:`~File`
        """
        if autoclose is None:
            autoclose = len(data) > 0

        if autoclose:
            mode = 'ab'
        else:
            mode = 'ab+'

        fd = self.open(mode=mode, reuse_if_open=True)
        self.backend.write_fd(fd, data)

        if autoclose:
            self.close(fd)

        return self.latest

    def read_bytes(self, count=None, offset=None, mode='rb', autoclose=None, rewind=True):
        """read bytes from the file
        :param count: how many bytes to read (defaults to ``None``: read all bytes)
        :param offset: skip this many bytes
        :param mode: default **'rb'**
        :param autoclose: when `True` closes the file at the end
        :param rewind: when `True` seek to position 0 at the end (ignored when ``autoclose=True``)
        :returns: ``bytes`` if mode contains **b**, ``unicode`` otherwise
        """
        fd = self.open(mode=mode, reuse_if_open=True)
        offset = offset or 0

        if count is None and not offset and autoclose is None:
            autoclose = True

        # apply offset
        if offset != 0:
            self.backend.seek_fd(fd, offset)

        read = self.backend.read_fd(fd, count, offset)
        if autoclose:
            self.close(fd)

        elif rewind:
            self.backend.seek_fd(fd, 0)

        return read

    def erase_bytes(self, rounds=1):
        with self.open('wb', reuse_if_open=True) as fd:
            for i in range(rounds):
                self.backend.erase_fd(fd)

        return self.latest

    def open(self, mode='wb', force=False, reuse_if_open=True, *args, **kw):
        """
        :param mode: (default: `"wb"`)
        :param force: `bool` - if `True` any existing file will be destroyed before writing data
        :param reuse_if_open: `bool`  if `True` tries to reuse an open file-descriptor before opening one.
        :raises: `~NodeAlreadyOpen` if ``reuse_if_open=False``
        """
        if force:
            self.destroy()

        fd = self.fd

        if fd is not None and reuse_if_open is False:
            raise FileAlreadyOpen(self)

        elif fd is None:
            fd = self.backend.open_fd(self.path, mode, *args, **kw)

        self._fd = fd

        return fd

    def close(self, fd=None):
        """
        :param fd: a `~fstree.backends.base.FileDescriptor`
        :param force: `bool` - if `True` any existing file will be destroyed before writing data
        :param reuse_if_open: `bool`  if `True` tries to reuse an open file-descriptor before opening one.
        :raises: `~NodeAlreadyOpen` if ``reuse_if_open=False``
        :returns: a reloaded version of self
        """
        fd = fd or self._fd

        if fd is None:
            self.log.warning(
                'ignore close file-descriptor None for file %s', self.path)
            return self

        if not FileDescriptor.ack_paternity(fd):
            raise TypeError(
                'fd must be a FileDescriptor, not a: {}'.format(objectid(fd)))

        if fd.fileno() != self.fileno and self.fileno is not None:
            raise InvalidFileDescriptor(
                self, target_path=fd.name, fileno=fd.fileno(), action='close')

        if fd and not fd.closed:
            self.backend.close_fd(fd)

        self._fd = None

        return self.latest

    def create(self, data=None, encoding=None, size=0, mode='wb', force=False, autoclose=None):
        """creates a file

        :returns: a `~File` instance
        """
        fd = self.open(mode, force=force, reuse_if_open=False)

        if isinstance(data, basestring):
            if encoding is not None:
                if 'b' in mode:
                    data = data.encode(encoding)
                else:
                    data = unicode(data)

            elif isinstance(data, unicode):
                data = data.encode(self.backend.get_default_encoding())

            elif 'b' in mode:
                data = bytes(data)

            if autoclose is None:
                autoclose = len(data) > 0

        else:
            data = '\0' * size
            if autoclose is None:
                autoclose = True

        self.backend.write_fd(fd, data)

        if autoclose is True:
            self.close(fd)

        return self.latest

    def destroy(self, rounds=1):
        """erases the bytes of the file and deletes it
        :param rounds: how many times to repeat the erase process
        """
        self.erase_bytes(rounds)
        return Node.destroy(self)
