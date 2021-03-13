import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
class detailCrawl(CrawlSpider):
    name = "detailuniCrawler"

    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    # async def parse(self, response):
    #     array_table = [11, 13, 15, 17]
    #     for count in array_table:
    #         css = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr"
    #         detail_table = response.css(css)
    #         count2 = 0
    #         for temp in range(2, len(detail_table)):
    #             css1 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(2) > a::attr(href)"
    #             css2 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(4)::text"
    #             css3 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(6) > a::text"
    #             css4 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(6)::text"
    #             reslink = response.css(css1).get()
    #             code = response.css(css2).get()
    #             year = response.css(css3).get()
    #             if year == None :
    #                 year = response.css(css4).get()
    #             link = response.urljoin(reslink)
    #             request = scrapy.Request(link, callback=self.parse_2, cb_kwargs=dict(code=code))
    #             request.cb_kwargs['year'] = year
    #             yield request
    #
    # def parse_2(self, response, code, year):
    #     i = {}
    #     arr_object = {}
    #     arr_object['code'] = code
    #     arr_object['year'] = year
    #     arr_object['wallImage'] = "https:"+response.css('#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr:nth-child(2) > td > a > img::attr(src)').get()
    #     i['url'] = arr_object
    #     return i
    async def parse(self, response):
        array_table = []
        css2 = f"#mw-content-text > div.mw-parser-output > table"
        count_table = len(response.css(css2))
        print("lentable")
        print(count_table)
        if count_table > 1:
            array_table = [10, 12, 14, 16]
        else:
            array_table = [1]
        for count in array_table:
            if count_table > 1:
                css0 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr"
            else:
                css0 = "#mw-content-text > div.mw-parser-output > table > tbody > tr"
            detail_table = response.css(css0)
            for temp in range(2, len(detail_table)):
                # css1 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(2) > a::attr(href)"
                # css2 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(4)::text"
                # css3 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(6) > a::text"
                # css4 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(6)::text"
                # css5 = f"#mw-content-text > div.mw-parser-output > table:nth-child({count}) > tbody > tr:nth-child({temp}) > td:nth-child(2) > a::text"
                css1 = css0 + f":nth-child({temp}) > td:nth-child(2) > a::attr(href)"
                css2 = css0 + f":nth-child({temp}) > td:nth-child(4)::text"
                css3 = css0 + f":nth-child({temp}) > td:nth-child(6) > a::text"
                css4 = css0 + f":nth-child({temp}) > td:nth-child(6)::text"
                css5 = css0 + f":nth-child({temp}) > td:nth-child(2) > a::text"
                css6 = css0 + f":nth-child({temp}) > td:nth-child(5) > a::text"
                reslink = response.css(css1).get()
                code = response.css(css2).get()
                name = response.css(css5).get()
                if count_table > 1:
                    year = response.css(css3).get()
                    if year == None:
                        year = response.css(css4).get()
                else:
                    year = response.css(css6).get()
                link = response.urljoin(reslink)
                request = scrapy.Request(link, callback=self.parse_2, cb_kwargs=dict(code=code))
                request.cb_kwargs['year'] = year
                request.cb_kwargs['name'] = name
                yield request

    def parse_2(self, response, code, year, name):
        i = {}
        # print(code)
        arr_object = {}
        arr_object['name'] = name
        arr_object['code'] = code
        arr_object['year'] = year
        print(year)
        arr_object['wallImage'] = "https:"+response.css(
            '#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr:nth-child(2) > td > a > img::attr(src)').get()
        # arr_object['wallImage'] = "https:" + response.css(
        #     '#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr:nth-child(2) > td > a > img::attr(src)').get()
        i['url'] = arr_object
        return i