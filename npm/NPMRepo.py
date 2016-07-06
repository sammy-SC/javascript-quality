import scrapy

class NPMRepo(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    github = scrapy.Field()
    month_downloads = scrapy.Field()
