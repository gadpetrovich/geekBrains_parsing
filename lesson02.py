from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from pprint import pprint
import json

url = "https://books.toscrape.com/"
headers = {"User-Agent": UserAgent().random}

session = requests.session()

books = []
page_number = 1

while True:
  response = session.get(url + f"/catalogue/page-{page_number}.html", headers=headers)
  if not response.ok:
    break

  soup = BeautifulSoup(response.text, "html.parser")
  
  images = soup.find_all('div', {'class': 'image_container'})
  for image in images:
    link = image.find('a').get('href')
    response = session.get(url + "catalogue/" + link, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    info = soup.find('div', {'class': 'col-sm-6 product_main'})
    title = info.find('h1').text.strip()
    price = info.find('p', {'class': 'price_color'}).text.strip()
    instock = info.find('p', {'class': 'instock availability'}).text.strip()
    instock_int =int(instock.split(' (')[1].split()[0])
    description = soup.find('meta', {'name': 'description'}).get('content').strip()
    
    book = {
      'title': title,
      'price': price,
      'instock': instock_int,
      'description': description,
    }
    books.append(book)
    #pprint(book)
  
  print("Обработано страница", page_number)
  page_number += 1

with open('books.json', 'w') as f:
  json.dump(books, f, indent=2)  
