# Homework 03
# [Please replace this comment with your name]

# allowed imports only (you may not need all of these):
import sys, os
import glob
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
# no other imports please!


############## Functions ##############
def load_report(filename):
    # Initializing final dictionary.
    errorCodeCountsDict ={} 
    # List for conversion of values.
    linesWithoutSpaces =[] 
    # List that will be used to append to the dictionary.
    errorCodeCountList = [] 
    # First val is datacenter ID.
    errorCodeCountsDict["DataCenter"] = filename.replace(".dat", "") 
    
    # Opening the files.
    file = open("reports/" + str(filename)) 
    # Reading the lines in the file.
    lines = file.readlines() 

    # For each line fromat the lines for use.
    for line in lines: 
        linesWithoutSpaces.append(line.replace(" ", "").replace("\n", "").replace(":", " "))
    
    file.close()
    
    # For each line if there is a space append it to the errorCodeList.
    for line in linesWithoutSpaces:
        for char in line:
            if char.isspace() == True: 
                errorCodeCountList.append(line)
    
    # All lines that contain spaces should have a number in the final index for error count.
    for errorCodeCount in errorCodeCountList:
        errorCodeCount = errorCodeCount.split(" ")
        if errorCodeCount[-1].isdigit() == True:
            errorCodeCountsDict[errorCodeCount[0]] = int(errorCodeCount[1])
    
    return(errorCodeCountsDict)
# [Define any of your other functions here, replacing this code comment]


############ End Functions ############



# [Organize code related to problems in the corresponding sections delineated
# below (if code is required). Place code specific to a (sub)problem BELOW that
# problem's header. Please do not delete header comments as they are used for
# automatic code search]

############## Problem 0 ##############

#### P0.1 ####

#### P0.2 Bonus/Required ####

############## Problem 1 ##############

#### P1.1 ####

#### P1.2 ####

#### P1.3 ####
# Initializing a list of dictionaries.
dataCenterErrorReportsList = [] 

# Listing the filenames in reports.
filenames = os.listdir("reports") 

# Append all generated dictionaries to the list.
for filename in filenames: 
    dataCenterErrorReportsList.append(load_report(filename))

# Print the length of the list.
print(len(dataCenterErrorReportsList)) 
print("")

# Create an input file to write to.
inputFile = open("tester_p1_input.txt", "w") 
for dataCenterReport in dataCenterErrorReportsList:
    # For each data center report write it to the file.
    for keys,values in dataCenterReport.items():
        # Step added from problem 1.5 to merge two of the variables. 
        if keys == "AirCon.":
            keys = "A/C"
        inputFile.write(str(dataCenterReport["DataCenter"]) + "\t" + keys + "\t" + 
                            str(values) + "\n" )
inputFile.close()
#### P1.4 ####
# Initialize a list of id's
listOfIds = []
# For each data cetner report append the id to the list of id's
for dataCenterReport in dataCenterErrorReportsList:
    listOfIds.append(dataCenterReport["DataCenter"])
# Print the sorted list of words to show their sequence.
print(sorted(listOfIds)) 
print("")

# For each entry in the list if there is a repeating entry turn repeats flag true
#if not trun it false. 
for i in range(len(listOfIds)-1):
    if listOfIds[i] == listOfIds[i+1]:
        repeats = True
    else:
        repeats = False
# Dpending on flag value display message. 
if repeats: 
    print("there are repeats")
    print("")

else:
    print("there are no repeats")
    print("")

#### P1.5 ####
# Create a list of error names.
listOfErrors = []
# For each data center report.
for dataCenterReport in dataCenterErrorReportsList:
    # For each key value pair in the report dictionary.
    dataCenterReportp['A/c'] = dataCenterReport.pop("AirCon.")
        # If the error name is not in the list append it to the list.
        if keys not in listOfErrors and keys != "DataCenter":
            listOfErrors.append(keys)
# Print the list of error names.          
print(listOfErrors)
print("")
#### P1.6 ####

#For each data center report.
for dataCenterReport in dataCenterErrorReportsList:
    # For each error code name in the list of erros. 
    for error in listOfErrors:
        #Try to print the the value for the error in the dictionary. 
        try: 
            print(dataCenterReport[error])
        # Exception for if error code count doesn't exist. 
        except KeyError:
            # Append the name of the key and give it the value of zero
            # because if it wasn't reported in the error report then that means 
            # it didn't happen so give it the value of zero. 
            dataCenterReport[error] = 0
############## Problem 2 ##############

