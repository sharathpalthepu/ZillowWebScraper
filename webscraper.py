import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import regex as re

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

#response = requests.get('https://www.zillow.com/chicago-il/rentals/', params=params, headers=headers)
#status_code = response.status_code # check to make sure it returns 200

with requests.session() as session:
    city = 'chicago/'
    curr_page = 1
    end_page = 20
    url = ''
    url_list = []
    request = ''
    request_list = []
    soup = ''
    soup_list = []

    while curr_page <= end_page:
        url = 'https://www.zillow.com/chicago-il/rentals/' +f'{curr_page}_p/'
        url_list.append(url)
        curr_page += 1
    
    for url in url_list:
        request = session.get(url, headers=headers)
        request_list.append(request)
    
    for request in request_list:
        encode = request.encoding
        content = request.content.decode(encode)
        soup = BeautifulSoup(content, 'html.parser')
        soup_list.append(soup)

df_pages = []
for soup in soup_list:
    df = pd.DataFrame()
    for i in soup:
        address = soup.find_all ('div',attrs={'property-card-addr'})
        rent = list(soup.find_all(class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr"))
        beds = list(soup.find_all(class_="property-card-details"))
        details = soup.find_all ('div', {'class': 'property-card-details'})
        last_updated = soup.find_all ('div', {'class': 'property-card-top'})
        link = soup.find_all (class_= 'property-card-link')

        df['address'] = address
        df['rent'] = rent
        df['beds'] = beds
    
    urls = []
    for link in soup.find_all("article"):
        href = link.find('a',class_="property-card-link")
        if(href):
            addresses = href.find('address')
            addresses.extract()
        urls.append(href)
    
    df['links'] = urls
    df['links'] = df['links'].astype('str')
    df['links'] = df['links'].replace('<a class="list-card-link list-card-link-top-margin" href="', ' ', regex=True)
    df['links'] = df['links'].replace('" tabindex="0"></a>', ' ', regex=True)
    df_pages.append(df)

print(df_pages[0])