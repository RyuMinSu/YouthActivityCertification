from youth.expactor.youthdata import get_data

file = open('../service_key.txt', 'r')
service_key = file.readline()
file.close()

#----------1st step
LIST_URL = f"http://apis.data.go.kr/1383000/YouthActivInfoCertiSrvc2/getCertiProgrmList?pageNo=1&numOfRows=10000&type=xml&serviceKey={service_key}"
list_columns = ["nums", "organnm", "pgmnm", "price", "target", "sdate"]

#데이터 가져오기 및 저장
get_data(LIST_URL, "programlist", list_columns)#list

