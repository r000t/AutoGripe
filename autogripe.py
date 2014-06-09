#!/usr/bin/python

## Configure AutoGripe Here

#SMTP Server Settings
#These are preset for Gmail TLS
smtpserver = 'smtp.gmail.com'
smtpport = 587

#Google Apps users:The first two fields need your full address
#I recommend making a user just for fail2ban, for security.
smtpusername = 'username'
smtpemailaddress = 'username@gmail.com'
smtppassword = 'password'

try:
	from querycontacts import ContactFinder
except:
	print 'A querycontacts.py was included with AutoGripe'
	print 'Put it in the same folder as this script.'
	print 'Need a copy? https://github.com/r000t/AutoGripe'
	exit()

import smtplib

def getloglines(address, logpath, failures=10):
	#gets log lines. eventually.
	log = open(logpath)
	listloglines = []
	for line in log:
		if ' ' + address + ' ' in line:
			listloglines.append(line)
	stringloglines = ''
	for relevantline in listloglines[-failures:]:
		stringloglines = stringloglines + relevantline
	
	return stringloglines		

def sendemail(ipaddress, recipient, loglinesm, session):
	headers = "\r\n".join(["from: " + smtpemailaddress,
                       "subject: " + 'Abuse from ' + ipaddress,
                       "to: " + recipient,
                       "mime-version: 1.0",
                       "content-type: text/plain"])

	message_body = '''To whomever it may concern, 
	
We have detected abuse from the IP address %s. According to the WHOIS
records for that IP address, this is the proper abuse address for it. 

The above listed host appears to be trying to brute force our server. It would
be greatly appreciated if you would look into this matter and take appropriate
action to stop the abuse. 

We've included log lines related to the incident. Feel free to reply to this
email if you require more information. 

%s

Thank you in advance for looking into this matter. 

--Fail2Ban

Note: This email was automatically generated by Fail2Ban''' % (ipaddress, loglines)

	session.sendmail(smtpemailaddress, recipient, headers + "\r\n\r\n" + message_body.replace('\n','\r\n')

def processaddress(thisip, logpath):
	emailist = ContactFinder().find(thisip)
	if len(emailist) != 0:
		session = smtplib.SMTP(smtpserver, smtpport)
		session.ehlo()
		session.starttls()
		session.login(smtpusername, smtppassword)
		for address in emailist:
			sendemail(thisip, address, getloglines(thisip, logpath), session)
	else:
		print 'No abuse addresses found.'
		exit()

if __name__ == "__main__":
	import sys
	thisip = sys.argv[1]
	logpath = sys.argv[2]
	
	processaddress(thisip, logpath)
	