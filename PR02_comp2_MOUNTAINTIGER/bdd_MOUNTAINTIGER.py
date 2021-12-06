#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOUNTAINTIGER
PR02 - Competition 2
Bad Data Detector

@authors: Tucker, Katey, Nolan, Chris
"""

import json

# Read in the file as a list of lines
filename = "input.txt" 
with open(filename, encoding='UTF-8', errors='strict') as f:
    lines = f.readlines()   

##### CALCULATIONS

def check_type(lines):
    '''
    Parameters
    ----------
    lines : list of strings
        All lines in the file.

    Returns
    -------
    Boolean determining file type. True denotes a file of dictionaries and
    False denoted a comma separated file.
    '''
    
    # Check if the line is in dictionary form
    if lines[0].startswith('{'):
        return True    
    else:
        return False
        
def UTF_error(lines, dict_type):
    '''
    Parameters
    ----------
    lines : list of strings
        All lines in the file.
    dict_type : bool
        True if data is in dictionary format.

    Returns
    -------
    Boolean determining if there are incorrect langauge conventions. 
    False denotes presence of error.
    '''
    
    if dict_type == True:
        for line in lines:
            line = json.loads(line)
            if '\\u' in line['TXT'] or '\xa0' in line['TXT']:
                return False
                break
        return True
    
    else:
        for line in lines:
            if '\\u' in line or '\xa0' in line:
                return False
                break
        return True

def action_error(lines, dict_type):
    '''
    Parameters
    ----------
    lines : list of strings
        All lines in the file.
    dict_type : bool
        True if data is in dictionary format.

    Returns
    -------
    Boolean determining if file has correct actions for text.
    False denotes presence of error.
    '''
    
    actions = ['WEATHER', 'PIZZA', 'GREET', 'JOKE', 'TIME'] # List of actions
   
    # Ensure action is one of the five requested
    if dict_type == True:
        for line in lines:
            line = json.loads(line)
            if line['ACTION'] not in actions:
                return False
                break
        return True
   
    else:
        for line in lines:
            line = line.split(',')
            if line[1].rstrip('\n') not in actions:
                return False
                break
        return True

def bracket_error(lines, dict_type):
    '''
    Parameters
    ----------
    lines : list of strings
        All lines in the file.
    dict_type : bool
        True if data is in dictionary format.
        
    Returns
    -------
    Boolean determining files (in dictionary form) have end brackets.
    False denotes presence of error.
    '''
    
    # Check if there are missing closing brackets.
    for line in lines:
        line = line.rstrip('\n')
        if dict_type and '}' not in line:
            return False
            break
    return True

def comma_error(lines, dict_type):
    '''
    Parameters
    ----------
    lines : list of strings
        All lines in the file.
    dict_type : bool
        True if data is in dictionary format.
        
    Returns
    -------
    Boolean determining if files (not in dictionary form) have unwanted commas
    which would interfere with parsing. False denotes presence of error.
    '''
    
    # Flag data with hardcoded quotation marks - lines with hardcoded "" have extra commas.
    for line in lines:
        splits = line.split(',') # splits - 1 is the number of commas
        if dict_type != True and (line.startswith('"') or len(splits) > 2):
            return False
            break
    return True

dict_type = check_type(lines) # Check if file is in dictionary form.

##### CONDITIONS

# Output
if UTF_error(lines, dict_type) and action_error(lines, dict_type) and bracket_error(lines, dict_type) and comma_error(lines, dict_type):
    print("good")
else:
    print("bad")
