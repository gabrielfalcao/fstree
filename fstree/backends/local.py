import os

if os.name == 'posix':
    from fstree.backends.posix import Posix as LocalBaseBackend
elif os.name == 'nt':
    from fstree.backends.nt import Windows as LocalBaseBackend
else:
    from fstree.backends.dummy import Dummy as LocalBaseBackend


class Local(LocalBaseBackend):
    """Local file-system backend.

    supports the following system platforms:

    - posix (Linux and BSDs) through :py:class:`fstree.backends.posix.Posix`
    - nt (Windows) through :py:class:`fstree.backends.nt.Windows`

    Using this in any other system plarform will cause it to behave as
    :py:class:`~fstree.backends.dummy.Dummy`
    """
