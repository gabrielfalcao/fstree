TODO
====

translate docs to portuguese
----------------------------

http://www.sphinx-doc.org/en/1.4.8/intl.html

backends
--------

- Shall implementn file-like objects that can be operated by ``backend.sync_fd()``
- Must implement file-like objects that are returned by ``backend.open_fd()``


extension Support
-----------------

- Plugins must have unique names
- Plugins must have unique namespaces
- Plugins can specify what backends they support
- Plugins can specify what types of ``Node`` they support:
  - ``fstree.node.Node``
  - ``fstree.node.File``
  - ``fstree.node.Folder``
  - ``fstree.tree.Tree``
  - ``fstree.tree.TempTree``
- Plugins can be loaded in the following ways:
  - Auto-load when initializing new ``Node`` instances
    - Globally
    - In any ``Backend`` instance (all nodes attached to it are affected: existing and new ones)
    - In any ``Node`` instance (only that instance will be affected)
- All plugin methods are available in the supported *nodes* through its namespace


Examples
========


Loading extensions
------------------

   .. code:: python

      import os
      import fstree.plugins

      from fstree_checksum import SHA1Checksum
      from fstree_diff import Diff

      # include plugins from other places
      fstree.plugins.register_python('~/fstree_plugins/blowfish.py')

      # include plugins from installed modules
      fstree.plugins.register_module('fstree_sed')
      # or
      fstree.plugins.register_module('fstree_checksum')

      # enable one-by-one
      fstree.plugins.load("md5")                 # by namespace
      fstree.plugins.load("fstree_sed.Sed")      # by full module path
      fstree.plugins.load("myfile.py:Plugin1")   # by python file
      fstree.plugins.load(Diff)            # by passing the plugin itself

      # customize the namespace
      fstree.plugins.enable("fstree_grep.grep", namespace='grep')
      fstree.plugins.enable("ext/dummy.py:Dummy", namespace='dummy')
      fstree.plugins.enable(SHA1Checksum, namespace='sha1')

      # or multiple plugins in one call
      fstree.plugins.load([
          "fstree_sed.Sed",
          Diff,
      ])

      # or multiple with custom namespaces
      fstree.plugins.load({
          SHA1Checksum: "sha1",
          "fstree_crypto.AES": "aes",
          "myfile.py:Plugin1": "plugin1",
      })


licensing
---------

1. start with a GNU license
2. consider downgrading to a more permissive license, such as apache
