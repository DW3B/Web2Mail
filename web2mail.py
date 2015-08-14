#!/usr/bin/python

# Web2Mail - A simple web 'proxy' using email. This script will 
# check the inbox of an email address that you have the credentials
# to for new messages with a certain subject line. By default, this
# is 'Proxy This!'. It will then look for URLs in the body of the 
# message, scrape the contents of each of them, save the contents as
# individual .html files, and finally send them back to you.
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# 
# Author: DW3B
# Email: dweb@dw3b.io 
# Version 1.0
# Date: 2015-08-13

import argparse, urllib2, imaplib, threading, email, sys, re
from pymail import PyMail

mail_defaults = {
	'outlook.com': ('imap-mail.outlook.com', 'smtp-mail.outlook.com'),
	'hotmail.com': ('imap-mail.outlook.com', 'smtp-mail.outlook.com'),
	'live.com': ('imap-mail.outlook.com', 'smtp-mail.outlook.com'),
	'gmail.com': ('imap.gmail.com', 'smtp.gmail.com'),
	'yahoo.com': ('imap.mail.yahoo.com', 'smtp.mail.gmail.com')
}

def parse_mail(messages, m):
	for msg in messages:
		try:
			sender, subject, body = m.get_mail_by_id(msg)
			if subject == 'Proxy This!' and re.match(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/', body.rstrip()):
				m.respond(m.get_mail_by_id(msg), 'Would have sent the static resources back!')
				return
		except:
			continue

def main():
	example = "Examples: \n\n./web2mail.py -u user@email.com -p password\n./web2mail.py -u user@email.com -p password -s imap.email.com --use-ssl"
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Web2Mail - A simple web 'proxy' using email by DW3B", epilog=example)
	required = parser.add_argument_group("Required")
	required.add_argument('-u', '--username', required=True, help='Full Email Address')
	required.add_argument('-p', '--password', required=True, help='Email Password')
	custom = parser.add_argument_group("Custom")
	custom.add_argument('-i', '--imap-server', help='IMAP Host Name')
	custom.add_argument('-s', '--smtp-server', help='SMTP Host Name')
	custom.add_argument('--use-ssl', default=True, help='Use SSL for IMAP and SMTP')
	args = parser.parse_args()
	
	print '\n ' + '-' * 69 + '\n ' + ' Web2Mail v1.1 by DW3B\n ' + '-' * 69 + '\n '
	
	# Check for valid email address
	addr_check = re.match(r'\A.+@(.+\..{2,})', args.username)
	if not addr_check:
		print '[!] Please provide a valid email address\n'
		return
		
	if args.imap_server and args.smtp_server:
		imap_server = args.imap_server
		smtp_server = args.smtp_server
	else:
		imap_server = mail_defaults[addr_check.group(1)][0]
		smtp_server = mail_defaults[addr_check.group(1)][1]
	m = PyMail(imap_server, smtp_server, args.username, args.password, ssl=args.use_ssl)		
	print ' IMAP SERVER:\t%s\n SMTP SERVER:\t%s\n USERNAME:\t%s\n' % (imap_server, smtp_server, args.username)
	
	m.login()
	unread = m.get_unread_mail()
	if len(unread) > 0:
		parse_mail(unread, m)
	else:
		return
	
if __name__ == '__main__':
	try:
		main()
	except KeyBoardInterrupt:
		sys.exit()