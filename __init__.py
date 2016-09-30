
from adapt.intent import IntentBuilder
from mycroft.messagebus.message import Message

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger


import httplib2
import os
from googleapiclient import discovery
import oauth2client
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow

import calendar
import datetime
import time
from os.path import dirname, abspath, join
import sys


logger = getLogger(dirname(__name__))
sys.path.append(abspath(dirname(__file__)))

__author__ = 'jcasoft'

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CID = "992603803855-06urqkqae0trrr2dfte4vljmj8ts2om2.apps.googleusercontent.com"
CIS = "y6K5-YmVEcN9riOTnAVeMYvc"
APPLICATION_NAME = 'Mycroft Google Calendar Skill'

loginEnabled = ""

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    print "checking for cached credentials"
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'mycroft-googlecalendar-skill.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        credentials = tools.run_flow(OAuth2WebServerFlow(client_id=CID,client_secret=CIS,scope=SCOPES,user_agent=APPLICATION_NAME),store)
        print 'Storing credentials to ' + credential_path

    return credentials


def loggedIn():
    """
    Future implementation
    To do:
	- Verify FaceLogin Skill
	- Verify ProximityLogin Skill (For use with SmartPhone Mycroft Client App and iBeacon function on Rpi)
	- Verify PhoneClientLogin Skill (For use with SmartPhone Mycroft Client App with fingerprint or Unlock code )
	- Maybe VoiceLogin Skill
    """
    return True

def todayDateEnd():
    todayEnd = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59)
    todayEnd += datetime.timedelta(days=1)	# Add extrea dat to rango for GTM delta
    todayEnd = todayEnd.isoformat() + 'Z'
    return todayEnd

def tomorrowDateStart():
    tomorrowStart = datetime.datetime.utcnow().replace(hour=00, minute=00, second=01)
    tomorrowStart += datetime.timedelta(days=1)
    tomorrowStart = tomorrowStart.isoformat() + 'Z'
    return tomorrowStart

def tomorrowDateEnd():
    tomorrowEnd = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59)
    tomorrowEnd += datetime.timedelta(days=2)	# Add extrea dat to rango for GTM delta
    tomorrowEnd = tomorrowEnd.isoformat() + 'Z'
    return tomorrowEnd

def otherDateStart(until):
    otherDayStart = datetime.datetime.utcnow().replace(hour=00, minute=00, second=01)
    otherDayStart += datetime.timedelta(days=until)
    otherDayStart = otherDayStart.isoformat() + 'Z'
    return otherDayStart

def otherDateEnd(until):
    otherDayEnd = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59)
    otherDayEnd += datetime.timedelta(days=until)
    otherDayEnd = otherDayEnd.isoformat() + 'Z'
    return otherDayEnd


def checkLocation(eventDict):
    locationFlag = True if "location" in eventDict else False
    return locationFlag	

def checkDescription(eventDict):
    descriptionFlag = True if "description" in eventDict else False
    return descriptionFlag	

