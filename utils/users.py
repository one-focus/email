import json
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
    return users  # test users [{'id': '1', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'sash.kardash@gmail.com', 'vc_inviting': 'Grigory Fray', 'vc_passport': 'MP8338818', 'vc_birth': '1965-10-16', 'vc_passport_from': '2021-07-20', 'vc_passport_to': '2031-07-20', 'vc_passport_by': 'MIA', 'vc_name': 'Valery', 'vc_surname': 'Vetlitcky', 'vc_phone': '+375256062209', 'vc_date_first_travel': '2022-08-15', 'vc_date_from': '2022-07-24', 'vc_date_to': '', 'vc_with': '0', 'vc_comment': '', 'vc_first': '1', 'vc_today': '1', 'vc_before_visit': '0'}, {'id': '3', 'vc_status': '2', 'vc_city': 'Schengenvisa', 'vc_type': 'Inviting', 'vc_mail': 'sash.kardash@gmail.com', 'vc_inviting': 'Grigory Fray', 'vc_passport': 'MP8338818', 'vc_birth': '1965-10-16', 'vc_passport_from': '2021-07-20', 'vc_passport_to': '2031-07-20', 'vc_passport_by': 'MIA', 'vc_name': 'Valery', 'vc_surname': 'Vetlitcky', 'vc_phone': '+375256062209', 'vc_date_first_travel': '2022-08-15', 'vc_date_from': '2022-07-24', 'vc_date_to': '', 'vc_with': '0', 'vc_comment': '', 'vc_first': '1', 'vc_today': '1', 'vc_before_visit': '0'}]


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


def update_fields(url, id, body):
    s.post(url=f'{url}/{id}', params=body)
