.. _API:

API Reference
=============

.. _backends:

backends
--------

.. autoclass:: fstree.backends.Local
.. autoclass:: fstree.backends.Posix
.. autoclass:: fstree.backends.Windows
.. autoclass:: fstree.backends.Dummy


.. _nodes:

nodes
-----

.. autoclass:: fstree.node.File
.. autoclass:: fstree.node.Folder

auto-creation
~~~~~~~~~~~~~

.. autofunction:: fstree.meta.node_from_path
.. autofunction:: fstree.meta.node_by_type_name_and_path


.. _trees:

trees
-----

.. autoclass:: fstree.tree.Tree
.. autoclass:: fstree.tree.ReadOnlyTree
.. autoclass:: fstree.tree.HardCodedTree
.. autoclass:: fstree.tree.TempTree

linux-specific
~~~~~~~~~~~~~~

.. autoclass:: fstree.tree.linux.FHSTree
.. autoclass:: fstree.tree.linux.FHSTree23

.. _defaults:

defaults
--------

.. autofunction:: fstree.default.set_default_logger
.. autofunction:: fstree.default.get_default_backend
.. autofunction:: fstree.default.set_default_backend

.. _bases:

Base Classes
------------

.. autoclass:: fstree.node.Node
.. autoclass:: fstree.tree.base.BaseTree
.. autoclass:: fstree.backends.Backend
