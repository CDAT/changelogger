import argparse

parser = argparse.ArgumentParser(description="Builds a changelog from GitHub activity",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-m","--milestone", metavar="M", type=str, nargs=1, help="The milestone to generate a changelog for")
parser.add_argument("-s","--since", action="store", dest="since", help="Date to filter by (mm/dd/yyyy)", default=None)
parser.add_argument("-u","--unlabeled", action="store_true", dest="unlabeled", help="Whether to allow issues without a milestone", default=False)
parser.add_argument("-r","--repo",help="repo to generate log for",default="uvcdat")

args = parser.parse_args()

milestone = args.milestone[0]

from datetime import date
if args.since is not None:
	__parts__ = [int(a) for a in args.since.split("/")]
	since = date(__parts__[2], __parts__[0], __parts__[1])
else:
	since = None

unlabeled = args.unlabeled
