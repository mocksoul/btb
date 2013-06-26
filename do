#!/usr/bin/env python

import os
import sys

# Ensure this script and its deps will not force python to write bytecode files
sys.dont_write_bytecode = True

sys.path[0] = os.path.abspath('tools')

from fabricate import run, main
import os
import shutil
import subprocess as subproc


BUILDDIR = os.path.abspath('.build')


def task(func):
    func.task = True
    return func


@task
def help():
    """ Show available tasks list """

    from fabricate import _parsed_options

    if _parsed_options is not None:
        _parsed_options[0].print_help()
        print('')

    print('Available script functions:')

    tasks = []
    for name, meth in sorted(globals().iteritems()):
        if not callable(meth):
            continue
        if getattr(meth, 'task', False):
            doc = meth.__doc__
            if isinstance(doc, basestring):
                doc = doc.strip()
            else:
                doc = ''
            tasks.append((name, doc))

    maxlen = max(len(t[0]) for t in tasks)

    for name, doc in tasks:
        print(('  %%-%ds : %%s' % (maxlen, )) % (name, doc))


@task
def sdist():
    """ Make source distribution at dist/ """
    run(
        'bash', [
            '-c',
            '"%s" -B tools/setup.py sdist --formats=bztar && rm -rf btb.egg-info' % (
                sys.executable,
            )
        ]
    )


@task
def develop():
    """ Install for development """
    from distutils import sysconfig
    pylib = sysconfig.get_python_lib()

    run(
        'bash', [
            '-c', subproc.list2cmdline([
                sys.executable, '-B', 'tools/setup.py', 'egg_info', 'install_scripts', '&&',
                'rm', '-rf', os.path.join(pylib, 'btb.egg-info'), '&&',
                'cp', '-r', 'btb.egg-info', pylib, '&&',
                'rm', '-rf', 'btb.egg-info', '&&',
                'rm', '-rf', os.path.join(pylib, 'btb'), '&&',
                'ln', '-sf', os.path.abspath('src'), os.path.join(pylib, 'btb'),
            ])
        ]
    )


@task
def clean():
    """ Auto-cleanup everything """
    if '-c' not in sys.argv:
        os.system('"%s" "%s" -c clean' % (sys.executable, __file__))
    else:
        if os.path.exists(BUILDDIR):
            print('deleting ' + BUILDDIR)
            shutil.rmtree(BUILDDIR)


if __name__ == '__main__':
    if not os.path.isdir(BUILDDIR):
        os.makedirs(BUILDDIR)
    main(depsname=os.path.join(BUILDDIR, 'deps'), default='help', ignoreprefix='.none')
