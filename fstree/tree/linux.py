from fstree.tree.base import ReadOnlyTree

#

FHS_2_3_NODES = (
    '/',
    (
        '/bin',
        '/boot',
        '/dev',
        '/etc',
        (
            '/etc/sgml',
            '/etc/X11',
            '/etc/xml',
        ),
        '/home',
        '/lib',
        (),
        '/media',
        '/mnt',
        '/opt',
        '/proc',
        '/root',
        '/run',
        '/sbin',
        '/srv',
        '/tmp',
        '/usr',
        (
            '/usr/bin',
            '/usr/include',
            '/usr/lib',
            (),
            '/usr/local',
            '/usr/sbin',
            '/usr/share',
            '/usr/src',
            '/usr/X11R6',
        ),

        '/var',
        (
            '/var/cache',
            '/var/lib',
            '/var/lock',
            '/var/log',
            '/var/mail',
            '/var/opt',
            '/var/run',
            '/var/spool/mail',
            '/var/tmp',
        )
    )
)


class FHSTree23(ReadOnlyTree):
    """A read-only tree that implements the `FHS v2.3
    <http://www.pathname.com/fhs/pub/fhs-2.3.html>`_
    """

    __tree_definition__ = FHS_2_3_NODES


class FHSTree(FHSTree23):
    """A read-only tree that represents the latest `FHS
    <https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard>`_.
    """
