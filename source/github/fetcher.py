import http.client
import json
from urllib.parse import urlencode
import time
import sys


def parseJSON(string):
    return json.loads(string.decode('utf-8'))


class Fetcher:
    __TOKENS = ["093621273f42838ff5df605d262bb4fbf72795ee", "4a9057dd8faebd3c06c8a38c73baa042d00ab948"]
    __API_URL = "www.api.github.com"

    def __get_headers(self):
        token = self.__TOKENS[0]
        return {
            "Authorization": "token {}".format(token),
            "User-Agent": "My User Agent 1.0"
        }

    rate_limit_remaining = None
    rate_limit = None
    rate_limit_reset = None

    def __log_rate(self):
        if self.rate_limit_remaining is None or self.rate_limit_reset is None:
            return

        remaining_seconds = self.rate_limit_reset - time.time()
        print("Rate limit, remaining = {remaining}, seconds to reset = {reset}".format(
            remaining=self.rate_limit_remaining, reset=remaining_seconds))

    def wait_if_needed(self):
        if self.rate_limit_remaining is None or self.rate_limit_reset is None:
            return

        remaining_seconds = int(self.rate_limit_reset - time.time())
        if self.rate_limit_remaining == 0:
            print('Rate limit exceeded, need to wait: {} s'.format(remaining_seconds))
            time.sleep(remaining_seconds + 10)

    def get(self, url, params=None):
        self.__log_rate()
        self.wait_if_needed()

        print("Performing GET request on: {url}".format(url=url))

        con = http.client.HTTPSConnection("api.github.com")

        if params is not None:
            url = "{url}?{query}".format(url=url, query=urlencode(params))
            print("With params: ", params)

        con.request('GET', url, headers=self.__get_headers())
        res = con.getresponse()

        try:
            self.rate_limit_remaining = int(res.getheader('X-RateLimit-Remaining'))
            self.rate_limit = int(res.getheader('X-RateLimit-Limit'))
            self.rate_limit_reset = int(res.getheader('X-RateLimit-Reset'))
        except:
            print("Unexpected error:", sys.exc_info()[0])

        print("Response from GET: {url} | code: {code}".format(url=url, code=res.status))
        if res.status != 200:
            return None
        else:
            return res.read()

    def get_user_repos(self):
        """https://developer.github.com/v3/repos/#list-your-repositories"""
        return self.get('/user/repos')

    def get_releases(self, owner, repo):
        return self.get('/repos/{}/{}/releases'.format(owner, repo))

    def get_repo(self, owner, repo):
        return self.get('/repos/{}/{}'.format(owner, repo))

    def get_most_popular_javascript_repos(self, page=1):
        """https://developer.github.com/v3/search/#search-repositories"""
        return self.get('/search/repositories'.format(page), params={
            'q': 'language:javascript',
            'sort': 'stars',
            'page': page,
            'per_page': 100
        })['items']

    def get_commits(self, owner, repo):
        return self.get('/repos/{}/{}/commits'.format(owner, repo))
