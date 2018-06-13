import re
import asyncio
from random import randint
from time import sleep
from pathlib import Path

from aiohttp import ClientSession
import json
import xml.etree.ElementTree as ET
from selenium import webdriver


async def update_ads(session):
    params = {
        'shortcut': 'active',  # active -- активные объявления, closed -- закрытые
        'offset': 0,
        'limit': 99
    }
    ads = []
    while True:
        async with session.get(url, params=params) as response:
            data = json.loads(await response.text())

            response_ads = data['result']['list']
            if len(response_ads) == 0:
                break

            ads.extend(response_ads)

            params['offset'] += 99
            sleep(3)

    with open("data.json", 'w') as file:
        json.dump(ads, file)


def load_ads():
    with open('data.json') as file:
        return json.loads(file.read())


def parse_ad(ad):
    advertisment = {}
    advertisment['Id'] = str(ad['id'])
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    driver = webdriver.Chrome("./chromedriver", chrome_options=options)

    driver.get(f"https://m.avito.ru{ad['url']}")

    # смотрим номер
    driver.find_element_by_class_name("action-show-number").click()
    sleep(1)
    phone_span = driver.find_element_by_class_name("js-phone-number")
    phone = phone_span.text
    advertisment['ContactPhone'] = phone

    full_address = driver.find_element_by_class_name("avito-address-text").text
    city = full_address.split(',')[0]
    advertisment['Region'] = city

    info_params = driver.find_element_by_class_name("info-params")
    params = info_params.find_elements_by_class_name("param")
    advertisment['Category'] = params[-1].text
    advertisment['GoodsType'] = params[0].text

    advertisment['AdType'] = "Товар приобретен на продажу"

    title = driver.find_element_by_class_name("single-item-header").text
    advertisment['Title'] = title

    description = driver.find_element_by_class_name("description-preview-wrapper").text
    advertisment['Description'] = description

    price = driver.find_element_by_class_name("price-value").text
    advertisment['Price'] = re.sub("\D", "", price)

    # print(advertisment, end="\n\n")

    driver.close()

    return advertisment


def save_to_file(advertisments):
    with open("parsed_ads.json", "w") as file:
        json.dump(advertisments, file)

    root = ET.Element("Ads")
    for advertisment in advertisments:
        ad = ET.SubElement(root, "Ad")
        for property, value in advertisment.items():
            ET.SubElement(ad, property).text = value

    tree = ET.ElementTree(root)
    tree.write("data.xml")


async def main():
    # async with ClientSession() as session:
        # await update_ads(session)

    advertisments = []
    ads = load_ads()
    for ad in ads:
        advertisments.append(parse_ad(ad))

        save_to_file(advertisments)
        sleep(randint(5, 10))


if __name__ == "__main__":
    data_file_name = Path('data.xml')
    url = "https://m.avito.ru/user/2155c5e5c0b8a2f64e12a7d40c06333b/profile/items"



    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
    event_loop.close()
