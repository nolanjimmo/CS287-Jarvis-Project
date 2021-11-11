#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 15:36:24 2021

@author: kateyforsyth
"""

#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 10:56:03 2021
@author: christopheroneil
secind iteration of jarvis's brain. 
"""

import sqlite3
import pickle
import os
import json
import pandas as pd

##### EDA of external data ####

#Upload external data 
os.chdir('/Users/kateyforsyth/Library/Mobile Documents/com~apple~CloudDocs/Graduate/CS287/PRO2_MOUNTAINTIGER')
file_names = os.listdir('data')
raw_data = []
#Read through each file and store into a list of strings
file_names.remove('.DS_Store')
for filename in file_names:
    
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

data_frame = pd.DataFrame(data = raw_data)

from sklearn.model_selection import train_test_split
# conn = sqlite3.connect("../jarvis.db")
# c = conn.cursor()

# # Fetches column txt from data base which containes questions.
# c.execute("SELECT txt FROM training_data")
# txt = c.fetchall()

# # Fetches action column from data base
# c.execute("SELECT action FROM training_data")
# action = c.fetchall()

# Converting the list of tuples to list of strings.
#X = ["%s" % x for x in txt]
X = data_frame["TXT"]
    
y = data_frame["ACTION"]

# Transorm labels to labels that the classifier can use.



# Split the data into training and testing sets. 
X_train, X_test , y_train, y_test = train_test_split(X,y, test_size = .2, random_state = 42)

# Contruct a pipeline that will convert X_train and X_test to count vectors
# then train on X_train, then predict on X_test.
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('clf', svm.SVC(C = 10, kernel = "rbf", gamma = .01)),
     ])

text_clf.fit(X_train, y_train)
prediction = text_clf.predict(X_test)

# Display a classifcation report
from sklearn.metrics import classification_report
print(classification_report(y_test, prediction)) 


test = text_clf.predict(["what pizza do you like"])

print(test)



# Save the model to the named file 
file = "jarvis_MOUNTAINTIGER.pkl"
pickle.dump(text_clf, open(file, "wb"), pickle.HIGHEST_PROTOCOL)



###################### TESTING FOR HYPERPARAMS ################################

# Using grid search and cross validation the best hyper params were found
# and put into the model above. 
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
X_test_counts = count_vect.fit_transform(X_test)
from sklearn.model_selection import GridSearchCV
# Preform a grid search to find the best parameters 
params = {"C" : [.1,1.0,10,100],
              "kernel" : ["linear", "rbf"],
              "gamma" : [1,.01,.001, .0001]}

grid = GridSearchCV(svm.SVC(), params, refit=True, verbose = 3)
grid.fit(X_train_counts, y_train)
print(grid.best_params_)
print(grid.best_estimator_) 


###################### TESTING FOR HYPERPARAMS ################################