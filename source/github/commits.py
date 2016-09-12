from fetcher import Fetcher, parseJSON
import pprint


gh = Fetcher()
result = gh.get_commits('expressjs', 'express')
result = parseJSON(result)
print(len(result))
pprint.pprint(result, width=400)
