from bs4 import BeautifulSoup
import bs4
import requests
import pandas as pd
import numpy as np
import time
import sqlalchemy as db
from sqlalchemy import create_engine,inspect,MetaData

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Setting name of database
db_name = 'WS_data'

def getnextpage2(soup):
    page = soup.find('nav',{'class':'yFHi8N'})

    if page.find('a',{'class':'_1LKTO3'}):
        link = page.find_all('a',{'class':'_1LKTO3'})
        
        if (len(link) == 2):
            return (link[-1]['href']).split("=")[-1]  
 
        elif (len(link) == 1):

            if( int((link[-1]['href']).split("=")[-1]) == 2 ):
                return (link[-1]['href']).split("=")[-1]
            else:
                return -1
        
            #     last_page = 1
            #     return (link[-1]['href']).split("=")[-1]
    else:
        return -1
        # link = page.find('a',{'class':'ge-49M _2Kfbh8'})
        # temp = int((link['href']).split("=")[-1]) + 1
        # return str(temp)


def get_soup(page_no,product_name):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    # update respone parameter.
    params = {
        'q': product_name,
        'otracker': 'search',
        'otracker1': 'search',
        'marketplace': 'FLIPKART',
        'as-show': 'on',
        'as': 'off',
        'page': page_no,
    }

    response = requests.get('https://www.flipkart.com/search', params=params, headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup


def get_data(soup):
    title_list = []
    price_list = []
    rating_list = []
    # meta_data = []



    for li in soup.find_all("div",{"class":"_4rR01T"}):
        title_list.append(li.text)

    for li in soup.find_all("div",{"class":"_30jeq3 _1_WHN1"}):
        price_list.append(li.text)

    for li in soup.find_all("div",{"class":"_3LWZlK"}):
        rating_list.append(li.text)

    # for li in soup.find_all("div",{"class":"fMghEO"}):
    #     meta_data.append(li.text)

    temp_df = pd.DataFrame(list(zip(title_list,price_list,rating_list)),
                columns =['Title', 'Price','Rating'])

    main_box = soup.find_all("div",{"class":"_2kHMtA"})
    final_list = []


    # Create dictionary file for metadata about the product.
    for box in main_box:

        text = box.find("div",{"class":"fMghEO"})
        str_list = {}
        temp = 0
        for x in (text.li.next_siblings):
        # filter of "b" tag and get its text
            if type(x) == bs4.element.Tag:
                str_list[temp] = x.get_text().strip()
                temp +=1
                # str_list.append(x.get_text().strip())


        final_list.append(str_list)
    # safety check
    try:
        temp_df['Meta-data-json'] = final_list
    except:
        temp_df['Meta-data-json'] = np.nan
        

    return temp_df


def Load_to_sqlite(df,db_name,table_name):
  try:
    engine = create_engine('sqlite:///'+db_name+'.db', echo=False)
    df.to_sql(table_name, con=engine, if_exists='replace',index=False)
    return table_name+' Data loaded to sqlite'

  except Exception as e:
    print(e)
    return "Data not loaded"
  

def main(query):

  try:
    # query = input("Enter the product name: ")
    num = 1
    # name = "laptop"
    df = pd.DataFrame(columns =['Title', 'Price','Rating','Meta-data-json'])
    # To set maximum limit of pages to scrape
    limit  = 100000
    # temp = 0

    while True:
        print(num,end=" ") # for debugging purpose  
        if(num == -1):
            break
        
        soup = get_soup(num,query)
        temp_df = get_data(soup)
        if temp_df.shape[0] ==0:
            break
        df = df.append(temp_df,ignore_index=True)
        
        # converting json to string for sqlite
        df = df.astype({"Meta-data-json": str})
        try:
            num = getnextpage2(soup)
        except:
            break
        # # for breaking swing between 2 and 3 page number.
        # temp = num
        time.sleep(0.5)
        

    message = Load_to_sqlite(df,db_name,query)
    return 1

  except Exception as e:
    print(e)
    return 0
