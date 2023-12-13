import requests
import time
import random
import json
from sign import generate_signature
import getTradeBucketed

# API config
api_key = ""
api_secret = ""
base_url = "https://www.bitmex.com"
endpoint = "/api/v1/order"

def place_order(symbol, side, quantity, price, ordID):
    expires = 1702440000
    # data = '{"symbol":"'+symbol+'","side":"'+side+'","ordType":'+"Market"+',"orderQty":"'+str(quantity)+'"}'
    data = '{"symbol":"'+symbol+'","price":"'+str(price)+'","clOrdID":'+str(ordID)+',"orderQty":"'+str(quantity)+'"}'
    # data = json.dumps(params)
    signature = generate_signature(api_secret, "POST", endpoint, expires, data)

    headers = {
        "api-expires": str(expires),
        "api-key": api_key,
        "api-signature": signature,
        "Content-Type": "application/json"
    }

    response = requests.post(base_url + endpoint, headers=headers, data=data)
    return response

# Trading config
symbol = "SOLUSDT"
quantity = 3000  # 交易數量，根據您的需要調整
ordIDCount = 222220000

while True:
    ordIDCount += 1
    avg = getTradeBucketed.getPrice()

    # if close > avg:
    #     side = "Sell"
    # elif close < avg:
    #     side = "Buy"
    # else:
    #     side = "None"
    #     time.sleep(10)
    #     continue
    
    # if side == "Buy":
    #     order_response = place_order(symbol, side, quantity, avg - 0.1, ordIDCount)
    # elif side == "Sell":
    #     order_response = place_order(symbol, side, 0 - quantity, avg + 0.1, ordIDCount)
    side = "Buy"
    order_response = place_order(symbol, side, quantity, avg - 0.01, ordIDCount)
    if order_response.status_code == 200:
        print(f"Success: {side}")
    else:
        print(f"Fali: {order_response.text}")

    ordIDCount += 1
    side = "Sell"
    order_response = place_order(symbol, side, 0 - quantity, avg + 0.01, ordIDCount)
    
    if order_response.status_code == 200:
        print(f"Success: {side}")
    else:
        print(f"Fali: {order_response.text}")

    # 等待10秒
    time.sleep(10)


