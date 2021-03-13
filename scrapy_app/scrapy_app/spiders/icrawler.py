import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class IcrawlerSpider(CrawlSpider):
    name = 'icrawler'

    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]


    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response):
        str_url = response.url
        if str_url.find("mien-trung") != -1 or str_url.find("da-nang") != -1:
            side = "Trung"
        elif str_url.find("mien-nam") != -1 or str_url.find("tp-hcm") != -1:
            side = "Nam"
        else:
            side = "Bac"
        list_uni = response.css('table.tabledata tbody>tr>td>a')
        yield from response.follow_all(list_uni, self.parse_uni , cb_kwargs=dict(side=side))

    def parse_uni(self, response, side):
        # def extract_with_css(query):
        #     return response.css(query).getall()

        i = {}
        uniobj = {}
        inforarr = response.css("body > div.container > div.container-content > div.detail-left > div > ul:nth-child(2)").extract()[0]
        x = re.search("(?<=Tên tiếng Anh: ).*?(?=<\/s)", inforarr)
        if re.search("(?<=Tên trường: ).*?(?=<\/s)", inforarr) != None:
            uniobj['vnName'] = re.search("(?<=Tên trường: ).*?(?=<\/s)", inforarr).group()
        # else:
        #     uniObj['uniViName'] = ''
        if re.search("(?<=Tên tiếng Anh: ).*?(?=<\/s)", inforarr) != None:
            uniobj['engName'] = re.search("(?<=Tên tiếng Anh: ).*?(?=<\/s)", inforarr).group()
        # else:
        #     uniObj['uniEngName'] = ''
        if re.search("(?<=Mã trường: ).*?(?=<\/s)", inforarr) != None:
            uniobj['code'] = re.search("(?<=Mã trường: ).*?(?=<\/s)", inforarr).group()
        # else:
        #     uniObj['code'] = ''
        if re.search("(?<=Loại trường: ).*?(?=<\/s)", inforarr) != None:
            uniobj['type'] = re.search("(?<=Loại trường: ).*?(?=<\/s)", inforarr).group()
        # else:
        #     uniObj['type'] = ''
        if re.search("(?<=Hệ đào tạo: ).*?(?=<\/s)", inforarr):
            uniobj['levelEdu'] = re.search("(?<=Hệ đào tạo: ).*?(?=<\/s)", inforarr).group()
        # else:
        #     uniObj['levelEdu'] = ''
        noneAddress = response.css(".detail-content ul")[0].css("li ul li span ::text").getall()
        if len(noneAddress) > 0:
            uniobj['address'] = response.css(".detail-content ul")[0].css("li ul li span ::text").getall()
        else:
            addressArr = []
            addressArr.append(re.search("(?<=Địa chỉ: ).*?(?=<\/s)", inforarr).group())
            uniobj['address'] = addressArr
        if re.search("(?<=SĐT: ).*?(?=<\/s)", inforarr) != None:
            uniobj['phone'] = re.search("(?<=SĐT: ).*?(?=<\/s)", inforarr).group()
        if re.search("(?<=Email: ).*?(?=<\/s)", inforarr) != None:
            uniobj['email'] = re.search("(?<=Email: ).*?(?=<\/s)", inforarr).group()
        if re.search("(?<=Website: <a href=\").*?(?=\")", inforarr) != None:
            uniobj['website'] = re.search("(?<=Website: <a href=\").*?(?=\")", inforarr).group()
        if re.search("(?<=Facebook: <a href=\").*?(?=\")", inforarr) != None:
            uniobj['facebook'] = re.search("(?<=Facebook: <a href=\").*?(?=\")", inforarr).group()
        # uniobj['domain'] = "Trung"
        uniobj['side'] = side
        i['url'] = uniobj
        yield i
    # def parse_item(self, response):
    #     # You can tweak each crawled page here
    #     # Don't forget to return an object.
    #     i = {}
    #     i['url'] = response.url
    #     return i