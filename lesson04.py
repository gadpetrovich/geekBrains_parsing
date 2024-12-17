from lxml import html
from fake_useragent import UserAgent
import requests
from pprint import pprint
import csv

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
url = 'https://news.mail.ru/'
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

articles = dom.xpath("//div[@role='navigation']/../..")
with open('articles.csv', 'w', newline='', delimiter=';', encoding='utf-8') as f:
  for article in articles:
    article_info = {}
    hrefs = article.xpath("./h3/a/@href")
    caption = article.xpath("./h3/a/text()")
    description = article.xpath(".//div[@data-qa='Text']/text()")
    if (len(caption) == 0 or len(description) == 0):
      continue

    article_info['href'] = hrefs[0]
    article_info['caption'] = caption[0]
    article_info['description'] = description[0]
    
    csv.writer(f).writerow([article_info['href'], article_info['caption'], article_info['description']])
    
