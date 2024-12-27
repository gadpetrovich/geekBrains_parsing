from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('lesson07hw.ini')

login = config["lesson07hw"]["login"]
password = config["lesson07hw"]["password"]
mails_count = int(config["lesson07hw"]["mails_count"])

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)
driver.get('https://mail.ru/')

client = MongoClient('localhost', 27017)
mongo_base = client.mailru
collection = mongo_base['letters']

def login_to_site():
  time.sleep(2)
  login_button = driver.find_element(By.XPATH, '//*[@id="mailbox"]/div[1]/button')
  login_button.click()

  time.sleep(2)
  
  # переходим в iframe аутентификации
  driver.switch_to.frame(frame_reference=driver.find_element(By.XPATH, '//iframe[@class="ag-popup__frame__layout__iframe"]'))

  username_input = driver.find_element(By.XPATH, '//input[@name="username"]')
  username_input.send_keys(login)

  next_login_button = driver.find_element(By.XPATH, '//button[@data-test-id="next-button"]')
  next_login_button.click()
  time.sleep(2)

  #vk_id
  try:
    vk_id_button = driver.find_element(By.XPATH, '//button[@data-test-id="bind-screen-vkid-change-restore-type-btn"]')
    vk_id_button.click()
    time.sleep(2)
  except:
    pass

  password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
  password_input.send_keys(password)

  enter_button = driver.find_element(By.XPATH, '//button[@data-test-id="submit-button"]')
  enter_button.click()
  time.sleep(2)

  driver.switch_to.parent_frame()
  
def get_letters():
  for letter_number in range(mails_count):    
    actions = ActionChains(driver)
    time.sleep(2)
    actions.send_keys(Keys.DOWN).perform()
    actions.send_keys(Keys.ENTER).perform()
    
    time.sleep(2)
    
    title = driver.find_element(By.XPATH, '//h2').text
    email = driver.find_element(By.XPATH, '//div[@class="letter__author"]/span').get_attribute('title')
    body = driver.find_element(By.CLASS_NAME, 'letter__body').text
    date = driver.find_element(By.CLASS_NAME, 'letter__date').text
    _id = driver.find_element(By.CLASS_NAME, 'thread__letter').get_attribute('data-id')
    print(letter_number, title, email, date)
    
    collection.insert_one({
      '_id': _id,
      'email': email,
      'title': title,
      'date': date,
      'body': body
    })
    
    actions.send_keys(Keys.ESCAPE).perform()

login_to_site()
get_letters()

