from fstree.backends.dummy import Dummy
from fstree.default import set_default_backend

# from fstree.default import set_default_logger
# from tests.unit.mocks import logger

# set_default_logger(logger)

set_default_backend(Dummy)
