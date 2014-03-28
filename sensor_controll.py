import urllib2
import json
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

andrea = "andreabeccaris88@gmail.com"
gabri = "consigliog@gmail.com"
dario = "io.dariofacchini@gmail.com"
barbara = "barbara.minutello@gmail.com"
subject_ok = "[DAILY REPORT]-Rasp"
subject_err = "[ERROR]-Rasp"
message_err = '<html><head></head><body>Hi,seems an error has occurred..please check! </body></html>' 

tot_report = 0
report_wrong = 0
report_good = 0


def send_mail(recipient,subject, message):
        print "send mail"
        sender = 'gruppo19malnati@gmail.com'
        try:
            msg = MIMEMultipart('alternative')
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login('gruppo19malnati','Spatang2014')
            msg['Subject'] = subject
            text = MIMEText(message, 'html')
            msg.attach(text)
            smtpObj.sendmail(sender, recipient, msg.as_string())         
            smtpObj.close()
            return True
        except smtplib.SMTPException:
            return False 
while True:
	if tot_report == 24:
		message_ok = '<html><head></head><body><h1>Hi,this is the daily report</h1> </br>report good: %s/%s</br>report wrong:%s/%s </body></html>' %(report_good,tot_report, report_wrong,tot_report) 
		if not send_mail(andrea,subject_ok,message_ok):
			print "fail andrea mail"
		if not send_mail(gabri,subject_ok,message_ok):
			print "fail gabri mail"
		if not send_mail(dario,subject_ok,message_ok):
			print "fail dario mail"
		if not send_mail(barbara,subject_ok,message_ok):
			print "fail barbara mail"
		
		print "Result:",report_good,"/",tot_report

		tot_report = 0
		report_wrong = 0
		report_good = 0
		
	response = urllib2.urlopen('http://crowdsensing.ismb.it/SC/rest/apis/device/80:1f:02:87:82:a5/posts/last')
	html = response.read()
	j = json.loads(html)

	print "system time: ",datetime.datetime.now()
	print "post time: ",j['send_timestamp']

	diff =  datetime.datetime.now()-datetime.datetime.strptime(j['send_timestamp'], "%Y-%m-%dT%H:%M:%S.%f+0100")

	hh,mm,ss =  str(diff).split(':')
	print hh,mm,ss
	if int(mm)>5:
		print "ERROR"
		report_wrong = report_wrong+1
		tot_report = tot_report +1
		
		if not send_mail(andrea,subject_err,message_err):
			print "fail andrea mail"
		if not send_mail(gabri,subject_err,message_err):
			print "fail gabri mail"
		if not send_mail(dario,subject_err,message_err):
			print "fail dario mail"
		if not send_mail(barbara,subject_err,message_err):
			print "fail barbara mail"
	else:
		print "EVERYTHINGS OK"
		report_good = report_good+1
		tot_report = tot_report +1
		print "tot report",tot_report
		print "good report",report_good

	time.sleep(3600)


