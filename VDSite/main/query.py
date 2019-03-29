import requests
from main.models import Query_Result
from django.core.cache import cache
import time

API_KEY = "a5a6312eb7a4dd14fb1dfb145aa1ec654beacc0f36c67fc6b98b109b0c3bf5b0"
QUERY_URL = "https://www.virustotal.com/vtapi/v2/file/report"
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

def query_hash(hash):
    res = cache.get(hash)
    if res:
        print("{} exists in Caches\n".format(hash))
    else:
        # Sleep 20 seconds to meet the restriction of public API (4 requests per min)
        time.sleep(20)
        params = {'apikey': API_KEY, 'resource': hash}
        res = Query_Result()
        res.hash = hash
        r = requests.get(QUERY_URL, params=params, headers=headers)
        r = r.json()
        fortinet_key_chain = ["scans", "Fortinet", "result"]
        res.fortinet = get_or_default(r, fortinet_key_chain)
        res.date = get_or_default(r, ["scan_date"])
        res.positive = get_or_default(r, ["positives"])
        # save in cached database
        cache.set(hash, res)
    return res


# Function to recursively read json object
def get_or_default(jsonObj, key_chain, default_value=None):
    if len(key_chain) == 1:
        return default_value if key_chain[0] not in jsonObj else jsonObj[key_chain[0]]

    return default_value if key_chain[0] not in jsonObj else get_or_default(jsonObj[key_chain[0]], key_chain[1:])
