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
from scipy import stats

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
    return(pd.read_csv("data/merged_data/" + filename))

df = load_data("data/merged_data/merged_suicide.csv")

def correlation_coefficient(X,Y):
    #referenced algorithm idea from:
    #https://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
    """Compute and return (as a float) the Pearson correlation coefficient
    between two lists of numbers X and Y.
    """
    n = len(X)
    avg_x = sum(X)/len(X)
    avg_y = sum(Y)/len(Y)
    difference_product = 0
    x_difference_2 = 0
    y_difference_2 = 0
    for i in range(n):
        x_difference = X[i] - avg_x
        y_difference = Y[i] - avg_y
        difference_product += x_difference * y_difference
        x_difference_2 += x_difference * x_difference
        y_difference_2 += y_difference * y_difference

    return difference_product / math.sqrt(x_difference_2 * y_difference_2)

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
    del_list = []
    for k, v in suicide_year_country.items():
        if len(v) < 10:
            del_list.append(k)
    for d in del_list:
        del suicide_year_country[d]
    print(suicide_year_country)

    # Gather the suicide counts per country by summing each count across the years
    suicide_counts = {country:sum(suicide_year_country[country]) for country in suicide_year_country.keys()} 
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
    five_test_countries = suicide_countries[len(suicide_countries)-2:]
    five_test_countries.append(suicide_countries[math.floor(len(suicide_countries)/2)])
    for i in suicide_countries[:2]:
        five_test_countries.append(i)
    print(f"five test countries {five_test_countries}")
    
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
    for n in five_test_countries:
        for i in years_dict[n].keys():
            years.add(years_dict[n][i])
    years = list(years)
    years = years[:len(years)-1]
    
    #alcohol
    alcohol_country_dict = {country:df[df['country'] == country]['Alcohol'] for country in five_test_countries}
    for country in alcohol_country_dict.keys():
        keys = alcohol_country_dict[country].keys()
        l = []
        for key in keys:
            l.append(alcohol_country_dict[country][key])
        l = l[:len(l)-1]
        alcohol_country_dict[country] = l
    vars_dicts["Alcohol"] = alcohol_country_dict
    
    #bmi
    bmi_country_dict = {country:df[df['country'] == country][' BMI '] for country in five_test_countries}
    for country in bmi_country_dict.keys():
        keys = bmi_country_dict[country].keys()
        l = []
        for key in keys:
            l.append(bmi_country_dict[country][key])
        l = l[:len(l)-1]
        bmi_country_dict[country] = l
    vars_dicts["BMI"] = bmi_country_dict
    
    #health spending
    hs_country_dict = {country:df[df['country'] == country]['Total expenditure'] for country in five_test_countries}
    for country in hs_country_dict.keys():
        keys = hs_country_dict[country].keys()
        l = []
        for key in keys:
            l.append(hs_country_dict[country][key])
        l = l[:len(l)-1]
        hs_country_dict[country] = l
    vars_dicts["Health Spending"] = hs_country_dict
    
    
    ######## SCATTER PLOTS ############
    scat_fig, scat_axs = plt.subplots(3,5, figsize=(20,15))
    scat_fig.suptitle('Variable count per year by country')
    col = 0
    row = 0
    for k,v in vars_dicts.items():
        col = 0
        for country in vars_dicts[k].keys():
            scat_axs[row,col].scatter(years, v[country])
            if row == 2:
                scat_axs[row,col].set(xlabel = "Year")
            if col == 0:
                scat_axs[row, col].set(ylabel = k)
            if row == 0:
                scat_axs[row,col].set_title(country)
            col += 1
        row += 1
    
    suicide_fig, suicide_axs = plt.subplots(1,5, figsize=(15,4))
    suicide_fig.suptitle('Suicide counts by year by country')
    col = 0
    for country in alcohol_country_dict.keys():
        suicide_axs[col].scatter(years, suicide_year_country[country])
        suicide_axs[col].set(xlabel="Year")
        suicide_axs[col].set_title(country)
        if col == 0:
            suicide_axs[col].set(ylabel="Suicide Count")
        col += 1
        
    ##### BIVARIATE SCATTER PLOTS #########
    bi_fig, bi_axs = plt.subplots(3,5, figsize=(20,15))
    bi_fig.suptitle('Bivariate scatter comparison per year per country')
    col = 0
    row = 0
    for k,v in vars_dicts.items():
        col = 0
        for country in vars_dicts[k].keys():
            bi_axs[row,col].scatter(suicide_year_country[country], v[country])
            if row == 2:
                bi_axs[row,col].set(xlabel = "Suicide Count")
            if col == 0:
                bi_axs[row, col].set(ylabel = k)
            if row == 0:
                bi_axs[row,col].set_title(country)
            col += 1
        row += 1

    ######## LINEAR REGRESSIONS ##########
    print("\n")
    lin_regs_dict = {}
    # k = variable names (the 3 we are focusing on)
    # v is the dictionary that is key=country name, v=[values of the time period for that variables and country]
    for k,v in vars_dicts.items():
        lin_regs_dict[k] = {}
        # country = country name for each dictionary
        for country, vals in vars_dicts[k].items():
            slope, intercept, r_value, p_value, std_err = stats.linregress(suicide_year_country[country], vars_dicts[k][country])
            line = [slope*xi + intercept for xi in suicide_year_country[country]]
            lin_regs_dict[k][country] = line
            print(f"{country}, {k}: {r_value}")
            
    reg_fig, reg_axs = plt.subplots(3,5, figsize=(19,14))
    reg_fig.suptitle('Linear regression on bivariate plots')
    col = 0
    row = 0
    for k,v in vars_dicts.items():
        col = 0
        for country in vars_dicts[k].keys():
            reg_axs[row, col].scatter(suicide_year_country[country], v[country])
            reg_axs[row, col].plot(suicide_year_country[country], lin_regs_dict[k][country], 'r-', linewidth=4)
            if row == 2:
                reg_axs[row,col].set(xlabel = "Suicide Count")
            if col == 0:
                reg_axs[row,col].set(ylabel = k)
            if row == 0:
                reg_axs[row,col].set_title(country)
            col += 1
        row += 1
        
    #### PEARSON CORRELATION COEFICIENTS #####
    pearson_coefs_dict = {}
    for k in five_test_countries:
        pearson_coefs_dict[k] = {}
        for v in vars_dicts.keys():
            coef = correlation_coefficient(suicide_year_country[k], vars_dicts[v][k])
            pearson_coefs_dict[k][v] = coef
    
    print()
    for k1,v1 in pearson_coefs_dict.items():
        print(f"{k1} Correlation Coefficients to Suicide Count (over time)")
        for k2, v2 in v1.items():
            print(f"{k2}: {v2:.5f}")
        print("\n")
        
        
    ##### ATTEMPTING PEARSON CORRELATIONS FOR THE WHOLE DATASET ######
'''    pearson_coefs_dict_global = {"Alcohol":[], " BMI ":[], "Total expenditure":[]}
    countries = suicide_year_country.keys()
    needed_dicts = {"Alcohol": alcohol_counts, " BMI ":bmi_counts, "Total expenditure":hs_counts}
    for k in countries:
        for v in vars_dicts.keys():
            coef = correlation_coefficient(suicide_year_country[k], needed_dicts[k])
            pearson_coefs_dict_global[v].append(coef)
    
    means = {"alcohol": int, " BMI ": int, "Total expenditure": int}
    for k,v in pearson_coefs_dict_global.items():
        means[k] = sum(v)/len(v)
    
    print(means) '''
            
            
data_selection(df) 
