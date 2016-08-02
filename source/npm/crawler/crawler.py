"""
Originally we were crawling https://www.npmjs.com to get package information, this package is not used anymore
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from NPMRepo import Repo
from time import gmtime, strftime


def log(message):
    time = strftime("%H:%M:%S | %m.%d", gmtime())
    print("{time}: \t {message}".format(time=time, message=message))


class NPMSpider(scrapy.Spider):
    name = 'NPM'
    # last offset 4176
    start_urls = ['https://www.npmjs.com/browse/star']

    custom_settings = {
        'ITEM_PIPELINES': {
            'JsonWritePipeline.JsonWritePipeline': 1,
        },
        'DOWNLOAD_DELAY': 0.5,
    }

    def parse(self, response):
        for href in response.css('.package-details h3 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_npm_repo_page)

        next_buttons = response.css('.pagination > a.next::attr(href)')
        if len(next_buttons) == 1:
            full_url = response.urljoin(next_buttons[0].extract())
            log('Page is done, moving to: {}'.format(full_url))
            yield scrapy.Request(full_url, callback=self.parse)
        elif len(next_buttons) > 1:
            raise Exception('there are more than one next button on the website')
        else:
            log('Done, no more pages')

    def parse_npm_repo_page(self, response):
        log('Parsing: {}'.format(response.url))
        item = Repo()
        item['title'] = response.css('.package-name a::text').extract_first()
        item['github'] = response.selector.xpath("""//div[contains(@class, 'sidebar')]
                                                    /ul[contains(@class, 'box')]
                                                    //a[contains(@href, 'https://github.com/')]
                                                    /@href""").extract_first()

        item['monthly_downloads'] = response.css('strong.monthly-downloads::text').extract_first()
        item['daily_downloads'] = response.css('strong.daily-downloads::text').extract_first()
        item['weekly_downloads'] = response.css('strong.weekly-downloads::text').extract_first()

        return item


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_ENABLED': True,
        'LOG_LEVEL': 'ERROR'
    })
    process.crawl(NPMSpider)
    process.start()
