from main.query import query_hash
from VDSite.settings import EMAIL_FROM
from django.core.mail import send_mail


def send_notification(email):
    email_title = 'Your Malware Detection is Completed'
    email_body = 'FYI'
    try:
        if email_check_valid(email):
            return_code = send_mail(email_title, email_body, EMAIL_FROM, [email])
            print(return_code)
    except:
        print("Error Occured When Sending Notification ")


def send_query(f, mode='test'):
    count = 0
    res_list = []
    for line in f:
        count += 1
        if mode == 'test' and count >= 5: # in test mode, take first 5 inputs
            break
        hash = line.decode("utf-8").replace('\n', '')

        res = query_hash(hash)
        res_list.append({'hash': res.hash, 'fortinet': res.fortinet, 'positive': res.positive, 'date': res.date})
    return res_list


def email_check_valid(email):
    # TODO
    return True