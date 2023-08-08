#-*-coding:utf-8-*-

import re
import time
from urllib.parse import quote_plus

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

from youth.expactor.db_mysql import read_table, insert_table


#---------- read data
data_sql = """
    SELECT orgName, address, roadAddress
    FROM orginfo
    GROUP BY orgName, address, roadAddress;
"""

data = read_table(data_sql)
columns = ["orgName", "address", "roadAddress"]
df = pd.DataFrame(data, columns=columns)
print(df.shape)


#----------geo_api
geo_key = open("../geo_key.txt", "r")
lines = geo_key.readlines()
lines = [line.strip() for line in lines]
geo_key = lines[0]

#---------- data scraping(e-청소년 홈페이지 크롤링 > geocoding api)
org_names = df['orgName'].tolist()
for idx, org_name in enumerate(org_names[324:]):

    org_info_dict = {}

    orgName = quote_plus(org_name)
    url = f"https://www.youth.go.kr/m/yap/operInsttGuidance/operInsttLstForm.mo?sort=&order=&page=1&rows=&kFcltySn=&nas.cmm.token.html.TOKEN=a79580f179c0d392ce18d13e8aea15c5&sCtprvnCode=&sFcltyNm={orgName}"

    res = requests.get(url)
    soup = bs(res.content, 'html.parser')
    try:
        name_box = soup.select_one("div.act-name-box")
        address = name_box.select("dd")[0].get_text().strip().replace("주소 :  ", "").split("(")[0]
        address = re.sub('[^가-힣0-9-~ ]', "", address).split(org_name)[0]
    except:
        address = "nodata"


    #---------- geocoding
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GEO_KEY}"
    params = {'language':'ko'}
    res = requests.get(geo_url, params=params)
    geo_json = res.json()

    try:
        lat = geo_json['results'][0]['geometry']['location']['lat']
        lng = geo_json['results'][0]['geometry']['location']['lng']

        org_info_dict["orgName"] = org_name
        org_info_dict["orgAddress"] = address
        org_info_dict["lat"] = lat
        org_info_dict["lng"] = lng

        #---------- reverse geocoding
        reverse_geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={org_info_dict['lat']},{org_info_dict['lng']}&key={GEO_KEY}"
        params = {"language":"ko"}
        res = requests.get(reverse_geo_url, params=params)
        res_json = res.json()

        road_address = res_json["results"][0]["formatted_address"]

        org_info_dict['roadAddress'] = road_address
        print(idx, org_info_dict)

        insert_sql = """
            INSERT INTO orginfo2(orgName, orgAddress, roadAddress, lat, lng)
            VALUES(
                '"""+org_info_dict['orgName']+"""',
                '"""+org_info_dict['orgAddress']+"""',
                '"""+org_info_dict['roadAddress']+"""',
                """+str(org_info_dict['lat'])+""",
                """+str(org_info_dict['lng'])+"""
            );
        """
        insert_table(insert_sql)

    except:
        lat = 99999
        lng = 99999

        org_info_dict["orgName"] = org_name
        org_info_dict["orgAddress"] = address
        org_info_dict["lat"] = lat
        org_info_dict["lng"] = lng
        org_info_dict['roadAddress'] = "Nodata"

        insert_sql = """
            INSERT INTO orginfo2(orgName, orgAddress, roadAddress, lat, lng)
            VALUES(
                '""" + org_info_dict['orgName'] + """',
                '""" + org_info_dict['orgAddress'] + """',
                '""" + org_info_dict['roadAddress'] + """',
                """ + str(org_info_dict['lat']) + """,
                """ + str(org_info_dict['lng']) + """
            );
        """
        insert_table(insert_sql)


