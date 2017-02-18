import sys
import logging
from fstree.backends import Local


__all__ = [
    'get_default_backend',
    'set_default_backend',
    'set_default_logger',
    'logger',
    'backend',
    'DEFAULT_BACKEND',
    'DEFAULT_BACKEND_KW',
]

__self__ = sys.modules[__name__]
DEFAULT_LOGGER = logging.getLogger('fstree')
logger = DEFAULT_LOGGER

DEFAULT_BACKEND = Local
DEFAULT_BACKEND_KW = {}


def set_default_backend(backend=None, **kw):
    """sets the default backend with the optional _kwargs_

    :param backend: a ``type`` that is a subclass of `~fstree.backends.base.Backend`. If not given resets to the original default: `~fstree.backends.Local`
    :param kw: forwarded during the construction of a new backend instance
    """
    if not backend:
        backend = Local
        kw = {}

    setattr(__self__, 'DEFAULT_BACKEND', backend)
    setattr(__self__, 'DEFAULT_BACKEND_KW', kw)
    setattr(__self__, 'backend', get_default_backend(**kw))


def set_default_logger(new=None):
    """sets the default logger instance.

    :param new: a logger instance
    """
    if not new:
        new = DEFAULT_LOGGER

    setattr(__self__, 'logger', new)


def get_default_backend(**kw):
    """retrieves an instance of the **default** backend.

    :returns: a instance of some any subclass of `~fstree.backends.base.Backend`
    """
    return getattr(__self__, 'DEFAULT_BACKEND')(**kw)


backend = get_default_backend()
