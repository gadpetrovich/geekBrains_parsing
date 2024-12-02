import requests
import os
from dotenv import load_dotenv
from pprint import pprint
import pandas

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
  load_dotenv(dotenv_path)

url = "https://api.foursquare.com/v3/places/search"


place = input("Введите категорию: ")

params = {
  "query": place,
  "fields": "name,location,rating",
}

headers = {
    "accept": "application/json",
    "Authorization": os.getenv("API_KEY")
}

response = requests.get(url, params=params, headers=headers)

j_data = response.json()

data = [[x.get("name"), x.get("location").get("address"), x.get("rating")] for x in j_data.get("results")]
df = pandas.DataFrame(data, columns=["Название", "Адрес", "Рейтинг"])
print(df)
print()

