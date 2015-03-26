#!/usr/bin/python
# coding=utf-8
# Parsing Estimated Cost from AWS
# Created by Ming Wu <neowym@gmail.com>, 2014/08/22

import re
import sys
import datetime
import subprocess

DEBUG = 0
AWS_CW_HOME = '/Path/To/CloudWatch-1.0.20.0'
AWS_CW_GS = '%s/bin/mon-get-stats' % AWS_CW_HOME
REGION = 'us-east-1'
mailServer = 'mail.abc.com.tw'
fromAddr = 'it@abc.com.tw'
ccAddrs = [ 'accounting@abc.com.tw', 'finance@abc.com.tw' ]
groups = {
        'IT': {
            'name': 'IT Department',
            'email': [ 'it@abc.com.tw' ], },
	'DivA': {
		'name': 'Division A',
		'email': [ 'managerA@abc.com.tw', ], },
	'DivB': {
		'name': 'Division B',
		'email': [ 'managerB@abc.com.tw', ], },
	'DivC': {
		'name': 'Division C',
		'email': [ 'managerC@abc.com.tw', ], },
}
accKeys = {
	'aws_acc01': {
		'name': 'AWS Account 01',
		'cname': 'For AWS Account 01',
		'group': 'DivA',
		'ACCKEY': 'YourAccessKey',
		'SECKEY': 'YourSecretKey', },
	'aws_acc02': {
		'name': 'AWS Account 02',
		'cname': 'For AWS Account 02',
		'group': 'DivA',
		'ACCKEY': 'YourAccessKey',
		'SECKEY': 'YourSecretKey', },
	'aws_acc03': {
		'name': 'AWS Account 03',
		'cname': 'For AWS Account 03',
		'group': 'DivB',
		'ACCKEY': 'YourAccessKey',
		'SECKEY': 'YourSecretKey', },
	'aws_acc04': {
		'name': 'AWS Account 04',
		'cname': 'For AWS Account 04',
		'group': 'DivC',
		'ACCKEY': 'YourAccessKey',
		'SECKEY': 'YourSecretKey', },
}

def main():
	sumAll = {}
	grpstr = {}
	[ periodTime, startTime, endTime ] = get_date()
	print 'Charge period: %s' % periodTime
	if DEBUG: print 'Debug information:'
	for acc in accKeys:
		if DEBUG: print 'Getting Estimated Charge from game %s ... ' % accKeys[acc]['name']
		cmdArr = [ AWS_CW_GS, 'EstimatedCharges', '--statistics', '\"Maximum\"', '--start-time', '\"%s\"' % startTime, '--end-time', '\"%s\"' % endTime, '--namespace', '\"AWS/Billing\"', '--dimensions', '\"Currency=USD\"', '-I', accKeys[acc]['ACCKEY'], '-S', accKeys[acc]['SECKEY'], '--region', REGION, ]
		if DEBUG: print 'CMD for %s:\n%s' % ( acc , cmdArr )
		p = subprocess.Popen( cmdArr, stdout=subprocess.PIPE )
		output, err = p.communicate()
		if len(output) > 1:
			strs = output.split()
			if DEBUG: print '%s\n' % strs[2]
			accKeys[acc]['charge'] = float(strs[2])
		else:
			if DEBUG: print 'No data.\n'
                        send_email( 'IT', 'Cannot get AWS billing information %s' % periodTime, 'Please check: \nAccount: %s\nCMD: %s\noutput: %s\nerr: %s' % ( acc, cmdArr, output, err ), [ fromAddr ] )
			accKeys[acc]['charge'] = 0.0
		try: 
			tmpstr = grpstr[accKeys[acc]['group']]
		except: 
			grpstr[accKeys[acc]['group']] = {}
			grpstr[accKeys[acc]['group']]['proj'] = []
			grpstr[accKeys[acc]['group']]['sum'] = 0.0
		grpstr[accKeys[acc]['group']]['proj'].append(acc)
		grpstr[accKeys[acc]['group']]['sum'] += float(strs[2])

	for grp in grpstr:
		title = 'AWS Estimated Cost %s' % periodTime
		msg = 'Hi Sir,\n\nListed below are estimated AWS cost of your division during %s :\n' % periodTime
		print '%s: %s' % ( groups[grp]['name'] , groups[grp]['email'] )
		for game in grpstr[grp]['proj']:
			msg += '%s (%s):\t%s\n' % ( accKeys[game]['name'], accKeys[game]['cname'], accKeys[game]['charge'] )
			print '%s(%s):\t%s' % ( accKeys[game]['name'], accKeys[game]['cname'], accKeys[game]['charge'] )
                msg += 'Total:  %s\nUnit: USD\n\n' % grpstr[grp]['sum']
		print 'Total charge: %s\n' % grpstr[grp]['sum']
		msg += 'Best Regards,\nSI\n'
		send_email(grp, title, msg, ccAddrs)

def send_email( group, title, mailmsg, ccAddrs):
	import smtplib
	from email.mime.text import MIMEText
	msg = MIMEText(mailmsg)
	msg['Subject'] = title
	msg['From'] = fromAddr
	msg['To'] = ", ".join(groups[group]['email'])
	msg['CC'] = ", ".join(ccAddrs)
	s = smtplib.SMTP(mailServer)
	result = s.sendmail( fromAddr, groups[group]['email'] + ccAddrs, msg.as_string() )
	if result: print 'Result: %s' % result
	s.quit()

def get_date():
	today = datetime.datetime.today()
	endTime = datetime.datetime(second=0, minute=0, hour=0, day=1, month=today.month, year=today.year)
	startTime = endTime - datetime.timedelta(hours=2)
	startDate = datetime.date(day=1, month=startTime.month, year=startTime.year)
	endDate = datetime.date(day=startTime.day, month=startTime.month, year=startTime.year)
	endTime = endTime + datetime.timedelta(hours=2)
	periodTime = '%s - %s' % ( startDate.strftime('%Y/%m/%d'), endDate.strftime('%Y/%m/%d') )
	return [ periodTime, startTime.strftime('%Y-%m-%dT%H:%M:%SZ'), endTime.strftime('%Y-%m-%dT%H:%M:%SZ') ]

if __name__ == '__main__':
	main()

