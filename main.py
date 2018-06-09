import os
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from random import randint




if __name__ == "__main__":

    url = "https://m.avito.ru/user/2155c5e5c0b8a2f64e12a7d40c06333b/profile?id=469263583&src=item"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        executable_path=os.path.realpath('./chromedriver'),
        chrome_options=chrome_options)
    driver.get(url)

    body = driver.find_element_by_tag_name("body")
    for i in range(100):
        body.send_keys(Keys.END)

        # profile-public-items-list
        # profile-public-items-list_closed profile-public-items-list_hidden js-items-list

        try:
            more_button = driver.find_element_by_class_name("profile-public-items-list-more")
            # print(more_button)
            more_button.click()
        except Exception as e:
            print(e)

        sleep(randint(1,2))

    items = driver.find_elements_by_class_name("b-item")

    for item in items:
        