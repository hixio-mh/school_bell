import time
def writeLog(type,text):
	log = open("logs/log_"+time.strftime("%Y-%m-%d",time.localtime())+".txt","a")
	if type == "warn":
		sign = "WARNING: "
	elif type == "err":
		sign = "ERROR:   "
	else:
		sign = "INFO:    "
	log.write(time.strftime("%H:%M:%S",time.localtime())+" "+sign+"	"+text+"\n")
writeLog("inf","Starting...\nCurrent time: "+time.strftime("%Y/%m/%d %H:%M:%S"))
try:
	import RPi.GPIO as gpio
	gpio.setmode(gpio.BOARD)
	gpio.setup(tvpin, gpio.OUT)
	global ispi
	ispi = True
except ImportError:
	global ispi
	ispi = False
	print("WARNING: Couldn't load the RPi.GPIO module, GPIO functions won't work")
	writeLog("warn","Couldn't load the RPi.GPIO module, GPIO functions won't work")
from init_vars import *
import os
import datetime
from threading import Thread
def ringBell(startend):
	if ispi:
		gpio.output(tvpin, gpio.HIGH)
	time.sleep(5)
	if startend == "start":
		os.system(termcommand+" sound/start.wav")
		writeLog("inf","Sending command to play end.wav")
	elif startend == "end":
		writeLog("inf","Sending command to play start.wav" )
		os.system(termcommand+" sound/end.wav")
	time.sleep(10)
	if ispi:
		gpio.output(tvpin, gpio.HIGH)
def importSchoolDays():
	dayfile = open("data/schooldays.txt","r")
	dayraw = dayfile.readlines()
	dayfile.close()
	try:
		days = dayraw[0].split(" ")
	except IndexError:
		days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
	i = 0
	while i<len(days):
		days[i] = days[i].replace("\n","")
		days[i] = days[i].replace("\r","")
		i=i+1
	return days
def importSatSchoolDays():
	satfile = open("data/satschooldays.txt","r")
	satraw = satfile.readline()
	satfile.close()
	satschooldays = []
	for lines in satraw:
		satschooldays.append(lines)
	i = 0
	while i < len(satschooldays):
		satschooldays[i] = satschooldays[i].replace("\n\r","")
		i=i+1
	return satschooldays
def isSchoolDay(schooldays):
	wdaytoday = time.strftime("%a")
	answ = False
	for weekday in schooldays:
		if weekday == wdaytoday:
			answ = True
	return answ
def isDay(satschool):
	curdate = time.strftime("%d/%m/%Y", time.localtime())
	answ = False
	for date in satschool:
		if date == curdate:
			answ = True
	return answ
def importWDaysWOutSchool():
	freedomfile = open("data/wdayswoutschool.txt","r")
	freedomraw = freedomfile.readlines()
	freedomfile.close()
	freedom = []
	for lines in freedomraw:
		freedom.append(lines)
	i = 0
	while i<len(freedom):
		freedom[i] = freedom[i].replace("\n","")
		freedom[i] = freedom[i].replace("\r","")
		i = i+1
	return freedom
def importBreaks():
	breaksfile = open ("data/breaks.txt","r")
	breaksraw = breaksfile.readlines()
	breaksfile.close()
	breaks = []
	for lines in breaksraw:
		breaks.append(lines.split(" "))
	i = 0
	while i < len(breaks):
		breaks[i][1] = breaks[i][1].replace("\n","")
		breaks[i][1] = breaks[i][1].replace("\r","")
		i=i+1
	return breaks
def isBreak(breaks):
	i =0
	breakday = False
	while i<len(breaks):
		if time.strptime(breaks[i][0],"%d/%m/%Y") < time.localtime() and time.localtime() < time.strptime(breaks[i][1],"%d/%m/%Y"):
			breakday = True
		i = i+1
	return breakday
