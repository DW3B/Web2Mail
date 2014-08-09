import imaplib, smtplib, email, urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass


class PyGmail:
	def __init__(self):
		self.IMAP_SERVER = 'imap.gmail.com'
		self.SMTP_SERVER = 'smtp.gmail.com'
		self.SMTP_PORT = '587'
		self.M = None
		self.response = None

	def login(self, username, password):
		self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER)
		rc, self.response = self.M.login(username, password)
		return rc

	def logout(self):
		self.M.logout()
	
	def get_unread_mail(self, folder):
		self.M.select(folder)
		rc, messages = self.M.search(None, 'UnSeen')
		return messages[0].split()

	def get_mail_by_id(self, mailID):
		status, resp = self.M.fetch(mailID, '(RFC822)')
		for respPart in resp:
			if isinstance(respPart, tuple):
				msg = email.message_from_string(respPart[1])
				sender = msg['from']
				subject = msg['subject']
				body = msg['body']
		return sender, subject, body

	def respond(self, toaddr, subj, body, fromaddr, pwd):
		msg = MIMEMultipart('alternative')
		msg['To'] = toaddr
		msg['From'] = fromaddr
		msg['Subject'] = subj
		msg.attach(MIMEText(body, 'html'))
		s = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(fromaddr, pwd)
		s.sendmail(fromaddr, toaddr, msg.as_string())
		s.close()
		
username = 'websterusaf@gmail.com'
password = getpass()

g = PyGmail()
g.login(username, password)

while True:
	unreadMails = g.get_unread_mail('Inbox')
	if len(unreadMails) == 0:
		pass	
	for mail in unreadMails:
		g.get_mail_by_id(mail)

	#mailMsg = unreadMails[0]
	#g.get_mail_by_id(mailMsg)
	#else:
		#mailMsg = unreadMails[0]
		#sender, subject, body = g.get_mail_by_id(mailMsg)
		#try:			
		#	respBody = str(urllib.urlopen(subject).read())
		#	respSubject = 'Valid Site Response'
		#except:
		#	respBody = "Could not find anything at '%s'" % subject
		#	respSubject = 'Invalid Site Response'
		#g.respond(sender, respSubject, respBody, username, password)


