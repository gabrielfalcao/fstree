# -*- coding: utf-8 -*-

"\033[0;33m@posix\n======\n\n\033[0;32mfstree.File\033[0m"
import os
from fstree import File
from fstree.meta import FileDescriptor
from fstree.default import backend
from fstree.exceptions import FileAlreadyOpen
from fstree.exceptions import InvalidFileDescriptor

from tests.functional.scenarios import posix, SubScenario


@posix
def test_open(context):
    ("can handle file-descriptors")

    path = backend.expand_path(context.path, 'empty.txt')
    empty = File(path, parent=context.sandbox).create()

    SubScenario('open')

    fd = empty.open(mode='wb', force=True, reuse_if_open=False)
    SubScenario('raising FileAlreadyOpen')

    empty.open.when.called_with(mode='wb', force=False, reuse_if_open=False).should.have.raised(FileAlreadyOpen, 'already has an open file-descriptor')
    empty.fd.should.equal(fd)

    empty.fileno.should.equal(fd.fileno())
    fd.should.be.a(FileDescriptor)
    fd.closed.should.be.false

    SubScenario('close invalid fd')
    otherfd = open(context.files[0])
    empty.close.when.called_with(otherfd).should.have.raised(InvalidFileDescriptor, 'but you tried to close the fileno')

    SubScenario('close')
    empty.close(fd)
    empty.fd.should.be.none
    fd.closed.should.be.true

    SubScenario('close ``None`` fd returns the ``File`` instance itself')
    empty.close(None).should.be.a(File)

    SubScenario('close non-fd obj')
    empty.close.when.called_with('foo').should.have.raised(TypeError, 'fd must be a FileDescriptor, not a: __builtin__.str')


@posix
def test_create_empty(context):
    ("can create files")
    SubScenario('empty')
    path = backend.expand_path(context.path, 'empty.txt')
    empty = File(path, parent=context.sandbox).create()
    empty.size.should.equal(0)

    SubScenario('with binary bytes')
    path = backend.expand_path(context.path, 'binary.txt')
    binary = File(path, parent=context.sandbox).create(os.urandom(32))
    binary.size.should.equal(32)

    SubScenario('with unicode text')
    path = backend.expand_path(context.path, 'binary.txt')
    binary = File(path, parent=context.sandbox).create(u'Brazão')
    binary.size.should.equal(7)

    SubScenario('with a specific encoding in binary mode')
    path = backend.expand_path(context.path, 'unicode.txt')
    empty = File(path, parent=context.sandbox).create(data=u'Brazão', encoding='utf-8', mode='wb')
    empty.size.should.equal(7)

    SubScenario('with a specific encoding in text mode')
    path = backend.expand_path(context.path, 'unicode.txt')
    empty = File(path, parent=context.sandbox).create(data=u'Brazão', encoding='utf-8', mode='w')
    empty.size.should.equal(7)

    SubScenario('auto-closing')
    path = backend.expand_path(context.path, 'unicode.txt')
    empty = File(path, parent=context.sandbox).create(data=u'Brazão', encoding='utf-8', autoclose=True)
    empty.size.should.equal(7)


@posix
def test_read_bytes(context):
    ("can read bytes")

    binfile = File('foo.bar', parent=context.sandbox).create('foobarbob')

    SubScenario('entirely')
    whole = binfile.read_bytes()
    whole.should.equal('foobarbob')

    SubScenario('without closing the file')
    foo = binfile.read_bytes(3, autoclose=False)
    foo.should.equal('foo')

    SubScenario('with a positive offset: skip from the beginning')
    bar = binfile.read_bytes(3, offset=3)
    bar.should.equal('bar')

    SubScenario('with a negative offset: skip from the end')
    bob = binfile.read_bytes(3, offset=-3, autoclose=True)
    bob.should.equal('bob')


@posix
def test_manipulate_bytes(context):
    ("can manipulate its byte content")

    SubScenario('write bytes autoclose by default')
    bin1 = File('1.bin', parent=context.sandbox).create()
    bin1 = bin1.write_bytes('foobar')
    bin1.fd.should.be.none

    SubScenario('write bytes leaving open')
    bin2 = File('2.bin', parent=context.sandbox).create()
    bin2 = bin2.write_bytes('foobar', autoclose=False)
    bin2.fileno.should.be.an(int)

    SubScenario("append bytes autoclose by default")
    bin3 = File('foo.bar', parent=context.sandbox).create('foo')
    bin3 = bin3.append_bytes('bar')
    bin3.fd.should.be.none
    bin3.read_bytes().should.equal('foobar')

    SubScenario("append bytes autoclose by default")
    bin4 = File('foo.bar', parent=context.sandbox).create('foo')
    bin4 = bin4.append_bytes('bar', autoclose=False)
    bin4.fileno.should.be.an(int)
    bin4.read_bytes().should.equal('foobar')


@posix
def test_supports_path(context):
    ('File.supports_path()')
    File.supports_path(context.files[0])


@posix
def test_metadata(context):
    ("can manipulate its metadata")
    fnode = File('1.bin', parent=context.sandbox).create('chucknorris')

    SubScenario('__str__ returns path')
    bytes(fnode).should.equal(fnode.path)

    SubScenario('retrieve NodeInfo')
    info1 = fnode.info
    info1.should.be.a('fstree.models.NodeInfo')
    info2 = fnode.load_info()
    info2.should.be.a('fstree.models.NodeInfo')

    SubScenario('retrieve AccessPolicy')
    ap1 = fnode.access_policy
    ap1.should.be.a('fstree.models.AccessPolicy')
    ap2 = fnode.load_access_policy()
    ap2.should.be.a('fstree.models.AccessPolicy')

    SubScenario('retrieve size')
    fnode.size.should.equal(11)


@posix
def test_destroy(context):
    ("can destroy")

    SubScenario('successfully')
    path = backend.expand_path(context.path, 'empty.txt')
    empty = File(path, parent=context.sandbox).create()
    empty.destroy().should.be.true
    empty.destroy().should.be.true
