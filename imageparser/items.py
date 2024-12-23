# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose

def process_photo(value):
    value = value.split()[0]
    return value

class ImageparserItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field(input_processor=MapCompose(process_photo), output_processor=TakeFirst())
    tags = scrapy.Field()
    
