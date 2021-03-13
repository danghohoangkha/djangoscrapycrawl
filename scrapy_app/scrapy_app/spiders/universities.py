import scrapy
import asyncio


class UniversitiesSpider(scrapy.Spider):
    name = "universities"

    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.year = kwargs.get('year')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse, cb_kwargs=dict(year=self.year))

    async def parse(self, response, year):
        universities = response.css(
            '#container > div > div > div.col-center.fl > div.col-513.bottom25 > div.seah-bemak > div.schol-fiter.bottom25.clearfix > div.list-schol.fl > ul.list_style > li')
        for i in range(1, len(universities)):
            css1 = f'#container > div > div > div.col-center.fl > div.col-513.bottom25 > div.seah-bemak > div.schol-fiter.bottom25.clearfix > div.list-schol.fl > ul.list_style > li:nth-child({i}) > a::attr(href)'
            css2 = f'#container > div > div > div.col-center.fl > div.col-513.bottom25 > div.seah-bemak > div.schol-fiter.bottom25.clearfix > div.list-schol.fl > ul.list_style > li:nth-child({i}) > a > strong::text'
            css3 = f'#container > div > div > div.col-center.fl > div.col-513.bottom25 > div.seah-bemak > div.schol-fiter.bottom25.clearfix > div.list-schol.fl > ul.list_style > li:nth-child({i}) > a::attr(title)'
            link = response.css(css1).get()
            arryear = year.split(",")
            # year = ['2019', '2020']
            # print(year)
            code = response.css(css2).get()
            name = response.css(css3).get()
            if link is not None:
                backuplink = link
                for itemyear in arryear:
                    intitemyear = int(itemyear)
                    link = backuplink
                    linkquery = f"?y={intitemyear}"
                    link += linkquery
                    link = response.urljoin(link)
                    request = scrapy.Request(link, callback=self.parse_2, cb_kwargs=dict(code=code))
                    request.cb_kwargs['year'] = itemyear
                    request.cb_kwargs['name'] = name
                    yield request
    def parse_2(self, response, code, year, name):
        # tableuni = response.css('#reBench > div.seah-bemak.resul-bemak > div.resul-seah > div.tabs > div')
        # tableuni = response.css('#reBench > div.seah-bemak.resul-bemak > div.resul-seah > div.tabs > div > table > tbody')
        # tableuni = response.css('#one > table > tbody > tr.gray'
        tableuni = response.css(
            '#reBench > div.seah-bemak.resul-bemak > div.resul-seah > div.tabs > div.tab > table > tr.bg_white')
        bench_mark = []
        for item in tableuni:
            item_benchmark = {}
            item_benchmark['major_code'] = item.css('td:nth-child(2)::text').get()
            item_benchmark['major_name'] = item.css('td:nth-child(3)::text').get()
            item_benchmark['block'] = item.css('td:nth-child(4)::text').get()
            item_benchmark['benchmark'] = item.css('td:nth-child(5)::text').get()
            item_benchmark['note'] = item.css('td:nth-child(6)::text').get()
            bench_mark.append(item_benchmark)
        i = {}
        arrObject = {}
        arrObject['year'] = year
        arrObject['code'] = code
        arrObject['name'] = name
        arrObject['benchmark'] = bench_mark
        i['url'] = arrObject
        yield i

        # for major in majors:
        #   infor = major.css('tr td::text').getall()
        #   return {
        #     'code': infor[1],
        #     'name': infor[2]
        #   }
