#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:59:01 2021

@author: christopheroneil
"""
import datetime
from Event import Event
schedule = []

while True:
    
    date_time = input("What is the date and time? ")
    event_class = input("What is the event for? ")
    event_description = input("What is the event? ")
    
    if len(schedule) == 0:
        schedule.append(Event(date_time, event_class, event_description))
    
    if len(schedule) > 0:
        for event in schedule:
            if event == Event(date_time, event_class, event_description):
                print("There is conflicting times with this new event with: ")
                print(event)
                continue
            else:
                schedule.append(Event(date_time, event_class, event_description))
    
    flag = input("Want to continue: yes or no? ")
    
    if flag[0].lower() == 'n':
        break

for event in schedule:
    print(event)
