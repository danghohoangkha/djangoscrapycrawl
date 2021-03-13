import scrapy
from selenium import webdriver
import time
class ProductSpider(scrapy.Spider):
    name = "tuitionuni"

    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
        self.driver = webdriver.Chrome()

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        print("Chay parse")
        next = self.driver.find_element_by_xpath('//*[@id="timtruong_viewmore"]')
        print(next)
        count = 0;
        for j in range(19):
            count += 1
            max = count * 15
            try:
                self.driver.execute_script("arguments[0].click();", next)
                print('click')
            except:
                break
            # time.sleep(0.5)
            for i in range(max-14, max):
                # css1 = f"#pjax_010 > div.uni-list.grid > div:nth-child({i}) > a"
                try:
                    link = self.driver.find_element_by_xpath(f'//*[@id="pjax_010"]/div[1]/div[{i}]/a').get_attribute("href")
                    code = self.driver.find_element_by_xpath(
                        f'//*[@id="pjax_010"]/div[1]/div[{i}]/div[4]/div[3]/span[2]/strong').text
                    time.sleep(1)
                    request = scrapy.Request(link, callback=self.parse_2, cb_kwargs=dict(code=code))
                    yield request
                except:
                    break
                # get the data and write it to scrapy items
    def parse_2(self,response,code):
        intro = response.css('body > section.list-school > div.main-lschool.container > div > div.col-lg-6.col-center > div > div.pc').extract()
        url = response.url
        extend = "/hoc-phi"
        urllink = url + extend
        # urllink = "https://kenhtuyensinh.vn/dai-hoc-my-tai-viet-nam-u-298/hocphi"
        request = scrapy.Request(urllink, callback=self.parse_3, cb_kwargs=dict(intro=intro))
        request.cb_kwargs['code'] = code
        yield request
    def parse_3(self, response, intro, code):
        tuition = response.css('body > section.list-school > div.container > div > div.col-lg-6.col-center > div > div').extract()
        # code = response.css('body > section.list-school > div.header-school > div > div > div.col-lg-8 > span::text').get()
        name = response.css('body > section.list-school > div.header-school > div > div > div.col-lg-8 > div.flex-wrapper > h1::text').get()
        i = {}
        arrObject = {}
        arrObject['code'] = code
        arrObject['name'] = name
        arrObject['intro'] = intro
        arrObject['tuition'] = tuition
        i['url'] = arrObject
        yield i

