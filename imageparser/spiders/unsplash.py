import scrapy

from imageparser.items import ImageparserItem
from scrapy.loader import ItemLoader


class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('query')}"]
        
    def parse(self, response):
        print()
        links = response.xpath("//figure[@data-testid='photo-grid-masonry-figure']/div/div/div/div/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_image)

    def parse_image(self, response):
        print()
        loader = ItemLoader(item=ImageparserItem(), response=response)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('photo', "//div[@class='xH5KD']/img/@srcset")
        loader.add_value('url', response.url)
        loader.add_xpath('tags', "//div[@class='uN4_r J83KD']//text()")
        
        yield loader.load_item()
        
