#!/usr/bin/env python

from __future__ import unicode_literals


from fstree import TempTree


def main():
    sandbox = TempTree('sandbox').create()

    readme = sandbox.create_file(
        'README',
        contents="\n".join([
            'The contents of this folder will disappear'
            'by the end of this routine'
        ])
    )

    assert readme.loaded.size == 68


if __name__ == '__main__':
    main()
