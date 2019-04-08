import requests
from main.models import Query_Result
from django.core.cache import cache
import time

API_KEY = "YOUR_API_KEY"
QUERY_URL = "https://www.virustotal.com/vtapi/v2/file/report"
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

def query_hash(hash, mode='test'):
    """query a hash value provided

    :param hash: the hash value to query
    :return: a Query_Result object
    """
    res = cache.get(hash)
    if res:
        print("{} exists in Caches\n".format(hash))
    else:
        ## Sleep 15 seconds to meet the restriction of public API
        # # If you scan for more than 4 files with a public API, uncomment the following
        #
        # if mode == 'test':
        #     time.sleep(15)

        params = {'apikey': API_KEY, 'resource': hash}
        res = Query_Result()
        res.hash = hash
        r = requests.get(QUERY_URL, params=params, headers=headers)
        r = r.json()

        fortinet_key_chain = ["scans", "Fortinet", "result"]
        res.fortinet = get_or_default(r, fortinet_key_chain)
        res.date = get_or_default(r, ["scan_date"])
        res.positive = get_or_default(r, ["positives"])

        cache.set(hash, res)  # save in cached database
    return res


def get_or_default(jsonObj, key_chain, default_value=None):
    """Recursively read json object

    :param jsonObj: json object to read
    :param key_chain: a list of keys ordered by the 'get' sequence
    :param default_value:  default value to return if a key error raises
    :return: value read from json object
    """
    if len(key_chain) == 1:
        return default_value if key_chain[0] not in jsonObj else jsonObj[key_chain[0]]

    return default_value if key_chain[0] not in jsonObj else get_or_default(jsonObj[key_chain[0]], key_chain[1:])
