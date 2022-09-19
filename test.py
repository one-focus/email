from utils import gmm, gsheets

gs = gsheets.GoogleSheets('germany')
all_emails = gs.ws.get_all_values()

all_emails = [email for email in all_emails if email[1] == '0']

for i, email in enumerate(all_emails):
    try:
        gmm.clear_mailbox(email[1], email[2])
        print(i)
    except Exception as e:
        print(f'Email: {email[1]}. Ошибка: {str(e)}')

soup = gmm.find_regex_in_email_with_title('kkrisrtina@mail.ru', '48LF91B46s9hZCSgZZ8A', 'Terminvereinbarung')
for s in soup:
    print(soup)

