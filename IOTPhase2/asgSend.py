import smtplib, ssl

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

print('asd')

SENDER = "seconddummytwo@gmail.com"
RECEIVER = "seconddummytwo@gmail.com" #"templatebuttondown@gmail.com"

server.login(SENDER, "sfpk znqg ixfo qzak")

message = "Hello world 2."

print('sending')

s.sendmail(SENDER, RECEIVER, message)
s.quit()

print("sent")