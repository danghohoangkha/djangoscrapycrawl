import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class MajorCrawler(CrawlSpider):
    name = "majorCrawler"

    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)
    def parse(self, response):
        list_uni = response.css('#tabContent > div:nth-child(9) > table > tbody > tr')


        for count in range(2, len(list_uni)):
            arrObject = {}
            i = {}
            css1 = f"#tabContent > div:nth-child(9) > table > tbody > tr:nth-child({count}) > td:nth-child(1) > p > b > span::text"
            css2 = f"#tabContent > div:nth-child(9) > table > tbody > tr:nth-child({count}) > td:nth-child(2) > p > b > span::text"
            css11 = f"#tabContent > div:nth-child(9) > table > tbody > tr:nth-child({count}) > td:nth-child(1) > p > span::text"
            css21 = f"#tabContent > div:nth-child(9) > table > tbody > tr:nth-child({count}) > td:nth-child(2) > p > span::text"
            code = response.css(css1).extract_first()
            name = response.css(css2).extract_first()
            if code == None:
                code = response.css(css11).extract_first()
            if name == None:
                name = response.css(css21).extract_first()
            arrObject['code'] = code
            arrObject['name'] = name
            i['url'] = arrObject
            yield i;