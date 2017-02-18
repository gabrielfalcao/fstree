"\033[0;33mBackends\n========\n\n\033[0;32mfstree.backends.Posix\033[0m"

import os
import tempfile

from fstree.default import backend

from tests.functional.scenarios import posix


@posix
def test_defaults(context):
    ("can retrieve system defaults")

    backend.get_root_path().should.equal('/')

    backend.get_uid().should.equal(os.getuid())
    backend.get_gid().should.equal(os.getgid())
    ap = backend.get_default_access_policy()
    ap.to_dict().should.equal({
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
        },
        'path': None
    })

    backend.get_temp_path().should.equal(tempfile.gettempdir())


@posix
def test_stat(context):
    ("can retrieve the expected file stats")

    # Given a file with 32 random bytes
    target = '{0}/foo.bin'.format(context.path)
    open(target, 'wb').write(os.urandom(32))

    # When I get stats about the file
    data = backend.stat(target)

    # Then it should have returned a dict with the expected keys
    data.should.be.a(dict)

    nstat = os.stat(target)
    data.should.have.key('permissions').being.equal({
        'group': {
            'execute': False,
            'read': True,
            'write': False
        },
        'owner': {
            'execute': False,
            'read': True,
            'write': True
        },
        'everyone': {
            'execute': False,
            'read': True,
            'write': False
        }
    })
    data.should.have.key('uid').being.equal(os.getuid())
    data.should.have.key('gid').being.equal(os.getgid())
    data.should.have.key('size').being.equal(32)
    data.should.have.key('created_at').being.equal(nstat.st_birthtime)
    data.should.have.key('last_accessed').being.equal(nstat.st_atime)
    data.should.have.key('last_changed').being.equal(nstat.st_ctime)
    data.should.have.key('last_modified').being.equal(nstat.st_mtime)

    # And .get_file_size() is a shortcut to the size
    size = backend.get_file_size(target)
    size.should.equal(32)

    # And actually any stat can be retrieved individually
    created_at = backend.stat(target, 'created_at')
    created_at.should.equal(nstat.st_birthtime)


@posix
def test_exists_and_is_file(context):
    ("can verify if a path exists and is file")

    # Given a path to an unexisting file
    target = '/'.join([context.path, 'foo.bin'])
    os.path.exists(target).should.be.false
    backend.exists(target).should.be.false

    # When I create a file in it
    backend.write_to_file(target, '\0' * 16)

    # Then it should exist
    os.path.exists(target).should.be.true
    backend.exists(target).should.be.true

    # And it should be a file
    os.path.isfile(target).should.be.true
    backend.is_file(target).should.be.true

    # And can be deleted
    backend.delete_file(target).should.be.true
    backend.is_file(target).should.be.false
    backend.delete_file(target).should.be.false


@posix
def test_exists_and_is_folder(context):
    ("can verify if a path exists and is folder")

    # Given a path to an unexisting folder
    target = '{0}/sub/folder'.format(context.path)
    os.path.exists(target).should.be.false
    backend.exists(target).should.be.false

    # When I create a folder in it
    os.makedirs(target)

    # Then it should exist
    os.path.exists(target).should.be.true
    backend.exists(target).should.be.true

    # And it should be a folder
    os.path.isdir(target).should.be.true
    backend.is_folder(target).should.be.true

    # And can be deleted
    backend.delete_folder(target).should.be.true
    backend.is_folder(target).should.be.false
    backend.delete_folder(target).should.be.false


@posix
def test_get_metadata(context):
    ("can retrieve environment variables")

    backend.get_metadata('PWD').should.equal(os.getenv('PWD'))
    backend.get_metadata('USER').should.equal(os.getenv('USER'))


@posix
def test_get_username(context):
    ("can retrieve the user name")

    backend.get_username().should.equal(os.getlogin())


@posix
def test_collapse_path(context):
    ("can collapse a path")

    # Given a file
    target = os.path.abspath('{0}/foo.bin'.format(context.path))
    open(target, 'wb').write('foobar')

    backend.collapse_path(target).should.match(r'^~')
