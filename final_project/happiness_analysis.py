#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 16:54:44 2021

@author: tuckerparon
Analysis of suicide rates with focus on Happiness
"""

### IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

### LOAD DATA
df = pd.read_csv("merged_data/merged_2015.csv")

### PROCESS DATA

# Add column (suicides per 100k people
df['suicides per 100k'] = ( df['suicides_no'] / df['population'] ) * 100000

### ANALYZE DATA
# Scatter plot to observe suicides per capita by several other variables
fig, axes = plt.subplots(4, 2, figsize=(9, 9))
plt.subplots_adjust(wspace=0.2, hspace=0.6)
df.plot(kind = 'scatter', x = 'Life Ladder', y = 'suicides per 100k', subplots=True, ax=axes[0][0]) # no correlation
c1 = df['Life Ladder'].corr(df['suicides per 100k'])
df.plot(kind = 'scatter', x = 'Social support', y = 'suicides per 100k', subplots=True, ax=axes[0][1]) # no correlation
c2 = df['Social support'].corr(df['suicides per 100k'])
df.plot(kind = 'scatter', x = 'Positive affect', y = 'suicides per 100k', subplots=True, ax=axes[1][0]) # no correlation
c3 = df['Positive affect'].corr(df['suicides per 100k'])
df.plot(kind = 'scatter', x = 'Negative affect', y = 'suicides per 100k', subplots=True, ax=axes[1][1]) # moderate negative
c4 = df['Negative affect'].corr(df['suicides per 100k'])
df.plot(kind = 'scatter', x = 'Generosity', y = 'suicides per 100k', subplots=True, ax=axes[2][0]) # weak negative
c5 = df['Generosity'].corr(df['suicides per 100k'])
df.plot(kind = 'scatter', x = 'Freedom to make life choices', y = 'suicides per 100k',subplots=True, ax=axes[2][1]) # no correlation
c6 = df['Freedom to make life choices'].corr(df['suicides per 100k'])
df.plot(kind = 'scatter', x = 'Confidence in national government', y = 'suicides per 100k',subplots=True, ax=axes[3][0]) # weak negative
c7 = df['Confidence in national government'].corr(df['suicides per 100k'])
df.plot(kind = 'scatter', x = 'Schooling', y = 'suicides per 100k', subplots=True, ax=axes[3][1]) # moderate positive
c8 = df['Schooling'].corr(df['suicides per 100k'])
# Histograms
df2 = df.groupby('Status', as_index=False)[['suicides_no','population']].sum()
df2['suicides per 100k'] = ( df2['suicides_no'] / df2['population'] ) * 100000
df2.plot(kind = 'bar', x = 'Status', y = 'suicides per 100k') # moderate negative

# Summary Statistics
print(df.nlargest(10, ['suicides per 100k']))
print(df.nsmallest(10, ['Life Ladder']))

print(df.nsmallest(10, ['suicides per 100k']))
print(df.nlargest(10, ['Life Ladder']))

print(df[["suicides per 100k", "Life Ladder", "Positive affect", "Generosity"]].describe())

# Other ideas
    # Do t-test on positive affects and negative affects