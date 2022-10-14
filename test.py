import re

from bs4 import BeautifulSoup
from seleniumwire import webdriver

from utils import gmm, gsheets

gs = gsheets.GoogleSheets('germany')
all_emails = gs.ws.get_all_values()

links = []

for email in all_emails[1:]:
    username = email[1]
    password = email[2]
    soup = gmm.find_regex_in_email_with_title(username, password, 'Terminvereinbarung', "SEEN")
    for s in soup:
        element = s.find("a", href=lambda href: href and "https://service2.diplo.de/rktermin/extern/confirmation_appointment.do?" in href)
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(element['href'].replace('&amp;', '&').replace('request_locale=de', 'request_locale=ru'))
        ps = BeautifulSoup(driver.page_source, "lxml")
        if confirmation := ps.find('fieldset'):
            try:
                confirmation = ' '.join(ps.find('fieldset').text.split())
                time = re.findall('время:(.*?)Место', confirmation)[0].strip()
                passport = re.findall('Visumbewerbers :(.*?)Grund', confirmation)[0].strip()
                surname = re.findall('Фамилия:(.*?)Электронная почта:', confirmation)[0].strip().replace('Имя: ', '')
                print(f'{time}: {surname} | {passport} | {email[1]}')
                links.append(f'{time}: {surname} | {passport} | {email[1]}')
            except Exception:
                pass

for link in links:
    print(link)

# for i, email in enumerate(all_emails):
#     try:
#         gmm.clear_mailbox(email[1], email[2])
#         print(i)
#     except Exception as e:
#         print(f'Email: {email[1]}. Ошибка: {str(e)}')

# soup = gmm.find_regex_in_email_with_title(username, password, 'Terminvereinbarung', "SEEN")
# for s in soup:
#     print(str(soup).replace('&amp;', '&').replace('request_locale=de', 'request_locale=ru'))
