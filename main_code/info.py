from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import requests

from youth.expactor.db_mysql import read_table
from youth.expactor.youthdata import get_data

#---------- 1차 시작
# sql = """
#     select pgcode from programlist
# """

#---------- 2차 시작
sql = """
    select programlist.pgCode
    from programlist
    where pgCode not in (
        select pgCode
        FROM programinfo
        );
"""
results = read_table(sql)
result = [result[0] for result in results]
print("keyword 갯수:", len(result))

file = open('../service_key.txt', 'r')
service_key = file.readline()
file.close()

info_columns = ["nums", "organnm", "pgmnm", "price", "target", "managernm", "email", "tel", "info1", "info2"]

error_key = []
for i, key in enumerate(result):
    print(i, end=" ")
    INFO_URL = f"http://apis.data.go.kr/1383000/YouthActivInfoCertiSrvc2/getCertiProgrmInfo?type=xml&serviceKey={service_key}&key1={key}"
    try:
        get_data(INFO_URL, 'programinfo', info_columns)
    except:
        error_key.append(i)
        get_data(INFO_URL, 'programinfo', info_columns)
print(error_key)


