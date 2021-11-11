"""
Christopher O'Neil

Event represents an event in a schedule and takes in a event id, date time, 
and an event description

"""
import datetime 
class Event():
    """
    Constructor for event
    
    Parameters
    ----------
    event_id is an assigned Id depending on when the event is in relation to
    other events.
    date_time is the date and time of the event
    event_class is the class of the event (work, not work, etc.)
    event_desicription is what the event is
    
    Returns
    -------
    None
    """
    def __init__ (self, date_time, event_class, event_description):
        

        self.date_time = datetime.datetime.strptime(date_time ,"%m/%d/%Y %I:%M%p" )
        self.event_class = event_class
        self.event_description = event_description 
   
    
    """
    getter for date and time of event
    
    Parameters
    ----------
    None
    
    Returns
    -------
    datetime object of date and time of event
    """
    def get_date_time(self):
        return self.date_time
    
    """
    getter for event class
    
    Parameters
    ----------
    None
    
    Returns
    -------
    string of event class
    """
    def get_event_class(self):
        return self.event_class
    
    """
    getter for event descirption
    
    Parameters
    ----------
    None
    
    Returns
    -------
    string of event description
    """
    def get_event_description(self):
        return self.event_description
    
    
    """
    setter for date and time of event
    
    Parameters
    ----------
    self
    string of date and time
    
    Returns
    -------
    None
    """
    def set_date_time(self, date_time):
        self.date_time = datetime.datetime.strptime(date_time 
                                                   ,"%m/%d/%Y %I:%M%p" )
    """
    setter for event class
    
    Parameters
    ----------
    string of event class
    
    Returns
    -------
    None
    """
    def set_event_class(self, event_class):
        self.event_class = event_class
        
    """
    setter for description of event
    
    Parameters
    ----------
    string of event description
    
    Returns
    -------
    None
    """
    def set_event_description(self, event_description):
        self.event_description = event_description
    
    """
    override string method
    
    Parameters
    ----------
    None
    
    Returns
    -------
    string that displays all information about the event
    """
    def __str__(self):
        
        return("Date and Time: " + 
               datetime.datetime.strftime(self.date_time, "%m/%d/%Y %I:%M%p" ) + 
               '\n' + 
               "Event Is For: " +
               str(self.event_class) + 
               '\n' +
               "Event Description: " +
               str(self.event_description))
    
    """
    override string method
    
    Parameters
    ----------
    None
    
    Returns
    -------
    True if two events datetimes are equal or if 
    two events id's are equal
    False if two events times are not equal
    """
    def __eq__(self, other):
        if (isinstance(other, Event)):
            if (self.date_time == other.date_time):
                return True
            return False
        