import aiohttp
import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def page_code(url):
    html_code = await fetch_html(url)  # Используем функцию fetch_html для получения HTML-кода страницы
    return html_code


async def kaif_parse():
    # Создаем объект webdriver для управления браузером
    browser = webdriver.Chrome()
    for page_id in range(1, 10):
        url = "https://www.mvideo.ru/promo/ubileinoe-kombo-mark202783495/f/page={}".format(page_id)
        browser.get(url)
        await asyncio.sleep(1)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # Загружаем страницу с помощью метода get объекта webdriver

        # Получаем HTML-код страницы, уже загруженной в браузере
        html_code = browser.page_source

        # Создаем объект BeautifulSoup для парсинга HTML-кода страницы
        soup = BeautifulSoup(html_code, 'html.parser')
        await asyncio.sleep(1)

        # Ищем все родительские элементы с классом "fl-product-tile"
        for parent in soup.find_all('div', class_=["fl-product-tile"]):
            # Ищем все ссылки, названия, цены и фотографии товаров
            links = parent.find_all('a')
            names = parent.find_all('a', class_=["fl-product-tile-title__link sel-product-tile-title"])
            prices = parent.find_all('span', class_=["fl-product-tile-price__current"])
            photos = parent.find_all('img')

            # Проходим по списку товаров и выводим информацию о каждом товаре
            for name, link, price, photo in zip(names, links, prices, photos):
                product_photo = photo.get("src")
                product_name = name.getText()
                product_price = price.getText()
                product_link = 'https://www.mvideo.ru/' + link.get("href")

                print(product_photo)
                print(product_name)
                print(product_price)
                print(product_link)
                print('--------------------------------------------------------------------------')
                await asyncio.sleep(1)

    browser.quit()  # Закрываем браузер после завершения работы


async def main():
    # Запускаем функцию kaif_parse в рамках цикла событий asyncio
    await kaif_parse()


if __name__ == '__main__':
    asyncio.run(main())