class GoogleCalendarSkill(MycroftSkill):
    """
    A Skill to check your google calendar
    also can add events
    """

    def google_calendar(self, msg=None):
	"""
    	Verify credentials to make google calendar connectionimport calendar
    	"""
        self.credentials = get_credentials()
        http = self.credentials.authorize(httplib2.Http())
        self.calendar_event = discovery.build('calendar', 'v3', http=http)

    def __init__(self):
        super(GoogleCalendarSkill, self).__init__('GoogleCalendarSkill')
    	"""
	Get the Google calandar parameters from config
	today = time.strftime("%Y-%m-%dT%H:%M:%S-06:00") for use on create event
	"""
	self.loginEnabled = self.config.get('loginEnabled')
	self.userLogin = self.config.get('userLogin')
	self.calendar_id = self.config.get('calendar_id')
	self.maxResults = self.config.get('maxResults')
	self.gmt = self.config.get('gmt')
	self.timeZone = self.config.get('timeZone')
	self.attendees_own = self.config.get('attendees_own')
	self.attendees_family = self.config.get('attendees_family')
	self.attendees_work = self.config.get('attendees_work')
	self.reminders_email = self.config.get('reminders_email')
	self.reminders_popup = self.config.get('reminders_popup')

	loginEnabled = self.loginEnabled 

    def initialize(self):
    	"""
	Mycroft Google Calendar Intents
	"""
        self.load_data_files(dirname(__file__))

        intent = IntentBuilder('NextEventIntent')\
            .require('NextKeyword')\
            .require('EventKeyword')\
            .build()
        self.register_intent(intent, self.handle_next_event)

        intent = IntentBuilder('TodaysEventsIntent')\
            .require('TodayKeyword')\
            .require('EventKeyword')\
            .build()
        self.register_intent(intent, self.handle_today_events)

        intent = IntentBuilder('TomorrowEventsIntent')\
            .require('TomorrowKeyword')\
            .require('EventKeyword')\
            .build()
        self.register_intent(intent, self.handle_tomorrow_events)

        intent = IntentBuilder('UntilTomorrowEventsIntent')\
            .require('UntilTomorrowKeyword')\
            .require('EventKeyword')\
            .build()
        self.register_intent(intent, self.handle_until_tomorrow_events)

        intent = IntentBuilder('EventsForWeekDayIntent')\
            .require('WeekdayKeyword') \
            .require('EventKeyword') \
            .build()
        self.register_intent(intent, self.handle_weekday_events)

        intent = IntentBuilder('EventsForXDaysIntent')\
            .require('XDaysKeyword') \
            .require('EventKeyword') \
            .build()
        self.register_intent(intent, self.handle_xdays_events)

        self.emitter.on(self.name + '.google_calendar',self.google_calendar)
        self.emitter.emit(Message(self.name + '.google_calendar'))

    def handle_next_event(self, msg=None):
	if not loggedIn():
		self.speak_dialog('NotAccess')
		return

	self.speak_dialog('VerifyCalendar')
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        eventsResult = self.calendar_event.events().list(
            calendarId='primary', timeMin=now, maxResults=self.maxResults, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            self.speak_dialog('NoEvents')
        else:
            event = events[0]
	    place = ''
	    description = ''
            start = event['start'].get('dateTime', event['start'].get('date'))
	    start = start[:22]+start[(22+1):]
	    start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S-%f")
	    startHour = ("{:d}:{:02d}".format(start.hour, start.minute))
	    startHour = time.strptime(startHour,"%H:%M")
	    startHour = time.strftime("%I:%M %p",startHour)
	    if (startHour[0]=='0'): startHour = startHour.replace('0','',1)
	    end = event['end'].get('dateTime', event['end'].get('date'))
	    end = end[:22]+end[(22+1):]
	    end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S-%f")
	    endHour = ("{:d}:{:02d}".format(end.hour, end.minute))
	    endHour = time.strptime(endHour,"%H:%M")
	    endHour = time.strftime("%I:%M %p",endHour)
	    if (endHour[0]=='0'): endHour = endHour.replace('0','',1)
	    if (checkLocation(event)):
	    	location = event['location']
	    	location = location.splitlines()
	    	place_city = ','.join(location[:1])
		place =  " on " + place_city 
	    else:
		place =  ""
	    organizer = event['organizer']
	    status = event['status']
	    summary = event['summary']
    	    if (checkDescription(event)):
		description = event['description'] 
	    else:
		description = ''
	    
	    rangeDate = "today"
	    if (len(organizer)) == 2:
		organizer = organizer['displayName']
	    	complete_phrase = organizer + " has scheduled a appointment for " + rangeDate  + " begining at " + startHour + " and ending at " + endHour + place
		complete_phrase = complete_phrase + ". About " + summary + ". " + description
	    elif (len(organizer)) == 3:
		complete_phrase = "You have a appointment " + rangeDate  + " from " + startHour + " at " + endHour + place 
		complete_phrase = complete_phrase + ". About " + summary + ". " + description

	    self.speak(complete_phrase)


    def handle_today_events(self, msg=None):
	if not loggedIn():
		self.speak_dialog('NotAccess')
		return

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	weekDayName = ""	# It's not necesary on this handle
        self.until_events(now, todayDateEnd(),0, weekDayName)

    def handle_tomorrow_events(self, msg=None):
	if not loggedIn():
		self.speak_dialog('NotAccess')
		return
	weekDayName = ""	# It's not necesary on this handle
        self.until_events(tomorrowDateStart(), tomorrowDateEnd(),1, weekDayName)

    def handle_until_tomorrow_events(self, msg=None):
	if not loggedIn():
		self.speak_dialog('NotAccess')
		return
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	weekDayName = ""	# It's not necesary on this handle
        self.until_events(now, tomorrowDateEnd(),2, weekDayName)

    def handle_weekday_events(self, message):
	if not loggedIn():
		self.speak_dialog('NotAccess')
		return
	# Calculate in range from the day after tomorrow plus 7 days 
	weekDayName = message.metadata.get("WeekdayKeyword")
	self.until_events(otherDateStart(2), otherDateEnd(8),7, weekDayName)

    def handle_xdays_events(self, message):
	if not loggedIn():
		self.speak_dialog('NotAccess')
		return
	XDayAfter = message.metadata.get("XDaysKeyword")
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	weekDayName = ""	# It's not necesary on this handle
        self.until_events(now, otherDateEnd(int(XDayAfter)),int(XDayAfter), weekDayName)

    def until_events(self, startDate, stopDate, rangeDays, weekDayName):
	self.speak_dialog('VerifyCalendar')
	if ( len(weekDayName) > 1):
		evaluateWeekDay = True
	else:
		evaluateWeekDay = False

        eventsResult = self.calendar_event.events().list(calendarId='primary', timeMin=startDate, timeMax=stopDate,singleEvents=True, orderBy='startTime').execute()
        events = eventsResult.get('items', [])

	today = datetime.datetime.strptime(time.strftime("%x"),"%m/%d/%y") 
    	tomorrow = today + datetime.timedelta(days=1)
    	other_date = today + datetime.timedelta(days=rangeDays)

        if not events:
		self.speak_dialog('NoEvents')
        else:
		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			start = start[:22]+start[(22+1):]
			start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S-%f")
			date_compare = datetime.datetime.strptime(start.strftime("%x"),"%m/%d/%y")
	    		startHour = ("{:d}:{:02d}".format(start.hour, start.minute))
	    		startHour = time.strptime(startHour,"%H:%M")
	    		startHour = time.strftime("%I:%M %p",startHour)
	    		if (startHour[0]=='0'): startHour = startHour.replace('0','',1)
	    		end = event['end'].get('dateTime', event['end'].get('date'))
	    		end = end[:22]+end[(22+1):]
	    		end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S-%f")
	    		endHour = ("{:d}:{:02d}".format(end.hour, end.minute))
	    		endHour = time.strptime(endHour,"%H:%M")
	    		endHour = time.strftime("%I:%M %p",endHour)
	    		if (endHour[0]=='0'): endHour = endHour.replace('0','',1)
	    		if (checkLocation(event)):
	    			location = event['location']
	    			location = location.splitlines()
	    			place_city = ','.join(location[:1])
				place =  " on " + place_city 
	    		else:
				place =  ""
	    		organizer = event['organizer']
			if (len(organizer)) == 2:
				phrase_part_1= organizer['displayName'] + " has scheduled a appointment for "
				phrase_part_2= " begining at " + startHour + " and ending at " + endHour + place
			elif (len(organizer)) == 3:
				phrase_part_1 = "You have a appointment "
				phrase_part_2= ", from " + startHour + " at " + endHour + place 

	    		status = event['status']
	    		summary = event['summary']

    	    		if (checkDescription(event)):
				description = event['description'] 
	    		else:
				description = ''

			phrase_part_3= ". About " + summary + ". " + description

			if (rangeDays == 0):		# compare the same day
				if (date_compare == today):
					rangeDate = "today"		
					complete_phrase = phrase_part_1 + rangeDate  + phrase_part_2 + phrase_part_3
	    				self.speak(complete_phrase)

			elif (rangeDays == 1 ):		# compare the next day
				if (date_compare == tomorrow):
					rangeDate = "tomorrow"		
					complete_phrase = phrase_part_1 + rangeDate  + phrase_part_2 + phrase_part_3
	    				self.speak(complete_phrase)

			elif (rangeDays == 2 ):		# compare until the next day
				if (date_compare <= tomorrow):
					rangeDate = "today"
					if (date_compare == today):
						rangeDate = "today"
					elif (date_compare == tomorrow):
						rangeDate = "tomorrow"
					complete_phrase = phrase_part_1 + rangeDate  + phrase_part_2 + phrase_part_3
					self.speak(complete_phrase)

			elif (evaluateWeekDay):		# compare the day name
				day_name_compare = (calendar.day_name[start.weekday()])
				if (day_name_compare.upper() == weekDayName.upper()):
					#rangeDate = weekDayName
					day = str(start.day)
					month_name = (calendar.month_name[start.month])
					rangeDate = weekDayName + ", " + month_name + " " + day
					complete_phrase = phrase_part_1 + rangeDate  + phrase_part_2 + phrase_part_3
					self.speak(complete_phrase)

			elif (rangeDays >2 ):		# compare until the nexts x days
				if (date_compare <= other_date):
					rangeDate = "today"
					if (date_compare == today):
						rangeDate = "today"
					elif (date_compare == tomorrow):
						rangeDate = "tomorrow"
					else:
						month_name = (calendar.month_name[start.month])
						day_name = (calendar.day_name[start.weekday()])
						day = str(start.day)
						rangeDate = day_name + ", " + month_name + " " + day

					complete_phrase = phrase_part_1 + rangeDate  + phrase_part_2 + phrase_part_3
					self.speak(complete_phrase)





def create_skill():
    return GoogleCalendarSkill()
