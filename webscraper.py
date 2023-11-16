from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np
import regex as re
import requests



headers = {
    'authority': 'www.zillow.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.zillow.com/?utm_medium=cpc&utm_source=google&utm_content=1471764169|65545421228|kwd-570802407|655686053248|&semQue=null&gad_source=1&gclid=CjwKCAiA9dGqBhAqEiwAmRpTC3-m_cx0vQP75H47bZGC3I3F_JvnVihISXNVci96fPwEf0KHRsL4YxoCPU0QAvD_BwE',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

params = {
    'searchQueryState': '{"pagination":{},"isMapVisible":true,"mapBounds":{"west":-88.20572740039063,"east":-87.25815659960938,"south":41.54121882182269,"north":42.125472337561625},"usersSearchTerm":"Chicago, IL","regionSelection":[{"regionId":17426,"regionType":6}],"filterState":{"ah":{"value":true},"fr":{"value":true},"fsba":{"value":false},"fsbo":{"value":false},"nc":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"fore":{"value":false},"sche":{"value":false},"schm":{"value":false},"schh":{"value":false},"schp":{"value":false},"schr":{"value":false},"schc":{"value":false},"schu":{"value":false}},"isListVisible":true}',
}

page_list = []
for i in range(1,21):
    page_list.append(i)

main_url = "https://www.zillow.com/chicago-il/rentals/"
page_url = "_p/"
urls = []
for i in page_list:
    urls.append(main_url + f'{i}' + page_url)

#sleep(8)

def scrape_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    apt_df = pd.DataFrame(columns=["Address", "Price", "Details", "Links"])
    apts = soup.find_all("article", {"class": "StyledPropertyCard-c11n-8-84-3__sc-jvwq6q-0 kbUUtf StyledPropertyCard-srp__sc-1o67r90-0 bdwyNr property-card list-card_for-rent list-card_not-saved"})
    
    #print(f"Number of property cards found: {len(apts)}")  # Debugging line

    for apt in apts:
        try:
            # Print the entire property card HTML for inspection
            #print(f"Property Card HTML: {apt}")

            address_element = apt.find("address", {"data-test": "property-card-addr"})
            price_element = apt.find("span", {"data-test": "property-card-price"})
            detail_element = apt.find("ul", {"class": "StyledPropertyCardHomeDetailsList-c11n-8-84-3__sc-1xvdaej-0 eYPFID"})
            link_element = apt.find("a", {"class": "property-card-link"})

            # Debugging lines
            #print(f"Address Element: {address_element}")
            #print(f"Price Element: {price_element}")
            #print(f"Detail Element: {detail_element}")
            #print(f"Link Element: {link_element}")

            # Extract text content
            address = address_element.text if address_element else None
            price = price_element.text if price_element else None
            link = link_element.get("href") if link_element else None
            # Example text editing controls
            detail_text = detail_element.text if detail_element else None

            # Add space between 'bd' and the following number
            detail_text = re.sub(r'(\b(bd|bds))(\d)', r'\1 \3', detail_text)

            # Add space between 'ba' and the following number
            detail_text = re.sub(r'(\bba)(\d)', r'\1 \2', detail_text)

            # Debugging line
            #print(f"Details: {detail_text}")
            detail = detail_text

            # Debugging lines
            #print(f"Address: {address}")
            #print(f"Price: {price}")
            #print(f"Details: {detail}")
            #print(f"Link: {link}")

        except Exception as e:
            print(f"An error occurred: {e}")

        apt_info = pd.DataFrame({"Address": [address], "Price": [price], "Details": [detail], "Links": [link]})
        apt_df = pd.concat([apt_df, apt_info], ignore_index=True)

    return apt_df

#sleep(30)
page1 = scrape_page(urls[19])
print(page1)

