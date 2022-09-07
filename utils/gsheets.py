import json
import os

import gspread
from google.oauth2.service_account import Credentials


class GoogleSheets:
    gs_key_file = os.path.abspath(os.curdir) + "/gsheet_email_key.json"
    data_columns = {'id': 'A',
                    'email': 'B',
                    'password': 'C',
                    'germany': 'D',
                    'kaliningrad': 'E'}

    def __init__(self, name):
        self.ws = self.authorize(name)

    def authorize(self, work_sheet):
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        if not os.path.isfile(self.gs_key_file):
            config_file = os.path.abspath(os.curdir) + "/config.json"
            with open(config_file) as json_file:
                data = json.load(json_file)['email_key']
            with open(self.gs_key_file, 'w') as fp:
                json.dump(data, fp)
        creds = Credentials.from_service_account_file(self.gs_key_file, scopes=scope)
        gs = gspread.authorize(creds).open_by_key('1aYR6tN9BygDJLOVmKkXKAxDkJtxuH1nh6J6pjmHPBNo')
        return gs.worksheet(work_sheet)

    def find_item_by_id(self, visa_item_id):
        cell = self.ws.row_values(visa_item_id + 1)
        return cell

    def update_visa_item_by_id(self, id, column, value):
        self.ws.update_acell("{}{}".format(self.data_columns[column], int(id) + 1), value)
