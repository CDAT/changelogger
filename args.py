import argparse

parser = argparse.ArgumentParser(description="Builds a changelog from GitHub activity")
parser.add_argument("milestone", metavar="M", type=float, nargs=1, help="The milestone to generate a changelog for")
parser.add_argument("--since", action="store", dest="since", help="Date to filter by (mm/dd/yyyy)", default=None)
parser.add_argument("--unlabeled", action="store_true", dest="unlabeled", help="Whether to allow issues without a milestone", default=False)
args = parser.parse_args()

milestone = args.milestone[0]

from datetime import date
if args.since is not None:
	__parts__ = [int(a) for a in args.since.split("/")]
	since = date(__parts__[2], __parts__[0], __parts__[1])
else:
	since = None

unlabeled = args.unlabeled