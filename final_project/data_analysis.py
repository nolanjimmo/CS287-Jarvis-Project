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
import matplotlib.pyplot as plt
import scipy

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
    #print(df.keys())
    # Gather the suicides per year per country in a dictionary
    suicide_year_country = {country:df[df['country'] == country]['suicides_no'] for country in df.country.unique()}
    for country in suicide_year_country.keys():
        keys = suicide_year_country[country].keys()
        l = []
        for key in keys:
            l.append(suicide_year_country[country][key])
        l = l[:len(l)-1]
        suicide_year_country[country] = l

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
    hs_counts = {country:df[df['country'] == country]['Total expenditure'].sum() for country in df.country.unique()}
    
    ordered_hs_counts = {key: values for key, values in sorted(hs_counts.items(), key=lambda item: item[1])}
    
    # getting the years that each country has data for
    years_dict = {country:df[df['country'] == country]['year'] for country in df.country.unique()}
    #print(years_countries["Sweden"].keys())
    
    # Analysis output
    suicide_countries = list(ordered_suicide_counts.keys())
    suicide_counts = list(ordered_suicide_counts.values())
    five_highest_s_countries = suicide_countries[len(suicide_countries)-5:]
    
    print("5 highest suicide # countries: ")
    print(suicide_countries[len(suicide_countries)-5:])
    
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
    
    print("\n\nMiddle Counts: Suicide")
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
        

    ###### PLOTTING ########
    # Setting up vars for plotting
    vars_dicts = {}
    
    years = set()
    for n in five_highest_s_countries:
        for i in years_dict[n].keys():
            years.add(years_dict[n][i])
    years = list(years)
    years = years[:len(years)-1]
    #print(years)
    
    #alcohol
    alcohol_country_dict = {country:df[df['country'] == country]['Alcohol'] for country in five_highest_s_countries}
    for country in alcohol_country_dict.keys():
        keys = alcohol_country_dict[country].keys()
        l = []
        for key in keys:
            l.append(alcohol_country_dict[country][key])
        l = l[:len(l)-1]
        alcohol_country_dict[country] = l
    vars_dicts["Alcohol"] = alcohol_country_dict
    
    #bmi
    bmi_country_dict = {country:df[df['country'] == country][' BMI '] for country in five_highest_s_countries}
    for country in bmi_country_dict.keys():
        keys = bmi_country_dict[country].keys()
        l = []
        for key in keys:
            l.append(bmi_country_dict[country][key])
        l = l[:len(l)-1]
        bmi_country_dict[country] = l
    vars_dicts["BMI"] = bmi_country_dict
    
    #health spending
    hs_country_dict = {country:df[df['country'] == country]['Total expenditure'] for country in five_highest_s_countries}
    for country in hs_country_dict.keys():
        keys = hs_country_dict[country].keys()
        l = []
        for key in keys:
            l.append(hs_country_dict[country][key])
        l = l[:len(l)-1]
        hs_country_dict[country] = l
    vars_dicts["Health Spending"] = hs_country_dict
    
    
    ######## SCATTER PLOTS ############
    for k,v in vars_dicts.items():
        for country in vars_dicts[k].keys():
            plt.scatter(years, v[country])
            plt.xlabel("Years")
            plt.ylabel(k)
            plt.title(country)
            plt.show()
    
    for country in alcohol_country_dict.keys():
        plt.scatter(years, suicide_year_country[country])
        plt.title(country)
        plt.legend(["Suicide"])
        plt.show()
        
        
    ##### BIVARIATE SCATTER PLOTS #########
    for k,v in vars_dicts.items():
        for country in vars_dicts[k].keys():
            plt.scatter(suicide_year_country[country], v[country])
            plt.xlabel("Suicide Num")
            plt.ylabel(k)
            plt.title(country)
            plt.show()
            
    ######## LINEAR REGRESSIONS ##########
    lin_regs_dict = {}
    

data_selection(df) 
