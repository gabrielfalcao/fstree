from fstree.backends.base import Backend
from fstree.backends.base import normalize_path_for_schema

from fstree.exceptions import UnsupportedPath


class InvalidS3Path(UnsupportedPath):
    schema_prefix = 's3'


class InvalidEFSPath(UnsupportedPath):
    schema_prefix = 'efs'


class S3(Backend):
    schema = 's3://'

    def __init__(self, *args, **kw):
        raise NotImplementedError

    def expand_path(self, path):
        path = normalize_path_for_schema(path, self.schema, InvalidS3Path)
        return path


class ElasticFileSystem(Backend):
    schema = 'efs://'

    def __init__(self, *args, **kw):
        raise NotImplementedError

    def expand_path(self, path):
        path = normalize_path_for_schema(path, self.schema, InvalidEFSPath)
        return path
