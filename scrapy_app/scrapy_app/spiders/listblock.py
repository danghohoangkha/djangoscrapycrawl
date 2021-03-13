import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class IcrawlerSpider(CrawlSpider):
    name = 'listBlock'

    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]


    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response):
        list_block = response.css('#post-2477 > div.content-wrap > div > div > table > tbody > tr').extract()
        arrObj = {}
        for item in range(2, len(list_block)):
            css1 = f'#post-2477 > div.content-wrap > div > div > table > tbody > tr:nth-child({item}) > td:nth-child(2)::text'
            css2 = f'#post-2477 > div.content-wrap > div > div > table > tbody > tr:nth-child({item}) > td:nth-child(3)::text'
            itemObj = {}
            print("Vao day")
            name = response.css(css1).get()
            subjects = response.css(css2).get()
            itemObj['name'] = name
            itemObj['subjects'] = subjects
            arrObj['url'] = itemObj
            yield arrObj

