import email, imaplib, os
from getpass import getpass

# User information
username = 'web2mail@dweblabs.com'
password = getpass()

# Connect to GMail via IMAP
mail = imaplib.IMAP4_SSL('imap.gmail.com')
print 'Logging in...',
conn = mail.login(username, password)
if conn[0] == 'OK':
	print 'Connected!'
else:
	print 'Error!'
	exit
mail.select()
items = mail.search(None, 'UnSeen')
print items[1][0].split()

#for emailID in items:
	#resp, data = mail.fetch(emailID, '(RFC822)')
	#print data

