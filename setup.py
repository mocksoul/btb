#!/usr/bin/env python

from __future__ import print_function

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand


from setuptools import setup
from setuptools.command.test import test as TestCommand
from setuptools.command.sdist import sdist as SourceDistCommand


class PyTestCommand(TestCommand):
    user_options = [
        ('opts=', 'o', 'Options for pytest'),
    ]

    def initialize_options(self):
        self.opts = ''

    def finalize_options(self):
        import shlex
        self.opts_str = self.opts
        self.opts = shlex.split(self.opts)

    def run(self):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(self.distribution.install_requires)
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)

        self.with_project_on_sys_path(self.run_pytest)

    def run_pytest(self):
        import sys
        import pytest
        import os

        if os.fork():
            status = os.wait()[1]
            if os.WIFEXITED(status):
                raise SystemExit(os.WEXITSTATUS(status))
            else:
                self.announce('Killed by signal: %d' % (os.WSTOPSIG(status), ))
                raise SystemExit(1)
        else:
            sys.argv[:] = ['setup.py test'] + self.opts
            self.announce('Running pytest %s' % (self.opts_str, ))
            raise SystemExit(pytest.main())


class MySourceDistCommand(SourceDistCommand):
    def make_distribution(self):
        import os
        import textwrap

        self.filelist.extend(['tools/setup.py', 'tools/ez_setup.py'])
        self.filelist.extend(['setup.py'])
        open('setup.py', 'wb').write(textwrap.dedent('''
            import os
            import sys
            sys.path.insert(0, 'tools')
            execfile('tools/setup.py')
        ''').strip())
        #os.symlink('tools/setup.py', 'setup.py')
        try:
            return SourceDistCommand.make_distribution(self)
        finally:
            os.unlink('setup.py')


try:
    variables = {}
    execfile('src/__version__.py', variables, variables)
    VERSION = str(variables['VERSION'])
except:
    VERSION = 'unknown'


setup(
    name='btb',
    version=VERSION,
    description='Backup system using rsync and btrfs snapshots',
    long_description=open('README.rst').read(),
    url='http://bitbucket.org/mocksoul/btb',
    author='Vadim Fint',
    author_email='mocksoul@gmail.com',
    license='BSD',
    zip_safe=True,
    install_requires=[
        'distribute',
    ],
    tests_require=['pytest'],
    packages=[
        'btb',
    ],
    entry_points={
        'console_scripts': [
            'btb = btb.__main__:main',
        ]
    },
    package_dir={'btb': 'src'},
    cmdclass={
        'test': PyTestCommand,
        'sdist': MySourceDistCommand,
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Communications',
    ]
)
