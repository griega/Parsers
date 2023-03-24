from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
for page_id in range(1, 10):
   url = "https://www.wildberries.ru/catalog/0/search.aspx?page={0}&sort=popular&search=%D1%81%D0%BA%D0%B8%D0%B4%D0%BA%D0%B8+40%25".format(page_id)
   browser.get( url )

   for x in range(300):
       browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
       browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ALT + Keys.ARROW_DOWN)

    #print("Page(%d) is ready!" % page_id )
   page_html = browser.page_source

   for i in range(100):
        start_item_id = page_html.find("<div data-nm-id") + 1
        html_erase = page_html[start_item_id: len(page_html)]

        end_item_id = html_erase.find("<div data-nm-id")
        item_info = html_erase[0: end_item_id]

        brand_name_found = "<span class=\"brand-name\">"
        name_start_id = item_info.find(brand_name_found) + len(brand_name_found);
        name_erase = item_info[name_start_id: name_start_id + 1000]

        name_end_id = name_erase.find("</span>");
        brand_name = name_erase[0: name_end_id]

        lower_price_found = "<ins class=\"price__lower-price\">"
        if (item_info.find(lower_price_found)== -1):
            page_html = html_erase[ end_item_id : len( html_erase ) ]
            continue
        lower_price_start_id = item_info.find(lower_price_found) + len(lower_price_found);
        lower_price_erase = item_info[lower_price_start_id: lower_price_start_id + 1000]

        lower_price_end_id = lower_price_erase.find("</ins>");
        lower_price = lower_price_erase[0: lower_price_end_id]

        lower_price = lower_price.replace(' ', '')
        lower_price = lower_price.replace('&nbsp;', '')

        link_found = "href=\""
        link_start_id = item_info.find(link_found) + len(link_found);
        link_erase = item_info[link_start_id: link_start_id + 1000]

        link_end_id = link_erase.find("\">");
        link_price = link_erase[0: link_end_id]

        print(i)
        print(brand_name)
        print(lower_price)
        print(link_price)

        print("----------------------")

        page_html = html_erase[end_item_id: len(html_erase)]

