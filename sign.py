import time
import hashlib
import hmac
import urllib.parse


def generate_signature(secret, verb, url, expires, data): 
    parsedURL = urllib.parse.urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query

    if isinstance(data, (bytes, bytearray)):
        data = data.decode('utf8')

    message = bytes(verb + path + str(expires) + data, 'utf-8')
    print("Computing HMAC: %s" % message)

    signature = hmac.new(bytes(secret, 'utf-8'), message, digestmod=hashlib.sha256).hexdigest()
    print("Signature: %s" % signature)
    return signature

# set to 2024/12/13 12:00:00 UTC +8
expires = 1702440000
data = '{"symbol":"SOLUSDT","price":67.3,"clOrdID":"102","orderQty":100000}'
# data = '{"symbol":"SOLUSDT","side":"Sell","orderQty":1000,"ordType":"Market"}'
print(generate_signature('', 'POST', '/api/v1/order', expires, data)) 
