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
    return signature

# set to 2024/12/13 12:00:00 UTC +8
expires = 1702440000
data = '{"symbol":"SOLUSDT","price":66.5,"clOrdID":"40","orderQty":10000}'
print(generate_signature('5ZnLrIFAA58JIlO3aJ4M8HOvPhqc5OJ3d2VWmIqAjZgL44Nf', 'POST', '/api/v1/order', expires, data)) #