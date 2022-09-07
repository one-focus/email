import re
from multiprocessing import Pool
from time import sleep

from bs4 import BeautifulSoup
from seleniumwire import webdriver

from utils import gsheets, gmm, telegram


if __name__ == "__main__":
    while True:
        try:
            gs = gsheets.GoogleSheets('germany')
            emails = gs.ws.get_all_values()[2:]
            for e in emails:
                try:
                    print(e)
                    soup = gmm.find_regex_in_email_with_title(e[1], e[2], 'Terminvereinbarung')
                    for s in soup:
                        print(soup)
                        element = s.find("a", href=lambda
                            href: href and "https://service2.diplo.de/rktermin/extern/confirmation_appointment.do?" in href)
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
                                telegram.send_doc(f'🟩💌 Германия подтвержден email({e[1]}):\nВремя: {time}\nПаспорт: {passport}', str(ps))
                            except Exception as ex:
                                telegram.send_doc(f'🟩💌 Германия подтвержден email({e[1]}):\nОшибка: {str(e)}', str(ps))
                        else:
                            telegram.send_doc(f'🔴💌 Германия НЕ подтвержден email({e[1]})', str(ps))
                except Exception as ex:
                    telegram.send_message(f'🔴💌 Германия ошибка проверки почты({e[1]}): {str(ex)}')
                sleep(1)
        except Exception as ex:
            telegram.send_message(f'Ошибка проверки почты: {str(ex)}')