import re 
from datetime import datetime
# needs to be installed:
from icalendar import Calendar, Event



c_name_pattern = r"([A-z\.\- ]+) \| .+Section"
c_dates_pattern = r"Class Begin: (\d+/\d+/\d+) \| Class End: (\d+/\d+/\d+)"
c_type_pattern = r"Schedule Type: ([A-z\.\- ]+)"
c_day_pattern = r"(\w+day)"
c_times_pattern = r"(\d+:\d+ AM|\d+:\d+ PM) - (\d+:\d+ AM|\d+:\d+ PM)"
c_location_pattern = r"Building: ([A-z\.\- ()]+) Room: ([A-z\.\-\d ]+)"
c_crn_pattern = r"CRN: (\d+)"

def nameSearch(line):
    match = re.search(c_name_pattern, line)
    if match:
        return match.group(1)
def dateSearch(line):
    match = re.search(c_dates_pattern, line)
    if match:
        return [match.group(1), match.group(2)]
def typeSearch(line):
    match = re.search(c_type_pattern, line)
    if match:
        return match.group(1)
def daySearch(line):
    match = re.search(c_day_pattern, line)
    if match:
        return match.group(1)
def timeSearch(line):
    match = re.search(c_times_pattern, line)
    if match:
        return [match.group(1), match.group(2)]
def locationSearch(line):
    match = re.search(c_location_pattern, line)
    if match:
        return match.group(1)+" "+match.group(2)
def crnSearch(line):
    match = re.search(c_crn_pattern, line)
    if match:
        return match.group(1)
    
def regexLine(current_line, previous_dict = {}):
    return_val = {}
    if nameSearch(current_line):
        c_name = (nameSearch(current_line))
        return_val['name'] = (c_name)
    if dateSearch(current_line):
        date_s = (dateSearch(current_line)[0])
        date_e = (dateSearch(current_line)[1])
        if 'date' in previous_dict.keys():
            return_val['date2'] = ([date_s, date_e])
        else:
            return_val['date'] = ([date_s, date_e])
    if typeSearch(current_line):
        c_type = (typeSearch(current_line))
        return_val['type'] = (c_type)
    if daySearch(current_line):
        c_day = (daySearch(current_line))
        if 'day' in previous_dict.keys():
            return_val['day2'] = (c_day)
        else:
            return_val['day'] = (c_day)
    if timeSearch(current_line):
        time_s = (timeSearch(current_line)[0])
        time_e = (timeSearch(current_line)[1])
        if 'time' in previous_dict.keys():
            return_val['time2'] = ([time_s, time_e])
        else:
            return_val['time'] = ([time_s, time_e])
    if locationSearch(current_line):
        c_location = locationSearch(current_line)
        return_val['location'] = c_location
    if crnSearch(current_line):
        crn = (crnSearch(current_line))
        return_val['crn'] = (crn)
    return return_val

def convertDatetime(raw_data):
    dt = datetime.strptime(raw_data, "%m/%d/%Y%I:%M %p")
    # dt = datetime.strptime(raw_data, "%m/%d/%Y %I:%M %p")
    result = dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt