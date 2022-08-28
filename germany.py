import imaplib, email

from utils import gsheets, gmm
from utils.gmm import Email

gs = gsheets.GoogleSheets('mail_ru')

emails_with_passwords = [item for item in gs.ws.get_all_values() if item[2]]
emails_with_passwords.pop(0)


username = 'visa.automation@mail.ru'
password = 'v4fGvZquiJsXDAudh93H'
text = Email().find_regex_in_email_with_title(username, password, "Полезные сервисы Mail.ru", 'https://mailer.mail.ru/pub/mailer/click/12536/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsZXR0ZXJfaWQiOjEyNTM2LCJ0ZXN0aW5nIjowLCJwb3N0X3R5cGUiOiJDIiwiZW1haWwiOiJ2aXNhLmF1dG9tYXRpb25AbWFpbC5ydSIsInBvc3RfaWQiOjIyNCwic2VuZF91dWlkIjoiN2M1ZDNlNGMtYTczMi00YWY3LWI1NzktMGUzZWQwNmFhYzc5IiwibGFuZ3VhZ2UiOiJydSIsInVybF9pZCI6MjE0MzExLCJ1cmwiOiJodHRwczovL2hlbHAubWFpbC5ydS9jYWxlbmRhci1oZWxwL2Fib3V0P3V0bV9zb3VyY2U9Z21haWxlcl9ta3QmdXRtX21lZGl1bT1lbWFpbCZ1dG1fY2FtcGFpZ249d2VsY29tZV9lbWFpbF85JnV0bV90ZXJtPWNhbGVuZGFyIn0.P2_snVaGF7FEdXtdbXWDVqCTceZf06vNGeaFgpQPdh0?mlr-mailru-auth=1')

print()
# зайти на почту, проверить есть ли новые письма
# зайти в новое письмо и открыть ссылку
# решить капчу и законфирмить
# отправить в телеграм страницу успешной реги