"\033[0;33m@posix\n======\n\n\033[0;32mfstree.Folder\033[0m"

import os
import shutil
from fstree import Folder
from fstree.exceptions import FolderAlreadyExists

from tests.functional.scenarios import posix


@posix
def test_create_self(context):
    ("can create itself")

    # Background: the sandbox folder does not exist
    path = context.path
    shutil.rmtree(path)

    sandbox = Folder(path).create()
    sandbox.path.should.equal(path)

    os.path.exists(path).should.be.true
    os.path.isdir(path).should.be.true


@posix
def test_supports_path(context):
    ('Folder.supports_path()')
    Folder.supports_path(context.files[0])


@posix
def test_create_self_existing_raises_error(context):
    ("raise exception if already exists")

    Folder(context.path).create.when.called.should.have.raised(FolderAlreadyExists)


@posix
def test_create_self_skip_existing(context):
    ("skip creation if already exists and force=False")

    path = context.path
    sandbox = Folder(path).create(force=True)
    sandbox.path.should.equal(path)

    os.path.exists(path).should.be.true
    os.path.isdir(path).should.be.true


@posix
def test_create_child(context):
    ("can create child folders recursively")

    sandbox = Folder(context.path)
    sub_path = '{}/foo/bar/bob'.format(sandbox.path)

    bob = sandbox.create(sub_path)

    os.path.isdir(sub_path)
    bob.path.should.equal(sub_path)


@posix
def test_destroy(context):
    ("can delete a tree recursively")

    sandbox = Folder(context.path).create(force=True)

    folder = sandbox.create_folder('folder1')
    child = folder.create_folder('folder2')
    file1 = child.create_file('file1.txt', 'file1')

    os.path.exists(file1.path).should.be.true
    os.path.isfile(file1.path).should.be.true

    sandbox.destroy()

    os.path.isdir(sandbox.path).should.be.false
    os.path.exists(sandbox.path).should.be.false
