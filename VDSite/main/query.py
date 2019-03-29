import requests
from main.models import Query_Result
from django.core.exceptions import ObjectDoesNotExist
import time

API_KEY = "a5a6312eb7a4dd14fb1dfb145aa1ec654beacc0f36c67fc6b98b109b0c3bf5b0"
QUERY_URL = "https://www.virustotal.com/vtapi/v2/file/report"
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

def sendQuery(f, mode='test'):
    count = 0
    res_list = []
    for line in f:
        count += 1
        if mode == 'test' and count >= 5:
            break
        hash = line.decode("utf-8").replace('\n', '')

        try:
            res = Query_Result.objects.get(hash=hash)
            print("{} exists in databse\n".format(hash))
        except ObjectDoesNotExist:
            # Sleep 20 seconds the meet the  restriction of public API (4 per min)
            time.sleep(20)
            params = {'apikey': API_KEY, 'resource':hash}
            res = Query_Result()
            res.hash = hash
            r = requests.get(QUERY_URL, params=params, headers=headers)
            r = r.json()
            fortinet_key_chain = ["scans", "Fortinet", "result"]
            res.fortinet = getOrDefault(r, fortinet_key_chain)
            res.date = getOrDefault(r, ["scan_date"])
            res.positive = getOrDefault(r, ["positives"])
            # save in cached database
            res.save()

        res_list.append({'hash': res.hash, 'fortinet': res.fortinet, 'positive': res.positive, 'date': res.date})
    return res_list

def getOrDefault(jsonObj, key_chain, default_value=None):
    if len(key_chain) == 1:
        return default_value if key_chain[0] not in jsonObj else jsonObj[key_chain[0]]

    return default_value if key_chain[0] not in jsonObj else getOrDefault(jsonObj[key_chain[0]], key_chain[1:])
