#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:53:55 2021

Christopher O'Neil
Reading, compiling, and cleaning the three data sets
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
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
    return(pd.read_csv("raw_data/" + filename))
    
def data_extraction():
    """ 
    data extraction extracts the relevant columns from the data frames
    and prepares data frames for merging. 
   
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Load in all three frames
    suicides_frame = load_data("master.csv")
    life_expectancy_frame = load_data("life_expectancy.csv")
    happiness_frame = load_data("happiness_report.csv")
    
    # Gather correct range of years for the frames
    current_suicides_frame = suicides_frame[suicides_frame["year"] >= 2005] 
    current_suicides_frame = current_suicides_frame[current_suicides_frame["year"] < 2016]
    # Sum up all suicide counts per year per country and create a new data frame
    suicides_aggregated = current_suicides_frame.groupby(["country", 
                                                          "year"]).suicides_no.sum().reset_index()
    # Sum up all population counts per year per country and create a new data frame
    population_aggregated = current_suicides_frame.groupby(["country", 
                                                            "year"]).population.sum().reset_index()
    # Concat the two dataframes together 
    su_pop_aggregated = pd.concat([suicides_aggregated, population_aggregated["population"]], 
                                  axis = 1)
    
    # Subset happiness by year 2015
    happiness_frame_2015 = happiness_frame[happiness_frame["year"] == 2015]
    
    merge_data(su_pop_aggregated, life_expectancy_frame, happiness_frame_2015)

def merge_data(su_pop, life_expectancy, happiness_frame):
    """ 
    merge data takes the extracted data and merges them into 
    the apporpriate data frames.
   
    Parameters
    ----------
    suicide and population aggregated frame
    life expectancy frame
    happiness report frame 

    Returns
    -------
    None
    """
    # Create sets of the countries and get their difference 
    su_pop_countries = set(su_pop["country"])
    life_expectancy_countries = set(life_expectancy["Country"])
    country_difference = life_expectancy_countries.difference(su_pop_countries)
    
    # Create new data frame with only the countries contained in su_pop
    country_indexed = life_expectancy.set_index("Country")
    country_indexed = country_indexed.drop(list(country_difference))
    
    # Drop the population column from the dataframe because the column
    # had very large discrepancies
    pop_country_indexed = country_indexed.drop("Population", axis = 1)
    
    # Merge the two frames so that only the years with suicides counts are 
    # included for analysis. 
    final_suicides_frame = su_pop.merge(pop_country_indexed, 
                                            how="left", left_on = ["country", "year"],
                                            right_on = ["Country", "Year"]) 
    # Year column from pop_country frame as an artifact so it was dropped
    final_suicides_frame = final_suicides_frame.drop("Year", axis = 1)
    
    # Do the same code as above but now subset that data to 2015
    final_suicdes_frame_2015 = final_suicides_frame[final_suicides_frame["year"] == 2015]
    
    final_suicdes_countries = set(final_suicdes_frame_2015["country"])
    happiness_frame_countries = set(happiness_frame["country"]) 
    
    countries_2015_difference = happiness_frame_countries.difference(final_suicdes_countries)
    
    country_2015_indexed = happiness_frame.set_index("country")
    country_2015_indexed = country_2015_indexed.drop(list(countries_2015_difference))
    
    final_2015_frame = country_2015_indexed.merge(final_suicdes_frame_2015,
                                                  how = "left", left_on = ["country", "year"],
                                                  right_on = ["country", "year"])
    explore_data(final_suicides_frame, final_2015_frame)

def explore_data(final_suicides, final_2015):
    """ 
    explore data takes the final merged frames and looks at the distributions 
    of the data see if there is any data cleaning required
   
    Parameters
    ----------
    final suicides frame 
    final 2015 frame

    Returns
    -------
    None
    """
    # Initialize a list to see which variables cannot be graphed
    invalid_hist_list = []
    # Initialize a dictionary to keep track of missing values 
    nan_dict = {}
    frame_list = [final_2015, final_suicides]
    frame_num = 1
    
    # For each frame graph the histogram and count nans.
    for frame in frame_list:
        nan_dict = {}
        for col in frame.columns:
            if (col != "year" and col != "country"):
                nan_count = frame[col].isnull().values.sum()
                nan_dict[col] = nan_count
                try:
                    plt.title("Frame " + str(frame_num) + " " + col + " Count")
                    plt.hist(frame[col], bins = 'auto')
                    plt.show()
                    pass
                except TypeError:
                    invalid_hist_list.append(col)
                except ValueError:
                    invalid_hist_list.append(col)
        frame_num += 1
        
        print(nan_dict)
        print(invalid_hist_list)
        
    
    # Alcohol was dropped because it only had two values for 2015 
    final_2015.drop('Alcohol', axis = 1, inplace = True)
    # Total expenditure was dropped because it had no values 
    final_2015.drop('Total expenditure', axis = 1, inplace = True)
    # Precentage expenditure was dropped because it was either zero or NA for 2015
    final_2015.drop('percentage expenditure', axis = 1, inplace = True)
    
    """
    Suicudes frame cleaning:
    Find the top countries with the highest NaN counts by iterating through
    and detecting na values for each column. Once that is found append them to 
    a list. Then use counter to count each countries na columns. A list
    of the highest na countries was found then they were dropped from the final
    frame. 
    """
    countries_with_na_cols = []
    for country in final_suicides.country.unique():
        for column in nan_dict.keys():
            if final_suicides[final_suicides['country'] == country][column].isnull().values.any():
                countries_with_na_cols.append(country)
    
    print(Counter(countries_with_na_cols))
    top_countries_na = ['Aruba', 'Czech Republic', 'Puerto Rico', 
                        'Saint Vincent and Grenadines', 'San Marino', 
                        'United Kingdom', 'United States']
    
    final_suicides.set_index("country", inplace = True)
    final_suicides.drop(top_countries_na, axis = 0, inplace = True)
    
    save_to_csv(final_suicides, final_2015)

def save_to_csv(f_s_frame, f_2015_frame):
    """ 
    save to csv takes the merged data frames and saves them to a csv
   
    Parameters
    ----------
    final suicides frame 
    final 2015 frame

    Returns
    -------
    None
    """
    
    f_s_frame.to_csv('merged_data/merged_suicide.csv')
    f_2015_frame.to_csv('merged_data/merged_2015.csv')
    

data_extraction()
