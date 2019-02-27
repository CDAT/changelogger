from distutils.core import setup
import os
import sys

Version = "0.1"
packages = {'changelogger': 'lib',
            'changelogger.gh':'lib/gh',
            }
scripts = ['scripts/changelog',
           ]

setup(name='changelogger',
      version=Version,
      url='http://github.com/cdat/changelogger',
      packages=packages.keys(),
      package_dir=packages,
      scripts=scripts,
      )
