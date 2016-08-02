"""
Repo class used to hold data about repository
"""

import scrapy


class Repo(scrapy.Item):
    title = scrapy.Field()
    github = scrapy.Field()
    monthly_downloads = scrapy.Field()
    weekly_downloads = scrapy.Field()
    daily_downloads = scrapy.Field()
