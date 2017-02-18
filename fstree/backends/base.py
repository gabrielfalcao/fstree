import re
from abc import abstractmethod
from abc import abstractproperty

from fstree._meta import BackendMeta
from fstree.exceptions import InvalidSchema
from fstree.exceptions import UnsupportedPath


schema_name_regex = re.compile(r'^(?P<name>\w+)[:]?[/]?[/]?')


def parse_label_from_schema(schema):
    found = schema_name_regex.search(schema.strip())
    if not found:
        raise InvalidSchema(schema)

    return found.group('name')


def compile_regex_for_schema(label):
    pattern = r'^(?P<schema>{0}[:][/][/])?[/]*(?P<path>\w+.*)'.format(label.strip())
    return re.compile(pattern, re.IGNORECASE | re.UNICODE | re.DOTALL)


def parse_path_of_schema(path, schema):
    regex = compile_regex_for_schema(schema)
    found = regex.search(path)
    if not found:
        return None

    return found.groupdict()


def normalize_path_for_schema(path, schema, exception_class=UnsupportedPath):
    found = parse_path_of_schema(path, schema)
    if not found:
        raise exception_class(path)

    context = found.groupdict()
    return '{schema}://{path}'.format(**context)


class Backend(object):
    __metaclass__ = BackendMeta

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def get_default_encoding(self):
        return b'utf-8'

    @abstractproperty
    def path_separator(self):
        """:returns: `bytes`"""

    @abstractmethod
    def get_temp_folder(self, name):
        """
        :param name:
        :returns: `bytes`
        """

    @abstractmethod
    def stat(self, path):
        """
        :param path:
        :returns: `dict`
        """

    @abstractmethod
    def expand_path(self, path):
        """
        :param path:
        :returns: `bytes`
        """

    @abstractmethod
    def get_temp_path(self):
        """:returns: `bytes`"""

    @abstractmethod
    def delete_file(self, path):
        """
        :param path:
        :returns: `bytes`
        """

    @abstractmethod
    def delete_folder(self, path, recursive=True):
        """
        :param path:
        :param recursive:
        :returns: `bytes`
        """

    @abstractmethod
    def exists(self, path):
        """
        :param path:
        :returns: `bool`
        """

    @abstractmethod
    def is_file(self, path):
        """
        :param path:
        :returns: `bool`
        """

    @abstractmethod
    def is_folder(self, path):
        """
        :param path:
        :returns: `bool`
        """

    @abstractmethod
    def set_default_access_policy(self, access_policy):
        """:returns: `bool`"""

    @abstractmethod
    def apply_access_policy(self, access_policy=None):
        """:returns: `bool`"""

    @abstractmethod
    def load_access_policy(self, path):
        """:returns: `AccessPolicy`"""

    @abstractmethod
    def load_info(self, path):
        """:returns: `NodeInfo`"""

    @abstractmethod
    def get_root_path(self):
        """:returns: `bytes`"""

    @abstractmethod
    def get_uid(self):
        """:returns: `int`"""

    @abstractmethod
    def get_gid(self):
        """:returns: `int`"""

    @abstractmethod
    def get_username(self):
        """:returns: `bytes`"""

    @abstractmethod
    def get_metadata(self, key):
        """:returns: `dict`"""

    @abstractmethod
    def supports_path(cls, path):
        """:returns: `bool`"""
