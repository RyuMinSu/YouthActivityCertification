import pandas as pd
from expactor.db_mysql import read_table, save_table_info_list
from youth.expactor.youthdata import get_data, get_soup, get_data_for

sql1 = """
    SELECT pgCode FROM programlist
"""
results = read_table(sql1)
result = [result[0] for result in results]

file = open('service_key.txt', 'r')
service_key = file.readline()
file.close()

date_columns = ["procno", "sdate", "edate"]

for i, key in enumerate(result):
    print(i, end=" ")
    DATE_URL = f"http://apis.data.go.kr/1383000/YouthActivInfoCertiSrvc2/getCertiActiDateList?pageNo=1&numOfRows=10&type=xml&serviceKey={service_key}&key1={key}"
    print(DATE_URL)
    try:
        items = get_soup(DATE_URL)
        for i in range(len(items)):
            row = get_data_for(i, items, date_columns)
            row['pgCode'] = key
            save_table_info_list('datelist', row, date_columns)
            print(row)
    except:
        items = get_soup(DATE_URL)
        for i in range(len(items)):
            row = get_data_for(i, items, date_columns)
            row['pgCode'] = key
            save_table_info_list('datelist', row, date_columns)
            print(row)
