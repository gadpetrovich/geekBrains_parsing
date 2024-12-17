import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class LabirintSpider(scrapy.Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]
    # фантастика
    start_urls = ["https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0"]

    def parse(self, response:HtmlResponse):
      
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
            
        links = response.xpath('//a[@class="product-card__name"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.product_parse)
            
        print(next_page)

    def product_parse(self, response:HtmlResponse):
        caption = response.xpath('//h1/text()').get()
        _id = response.url.split('/')[-2]
        description = ' '.join(response.xpath('//div[@id="product-about"]//p//text()').getall())
        if len(response.xpath('//span[@class="buying-priceold-val"]')) == 0:
          price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
          if not price:
            price = response.xpath('//span[@class="buying-price-val-number"]/text()').get()
          
          salary = price + ' ' + response.xpath('//span[@class="buying-pricenew-val-currency"]/text()').get()
        else:
          salary = None
        url = response.url
        
        yield JobparserItem(caption=caption, description=description, url=url, salary=salary, _id=_id)

