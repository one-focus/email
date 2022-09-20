import logging
import re
from multiprocessing import Pool
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

from utils import gsheets, gmm, telegram


if __name__ == "__main__":
    while True:
        try:
            gs = gsheets.GoogleSheets('germany')
            emails = gs.ws.get_all_values()
            emails = [email for email in emails if email[5] == '1']
            for e in emails:
                errors = []
                for _ in range(5):
                    try:
                        logging.warning(e)
                        soup = gmm.find_regex_in_email_with_title(e[1], e[2], 'Terminvereinbarung')
                        for s in soup:
                            logging.warning(soup)
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
                            gs.ws.update_acell(f'F{int(e[0])+1}', int(e[5])-1)
                        break
                    except Exception as ex:
                        errors.append(str(ex))
                        telegram.send_message(f'Email error: {str(ex)}')
                        sleep(1)
                else:
                    telegram.send_message(f'🔴💌 Германия ошибка проверки почты({e[1]}): {errors}')
                sleep(1)
        except Exception as ex:
            telegram.send_message(f'Ошибка проверки почты: {str(ex)}')
        sleep(30)
        logging.warning('---')