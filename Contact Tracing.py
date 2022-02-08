MIN_PER_HR = 60
VIS_PERSON = 0
VIS_LOC = 1
VIS_DAY = 2
VIS_HR = 3
VIS_MIN = 4
END_HR = 5
END_MIN = 6
TIME = 1
CONTACT_INFO = 0
CONTACT_LOC = 0
CONTACT_DAY = 1
CONTACT_HOUR = 2
CONTACT_MINUTE = 3
DT_DAY = 0
DT_HR = 1
DT_MIN = 2

'''
visits = [('Russel', 'Nutrity', 1, 5, 0, 6, 0),
          ('Russel', 'Foodigm', 2, 9, 0, 10, 0),
          ('Russel', 'Afforage', 2, 10, 0, 11, 30),
          ('Russel', 'Nutrity', 2, 11, 45, 12, 0),
          ('Russel', 'Liberry', 3, 13, 0, 14, 15),
          ('Natalya', 'Nutrity', 1, 5, 30, 6, 45),
          ('Natalya', 'Afforage', 2, 8, 15, 10, 0),
          ('Natalya', 'Nutrity', 4, 10, 10, 11, 45),
          ('Chihiro', 'Foodigm', 2, 9, 15, 9, 30),
          ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30),
          ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]
'''

def visit_length(visit):
    
    ''' Takes an argument visit (7-tuple) which details a person's visit to a
    location and returns a tuple (visit length) if valid and None otherwise '''
   
    # Calculate the minute and hour differences of the visit.
    minute = visit[END_MIN] - visit[VIS_MIN]
    hour = visit[END_HR] - visit[VIS_HR]
    
    # Carrying negative minutes to hours
    if minute < 0:
        hour -= 1
        minute += MIN_PER_HR

    
    # Visit is invalid if hour is negative
    if hour < 0:
        return None
    
    # Visit is invalid if length is 0
    elif minute == 0 and hour == 0:
        return None
    
    # If all checks passed, the length is returned.
    else:
        return (hour, minute)
        

def convert_time_to_dec(visit):

    ''' Accepts a 7-tuple & returns the start & end visit time in decimal form '''
    
    vis_time = visit[VIS_HR] + (visit[VIS_MIN] / MIN_PER_HR)
    end_time = visit[END_HR] + (visit[END_MIN] / MIN_PER_HR)

    return vis_time, end_time
    
def calc_intercept_length(vis_time, end_time):

    ''' Takes two tuples (hour, minute) and returns the time of intercept '''
    vis_hr, vis_min = vis_time[0], vis_time[1]
    end_hr, end_min = end_time[0], end_time[1]
    
    # Calculate the minute and hour differences of the visit.
    minute = end_min - vis_min
    hour = end_hr - vis_hr
    
    # Converting minute and hour to be greater than 0
    if minute < 0:
        hour -= 1
        minute += MIN_PER_HR
    return (hour, minute)
    
    
def potential_contacts(person_a, person_b):
    
    ''' Accepts two peoples visit history (set of 7-tuples) and returns a tuple
    containing a set of 6-tuples that includes the location, day, and time when
    both people were at the same location. It also output a 2-tuple that states
    the time that the two people were overlapping for '''

    def contact_event(visit_a, visit_b):
        
        ''' Accepts two arguments (7-tuples) that contain information regarding two
        seperate visits. Returns True if visits between unique people at the same 
        place overlap, returns False if not and None if a visit is invalid. '''
        
        # Checking if visits are are valid
        if visit_length(visit_a) is None or visit_length(visit_b) is None:
            return None 

        # Validity checks
        same_person = (visit_a[VIS_PERSON] == visit_b[VIS_PERSON])
        diff_loc = (visit_a[VIS_LOC] != visit_b[VIS_LOC])
        diff_day = (visit_a[VIS_DAY] != visit_b[VIS_DAY])

        # Check for false contact (I.e same person or different location)
        if same_person or diff_loc or diff_day:
            return False
        
     
        # Converting times into numbers (i.e (13, 30) into 13.50)
        nonlocal a_vis, a_end, b_vis, b_end
        
        a_vis, a_end = convert_time_to_dec(visit_a)
        b_vis, b_end = convert_time_to_dec(visit_b)
        
        # Creating all possible intervals of overlap.
        interval_1, interval_2 = a_vis <= b_vis < a_end, a_vis < b_end <= a_end
        interval_3, interval_4 = b_vis < a_end <= b_end, a_vis < b_end <= a_end
        
        # Overlap if either interval returns True
        if interval_1 or interval_2 or interval_3 or interval_4:
            return True
        else:
            return False


    time, pot_contact = [], []
    total_hours, total_minutes = 0, 0
    a_vis, a_end, b_vis, b_end = 0, 0, 0, 0
        
    # Checks each entry in person_a with each entry in person_b
    for visit_a in person_a:
        for visit_b in person_b:
            if contact_event(visit_a, visit_b):
                # Finds the lastest start time and most recent exit time
                intercept1 = max(a_vis, b_vis)
                intercept2 = min(a_end, b_end)
                
                # Retrieves time in format [h, m] from visit history
                if intercept1 == a_vis:
                    intercept_vis_time = [visit_a[VIS_HR], visit_a[VIS_MIN]]
                else:
                    intercept_vis_time = [visit_b[VIS_HR], visit_b[VIS_MIN]]
                
                if intercept2 == a_end:
                    intercept_end_time = [visit_a[END_HR], visit_a[END_MIN]]
                else:
                    intercept_end_time = [visit_b[END_HR], visit_b[END_MIN]]
                    
                time.append(calc_intercept_length(intercept_vis_time, intercept_end_time))
                pot_contact.append((visit_a[VIS_LOC], visit_a[VIS_DAY], 
                                    intercept_vis_time[0],                  # [hour, minute]
                                    intercept_vis_time[1], 
                                    intercept_end_time[0], 
                                    intercept_end_time[1]))
                
                
    # Adds together all times in list time
    for i in range(len(time)):
        total_hours += time[i][VIS_PERSON]
        total_minutes += time[i][VIS_LOC]
    
    # Converts minutes to hour
    if total_minutes >= MIN_PER_HR:
        total_hours += int(total_minutes / MIN_PER_HR)
        total_minutes = total_minutes % MIN_PER_HR
    
    return (set(pot_contact), (total_hours, total_minutes))


