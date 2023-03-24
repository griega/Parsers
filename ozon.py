from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import service
import sqlite3

conn = sqlite3.connect('ozon.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE products (name TEXT, price TEXT, link text)")

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
    url = 'https://www.ozon.ru/highlight/globalpromo/?page={0}'.format(page_id)
    browser.get(url)
    time.sleep(1)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(1)


    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')

    for parent in soup.find_all('div', class_=["ne0", "ne1", "e4n", "aec3"]):
        names = parent.find_all('span', class_=["ie2", "ei3", "ie3", "ie5", "tsBodyL", "n5e"]) + parent.find_all('span', class_=["ie2", "ei3", "ie3", "ie5", "tsBodyL", "j4v", "v4j"])
        links = parent.find_all('a')
        prices = parent.find_all('div', class_=["aa2-a0"])
        for name, link, price in zip(names, links, prices):
            product_name = name.getText()
            product_price = price.getText()
            product_link = 'https://www.ozon.ru' + link.get("href")

            print(product_name)
            print(product_price)
            print(product_link)
            print('--------------------------------------------------------------------------')

            # # запись данных в таблицу
            # cursor.execute("INSERT INTO products (name, price, link) VALUES (?, ?, ?)",
            #                (product_name, product_price, product_link))
            # conn.commit()

    for parent1 in soup.find_all('div', class_=["jy8 y8j"]):
        names = parent1.find_all('span', class_=["ei3 ie3 ei4 ei6 tsBodyL vj7 jv8"]) + parent1.find_all('span', class_=["ie2", "ei3", "ie3", "ie5", "tsBodyL", "j4v", "v4j"])
        links = parent1.find_all('a')
        prices = parent1.find_all('div', class_=["aa2-a0"])
        for name, link, price in zip(names, links, prices):
            product_name = name.getText()
            product_price = price.getText()
            product_link = 'https://www.ozon.ru' + link.get("href")

            print(product_name)
            print(product_price)
            print(product_link)
            print('--------------------------------------------------------------------------')

            # запись данных в таблицу
            cursor.execute("INSERT INTO products (name, price, link) VALUES (?, ?, ?)",
                           (product_name, product_price, product_link))
            conn.commit()


conn.close()
# завершение работы
time.sleep(30)
browser.quit()
