#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 16:23:00 2021

Christopher O'Neil 
Nolan Jimmo
Selection and analysis of suicide by country dataset
"""
import pandas as pd 
import math
def load_data(filename):
    """ 
    load_data loads csv files to data frames
   
    Parameters
    ----------
    name of file

    Returns
    -------
    dataframe
    
    """
    return(pd.read_csv("merged_data/" + filename))

df = load_data("merged_suicide.csv") 

def data_selection(df):
    """
    data selection selects relevent countries for analysis

    Parameters
    ----------
    df : merged dataframe of susicide data

    Returns
    -------
    None

    """
    # Gather the suicide counts per country by summing each count across the years
    suicide_counts = {country:df[df['country'] == country]['suicides_no'].sum() for country in df.country.unique()} 
    # Order the dictionary
    ordered_suicide_counts = {key: values for key, values in sorted(suicide_counts.items(), key=lambda item: item[1])}
    # Gather the extremas and midpoints and display them for countries to be
    # selected for analysis 
    countries = list(ordered_suicide_counts.keys())
    counts = list(ordered_suicide_counts.values())
    
    print("\nExtrema Counts: ")
    for i in range(1,3):
        print(str(countries[-i]) + ": " + str(counts[-i]))
        print(str(countries[i-1]) + ": " + str(counts[i-1]))
    print("")
    print("Middle Counts: ")
    midpoint = math.floor(len(countries)/2)
    
    for i in range(midpoint, midpoint + 2):
        print(str(countries[i] + ": " + str(counts[i])))

data_selection(df) 