def contact_trace(visits, index, day_time):
    people, contact_tracing = dict(), dict()
    # Groups visits by name in a dictionary
    for visit in visits:
        person_name = visit[VIS_PERSON]
        people.setdefault(person_name, [])
        people[person_name].append(visit)
        
    person_1 = people[index]
    
    # Check the visits of the index against every other person
    for person_2 in list(people.values()):
        pot_contact = potential_contacts(person_1, person_2)
        name = person_2[0][VIS_PERSON]
        
        # Determine if the intercept time is after index infection was detected
        # pot_contact: ([loc, day, vis_hour, vis_min, end_hour, end_min], (hour, min))
        if pot_contact[TIME] != (0, 0):  
            for contact_instance in pot_contact[0]:
                hours = contact_instance[CONTACT_HOUR]
                minutes = contact_instance[CONTACT_MINUTE]
                
                # Contact if intercept days after infection
                if contact_instance[CONTACT_INTERVAL] > day_time[DT_DAY]:
                    contact_tracing.setdefault(name, [])
                    contact_tracing[name].append(contact_instance[1:4])
                    
                # If intercept day is equal, check if time is after infection
                elif contact_instance[CONTACT_INTERVAL] == day_time[DT_DAY]:
                    infect_time = day_time[DT_HR] + (day_time[DT_MIN] / MIN_PER_HR)
                    contact_time = hours + (minutes / MIN_PER_HR)
                    
                    if infect_time < contact_time:
                        contact_tracing.setdefault(name, [])
                        contact_tracing[name].append(contact_instance[1:4])
                            
    return contact_tracing

def forward_contact_trace(visits, index, day_time, second_order=False):
    
    ''' Accepts a list of 7-tuples, infected name, and time of infection. If
    second_order is false, returns a list of potential contacts after 
    infection. If second_order is true, another search of potential contacts
    from the first order contacts will be done, returning a list of potential
    contacts that include a second order search. '''
    
    contact_tracing = contact_trace(visits, index, day_time)
    second_contacts = []
    contacts = []

    # Repeats another instance of contact tracing for each of the first order contacts
    if second_order:
        for contact in list(contact_tracing.keys()):
            second_contacts.append(forward_contact_trace(visits, contact, contact_tracing[contact][0]))

    # Retrieving first and second order contact names
    for key in list(contact_tracing.keys()):
        contacts.append(key)
        
    for contact in second_contacts:
        for person in contact:
            contacts.append(person)
    
    # Removing duplicate contacts and index
    contacts = list(dict.fromkeys(contacts))
    
    if index in contacts:
        contacts.remove(index)

    return sorted(contacts)
                    

def backward_contact_trace(visits, index, day_time, window):
    
    ''' Accepts a list of 7-tuples, the infected person, and day of infection.
    The function will search for potential contacts x days backward where 
    x = window. The function will return a list of names that fit this
    criteria '''
    
    people = dict()
    contact = []
    window -= 1

    # Appending contact instances to dictionary in form {name: pot_contacts}
    for visit in visits:
        name = visit[VIS_PERSON]
        people.setdefault(name, [])
        people[name].append(visit)
        
    person_1 = people[index]
    
    # Cycles through a list of all of person2's contact history
    for person_2 in list(people.values()):
        
        # Skips to next person if person_1 is the same as person_2
        if person_1 != person_2:
            pot_contact = potential_contacts(person_1, person_2)
        else:
            continue
        
        person_to_contact = person_2[0][VIS_PERSON]
        contact_instances = pot_contact[CONTACT_INFO]
        
        # Only check a contact instance if length > 0
        if pot_contact[TIME] != (0, 0):
            for contact_instance in contact_instances:
                contact_day = contact_instance[CONTACT_DAY]
                
                # Contact person2 if overlapped before infection day
                if contact_instance[CONTACT_DAY] + window >= day_time[DT_DAY]:
                    contact.append(person_to_contact)
                
                # Contact person2 if overlapped time before infection time
                elif contact_day == day_time[DT_DAY]:
                    inf_hour, inf_min = day_time[DT_HR], day_time[DT_MIN]
                    con_hour = contact_instance[CONTACT_HOUR]
                    con_min = contact_instance[CONTACT_MINUTE]
                    
                    infect_time = inf_hour + (inf_min / MIN_PER_HR)
                    contact_time = con_hour + (con_min / MIN_PER_HR)

                    if contact_time < infect_time:
                        contact.append(person_to_contact)
    
    # Sort and remove duplicate contacts from repeated overlaps
    return sorted(list(dict.fromkeys(contact)))



