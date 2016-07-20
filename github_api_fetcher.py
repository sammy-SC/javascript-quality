import pprint
import os
import sys
from github.fetcher import Fetcher
from npm_fetch_all import load_data


class Repo:
	def __init__(self, data):
		self.id = data["id"]
		self.forks_count = data["forks_count"]
		self.open_issues_count = data["open_issues_count"]
		self.stargazers_count = data["stargazers_count"]
		self.watchers_count = data["watchers_count"]
		self.network_count = data["network_count"]
		self.full_name = data["full_name"]

gh = Fetcher()


data = load_data()

target_owner = 'git@github.com:urbaneinnovation'
target_repo_name = 'node-myo'

for i, e in enumerate(data):
    owner = e['owner']
    repo_name = e['github_repo_name']
    if owner == target_owner and repo_name == target_repo_name:
        data = data[i:]
        print("Found at: ", i)


print("Left to load: ", len(data))

for i, e in enumerate(data):
    owner = e.get('owner')
    repo_name = e.get('github_repo_name')
    if not owner or not repo_name: continue

    print("owner: {}, name: {} -- {} / {}".format(owner, repo_name, i, len(data)))

    try:
        result = gh.get_repo(owner, repo_name)
    except:
        print("Unexpected error: ", sys.exc_info()[0])
        continue

    if not result: continue

    target_directory = 'data/repos/{}'.format(owner)
    target_filepath = 'data/repos/{}/{}.json'.format(owner,repo_name)

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    with open(target_filepath, 'wb') as f:
        f.write(result)


