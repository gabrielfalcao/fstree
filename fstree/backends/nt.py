from fstree.backends.posix import Posix


class Windows(Posix):
    """Windows backend.

    It's fully based on the `~fstree.backends.Posix` backend but
    overwrites the necessary methods for full compatibility.

    .. seealse:: Please read the `contribution guide <:ref:contribution guide>`_  to FSTree to make this work well on MS-Windows
    """
