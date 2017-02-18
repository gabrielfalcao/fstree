.. _Usage Guide:


.. highlight:: bash



Usage Guide
===========

.. note:: Consider running the commands below inside a `virtualenv
          <https://virtualenv.pypa.io/en/stable/>`_.


Instalation
-----------

.. code-block:: bash

    pip install fstree


.. _file-manifulation:

Working with files
------------------


create an empty one
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:
   :emphasize-lines: 3

   from fstree import File

   readme = File("~/README.txt").create()
   assert readme.latest.size == 0


copy its contents to a new one
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:
   :emphasize-lines: 1

   backup1 = readme.copy("~/README.bkp")
   assert backup1.info != readme.info
   assert backup1.info.created_at > readme.info.created_at


or clone it entirely along with dates, permissions, etc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:
   :emphasize-lines: 1

   backup2 = readme.clone("~/README.bkp")

   assert backup2.info == readme.info
   assert backup2.info.created_at == readme.info.created_at


.. _permissions:

verify permissions
~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:
   :emphasize-lines: 1

   permissions = readme.load_access_policy()
   assert permissions.to_dict() == {
       'group': {
           'execute': True,
           u'read': True,
           u'write': False
       },
       'owner': {
           'execute': True,
           u'read': True,
           u'write': True
       },
       'everyone': {
           u'execute': True,
           u'read': True,
           u'write': False,
       }
   }



Working with folders
--------------------


.. code-block:: python
   :linenos:

   from fstree import Folder

   home = Folder("~/")


Working with trees
------------------


.. code-block:: python
   :linenos:
   :emphasize-lines: 3


   from fstree import Tree

   myproj = Tree("~/")
