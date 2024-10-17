from constants import *

course_list = []
current_course = {}
cal = Calendar()

input_file = open("my_schedule.txt", "r")
for line in input_file:
    e = Event()
    if regexLine(line, current_course) != {}:
        current_course.update(regexLine(line, current_course))
    if re.search(c_crn_pattern, line):
        e.add('summary', current_course['name']+" "+current_course['type'])
        e.add('dtstart', convertDatetime(current_course['date'][0]+current_course['time'][0]))
        e.add('dtend', convertDatetime(current_course['date'][0]+current_course['time'][1]))
        e.add('dtstamp', datetime.now())
        e.add('comment', f"CRN: {current_course['crn']}")
        e.add('location', current_course['location'])
        if 'day2' in current_course.keys():
            e.add('rrule', {
            'freq': 'weekly',       
            'until': convertDatetime(current_course['date'][1]+current_course['time'][1]),
            'byday': [current_course['day'][0:2],current_course['day2'][0:2]]           
            })
        else:
            e.add('rrule', {
            'freq': 'weekly',       
            'until': convertDatetime(current_course['date'][1]+current_course['time'][1]),
            'byday': current_course['day'][0:2]           
            })
        cal.add_component(e)
        current_course = {}
input_file.close()

with open('schedule.ics', 'wb') as f:
    f.write(cal.to_ical())