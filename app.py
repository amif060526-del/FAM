
import requests
 
# 使用者輸入
stock_no = input("請輸入股票代號（例如 2330）：")
#date = input("請輸入查詢年月（格式：YYYYMMDD，例如 20260301）：")
 
# API URL
url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={stock_no}"
 
# 發送請求
res = requests.get(url)
data = res.json()
 
# 判斷是否成功
if data["stat"] == "OK":
    print( data["title"])
    print( data["fields"])
    print("資料：")
    for row in data["data"]:
        print(row)
else:
    print("查無資料，請確認股票代號或日期")
