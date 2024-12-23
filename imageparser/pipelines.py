# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import csv

class ImageparserPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func = None, settings = None, *, crawler = None):
        self.csv_file = open('photos.csv', 'w', newline='\n', encoding='utf-8')
        super().__init__(store_uri, download_func, settings, crawler=crawler)
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)
        #return super().get_media_requests(item, info)
        
    def item_completed(self, results, item, info):
        if results:
            item['photo'] = results[0][1]['path'] if results[0][0] else None
        csv.writer(self.csv_file, delimiter=';').writerow([item['url'], item['title'], item['photo'], item['tags']])
        return item
        #return super().item_completed(results, item, info)
        
