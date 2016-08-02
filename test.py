from helpers.db import insert
import glob
import json

destination = '/Users/samuelsusla/Downloads/repos/**/*.json'
packages = glob.iglob(destination, recursive=True)

for filepath in packages:
    with open(filepath) as file:
        data = json.load(file)
        params = (
            data.get('stargazers_count'),
            data.get('forks_count'),
            data.get('open_issues_count'),
            data.get('size'),
            data.get('subscribers_count'),
            data.get('id'),
            data.get('name'),
            data.get('owner').get('login')
        )

        insert('''
            INSERT INTO repos (stargazers_count, forks_count,
            open_issues_count, size, subscribers_count, github_id, name, owner)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        ''', params)
