import re
import time

import requests
from bs4 import BeautifulSoup as bs

# from eYouth.expactor.db_mysql import read_table, insert_table, get_data

from expactor.db_mysql import read_table, insert_table

for i in range(204, 301):
    print(i)
    active_url = f"https://www.youth.go.kr/youth/act/actSearch/allActSearchLst.yt?sCrtfc=Y&sCrtfcText=&sSttemntText=&sort=&order=&page={i}&rows=&kCrtfcSn=&kFcltySn=&kSnOne=&kProgrmseCode=&kSnTwo=&kSttemntManageNo=&kSttemntSn=&kCrtfcAt=&kSttemntAt=&kSttemntNo=&kExclnccrtfcAtchmnflId=&searchDtl=&search=&sActRelmcode=&sActRelmcode1=&sActRelmcode2=&sActRelmcode3=&sActRelmcode4=&sActRelmcode5=&sActRelmcode6=&sActRelmcode7=&sActRelmcode8=&sActRelmcode9=&sActRelmcode10=&sActRelmcode11=&sActRelmcode12=&nas.cmm.token.html.TOKEN=93c955834e17dd4f878551839d077332&sKeyword=&sActCtprvnCode1=&sActSignguCode1=&sActCtprvnCode2=&sActSignguCode2=&sActCtprvnCode3=&sActSignguCode3=&sInsttTyCode=&sInsttTyCode2=&sTrget=&sAge=&stayng=&pc=&acteraDe=on&sActeraBeginDe=&sActeraEndDe=&sCurSearchFlag=Y&sChkSearchFlag=&curMenuSn=1619"
    res = requests.get(active_url)
    time.sleep(0.5)
    soup = bs(res.content, 'html.parser')

    box = soup.select_one("ul.actlist-thum-ul")
    rows = box.select("li")
    for i in range(len(rows)):
        orgInfo_dict = {}
        pginfo_dict = {}

        title_info = rows[i].select_one("dt")
        pgName = title_info.select_one("a").get_text().replace("'","")
        pgName = re.sub("[\',\"!]", "", pgName)
        pginfo_dict['pgName'] = pgName

        title_spans = title_info.select("span")
        opMethod = title_spans[0].get_text()
        try:
            avArea = title_spans[1].get_text()
        except:
            avArea = "없음"

        pginfo_dict['opMethod'] = opMethod
        pginfo_dict['avArea'] = avArea

        comps = rows[i].select("dd")
        for comp in comps:
            if "기관명" in comp.get_text():
                orgName = comp.get_text().split(" : ")[1]
                orgInfo_dict['orgName'] = orgName

            if "지역" in comp.get_text():
                avRegion = comp.get_text().split(" : ")
                orgInfo_dict['avRegion'] = avRegion[1]

            if "인증번호" in comp.get_text():
                pgcode = comp.get_text().split(" : ")[1]
                pginfo_dict["pgcode"] = pgcode

            if "등록일" in comp.get_text():
                regDate = comp.get_text().split(" : ")[1]
                pginfo_dict["regDate"] = regDate

            if "활동일" in comp.get_text():
                avDate = comp.get_text().split(" : ")[1]
                pginfo_dict["avDate"] = avDate

            if "인증기간" in comp.get_text():
                authDate = comp.get_text().split(" : ")[1]
                pginfo_dict["authDate"] = authDate


        #---------- orginfo 저장
        print("orginfo:", orgInfo_dict)
        read_sql = f"""
            SELECT COUNT(*) FROM orginfo WHERE orgName="{orgInfo_dict['orgName']}";
        """
        results = read_table(read_sql)
        result = results[0][0]
        if result == 0:
            insert_sql = """
                INSERT INTO orginfo(orgName, addr) VALUES(
                    '""" + orgInfo_dict['orgName'] + """',
                    '""" + orgInfo_dict['avRegion'] + """'
                )
            """
            insert_table(insert_sql)

        #---------- pginfo 저장
        print("pginfo:", pginfo_dict)
        read_sql = f"""
            SELECT idx, orgName FROM orginfo WHERE orgName='{orgInfo_dict["orgName"]}'
        """
        results = read_table(read_sql)
        orginfo_idx = results[0][0] # 1

        read_sql = f"""
            SELECT COUNT(pgCode) FROM pginfo WHERE pgCode='{pginfo_dict["pgcode"]}'
        """
        results = read_table(read_sql)
        results = results[0][0]
        if results == 0:
            insert_sql = """
                INSERT INTO pginfo(orginfo_idx, pgCode, opMethod, avArea, regDate, avDate, pgName) VALUES(
                    """+str(orginfo_idx)+""",
                    '"""+pginfo_dict["pgcode"]+"""',
                    '"""+pginfo_dict["opMethod"]+"""',
                    '"""+pginfo_dict["avArea"]+"""',
                    '"""+pginfo_dict["regDate"]+"""',
                    '"""+pginfo_dict["avDate"]+"""',
                    '"""+pginfo_dict["pgName"]+"""'
                )
            """
            insert_table(insert_sql)
        else:
            pass

        #---------- pgdetail데이터 수집
        onclick_str = title_info.select_one('a')['onclick'].replace("fnDtl","").replace(";return false;", "")
        eval_onclick = eval(onclick_str)
        # print(eval_onclick)

        detail_pg_url = f"https://www.youth.go.kr/youth/act/actSearch/actSearchDtl.yt?sCrtfc=Y&sCrtfcText=&sSttemntText=&sort=&order=&page=1&rows=10&kCrtfcSn={eval_onclick[1]}&kFcltySn={eval_onclick[0]}&kSnOne={eval_onclick[2]}&kProgrmseCode={eval_onclick[3]}&kSnTwo={eval_onclick[4]}&kSttemntManageNo={eval_onclick[2]}&kSttemntSn=0&kCrtfcAt={eval_onclick[5]}&kSttemntAt={eval_onclick[6]}&kSttemntNo={eval_onclick[7]}&kExclnccrtfcAtchmnflId=&searchDtl=&search=&sActRelmcode=&sActRelmcode1=&sActRelmcode2=&sActRelmcode3=&sActRelmcode4=&sActRelmcode5=&sActRelmcode6=&sActRelmcode7=&sActRelmcode8=&sActRelmcode9=&sActRelmcode10=&sActRelmcode11=&sActRelmcode12=&nas.cmm.token.html.TOKEN=a26774b394cf244c01c2406cf07905ea&sKeyword=&sActCtprvnCode1=&sActSignguCode1=&sActCtprvnCode2=&sActSignguCode2=&sActCtprvnCode3=&sActSignguCode3=&sInsttTyCode=&sInsttTyCode2=&sTrget=&sAge=&stayng=&pc=&acteraDe=on&sActeraBeginDe=&sActeraEndDe=&sCurSearchFlag=Y&sChkSearchFlag=&curMenuSn=1619"
        res = requests.get(detail_pg_url)
        soup = bs(res.content, 'html.parser')


        try:
            table_title_list = []
            table_value_list = []
            table_box = soup.select_one("tbody")
            tr_rows = table_box.select("tr")

            for tr_row in tr_rows:
                list1 = [th.get_text() for th in tr_row.select("span.th-division")]
                list2 = [re.sub("[\r\n\t\xa0 ]","", td.get_text().replace("열기", "")) for td in tr_row.select("td")]
                table_title_list.extend(list1)
                table_value_list.extend(list2)
        except:
            table_title_list = ["지역", "인원 및 연령", "참가비", "숙박여부"]
            table_value_list = ["오류", "9999999명오류", "9999999", "9999999"]


        # print(table_title_list)
        # print(table_value_list)

        pgdetail_dict = {}
        for t, v in zip(table_title_list, table_value_list):
            if t == "지역":
                pgdetail_dict["avRegion"] = v
            if t == "인원 및 연령":
                pgdetail_dict["peopleNum"] = int(v.split("명")[0])
                pgdetail_dict["age"] = v.split("명")[1]
            if t == "참가비":
                price = v.replace(",","").replace("원","")
                if price == "무료":
                    price = "0"
                pgdetail_dict["price"] = int(price)
            if t == "숙박여부":
                pgdetail_dict["sleepOk"] = v

        #---------- pgdetail 저장
        print("pgdetail:", pgdetail_dict)
        print()
        read_sql = f"""
                    SELECT COUNT(pgCode) FROM pgdetail WHERE pgCode='{pginfo_dict["pgcode"]}'
                """
        results = read_table(read_sql)
        results = results[0][0]
        if results == 0:
            insert_sql = """
                INSERT INTO pgdetail(pgCode, avRegion, peopleNum, age, price, sleepOk) VALUES(
                    '"""+pginfo_dict["pgcode"]+"""',
                    '"""+pgdetail_dict["avRegion"]+"""',
                    """+str(pgdetail_dict["peopleNum"])+""",
                    '"""+pgdetail_dict["age"]+"""',
                    """+str(pgdetail_dict["price"])+""",
                    '"""+pgdetail_dict["sleepOk"]+"""'
                )
            """
            insert_table(insert_sql)
        else:
            pass

























