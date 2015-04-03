import argparse

parser = argparse.ArgumentParser(description="Builds a changelog from GitHub activity")
parser.add_argument("milestone", metavar="M", type=float, nargs=1, help="The milestone to generate a changelog for")

args = parser.parse_args()

milestone = args.milestone[0]