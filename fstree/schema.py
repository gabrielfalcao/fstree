from fstree.schemadict import schemadict


permission_dict = schemadict({
    '__name__': 'permission_dict',
    'read': bool,
    'write': bool,
    'execute': bool,
})


mode_dict = schemadict({
    '__name__': 'stat_mode_dict',
    'owner': permission_dict,
})


stat_dict = schemadict({
    '__name__': 'stat_dict',
    'access_policy': None,
    'umask': None,
    'chmod': None,
    'gid': None,
    'uid': None,
    'size': None,
    'created_at': None,
    'last_changed': None,
    'last_modified': None,
    'last_accessed': None,
})
