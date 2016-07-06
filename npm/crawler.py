import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.settings import Settings
import NPMRepo
import pprint


class NPMSpider(scrapy.Spider):
    name = 'NPM'
    start_urls = ['https://www.npmjs.com/browse/star']
    __pp = pprint.PrettyPrinter(indent=4, width=120)


    custom_settings = {
        'ITEM_PIPELINES' : {
            'JsonWritePipeline.JsonWritePipeline': 1,
        },
        'DOWNLOAD_DELAY': 0.5,
    }


    def parse(self, response):
        for href in response.css('.package-details h3 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            print('Downloading: ', full_url)
            yield scrapy.Request(full_url, callback=self.parse_npm_repo_page)

        next_buttons = response.css('.pagination > a.next::attr(href)')
        if len(next_buttons) == 1:
            print('Page is done, moving to: ', full_url)
            full_url = response.urljoin(next_buttons[0].extract())
            yield scrapy.Request(full_url, callback=self.parse)
        elif len(next_buttons) > 1:
            raise Exception('there are more than one next button on the website')
        else:
            print('Done, no more pages')


    def parse_npm_repo_page(self, response):
        item = NPMRepo()
        item['title'] = response.css('.package-name a::text').extract_first()
        item['link'] = response.url
        item['github'] = response.selector.xpath("""//div[contains(@class, 'sidebar')]
                                                    /ul[contains(@class, 'box')]
                                                    //a[contains(@href, 'https://github.com/')]
                                                    /@href""").extract_first()
        item['month_downloads'] = response.css('strong.monthly-downloads::text').extract_first()

        print('Item: ')
        self.__pp.pprint(item)
        print('--------------------')

        return item



if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_ENABLED': False
    })
    process.crawl(NPMSpider)
    process.start()
