#!usr/bin/python

# PyMail - A module built for Web2Mail in order to simplify interaction
# with the impalib and smtplib libraries.
# Copyright (C) 2015  DW3B
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email: dweb@dw3b.io 
# Version 1.1
# Date: 2015-08-14

import imaplib, smtplib, email, urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class PyMail:
	def __init__(self, imap, smtp, username, password, ssl=True):
		self.IMAP_SERVER = imap
		self.SMTP_SERVER = smtp
		if ssl:
			self.IMAP_PORT = 993
			self.SMTP_PORT = 587
		else:
			self.IMAP_PORT = 143
			self.SMTP_PORT = 25
		self.USERNAME = username
		self.PASSWORD = password
		self.M = None
		self.response = None

	def login(self):
		if self.IMAP_PORT == 993:
			self.M = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
		else:
			self.M = imaplib.IMAP4(self.IMAP_SERVER, self.IMAP_PORT)
		rc, self.response = self.M.login(self.USERNAME, self.PASSWORD)
		self.M.select('INBOX')
		return rc

	def logout(self):
		self.M.logout()
	
	def get_unread_mail(self, folder):
		rc, messages = self.M.search(None, 'UnSeen')
		return messages[0].split()

	def get_mail_by_id(self, mailID):
		status, resp = self.M.fetch(mailID, '(RFC822)')
		for respPart in resp:
			if isinstance(respPart, tuple):
				msg = email.message_from_string(respPart[1])
				sender = msg['from']
				subject = msg['subject']
				body = msg.get_payload()[0].get_payload()
		return sender, subject, body

	def respond(self, msg, response):
		reply = MIMEMultipart('alternative')
		reply['To'] = msg['from']
		reply['From'] = self.USERNAME
		reply['Subject'] = 'Re: %' % msg['subject']
		reply.attach(MIMEText(response, 'html'))
		if ssl:
			s = smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT)
		else:
			s = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(self.USERNAME, self.PASSWORD)
		s.sendmail(self.USERNAME, toaddr, reply.as_string())
		s.close()
