import pymysql
from sqlalchemy import create_engine



conn = pymysql.connect(host="localhost", port=3306, user="root", password="123123", db="youth", charset="utf8")
cursor = conn.cursor()



#---------- table 생성
CREATE_SQL1 = """
    CREATE TABLE PROGRAMLIST(
        pgCode VARCHAR(50),
        orgName VARCHAR(100),
        pgName VARCHAR(100),
        price INT,
        target VARCHAR(100),
        regDate VARCHAR(30)
    );
"""
CREATE_SQL2 = """
    CREATE TABLE PROGRAMINFO(
        pgCode VARCHAR(50),
        orgName VARCHAR(100),
        pgName VARCHAR(100),
        price INT,
        target VARCHAR(100),
        mngName Varchar(20),
        email VARCHAR(70),
        tel VARCHAR(20),
        dtInfo TEXT
    );
"""
CREATE_SQL3 = """
    CREATE TABLE DATELIST(
        pgCode VARCHAR(50),
        procNo INT,
        stDate VARCHAR(30),
        edDate VARCHAR(30)
    );
"""


def create_table(sql):
    cursor.execute(sql)
    conn.commit()

def insert_table(sql):
    cursor.execute(sql)
    conn.commit()

def read_table(sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def save_table_info_list(table_name, row_dict, url_columns=None):
    # if table_name=='programlist':
    #     sql = """
    #         INSERT INTO """+table_name+""" VALUES(
    #             '"""+row_dict[url_columns[0]]+"""',
    #             '"""+row_dict[url_columns[1]]+"""',
    #             '"""+row_dict[url_columns[2]]+"""',
    #             """+row_dict[url_columns[3]]+""",
    #             '"""+row_dict[url_columns[4]]+"""',
    #             '"""+row_dict[url_columns[5]]+"""'
    #         )
    #     """
    #     cursor.execute(sql)
    #     conn.commit()
    #
    # elif table_name == 'programinfo':
    # sql = """
    #     INSERT INTO """+table_name+""" values(
    #         '"""+row_dict[url_columns[0]]+"""',
    #         '"""+row_dict[url_columns[1]]+"""',
    #         '"""+row_dict[url_columns[2]]+"""',
    #         """+row_dict[url_columns[3]]+""",
    #         '"""+row_dict[url_columns[4]]+"""',
    #         '"""+row_dict[url_columns[5]]+"""',
    #         '"""+row_dict[url_columns[6]]+"""',
    #         '"""+row_dict[url_columns[7]]+"""',
    #         '"""+row_dict[url_columns[8]]+"""',
    #         '"""+row_dict[url_columns[9]]+"""'
    #     )
    # """
    # cursor.execute(sql)
    # conn.commit()
    #
    # elif table_name == "datelist":
    sql = """
        INSERT INTO """+table_name+""" VALUES(
            '"""+row_dict['pgCode']+"""',
            """+row_dict[url_columns[0]]+""",
            '"""+row_dict[url_columns[1]]+"""',
            '"""+row_dict[url_columns[2]]+"""'
        )
    """
    cursor.execute(sql)
    conn.commit()

