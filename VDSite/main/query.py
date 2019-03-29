import requests
from main.models import Query_Result
from django.core.exceptions import ObjectDoesNotExist


API_KEY = "a5a6312eb7a4dd14fb1dfb145aa1ec654beacc0f36c67fc6b98b109b0c3bf5b0"
QUERY_URL = "https://www.virustotal.com/vtapi/v2/file/report"

def sendQuery(f):
    count = 0
    res_list = []
    for line in f:
        hash = line.decode("utf-8").replace('\n', '')

        try:
            res = Query_Result.objects.get(hash=hash)
            print("{} exists in databse\n".format(hash))
        except ObjectDoesNotExist:
            params = {'apikey': API_KEY, 'resource':hash}
            res = Query_Result(hash=hash)
            try:
                r = requests.get(QUERY_URL, params=params)
                print(r.text)
                r = r.json()

                fortinet_key_chain = ['scans', 'Fortinet', 'result']
                res.fortinet = getOrDefault(r, fortinet_key_chain)
                res.date = getOrDefault(r, ['scan_date'])
                res.positive = getOrDefault(r, ['positives'])
                # save in cached database.
                res.save()
            except Exception as e:
                print(e)
                print('Cannot resolve query from {}\n'.format(hash))
        res_list.append({'hash': res.hash, 'fortinet': res.fortinet, 'positive': res.positive, 'date': res.date})
        count += 1
        if count >= 10:
            break
    return res_list

def getOrDefault(jsonObj, key_chain, default_value=None):
    if len(key_chain) == 1:
        return default_value if key_chain[0] not in jsonObj else jsonObj[key_chain[0]]

    return default_value if key_chain[0] not in jsonObj else getOrDefault(jsonObj[key_chain[0]], key_chain[1:], default_value)
