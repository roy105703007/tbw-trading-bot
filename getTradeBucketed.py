import requests
import json

url = "https://www.bitmex.com/api/v1/trade/bucketed"

params = {
    "binSize": "5m",         # 時間間隔
    "partial": "false",      
    "symbol": "SOLUSDT",     # 標的資產
    "count": 100,            
    "reverse": "true"        
}

# 發送 GET 請求
response = requests.get(url, params=params)

# 檢查響應狀態
if response.status_code == 200:
    # 解析並打印響應內容
    data = response.json()
    print(json.dumps(data, indent=4))
else:
    print("Error:", response.status_code)

# 處理錯誤和異常
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as errh:
    print ("Http Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print ("OOps: Something Else", err)
