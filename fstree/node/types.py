from fstree._meta import FileTypeMeta

__all__ = [
    'FileType',
    'FolderType',
    'DeviceType',
    'SymlinkType',
    'HardlinkType',
    'PipeType',
    'SocketType',
]


class BaseFileType(object):
    __metaclass__ = FileTypeMeta


class FileType(BaseFileType):
    """supported by all backends"""
    __symbol__ = 'FILE'


class FolderType(BaseFileType):
    """supported by all backends"""
    __symbol__ = 'FOLDER'


class DeviceType(BaseFileType):
    """a posix device file"""
    __symbol__ = 'DEVICE'


class SymlinkType(BaseFileType):
    """a posix symbolic link file"""
    __symbol__ = 'SYMLINK'


class HardlinkType(BaseFileType):
    """a posix hard link file"""
    __symbol__ = 'HARDLINK'


class PipeType(BaseFileType):
    """a posix pipe file"""
    __symbol__ = 'PIPE'


class SocketType(BaseFileType):
    """a posix socket file"""
    __symbol__ = 'SOCKET'
