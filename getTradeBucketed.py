import requests
import json

def getPrice():
    url = "https://www.bitmex.com/api/v1/trade/bucketed"

    params = {
        "binSize": "1m",         # 時間間隔
        "partial": "false",      
        "symbol": "SOLUSDT",     # 標的資產
        "count": 1,            
        "reverse": "true"        
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # 提取並打印 open 值
        if data:  # 確保數據不是空的
            open_price = data[0]["open"]
            high = data[0]["high"]
            low = data[0]["low"]
            avg = (high + low) / 2
            print("Data returned:", data)
            return round(avg, 2)
        else:
            print("No data returned")
    else:
        print("Error:", response.status_code)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else", err)

print(getPrice())
