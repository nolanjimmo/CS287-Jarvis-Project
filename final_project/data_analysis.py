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
    print(df.keys())
    # Gather the suicide counts per country by summing each count across the years
    suicide_counts = {country:df[df['country'] == country]['suicides_no'].sum() for country in df.country.unique()} 
    # Order the dictionary
    ordered_suicide_counts = {key: values for key, values in sorted(suicide_counts.items(), key=lambda item: item[1])}
    # Gather the extremas and midpoints and display them for countries to be
    # selected for analysis 
    
    # same for alcohol
    alcohol_counts = {country:df[df['country'] == country]['Alcohol'].sum() for country in df.country.unique()}
    
    ordered_alcohol_counts = {key: values for key, values in sorted(alcohol_counts.items(), key=lambda item: item[1])}
    
    # same for BMI
    bmi_counts = {country:df[df['country'] == country][' BMI '].sum() for country in df.country.unique()}
    
    ordered_bmi_counts = {key: values for key, values in sorted(bmi_counts.items(), key=lambda item: item[1])}
    
    # same for health spending
    hs_counts = {country:df[df['country'] == country]['percentage expenditure'].sum() for country in df.country.unique()}
    
    ordered_hs_counts = {key: values for key, values in sorted(hs_counts.items(), key=lambda item: item[1])}
    
    # Analysis output
    suicide_countries = list(ordered_suicide_counts.keys())
    suicide_counts = list(ordered_suicide_counts.values())
    
    alcohol_countries = list(ordered_alcohol_counts.keys())
    alcohol_counts = list(ordered_alcohol_counts.values())
    
    bmi_countries = list(ordered_bmi_counts.keys())
    bmi_counts = list(ordered_bmi_counts.values())
    
    hs_countries = list(ordered_hs_counts.keys())
    hs_counts = list(ordered_hs_counts.values())
    
    print("\nExtrema Counts: Suicide")
    for i in range(1,3):
        print(str(suicide_countries[-i]) + ": " + str(suicide_counts[-i]))
        print("A: " + str(ordered_alcohol_counts[str(suicide_countries[-i])]))
        print("BMI: " + str(ordered_bmi_counts[str(suicide_countries[-i])]))
        print("S: " + str(ordered_hs_counts[str(suicide_countries[-i])]) + "\n")
        print(str(suicide_countries[i-1]) + ": " + str(suicide_counts[i-1]))
        print("A: " + str(ordered_alcohol_counts[str(suicide_countries[i-1])]))
        print("BMI: " + str(ordered_bmi_counts[str(suicide_countries[i-1])]))
        print("S: " + str(ordered_hs_counts[str(suicide_countries[i-1])]) + "\n")
    print("\n\nExtrema Counts: Alcohol")
    for i in range(1,3):
        print(str(alcohol_countries[-i]) + ": " + str(alcohol_counts[-i]))
        print(str(alcohol_countries[i-1]) + ": " + str(alcohol_counts[i-1]))
    
    print("\nExtrema Counts: BMI")
    for i in range(1,3):
        print(str(bmi_countries[-i]) + ": " + str(bmi_counts[-i]))
        print(str(bmi_countries[i-1]) + ": " + str(bmi_counts[i-1]))
        
    print("\nExtrema Counts: Spending")
    for i in range(1,3):
        print(str(hs_countries[-i]) + ": " + str(hs_counts[-i]))
        print(str(hs_countries[i-1]) + ": " + str(hs_counts[i-1]))
    
    print("Middle Counts: Suicide")
    midpoint = math.floor(len(suicide_countries)/2)
    
    for i in range(midpoint, midpoint + 2):
        print(str(suicide_countries[i] + ": " + str(suicide_counts[i])))
        print("A: " + str(ordered_alcohol_counts[str(suicide_countries[i])]))
        
    print("\nMiddle Counts: Alcohol")
    midpoint = math.floor(len(alcohol_countries)/2)
    
    for i in range(midpoint, midpoint + 2):
        print(str(alcohol_countries[i] + ": " + str(alcohol_counts[i])))
        
    print("\nMiddle Counts: BMI")
    midpoint = math.floor(len(bmi_countries)/2)
    
    for i in range(midpoint, midpoint + 2):
        print(str(bmi_countries[i] + ": " + str(bmi_counts[i])))
        
    print("\nMiddle Counts: Spending")
    midpoint = math.floor(len(hs_countries)/2)
    
    for i in range(midpoint, midpoint + 2):
        print(str(hs_countries[i] + ": " + str(hs_counts[i])))

data_selection(df) 
