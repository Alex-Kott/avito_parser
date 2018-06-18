import json
from xml.etree import ElementTree as ET
from collections import defaultdict

from bs4 import BeautifulSoup

if __name__ == "__main__":
    #
    # ids = set()
    # with open("missed_ids.txt") as file:
    #     ids = {int(line) for line in file.readlines()}
    #     print(len(ids))
    #
    # with open("missed_ids.txt", "w") as file:
    #     for i in ids:
    #         file.write(f"{i}\n")

    # with open("data.json") as file:
    #     data = json.loads(file.read())
    #
    # interesting_ids = [ad['id'] for ad in data]
    #
    # print(len(interesting_ids))
    # exit()
    #
    # parsed_ads = defaultdict()
    #
    with open("data.xml") as file:
        data = file.read()
        soup = BeautifulSoup(data, "lxml")

        ads = soup.find_all("ad")



        parsed_ids = set()
        for ad in ads:
            parsed_ids.add(ad)
            parsed_ids.add(int(ad.id.text))


        data = ET.parse('data.xml')

        root = ET.Element("Ads")
        for ad in data.findall('Ad'):
            ad_id = int(ad.find('Id').text)
            if ad_id in parsed_ids:
                root.append(ad)

        tree = ET.ElementTree(root)
        tree.write("data_lol.xml")

        # for ad in s:
        #     element = ET.fromstring(str(ad))
        #
        #     ET.SubElement(root, element)
        #


    # with open("parsed_ad_ids.txt") as file:
    #     # data = file.read()
    #     s = set()
    #     for i in file.readlines():
    #         s.add(int(i))
    #
    #     print(len(s))


        # for k, v in ad_count.items():
        #     print(k,v)