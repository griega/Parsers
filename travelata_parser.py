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


url = 'https://m.travelata.ru/tury/egypt#?fromCity=2&dateFrom=28.03.2023&dateTo=28.03.2023&nightFrom=3&nightTo=10&adults=2&hotelClass=all&meal=all&sid=ooq7ndn3fy&sort=priceUp&f_minPrice=100&f_maxPrice=5000000&f_good=true&toCountries=29'
browser.get(url)
time.sleep(1)
browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
time.sleep(1)


page_html = browser.page_source
soup = BeautifulSoup(page_html, 'html.parser')

for parent in soup.find_all('div', class_=["serpHotelCard__resort"]):
    # links = parent.find_all('a')
    names = parent.find_all('div', class_=["serpHotelCard__resort"])
    prices = parent.find_all('div', class_=["serpHotelCard__btn-price"])
    photos = parent.find_all('div', {"class": "hotels_item_preview_img"})
    tiimes1 = parent.find_all('span', class_=["serpHotelCard__group"])
    for name,price, photo, tiime1 in zip(names, prices, photos, tiimes1):
        product_photo = photo.getText()
        product_name = name.getText()
        product_price = price.getText()
        tiime1 = tiime1.getText()
        # product_link = 'https://m.travelata.ru/' + link.get("href")

        print(product_photo)
        print(product_name)
        print(tiime1)
        print(product_price)
        # print(product_link)
        print('--------------------------------------------------------------------------')

            # запись данных в таблицу
            # cursor.execute("INSERT INTO tures (photo, name, price, link) VALUES (?, ?, ?, ?)",
            #                (product_photo, product_name.lstrip(), product_price.lstrip(), product_link))
            # conn.commit()


# conn.close()
# завершение работы
time.sleep(30)
browser.quit()