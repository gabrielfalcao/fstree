.. _Guide:


.. highlight:: bash



Usage Guide
===========


Instalation
-----------

.. code-block:: bash

    pip install fstree


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



Working with trees
------------------









.. code-block:: python
   :linenos:
   :emphasize-lines: 3


   from fstree import

   myproj = Folder("~/")
