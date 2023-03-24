from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import service
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
    url = 'https://pegast.ru/hotels/search?from=76&countries=%5B73%5D'.format(page_id)
    browser.get(url)
    time.sleep(1)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(1)


    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    for parent in soup.find_all('div', class_=["hotel-search-item"]):
        links = parent.find_all('a')
        names = parent.find_all('a', class_=["hotel-search-item__hotel-name"])
        prices = parent.find_all('a', class_=["hotel-search-tour-price__price button button_theme_main button_view_pseudo button_size_lg"])
        photos = parent.find_all('img')
        for name, link, price, photo in zip(names, links, prices, photos):
            product_photo = photo.get("src")
            product_name = name.getText()
            product_price = price.getText()
            product_link = 'https://pegast.ru/' + link.get("href")

            print(product_photo)
            print(product_name.lstrip())
            print(product_price.lstrip())
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