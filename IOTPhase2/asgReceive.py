import imaplib
import email

mail = imaplib.IMAP4_SSL('imap.gmail.com')

ID = "seconddummytwo@gmail.com"
KEY = "sfpk znqg ixfo qzak"
mail.login(ID, KEY)
mail.list()

mail.select("inbox")
result, data = mail.search(None, "ALL")

print('splitting')

ids = data[0]
id_list = ids.split()
latest_email_id = id_list[-1]

print('fetching....')

result, data = mail.fetch(latest_email_id, "(RFC822)")

raw_email = data[0][1]
msg = email.message_from_bytes(raw_email)

FROM = msg['From']
BODY = msg.get_payload(decode=True)
#BODY = mail.fetch(latest_email_id, "(UID BODY[TEXT])")

print('Sender: ', FROM)
print('BODY: ', BODY)