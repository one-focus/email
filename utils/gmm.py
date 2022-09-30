import datetime
import imaplib, email
import quopri
import re
import logging

from bs4 import BeautifulSoup


def get_imap(username):
    if any(word in username for word in ('mail.ru', 'internet.ru', 'bk.ru', 'list.ru', 'inbox.ru')):
        return 'imap.mail.ru'


def make_seen(username, password):
    mail = imaplib.IMAP4_SSL(get_imap(username))
    mail.login(username, password)
    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, "UNSEEN")  # (ALL/UNSEEN)
    i = len(data[0].split())  # emails count
    for x in range(i):
        latest_email_uid = data[0].split()[x]
        mail.uid('fetch', latest_email_uid, '(RFC822)')


def find_regex_in_email_with_title(username, password, subj, seen_type="UNSEEN"):
    mail = imaplib.IMAP4_SSL(get_imap(username))
    mail.login(username, password)
    mail.list()
    folders = []
    for i in mail.list()[1]:
        folders.append(i.decode().split(' "/" ')[1].replace('"',''))
    s = []
    for folder in folders:
        mail.select(f'"{folder}"')
        result, data = mail.uid('search', None, seen_type)  # (ALL/UNSEEN)
        i = len(data[0].split())  # emails count
        for x in range(i):
            latest_email_uid = data[0].split()[x]
            result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email_string = email_data[0][1].decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            # Header Details
            date_tuple = email.utils.parsedate_tz(email_message['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
            email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
            email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
            subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
            # Body details
            if subj in subject:
                for part in email_message.walk():
                    logging.warning(subject)
                    if part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True)
                        soup = BeautifulSoup(body.decode('utf-8'), "lxml")
                        s.append(soup)
                        break
                    else:
                        continue
    return s


def clear_mailbox(username, password):
    mail = imaplib.IMAP4_SSL(get_imap(username))
    mail.login(username, password)
    mail.list()
    mail.select('inbox')
    typ, data = mail.search(None, 'ALL')
    for num in data[0].split():
        mail.store(num, '+FLAGS', '\\Deleted')
