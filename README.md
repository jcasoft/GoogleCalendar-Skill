**GoogleCalendar-Skill**
===================


An skill to use with Mycroft which allow to interact with google calendar.
In the following release will be possible add events

----------


Installation
-------------------
Enter inside mycroft virtualenv

    workon mycroft

    pip install google-api-python-client apiclient oauth2client httplib2

    cd  /opt/mycroft/third_party/

    git clone  https://github.com/jcasoft/GoogleCalendar-Skill.git

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


> **Note:**

> - The previous configuration will be necesary for the future feature of add events

Restart Skills

    ./start.sh skills

----------


Features
--------------------

Currently this skill can do the following things (with some variation):

- Whats my next meeting
- List my todays appointments
- What's scheduled for tomorrow
- List my appointments until tomorrow
- My compromises for the Sunday
- Whats my scheduled for the following 5 days

> **Note:**

> - The name of the day of the week intent, will be calculated from the next day until the same day of the following week
> - You can toggle key word with:
> - Next, today, tomorrow, until tomorrow, name of the day of the week , from 2 until 30 for the following X days.
> - Events, Events, Meeting, Mettings, Appointmen, Appointmens, Schedule, Scheduled, Compromise, Compromises



Coming soon: " Add events"

**Enjoy !**
--------