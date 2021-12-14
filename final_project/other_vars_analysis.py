

#import statements
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.impute import KNNImputer
import matplotlib.pyplot as plt
import numpy as np
import scipy, scipy.stats


#OLS Function call

def linear_reg(X, target):
  #linear_reg() runs the statsmodels OLS linear regression model on the two parameters
  #Parameters:
    #X is the independent variable
    #target is the dependent variable
  #Returns:
    #result which is the results provided by model.fit()
    #summary which is a OLS linear regression model summary that contains mumerical info about the results of the model 
    #vals which is a dictionary containing the models p_values and condition number 

  model = sm.OLS(target, X)
  result = model.fit()
  summary = result.summary2()
  
  #print("P-value: ", result.pvalues)
  #print("coefficents: ", result.params)
  #print("rsquared: ", result.rsquared)
  #print("Cond number: ", result.condition_number)
  #print(type(result.pvalues))
  
  #Create dictionary of p-value and condition number
  vals = {"p-value": result.pvalues, "condition_number" :result.condition_number}
  #Return result, vals and summary
  return result, summary, vals

#Graphing time!
def graphing_linear(x_name, target):
  #graphing_linear() is a function to easily create scatterplots with a 
  #line showing the linear relationship between the x and y variables created by running a linear regression model
  #Parameters:
    #x-name is a string containing the column name of the x variable of interest 
    #target is the dependent variable 
  #Returns
    #Nonetype, but does print out graph

  #Create X data set
  X = data[x_name]
  #Call scipy.stats.linregress(X, target) to get slope and intercept
  slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X,target)
  
  #Plot scatterplot with line showing linear relationship 
  plt.plot(X,target, 'o')
  plt.plot(X, slope*X+intercept, 'r-', label = "LR")
  plt.xlabel(x_name)
  plt.ylabel("Number of suicides")
  plt.title(x_name + " vs Number of suicides")
  plt.legend()




#main
#Load merged_2015 table into pandas data frame

merged_2015_df = pd.read_csv("data/merged_data/merged_2015.csv")
#merged_2015_df.info()

#Replace column names such that there are no leading/trailing spaces, all lowercase, and have _ where spaces once were

#df.rename(columns={"A": "a", "B": "b", "C": "c"}, errors="raise")
key_map = {}
for key in merged_2015_df.keys():
  x = key
  x = x.strip().lower().replace(" ", "_")
  key_map[key] = x
  
merged_2015_df.rename(columns = key_map, errors = "raise", inplace = True)



#Split data into two data frames 
  #target is y variable (number of suicides)
  #data is the rest of the dataframe that contains numerical data except index and number of suicides 
target = merged_2015_df["suicides_no"]

data = merged_2015_df.select_dtypes(include=[np.number])
data.drop(["suicides_no"], axis = 1, inplace = True)
data.drop(["unnamed:_0"], axis = 1, inplace = True)

#Use KNNImputer to impute missing data based on (numeric) closest neighbors (Link: https://scikit-learn.org/stable/modules/impute.html)
data_cols = list(data.keys())

imputer = KNNImputer(n_neighbors=2, weights="uniform")

x = imputer.fit_transform(data)

data[:] = imputer.fit_transform(data)
x = data[data_cols]


#Linear regression for single variable correlations 

#Test one variable at a time
#Pick a column to test
name = "gdp"
X_test = data[name] ## X  independent variable
#Add constant 
X_test = sm.add_constant(X_test) 
#Call linear_reg()
result_test, summary_test, values_test = linear_reg(X_test, target)

#Print results
print(name)
print(result_test.summary2())

#Use scipy.stats.pearsonr to get Pearon's r 
#Note: scipy.stats.pearsonr = (r, p-value)
print("Pearson's r ", scipy.stats.pearsonr(data[name], target))

#Test all columns for potential linear regression 
#Get column names
keys = data.columns
#Set alpha value 
alpha = 0.06
#For each column in data 
for key in keys:
  #X_key is the data values
  X_key = data[key]
  #Add a constant
  X_key = sm.add_constant(X_key, prepend = True)
  
  #Call linear_reg() function
  result, summary, value_dict = linear_reg(X_key, target)
  
  #To weed out less significant results, only print results with p-value and condition number that are small enough to be considered "statistically significant" and avoid multicollinearity 
  if value_dict["condition_number"] < 1000 and value_dict["p-value"].loc[key] < alpha:
    print(key)
    print(summary)
    print("Pearon's r")
    print(scipy.stats.pearsonr(data[key], target))




#Graphing time!

#Make variables to store string of column name 
gini_income = "gini_of_household_income_reported_in_gallup,_by_wp5-year"
infant = "infant_deaths"
under_five = "under-five_deaths"

#Pass x variable and target to graphing_linear()
graphing_linear(under_five, target)



#Multi-variable Linear regression             

#Decide which variables you want to combine and store in a list
col_names = ["perceptions_of_corruption", "positive_affect"]

#Create another list to store data[column_name1, column_name2, etc]
cols =[]
for c in col_names:
  z = data[c]
  cols.append(z)
#Cast cols into a tuple so it can be used with column_stack
x_tuple = tuple(cols)

#Create X data 
multi_x = np.column_stack( x_tuple )
#Add constant 
multi_x = sm.add_constant(multi_x, prepend = True)
#Run linear_reg()
linear_reg(multi_x, target)
