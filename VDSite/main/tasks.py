from smtplib import SMTPException
from main.query import query_hash
from VDSite.settings import EMAIL_FROM
from django.core.mail import send_mail


def send_notification(email):
    """Send email notifications to the email address provided

    :param email: email address to send to
    :return:
    :raises: SMTPException if an error occurs during send_mail()
    """
    email_title = 'Your Malware Detection is Completed'
    email_body = 'FYI'
    try:
        if email_check_valid(email):
            return_code = send_mail(email_title, email_body, EMAIL_FROM, [email])
            print(return_code)
    except SMTPException:
        print("Error Occured When Sending Notification ")


def send_query(f, mode='test'):
    """Send query with the HD5 set provided

    :param f: file object of the HD5 set
    :param mode: only up to 5 hashes would be sent to query if set to 'test'
    :return: a list of query result in a form of dictionary
    """
    count = 0
    res_list = []
    for line in f:
        count += 1
        if mode == 'test' and count >= 5:
            break
        hash = line.decode("utf-8").replace('\n', '')

        res = query_hash(hash)
        res_list.append({'hash': res.hash, 'fortinet': res.fortinet, 'positive': res.positive, 'date': res.date})
    return res_list


def email_check_valid(email):
    # TODO
    return True