from __future__ import unicode_literals

import os
import sys
import shutil

from fstree.default import set_default_backend

from fstree import Tree
from fstree.node import Folder

from fstree.backends.dummy import Dummy
from fstree.backends.posix import Posix
from fstree.backends.posix import delete
from fstree.backends.posix import path_to_folder
from fstree.backends.posix import join
from sure import scenario

here = path_to_folder(__file__)


def create_posix_sandbox(context):
    set_default_backend(Posix)
    sandbox = join(here, 'sandbox')
    delete(sandbox)
    os.makedirs(sandbox)

    context.path = sandbox
    context.sandbox = Tree(sandbox)
    context.files = []

    context.backend = Posix()
    context.sandbox.create(force=True)

    nfolder = Folder(sandbox)
    nfile = nfolder.create_file(
        'README.md',
        '\n'.join([
            '# FSTree Sandbox',
            '',
            '_used only during tests_',
            '',
            '',
            '**feel free to delete this folder and subdirectories*',
            ''
        ])
    )
    context.files.append(nfile.path)

    for index in range(3):
        index = index + 1
        sub = 'sub-' * (index + 1)
        name = ''.join([sub, 'folder-', bytes(index)])
        nfolder = nfolder.create(name)
        nfile = nfolder.create_file(
            'file{}.txt'.format(index),
            format(index, 'x') * int(os.urandom(1).encode('hex'), 16)
        )
        context.files.append(nfile.path)


def create_dummy_sandbox(context):
    set_default_backend(Dummy)
    context.backend = Dummy()
    context.sandbox = Tree('/sandbox', backend=context.backend)


def delete_sandbox(context):
    context.sandbox.destroy()
    try:
        shutil.rmtree(context.path)
    except:
        pass

posix = scenario(create_posix_sandbox, delete_sandbox)
dummy = scenario(create_dummy_sandbox, delete_sandbox)


def SubScenario(message, indent=2):
    sys.stderr.write('\033[0;36m{dent}- {msg}\033[0m\n'.format(dent=' ' * indent, msg=message))
