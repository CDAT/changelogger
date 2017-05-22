from . import gh
import os
import sys

if sys.version_info < (2,7,9):
	import urllib3.contrib.pyopenssl
	urllib3.contrib.pyopenssl.inject_into_urllib3()

