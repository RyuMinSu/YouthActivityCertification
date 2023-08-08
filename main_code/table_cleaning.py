import pandas as pd
import numpy as np
import requests

from expactor.db_mysql import read_table, insert_table


#---------- 데이터 불러오기
data_sql = """
    SELECT * FROM programinfo;
"""
col_sql = """
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME="programinfo";
"""

result = read_table(data_sql)
cols = read_table(col_sql)
columns = [col[0] for col in cols]
df = pd.DataFrame(result, columns=columns)
print(df.shape)

#---------- naver api
url = "https://openapi.naver.com/v1/search/local.json"

naver_key = open("../naver_api_key.txt", "r")
lines = naver_key.readlines()
lines = [line.strip() for line in lines]
naver_id = lines[0]
naver_pw = lines[1]

headers = {
    "X-Naver-Client-Id": naver_id,
    "X-Naver-Client-Secret": naver_pw
}
print(headers)
#
# org_names = df['orgName'].tolist()
# for idx, org_name in enumerate(org_names):
#     params = {"query": org_name}
#     res = requests.get(url, params=params, headers=headers)
#
#     try:
#         items = res.json()['items'][0] #dict
#         print(idx, org_name, items['mapx'], items['mapy'])
#         sql = """
#             INSERT INTO orgxy(orgName, address, roadAdress, x, y) VALUES(
#                 '"""+org_name+"""',
#                 '"""+items['address']+"""',
#                 '"""+items['roadAdress']+"""',
#                 """+str(items['mapx'])+""",
#                 """+str(items['mapy'])+"""
#             );
#         """
#         # print(sql)
#         insert_table(sql)
#     except:
#         # addr = ''
#         # road_addr = ''
#         print(idx, org_name, '', '')
#         sql = """
#             INSERT INTO orgxy(orgName) VALUES(
#                 '"""+org_name+"""'
#             );
#         """
#         # print(sql)
#         insert_table(sql)




params = {"query": "장흥청소년수련관"}
res = requests.get(url, params=params, headers=headers)
print(res.json())






