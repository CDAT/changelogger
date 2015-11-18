import init, gh, sys
from args import milestone

repo = gh.GithubModel("/repos/UV-CDAT/uvcdat")

milestones = repo["milestones"]

for m in milestones:
    if m["title"] == str(milestone):
        break
else:
    print "Unable to find milestone %s" % milestone
    sys.exit(1)

issues = gh.GithubModel("/repos/UV-CDAT/uvcdat/issues?milestone=%d&state=closed" % m["number"])

labels = repo["labels"]

# Used to sort open issues and stick at end of log
severity = ["High Priority", "Low Priority", "Critical"]

# Used to split category closed issues 
kind = ["Enhancement", "Bug"]
# Used to categorize issues
category = []

# Ignored
irrelevant = ["wontfix", "Other", "Duplicate", "Invalid", "Question", "Gatekeeper", "unconfirmed"]
skip = ["wontfix", "Duplicate", "Invalid"]

for label in labels:
    if label["name"] in severity or label["name"] in kind or label["name"] in irrelevant:
        continue
    category.append(label["name"])

issues_sorted = {}
issues_kinds = {}
for issue in issues:
    issue_labels = issue["labels"]
    labels = [l["name"] for l in issue_labels]
    if (any(s in labels for s in skip)):
        continue
    for l in labels:
        if l in category:
            if l not in issues_sorted:
                issues_sorted[l] = []
            issues_sorted[l].append(issue)
        if l in kind:
            issues_kinds[issue["url"]] = l

print "## Closed Issues"

categories = sorted(issues_sorted.keys())
for cat in categories:
    print "### {category}".format(category=cat)
    print ""
    for issue in issues_sorted[cat]:
        values = {
            "bug_or_enh": issues_kinds[issue["url"]] if issue["url"] in issues_kinds else "",
            "title": issue["title"],
            "url": issue["html_url"]
        }
        print " * **{bug_or_enh}**: [{title}]({url})".format(**values)
    print ""


gatekeepers = gh.GithubModel("/repos/UV-CDAT/uvcdat/issues?state=open&labels=Gatekeeper")

if len(gatekeepers):
    print "## OPEN GATEKEEPERS"
    for issue in gatekeepers:
        print " * [{title}]({url})".format(title=issue["title"], url=issue["html_url"])
    print ""


print "## Known Bugs\n"

critical_issues = gh.GithubModel("/repos/UV-CDAT/uvcdat/issues?state=open&labels=critical")

if len(critical_issues) > 0:
    print "### Critical\n"
    for issue in critical_issues:
        print " * [{title}]({url})".format(title=issue["title"], url=issue["html_url"])
    print ""

high_issues = gh.GithubModel("/repos/UV-CDAT/uvcdat/issues?state=open&labels=high")
if len(high_issues) > 0:
    print "### High Priority\n"
    for issue in high_issues:
        print " * [{title}]({url})".format(title=issue["title"], url=issue["html_url"])
    print ""


if len(high_issues) == 0 and len(critical_issues) == 0:
    print "No known issues!"