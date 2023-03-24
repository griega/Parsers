from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3

# conn = sqlite3.connect('pegas.db')
# cursor = conn.cursor()

# cursor.execute("CREATE TABLE tures (photo TEXT, name TEXT, price TEXT, link text)")

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

service = service.ChromiumService('C:\chromedriver_win32 (1)/chromedriver.exe')
service.start()

browser = webdriver.Chrome(options=options, service=service)

browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })

for page_id in range(1, 10):
    url = 'https://level.travel/hot'
    browser.get(url)
    time.sleep(1)
    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ALT + Keys.ARROW_DOWN)
    time.sleep(1)


    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')


    for parent in soup.find_all('div', class_=["htours_hotels_item"]):
        links = parent.find_all('a')
        names = parent.find_all('div', class_=["hotels_item_city-name"])
        prices = parent.find_all('div', class_=["hotels_item_price_number"])
        photos = parent.find_all('div', {"class": "hotels_item_preview_img"})
        tiimes1 = parent.find_all('span', class_=["hotels_item_ditem_label"])
        for name, link, price, photo, tiime1 in zip(names, links, prices, photos, tiimes1):
            product_photo = photo.getText()
            product_name = name.getText()
            product_price = price.getText()
            tiime1 = tiime1.getText()
            product_link = 'https://level.travel/' + link.get("href")

            print(product_photo)
            print(product_name)
            print(tiime1)
            print(product_price)
            print(product_link)
            print('--------------------------------------------------------------------------')

            # запись данных в таблицу
            # cursor.execute("INSERT INTO tures (photo, name, price, link) VALUES (?, ?, ?, ?)",
            #                (product_photo, product_name.lstrip(), product_price.lstrip(), product_link))
            # conn.commit()


# conn.close()
# завершение работы
time.sleep(30)
browser.quit()