#### P2.1 ####
# Initializing a count of erros for each error code report.
numberOfErrorsPerDataCenter = 0
# For each report in the list of reports.
for dataCenterReport in dataCenterErrorReportsList:
    # For each error code name add the count to the accumulator. 
    for error in listOfErrors: 
        numberOfErrorsPerDataCenter += dataCenterReport[error]
    
    # Print the total error code count for each data center. 
    print(str(dataCenterReport["DataCenter"]) + ": "+ 
          str(numberOfErrorsPerDataCenter))
    print("")
    numberOfErrorsPerDataCenter = 0        

#### P2.2 ####

# Initializing a list that will store the summed error counts for each data center.
totalNumberOfErrorsList = []

# For each data center report. 
for dataCenterReport in dataCenterErrorReportsList:
    # Initialize the counts per center.
    errorsPerCenter = 0
    # For each error in the list of possible errors.
    for error in listOfErrors: 
        # dd each error count to our accumulator. 
        errorsPerCenter += dataCenterReport[error]
    #Append them to our list.    
    totalNumberOfErrorsList.append(errorsPerCenter)

#A massive outlier was found so it was removed. 
outlier = 76911
totalNumberOfErrorsList.remove(outlier)

#Take the average and the standard deviation of our list, and display them 
#In the terminal. 
average = np.mean(totalNumberOfErrorsList)
stDev = np.std(totalNumberOfErrorsList)
print("Average number of erros per work station is: " + "{:.2f}".format(average))
print("The Standard Deviation is: " + "{:.2f}".format(stDev))


#### P2.3 ####
# Getting the outlier ID so it can be removed. 
outlierId = "001137"

# Creating adictionary that will show all of the different errors summed.
mostCommonErrosDict = {}

# Adding the keys to the dictionary and initializing the values.
for errors in listOfErrors:
    mostCommonErrosDict[errors] = 0

# Deleting the outlier so it doesn't mess with the counts. 
for i in range(len(dataCenterErrorReportsList)):
    if dataCenterErrorReportsList[i]["DataCenter"] == outlierId:
        del dataCenterErrorReportsList[i]
        break

# For each data center accumulate the the counts of each type of error. 
for dataCenterReport in dataCenterErrorReportsList:          
    for keys,values in dataCenterReport.items():
        if keys in mostCommonErrosDict.keys():
            mostCommonErrosDict[keys] += values

# Display in the console the dictionary with all of the counts for each error
# summed. 
print("")
for keys, values in mostCommonErrosDict.items():
    print(str(keys) + ": " + str(values))
print("")

#### P2.4 ####



############## Problem 3 ##############

#### P3.1 ####
# Intialize a total error count per center and a porportion dictionary for water
# errors proportions per data center. 
totalErrorCountPerCenter = 0
proportionOfErrorsDict ={}

# For each data center report.
for dataCenterReport in dataCenterErrorReportsList:
     
    # For each possible error.
    for error in listOfErrors: 
        
        #A dd up the toal errors per center.
        totalErrorCountPerCenter += dataCenterReport[error]
    # Calculate the proportion of errors that are floods per data center. 
    proportionOfFloods = dataCenterReport["Physicalintrusion(water)"]/totalErrorCountPerCenter
    # Add the data center Id and the proportion to the dictionary.
    proportionOfErrorsDict[dataCenterReport["DataCenter"]] = proportionOfFloods

#Sort the proportions and get the last five entries, then reverse them.
sortedProportions = sorted(proportionOfErrorsDict.values())[-5:]
sortedProportions.reverse()

# Print the header for the table. 
print("Center ID:      Proportion:")

#For each proportion in the sorted lise.
for top5RiskCenterProportions in sortedProportions:
    #For each key and value in the proportion dict. 
    for keys, values in proportionOfErrorsDict.items():
        #If the proportions match print them out. 
        if top5RiskCenterProportions == values:
            print("  " + str(keys) + "         " 
                  + "{:.2f}".format(values))

#### P3.3 ####
#Sort all proportions from greatest to least greatest proportions.
sortedProportions = sorted(proportionOfErrorsDict.values())
#Reverse the list so it is descending.
sortedProportions.reverse()
#Initialize a dictionary for the ranked center ids. 
rankedCenterIdList = {}
count = 0
#For each proportion create a ranked dictionary of all of the data centers.
for proportionsOfFloodRisk in sortedProportions:
    for keys,values in proportionOfErrorsDict.items():

        if proportionsOfFloodRisk == values and keys not in rankedCenterIdList.values():
            count += 1
            rankedCenterIdList[count] = keys

#print the final dictionary.
print(rankedCenterIdList)

#### P3.3.Bonus/Required ####

#### P3.3 Bonus/Required ####