def importSchedule():
	schedulefile = open("data/ringschedule.txt","r")
	scheduleraw = schedulefile.readlines()
	schedulefile.close()
	schedule = []
	for lines in scheduleraw:
		schedule.append(lines.split(" "))
	i = 0
	if len(schedule) == 0:
		print("ERROR: The schedule file is empty.")
		print("Stopping...")
		exit()
	while i < len(schedule):
		schedule[i][1] = schedule[i][1].replace("\n","")
		i = i+1
	return schedule
def isBellTime(schedule):
	i =0
	j=0
	belltime = [False , j]
	while i < len(schedule):
		j = 0
		while j < 2:
			if schedule[i][j] == time.strftime("%H:%M", time.localtime()):
				belltime = [True , j]
			j = j+1
		i=i+1
	return belltime
def isPreBellTime(schedule):
	i=0
	timenow = time.localtime()
	answ = False
	while i < len(schedule):
		timesplit = schedule[i][0].split(":")
		timesplit[0] = int(timesplit[0])
		timesplit[1] = int(timesplit[1])
		if timesplit[1] - 2 < 0:
			timesplit[1] = (timesplit[1] - 2)+60
		else:
			timesplit[1] = timesplit[1]-2
		if timenow.tm_hour == timesplit[0] and timenow.tm_min == timesplit[1]:
			answ = True
		i = i+1
	return answ
def dateConvert(dates):
	year,month,day = dates.split('-')
	return day+"/"+month+"/"+year
def startTimer(schedule):
	thisday = time.strftime("%d/%m/%Y",time.localtime())
	while True:
		asd = isBellTime(schedule)
		if thisday != time.strftime("%d/%m/%Y",time.localtime()):
			print("INFO: Day is over")
			print("Stopping...")
			writeLog("inf","End of day --> Stopping")
			exit()
		if asd[0] == True:
			writeLog("inf","Ringing bell")
			if asd[1] == 0:
				print("INFO: Ringing bell (start) at "+time.strftime("%H:%M",time.localtime()))
				ringBell("start")
				time.sleep(60)
			elif asd[1] == 1:
				print("INFO: Ringing bell (end) at "+time.strftime("%H:%M",time.localtime()))
				ringBell("end")
				time.sleep(60)
		elif isPreBellTime(schedule):
			writeLog("inf","Ringing warning bell")
			print("INFO: Ringing warning bell at "+time.strftime("%H:%M",time.localtime()))
			ringBell("start")
			time.sleep(60)
		else:
			time.sleep(10)
try:
	breaks = importBreaks()
	schedule = importSchedule()
	satschool = importSatSchoolDays()
	freedays = importWDaysWOutSchool()
	schooldays = importSchoolDays()
except IOError:
	print("ERROR:Couldn't import every file from the data folder, file may be deleted, or may be renamed to a wrong name")
	print("Stopping...")
	writeLog("err","Couldn't import every file --> Stopping")
	exit()
print("INFO: All data has been read succesfully!")
writeLog("inf","All data has been read succesfully")
print("Ring schedule:")
print(schedule)
print("Breaks:")
print(breaks)
print("Saturday schooldays:")
print(satschool)
print("Weekdays without school:")
print(freedays)
print("Days of the week with school:")
print(schooldays)
stopped = True
if isSchoolDay(schooldays):
	if isBreak(breaks) == False:
		if isDay(freedays) == False:
			print("INFO: Starting timer functions")
			writeLog("inf","Today is a schoolday")
			writeLog("inf","Starting timer functions")
			startTimer(schedule)
			stopped = False
		else:
			print("INFO: Today is a weekday without school")
			writeLog("inf","Today is a weekday without school")
	else:
		print("INFO: Today there is a break going on")
		writeLog("inf","Today is included in a break")
else:
	print("INFO: Today is not a weekday with school")
	writeLog("inf","")
if isDay(satschool) and stopped:
	print("INFO: Today is a saturday with school")
	writeLog("inf", "Today is a saturday with school")
	print("Starting timer functions")
	writeLog("inf","Starting timer functions")
	startTimer(schedule)
print("INFO: Exiting")
writeLog("inf","Exiting")
