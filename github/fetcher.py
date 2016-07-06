import http.client
import json
from urllib.parse import urlencode
import time

def parseJSON(string):
	return json.loads(string.decode('utf-8'))


class Fetcher:
	__TOKEN = "093621273f42838ff5df605d262bb4fbf72795ee"
	__API_URL = "www.api.github.com"
	__AUTH_HEADERS = {
		"Authorization": "token 093621273f42838ff5df605d262bb4fbf72795ee",
		"User-Agent": "My User Agent 1.0"
	}

	rate_limit_remaining = None
	rate_limit = None
	rate_limit_reset = None


	def __log_rate(self):
		if self.rate_limit_remaining is None or rate_limit_reset is None:
			return

		remaining_seconds = self.rate_limit_reset - time.time()
		print("Rate limit, remaining = {remaining}, seconds to reset = {reset}"
			.format(remaining=self.rate_limit_remaining,
					reset=remaining_seconds))


	def get(self, url, params=None):
		self.__log_rate()

		print("Performing GET request on: {url}".format(url = url))

		con = http.client.HTTPSConnection("api.github.com")

		if params is not None:
			url = "{url}?{query}".format(url=url, query=urlencode(params))
			print("With params: ", params)

		con.request('GET', url, headers=self.__AUTH_HEADERS)
		res = con.getresponse()

		self.rate_limit_remaining = res.getheader('X-RateLimit-Remaining')
		self.rate_limit = res.getheader('X-RateLimit-Limit')
		self.rate_limit_reset = res.getheader('X-RateLimit-Limit')

		print("Response from GET: {url} | code: {code}".format(url = url, code = res.status))
		return parseJSON(res.read())


	def get_user_repos(self):
		"""https://developer.github.com/v3/repos/#list-your-repositories"""
		return self.get('/user/repos')


	def get_most_popular_javascript_repos(self, page=1):
		"""https://developer.github.com/v3/search/#search-repositories"""
		return self.get('/search/repositories'.format(page), params={
			'q': 'language:javascript',
			'sort': 'stars',
			'page': page,
			'per_page': 100
			})['items']

