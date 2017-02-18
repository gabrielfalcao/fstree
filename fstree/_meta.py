import copy
# from collections import OrderedDict
from fstree.utils import objectid
from fstree.utils import unique
from fstree.utils import iter_lifo
from fstree.utils import Sorter
from fstree.utils import import_from_objectid

_NODE_SET = set()
_FILE_TYPE_SET = set()
_BACKEND_SET = set()

_NODE_REGISTRY = []
_FILE_TYPE_REGISTRY = []
_BACKEND_REGISTRY = []
_MODEL_REGISTRY = []
_NODE_ERROR_REGISTRY = []


def get_member(members, cls, key):
    return copy.deepcopy(members.get(key) or getattr(cls, key, None))


def set_member(members, cls, key, value):
    members[key] = value
    setattr(cls, key, value)


def validates_module(name, *forbidden_modules):
    forbidden_modules = (__name__, ) + forbidden_modules
    checks = []
    for forbidden in forbidden_modules:
        checks.append(not forbidden.startswith(name))
        checks.append(not name.startswith(forbidden))

    return all(checks)


def validates_subclass(module, name, *forbidden_names):
    checks = [validates_module(module)]
    name = name.strip()
    for forbidden in forbidden_names:
        checks.append(name != forbidden.strip())

    return all(checks)


# class MetaMeta(type):
#     def __init__(cls, name, bases, members):
#         full_members = OrderedDict()
#         for member_name in cls.declare_members():
#             full_members[member_name] = get_member(members, cls, member_name)

#         if cls.matches_condition(name, full_members):
#             item = cls.registry_envelope(name, full_members)
#             cls._REGISTRY.append(item)

#         super(MetaMeta, cls).__init__(name, bases, members)

#     @classmethod
#     def matches_condition(cls, name, full_members):
#         return not name.endswith('Meta') and cls.registry_filter(name, full_members)

#     @classmethod
#     def registry_envelope(cls, name, full_members):
#         label = name.lower()
#         errno = full_members.get('__errno__')
#         nodepath = full_members.get('__nodepath__')
#         template = full_members.get('__template__')
#         return (nodepath, errno, cls, label, template)

#     @classmethod
#     def registry_filter(cls, name, full_members):
#         return True

#     @classmethod
#     def declare_members(cls):
#         return (
#             '__errno__',
#             '__nodepath__',
#             '__template__',
#         )


class ModelMeta(type):
    def __init__(cls, name, bases, members):
        label = name.lower()
        fields = get_member(members, cls, '__fields__') or []

        if name not in ('ModelMeta', ):
            item = (cls, label, fields)
            set_member(members, cls, 'fields', Sorter(fields))
            set_member(members, cls, '__fields__', fields)
            _MODEL_REGISTRY.append(item)

        super(ModelMeta, cls).__init__(name, bases, members)


class ErrorMeta(type):
    def __init__(cls, name, bases, members):
        label = name.lower()
        errno = get_member(members, cls, '__errno__')
        nodepath = get_member(members, cls, '__nodepath__')
        template = get_member(members, cls, '__template__')

        if name not in ('ErrorMeta', ) and cls not in _NODE_SET:
            item = (nodepath, errno, cls, label, template)
            _NODE_ERROR_REGISTRY.append(item)

        super(ErrorMeta, cls).__init__(name, bases, members)


class NodeMeta(type):
    def __init__(cls, name, bases, members):
        module = get_member(members, cls, '__module__')
        filetype = get_member(members, cls, '__filetype__')

        class_id = (module, name)

        if validates_subclass(module, name, 'NodeMeta') and cls not in _NODE_SET:
            item = (cls, class_id, filetype)
            _NODE_SET.add(cls)
            _NODE_REGISTRY.append(item)
            set_member(members, cls, '__meta__', item)
            set_member(members, cls, '__label__', name.lower())

        super(NodeMeta, cls).__init__(name, bases, members)


class FileTypeMeta(type):
    def __init__(cls, name, bases, members):
        module = get_member(members, cls, '__module__')
        symbol = get_member(members, cls, '__symbol__')

        class_id = (module, name)

        if validates_subclass(module, name, 'FileTypeMeta', 'BaseFileType') and cls not in _FILE_TYPE_SET:
            item = (cls, class_id, symbol)
            _FILE_TYPE_SET.add(cls)
            _FILE_TYPE_REGISTRY.append(item)
            set_member(members, cls, '__meta__', item)

        super(FileTypeMeta, cls).__init__(name, bases, members)


class BackendMeta(type):
    def __init__(cls, name, bases, members):
        module = get_member(members, cls, '__module__')
        schema = get_member(members, cls, 'schema')
        class_id = (module, name)

        if validates_subclass(module, name, 'BackendMeta') and cls not in _BACKEND_SET:
            item = (cls, class_id, schema)
            _BACKEND_REGISTRY.append(item)
            _BACKEND_SET.add(cls)
            set_member(members, cls, '__meta__', item)

        super(BackendMeta, cls).__init__(name, bases, members)


def list_nodes():
    """returns all registered nodes ordered by newest first (LIFO)"""
    return unique(iter_lifo(_NODE_REGISTRY))


def list_backends():
    """returns all registered backends ordered by newest first (LIFO)"""
    return unique(iter_lifo(_BACKEND_REGISTRY))


def list_file_types():
    """returns all registered node types ordered by newest first (LIFO)"""
    return unique(iter_lifo(_FILE_TYPE_REGISTRY))


def get_node_error(node, errno):
    if errno is not None:
        errno = int(errno)

    for nodepath, errno, Exc, label, template in unique(iter_lifo(_NODE_ERROR_REGISTRY)):
        NodeClass = import_from_objectid(nodepath)

        if not isinstance(node, NodeClass):
            continue

        if errno == errno:
            break

        if objectid(node) == nodepath:
            break

    return Exc
