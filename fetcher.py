from github.fetcher import Fetcher
import pprint


class Repo:
	def __init__(self, data):
		self.id = data["id"]
		self.forks_count = data["forks_count"]
		self.has_issues = data["has_issues"]
		self.stargazers_count = data["stargazers_count"]
		self.watchers_count = data["watchers_count"]
		self.full_name = data["full_name"]

gh = Fetcher()

# print(gh.get_user_repos())
pp = pprint.PrettyPrinter(indent=4, width=120)

repos = gh.get_most_popular_javascript_repos(page=1)

interesting_values = []

for r in repos:
	repo = Repo(r)
	interesting_values.append(repo)
	print(vars(repo))

print(len(interesting_values))



