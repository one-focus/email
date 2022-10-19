import json
import logging
import random
import sys
from datetime import datetime
from time import sleep

import requests

s = requests.Session()
s.auth = ('rest_user', sys.argv[1])


def get_users(vc_type):
    sleep(random.uniform(0, 1.5))
    if vc_type == 'Inviting':
        vc_type = ('Inviting', 'Buisness')
    users = s.get(sys.argv[2])
    users = [user for user in json.loads(users.text) if user["vc_type"] in vc_type]
    return users


def get_families_for_dates(users_list, dates_list):
    for date in dates_list:
        for i, user in enumerate(users_list):
            date_from = datetime.strptime(user['date_from'] if user['date_from'] else '01/01/2022', '%d/%m/%Y')
            date_to = datetime.strptime(user['date_to'] if user['date_to'] else '01/01/3000', '%d/%m/%Y')
            actual_date = datetime.strptime(date, '%d.%m.%Y')
            if date_from < actual_date <= date_to:
                users_list[i].setdefault("dates", []).append(date)


def update_status(url, id, status):
    s.post(url=f'{url}/{id}', params={"vc_status": f"{status}"})


def update_fields(url, id, body, file=None):
    s.post(url=f'{url}/{id}', params=body, files={'file': open(file, 'rb')} if file else None)
