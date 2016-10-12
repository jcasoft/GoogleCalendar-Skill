**GoogleCalendar-Skill with add events**
===================


An skill to use with Mycroft which allow to interact with google calendar.
Now is possible to add events with a lot of intents

----------


Installation
-------------------
Is necesary to make this procedure two times

outside mycroft virtual environment for python 2

    pip install google-api-python-client apiclient oauth2client httplib2
	
    or 

    pip2 install google-api-python-client apiclient oauth2client httplib2


Now enter inside mycroft virtual environment

Inside mycroft virtual environment

    workon mycroft

    pip install google-api-python-client apiclient oauth2client httplib2


Now got to Mycroft thord party skill directory

    cd  /opt/mycroft/third_party/

    git clone  https://github.com/jcasoft/GoogleCalendar-Skill.git mycroft-googlecalendar-skill

<i class="icon-cog"></i>Add 'GoogleCalendar-Skill' section in your Mycroft configuration file on:

    /home/pi/.mycroft/mycroft.ini

        [GoogleCalendarSkill]
        loginEnabled = False
        calendar_id = 'xxxxxx@gmail.com' # For add events to your calendar
        maxResults = 10
        gmt = '-06:00'
        timeZone = 'America/El_Salvador'
        attendees_own = 'xxxxx1@gmail.com,xxxxx2@icloud.com'
        attendees_family = 'xxxx1@yahoo.com,xxxx2@hotmail.com'
        attendees_work = 'support.mywork@gmail.com,sales.mywork@gmail.com,info.mywork@icloud.com'
        reminders_email = 1440  # in minutes --> 24 *60
        reminders_popup = 10    # in minutes
        default_duration = 2	# Default duration of appointments, in hours
        time_format = 12h 	# Options are 12h and 24h


> **Note:**

> - The previous configuration it's necesary for add events to your calendar


If had installed this skill previusly (delete credential file to re-create a new credential)

    cd ~
    cd .credentials
    rm mycroft-googlecalendar-skill.json


Authorize Google Calendar Skill in distro with local web browser, wait web browse open and select "Allow"

    From your command line go to third_party folder skill

    cd /opt/mycroft/third_party

    python mycroft-googlecalendar-skill

	
Authorize Google Calendar Skill in distro without local web browser

    From your command line go to third_party folder skill

    cd /opt/mycroft/third_party

    python mycroft-googlecalendar-skill --noauth_local_webserver

Open the generated link in computer with browser and wait the verification code and paste

     Enter verification code: 4/oxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   (Please copy the code generated, and paste it there)



Restart Skills

    ./start.sh skills

----------


Features
--------------------

Currently this skill can do the following things to get information from your calendar (with some variation):

- Whats my next meeting
- List my appointments for today
- List My events for tomorrow
- List my appointments until tomorrow
- My compromises for the Sunday
- Whats my events for the following 5 days
- Whats my next appointment with gianluca (New)
- Where is my next meeting (New)


> **Note:**

> - The name of the day of the week intent, will be calculated from the next day until the same day of the following week
> - You can toggle key word with:
> - Next, today, tomorrow, until tomorrow, name of the day of the week , from 2 until 30 for the following X days.
> - Events, Events, Meeting, Mettings, Appointmen, Appointmens, Schedule, Scheduled, Compromise, Compromises


New Features: Add Events
--------------------

Currently this skill can do the following things to set events to your calendar (with some variation):

- Whats my next meeting
- Add new event tomorrow from 2:30 pm to 4:45 pm Lunch with Gianluca on Olive Garden's
- Set compromise today from 18:30 to 21:45 pm Dinner whit Gianluca after work
- Add new appointment from 8:30 am to 11:45 am Marketing planification
- Add new event friday from 11:30 am to 5:45 pm birthday party on carlos house

- Schedule meeting on march 2 from 8:30 am to 11:45 am Support team planification
- Schedule my meeting on october 25 from 8:30 am to 11:45 am Halloween party planification
- Schedule family meeting on november 2 from 1:30 pm to 5:45 pm New years party planification
- Schedule work meeting on november 13 from 13:30 to 16:45  Sales planification with customers
- Schedule meeting on march 2 at 18:30 Visit Carlos at Hospital

- Set event today at 7:45 pm Dinner with Gianluca
- Set event tomorrow at 7:45 am Breakfast with Gianluca
- Set event at 13:45 Lunch with Gianluca
- Set event saturday at 11:30 PM New years party planification


> **Note:**

> - You can toggle key word with:
> - Today, tomorrow, name of the day of the week , month and day
> - Events, Events, Meeting, Mettings, Appointmen, Appointmens, Schedule, Scheduled, Compromise, Compromises


Bonus Features: 
--------------------
- When is the end of the world?
- when is the judgment day ?



**Enjoy !**
--------