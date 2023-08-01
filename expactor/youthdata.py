import re
import time

import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from youth.expactor.db_mysql import save_table_info_list


def get_data_for(i, items, url_columns=None):
    row = {}
    for j in range(len(url_columns)):
        try:
            val = items[i].select_one(url_columns[j]).get_text().strip().replace("'",'"')
            val = re.sub('[^0-9a-zA-Z가-힣-() ]', "", val).strip()
            row[url_columns[j]] = val
        except:
            val = ""
            row[url_columns[j]] = val
    return row

def get_soup(url):
    res = requests.get(url)
    time.sleep(.3)
    soup = bs(res.text, 'html.parser')
    items = soup.select('item')
    return items

def get_data(url, table_name, url_columns=None):
    items = get_soup(url) #soup을 통한 내용 추출
    for i in range(len(items)):
        row = get_data_for(i, items, url_columns)
        print(row)
        # save_table_info_list(table_name, row, url_columns) #저장






