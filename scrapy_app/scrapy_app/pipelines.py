# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from api.models import ScrapyItem
import json
import requests

class ScrapyAppPipeline:
    def __init__(self, unique_id, *args, **kwargs):
        y = json.loads(unique_id)
        print(unique_id)
        self.unique_id = y['unique_id']
        self.items = []
        self.type = y['type']
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )
    def process_item(self, item, spider):

        self.items.append(item['url'])
        # print(item['url'])
        return item
    def close_spider(self, spider):
        # And here we are saving our crawled data with django models.
        if self.type == 'newslist':
            requests.post('http://localhost:3005/api/crawler/listnews', {
                    "data": json.dumps(self.items, ensure_ascii=False),
                    "unique_id": self.unique_id,
            })
        elif self.type == 'lastestnewslist':
            requests.post('http://localhost:3005/api/crawler/listnews/update', {
                "data": json.dumps(self.items, ensure_ascii=False),
                "unique_id": self.unique_id,
            })
        elif self.type == 'benchmarks':
            requests.post('http://localhost:3005/api/crawler/benchmarks', {
                "data": json.dumps(self.items, ensure_ascii=False),
                "unique_id": self.unique_id,
            })
        elif self.type == 'major':
            requests.post('http://localhost:3005/api/crawler/edumajors', {
                "data": json.dumps(self.items, ensure_ascii= False),
                "unique_id": self.unique_id,
            })
        elif self.type == "icon":
            requests.post('http://localhost:3005/api/crawler/universities-logo', {
                "data": json.dumps(self.items, ensure_ascii=False),
                "unique_id": self.unique_id
            })
        elif self.type == "tuition":
            requests.post('http://localhost:3005/api/crawler/universities-add', {
                "data": json.dumps(self.items,ensure_ascii=False),
                "unique_id": self.unique_id
            })
        elif self.type == "listblock":
            requests.post('http://localhost:3005/api/crawler/block', {
                "data": json.dumps(self.items, ensure_ascii=False),
                "unique_id": self.unique_id
            })
        elif self.type == "detailUni":
            requests.post('http://localhost:3005/api/crawler/universities', {
                "data": json.dumps(self.items, ensure_ascii=False),
                "unique_id": self.unique_id
            })
        item = ScrapyItem()
        item.unique_id = self.unique_id
        item.data = json.dumps(self.items, ensure_ascii=False)
        item.save()

