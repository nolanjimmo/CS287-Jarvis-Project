#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyzing external training data, team's project 1 training data, and 
a combined data set consisting of both the external and project 1 training data
"""

#Import
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import numpy as np

def mean_metric(N, external,internal,combined):
    """Parameters: Number of itmes: N 
    External data set metric: external  
    Internal data set metric: internal
    Combined data set metric: combined
    Returns avg of metrics
    """
    avg = (external + internal + combined)/N
    return avg

def create_df_data(external, internal, combined, metric_list):
    """Parameters: List of metrics: metric_list 
    External data set metric: external  
    Internal data set metric: internal
    Combined data set metric: combined
    Returns list of dictionaries of each metric 
    """
    dict_list = []
    for m in metric_list: 
        m_dict = {"external":efficacy_external[m], "internal":efficacy_internal[m], "combined": efficacy_combined[m]}
        dict_list.append(m_dict)
    return dict_list
        

##### EDA of external data ####

    
#Upload external data 

file_names = os.listdir('data')
raw_data = []
#Read through each file and store into a list of strings
file_names.remove('.DS_Store')
for filename in file_names:
    #print(filename)
    for line in open('data/'+filename, 'rt'):
        l = ''
        try: 
            l = json.loads(line)
        except:
            pieces = line.split(",")
            ACTION = pieces[-1].strip("\n")
            TXT = ",".join(pieces[:-1])
            l = {"TXT": TXT, "ACTION": ACTION}
            
        raw_data.append(l)
   
#raw_data is a list of dictionaries, where each item is a command and category 

#Upload raw_data to a pandas dataframe
external_data = pd.DataFrame(data = raw_data)

print("\t External Data EDA")
print(external_data.info())
#Check for missing entries
print("shape",external_data.shape)
#No missing entries since for shape(x,y), x is same as number of entries provided from .info() method above

#Training data does contain multiples (ex: 43 instances of what time is it?)
print(external_data["TXT"].value_counts())


#Counts of each category

#Percentage of each category
val_count_external = external_data["ACTION"].value_counts()
N_external = 3884
print(val_count_external)

external_greet_per = val_count_external[0]/N_external
external_time_per = val_count_external[1]/N_external
external_weather_per = val_count_external[2]/N_external
external_pizza_per = val_count_external[3]/N_external
external_joke_per = val_count_external[4]/N_external

print("Percentage of data in each category")
print("greet:", external_greet_per)
print("time", external_time_per)
print("weather", external_weather_per)
print("pizza",external_pizza_per)
print("joke", external_joke_per)




#Graph of TXT item frequency distribution
txt_counts = external_data["TXT"].value_counts()
plt.hist(txt_counts, bins = 30)
plt.yscale("log")
plt.title("External Training Data ""TXT"" item repetition frequency")
plt.xlabel("Repetitions")
plt.ylabel("Count")


####Project 1 training data 

print("\n\t PROJECT 1 DATA EDA")


# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("/Users/kateyforsyth/Library/Mobile Documents/com~apple~CloudDocs/Graduate/CS287/PRO2_MOUNTAINTIGER/jarvis.db")
internal_data = pd.read_sql_query("SELECT * FROM training_data", con)
con.close()
print(internal_data.info())

#Check for missing entries
print("shape",internal_data.shape)
#No missing entries since for shape(x,y), x is same as number of entries provided from .info() method above


#No repeated items
#print(internal_data["txt"].value_counts())


#Counts of each category
val_count_internal = internal_data["action"].value_counts()
N_internal= 56
print(val_count_internal)



#Percentage of each category

internal_greet_per = val_count_internal[1]/N_internal
internal_time_per = val_count_internal[4]/N_internal
internal_weather_per = val_count_internal[0]/N_internal
internal_pizza_per = val_count_internal[3]/N_internal
internal_joke_per = val_count_internal[2]/N_internal
print("Percentage of data in each category")
print("greet:", internal_greet_per)
print("time", internal_time_per)
print("weather",internal_weather_per)
print("pizza",internal_pizza_per)
print("joke", internal_joke_per)





#Combined Data set 

#Find overlap between project 1 data and external data

#Make copy of internal_data to modify so it can be combined with external_data_copy 
internal_data_copy = internal_data.copy()
#Rename columns of internal_data and get rid of id column
internal_data_copy.drop(['id'], axis = 1, inplace = True)
internal_data_copy.columns=["TXT", "ACTION"]


#Make copy of external_data so it can be combined with internal_data_copy
external_data_copy = external_data.copy()
external_data_copy.drop_duplicates(subset = ["TXT"], inplace = True)

overlap_df = pd.merge(internal_data_copy, external_data_copy, how = "inner", on = ["TXT", "ACTION"])
#print(overlap_df)


print("\n\t Combined Data EDA")

frames = [external_data, internal_data_copy]
combined_data = pd.concat(frames)
print(combined_data.info())

#Check for missing entries
print("shape",combined_data.shape)
#No missing entries since for shape(x,y), x is same as number of entries provided from .info() method above


#Training data does contain multiples (ex: 44 instances of What time is it?) similar to external_data 
print(combined_data["TXT"].value_counts())


# #Percentage of each category

#Counts of each category
val_count_combined = combined_data["ACTION"].value_counts()
N = 3940
print(val_count_combined)

#Divide counts by N

combined_greet_per = val_count_combined[0]/N
combined_time_per = val_count_combined[1]/N
combined_weather_per = val_count_combined[2]/N
combined_pizza_per = val_count_combined[3]/N
combined_joke_per = val_count_combined[4]/N
print("Percentage of data in each category")
print("greet:", combined_greet_per)
print("time", combined_time_per)
print("weather", combined_weather_per)
print("pizza",combined_pizza_per)
print("joke", combined_joke_per)




####Comparing Jarviss efficacy across 3 data sets
#Hard coded metric scores for each data set because otherwise we would have had to 
#train Jarvis three times in one file to get the metric scores and that seems like it 
#would negatively impact readability  of file. 
#So we trained Jarvis in separate files for each data set 
#Training with proj 1 dataset: proj1_data_training_MOUNTAINTIGER.py
#Training with external data set: external_data_training_MOUNTAINTIGER.py
#Training with combined data set: combined_data_training_MOUNTAINTIGER.py

print("\n\t Jarvis Efficacy")

#Create dictionary of efficacy metrics for each data set (accuracy and f1-scores for each category)
efficacy_external = {"accuracy": 0.81, "GREET_f1" : 0.8, "JOKE_f1":0.86,"PIZZA_f1":0.79, "TIME_f1":0.81, "WEATHER_f1":0.82}
efficacy_internal = {"accuracy":0.92, "GREET_f1": 1, "JOKE_f1":1,"PIZZA_f1":1, "TIME_f1": 0.8 , "WEATHER_f1": 0.86}
efficacy_combined = {"accuracy": 0.83, "GREET_f1": 0.83, "JOKE_f1":0.83,"PIZZA_f1":0.83, "TIME_f1": 0.86, "WEATHER_f1":0.81 }





#List of metric names 
metric = ["accuracy", "GREET_f1", "JOKE_f1", "PIZZA_f1", "TIME_f1", "WEATHER_f1"]

#Find mean for each category f1_score and accuracy 
for x in metric:
    mean = mean_metric(3, efficacy_external[x], efficacy_internal[x], efficacy_combined[x])
    print(f"Mean {x} score: {mean:.2f}")
    

#Graphing time!

#Bar graph grouped by metric

#Create a list to use to create a data frame 
efficacy_df_data = create_df_data(efficacy_external, efficacy_internal, efficacy_combined, metric) 
#Create data frame using efficacy_df_data
efficacy_df = pd.DataFrame(efficacy_df_data, index = metric)

#Plot efficacy_df
efficacy_df.plot.bar() 
plt.title("Jarvis Efficacy Metric Scores Grouped by Metric")
plt.legend(["External data set", "Project 1 data set", "Combined data set"],bbox_to_anchor=(1.0, 0.75), title = "Data set")
plt.ylabel("Score")
plt.xlabel("Metric")



#Bar graph grouped by data set

#Create list containing the efficacy metrics of all the data sets
efficacy_list = [efficacy_external, efficacy_internal, efficacy_combined]
#Create dataframe using efficacy_list
efficacy_list_df = pd.DataFrame(efficacy_list, index = ["external","project 1","combined"])


#Plot efficacy_list_df
efficacy_list_df.plot.bar()
plt.title("Jarvis Efficacy Metric Scores Grouped by Data Set")
plt.legend(bbox_to_anchor=(1.0, 1.0), title = "Metric")
plt.ylabel("Score")
plt.xlabel("Dataset")
plt.show()

