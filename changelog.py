import init, gh, sys
from args import milestone

repo = gh.GithubModel("/repos/UV-CDAT/uvcdat")

milestones = repo["milestones"]

for m in milestones:
	if m["title"] == milestone:
		break
else:
	print "Unable to find milestone %s" % milestone
	sys.exit(1)

