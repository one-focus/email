from utils import gmm, gsheets

gs = gsheets.GoogleSheets('germany')
all_emails = gs.ws.get_all_values()

username = 'gaiclersurcyto7740@mail.ru'
password = [email for email in all_emails if email[1] == username][0][2]

# for i, email in enumerate(all_emails):
#     try:
#         gmm.clear_mailbox(email[1], email[2])
#         print(i)
#     except Exception as e:
#         print(f'Email: {email[1]}. Ошибка: {str(e)}')

soup = gmm.find_regex_in_email_with_title(username, password, 'Terminvereinbarung', "SEEN")
for s in soup:
    print(str(soup).replace('&amp;', '&').replace('request_locale=de', 'request_locale=ru'))
