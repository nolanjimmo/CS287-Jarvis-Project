#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:53:55 2021

Christopher O'Neil
Reading, compiling, and cleaning the three data sets
"""
import pandas as pd

def load_data(filename):
    """ 
    load_data loads csv files to data frames
   
    Parameters
    ----------
    name of file

    Returns
    -------
    None.
    
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
    for country in list(country_difference):
        country_indexed = country_indexed.drop(country)
    
 
data_extraction()
