from distutils.core import setup
import os
import sys

Version = "0.1"
packages = {'changelogger': 'lib',
            }
scripts = ['scripts/changelog',
           ]

setup(name='changelogger',
      version=Version,
      url='http://github.com/uv-cdat/changelogger',
      packages=packages.keys(),
      package_dir=packages,
      scripts=scripts,
      )
