FSTree - file-system manipulation for python
============================================

.. image:: https://readthedocs.org/projects/fstree/badge/?version=latest
   :target: http://fstree.readthedocs.io/en/latest/?badge=latest

.. image:: https://travis-ci.org/gabrielfalcao/fstree.svg?branch=master
   :target: https://travis-ci.org/gabrielfalcao/fstree

.. image:: https://codecov.io/gh/gabrielfalcao/fstree/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/gabrielfalcao/fstree


Features
--------

- automatic error handling:
  - mapped exceptions for every posix errno: http://www.ioplex.com/~miallen/errcmp.html
  - operate with objects in 2 different modes:
    - raise exceptions with useful debug messages
    - suppress exceptions and forward full tracebacks to ``logging``

- pluggable backends:
  - Local (Posix and Windows)
  - FTP
  - WebDav
  - SFTP
  - Amazon S3
  - Amazon ElasticFileSystem
  - DreamObjects

- file manipulation:
  - auto-load size, permissions
  - create plaintext
  - create binary
  - change access policy
  - write/read
  - auto-erase: multiple rounds of byte-scrubbing on an existing file.
  - delete with optional auto-erase.

- folders:
  - create
  - recursive deletion contents with optional auto-erase
  - child traversing

- trees (folders with super-powers):
  - traverse files:
    - filter by:
      - fnmatch/glob
      - regex of filename
      - extension
      - mime-type
      - size
      - timestamps (created, last access, last changed, last modified)
      - access policy

    - ordering by metadata:
      - owner
      - group
      - size
      - timestamps (created, last access, last changed, last modified)

  - search files by fnmatch/glob


Installing
----------


.. code:: shell

   pip install fstree


Usage
------

.. code:: python


   import fstree.plugins
   from fstree import File

   fstree.plugins.load([
     "crypto",
     "checksum",
   ])

   # load a plain-text file
   note1 = File("~/diary/how-was-my-first-kiss.txt")

   # encrypt its contents with AES-128-CBC
   ciphertext = note1.crypto.aes.cbc_encrypt("the passphrase", blocksize=128)

   # scrub the bytes of the original file and replace its contents
   with the ciphertext
   note1.erase().write_bytes(ciphertext)



Related Links
-------------

- https://pypi.python.org/pypi/pathlib
- https://pypi.python.org/pypi/node
