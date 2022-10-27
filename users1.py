import sys
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

from utils import gsheets, users, gmm


# gs = gsheets.GoogleSheets('germany')
# all_emails = gs.ws.get_all_values()

# us = users.get_users('Inviting') + users.get_users('Tourism')
#
# user = [user for user in us if 'thomtheceahernfwen5841@mail.ru' in user['vc_comment']]
# if user:
#     user_id = user[0]['id']
#     family = [user for user in us if user['vc_with'] == '160']
#     user = user + family
#
# print()


for u in ('507', '506', '505', '498', '473'):
    users.update_fields(url=f'{sys.argv[2]}', id=u, body={'vc_status': '2'})
# users.update_fields(url=f'{sys.argv[2]}', id='72', body={'vc_comment': f'FAKE|thomtheceahernfwen5841@mail.ru|'})

# us = [u for u in us if '|' in u['vc_comment']]
#
#
# for user in us:
#     email = user["vc_comment"].split("|")[1]
#     users.update_fields(url=f'{sys.argv[2]}', id=user['id'], body={'vc_comment': f'{user["vc_comment"].replace(f"|{email}|", "")}'})
