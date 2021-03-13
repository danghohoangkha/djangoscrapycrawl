import scrapy
import random
from urllib.parse import urlparse
from datetime import datetime as dt, timedelta

# run comand
# scrapy runspider --set FEED_EXPORT_ENCODING=utf-8 universityNews.py -o universityNews.json

def findTag(contentStr):
    defaultTags = ['tuyển sinh', 'điểm chuẩn', 'xét tuyển', 'chỉ tiêu', 'điều chỉnh nguyện vọng',
                   'đánh giá năng lực']
    resultTags = []
    for tag in defaultTags:
        result = contentStr.lower().find(tag)
        if result != -1:
            resultTags.append(tag)

    return resultTags

class BrickSetSpider(scrapy.Spider):
    name = 'lastestnewscrawler'
    def __init__(self, *args, **kwargs):

        self.url = kwargs.get('url')
        self.crawlDate = kwargs.get('crawlDate')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]
    # start_urls = ['https://kenhtuyensinh.vn/dai-hoc-cao-dang']
    def start_requests(self):
        yield scrapy.Request(self.url, self.parse)
    nextPageMax = 10

    def parse(self,response):
        def __init__(self):
            self.count = 1

        crawlDateFormat = dt.strptime(self.crawlDate, "%Y/%m/%d")
        # universityNewsLink1 = response.css(".fsz-lg a")
        # universityNewsLink2 = response.css('.featured-article div.col-lg-5.col-md-12.col-5 a')
        #
        # yield from response.follow_all(universityNewsLink1, self.parseUniversitynewsDetail)
        # yield from response.follow_all(universityNewsLink2, self.parseUniversitynewsDetail)

        eleList = response.css('div.row.no-gutters.article-box')
        for x in eleList:
            str = x.css('div.catntime::text').get()
            preNumberDate = [int(s) for s in str.split() if s.isdigit()]
            d = dt.today() - timedelta(days=preNumberDate[0])
            if d > crawlDateFormat:
                universityNewsLink3 = x.css('.hotnews-title a')
                yield from response.follow_all(universityNewsLink3, self.parseUniversitynewsDetail)
            else:
                return

        nextPage = response.xpath('//*[@id="w0"]/div[2]/a[text()= "' + str(int(currentPage) + 1) + '"]')

        yield from response.follow_all(nextPage, self.parse)

    def parseUniversitynewsDetail(self, response):
        tags = response.css('.tag ::text').getall()
        topic = response.css(".topic ::text").extract_first().strip()
        title = response.css(".post-heading ::text").extract_first().strip()
        findTagList = findTag(title)
        tags.append(topic)
        tags = tags + findTagList
        if response.css('p>img::attr(data-src)').extract_first():
            avatar = response.css('p>img::attr(data-src)').extract_first()
        else:
            avatar = response.css('img::attr(src)').extract_first()
        if response.css('.post-content img::attr(data-src)').extract():
            news_image = response.css('.post-content img::attr(data-src)').extract(),
        else:
            news_image = response.css('.post-content img::attr(src)').extract(),
        uniobj = {
            'source': urlparse(response.request.url).path,
            'avatarImage': avatar,
            "title": title,
            'author': response.css(".author-name ::text").extract_first().strip(),
            'date': response.css(".author-posted-date ::text").extract_first().strip()[-10:],
            'detailContent': response.css(".post-content").extract()[0].replace("data-src", "src").replace("\\","").strip(),
            "tags": tags,
            "tag_category": topic,
            'news_image': news_image[0],
            'briefContent': response.css(".post-content>p::text").extract_first().strip()
        }
        i ={}
        i['url'] = uniobj
        yield i