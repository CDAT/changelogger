#/usr/bin/env python
import markdown2
import sys

f = sys.argv[1]

with open(f) as infile:
	file_data = infile.readlines()
	data = "".join(file_data)
	out = markdown2.markdown(data, extras=["code-friendly"])
	print out
