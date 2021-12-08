# Homework 06
# [Please replace this comment with your name]


"""
*** DESCRIBE YOUR CODE ORGANIZATION HERE ***
"""


#################### PLEASE PLACE ALL IMPORTS HERE #####################
#import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import gzip
import json
import csv
import traceback
import matplotlib.pyplot as plt
import numpy as np
import datetime
########################################################################


################ PLEASE DEFINE ANY HERE FUNCTIONS HERE #################

def contains_obama (text ):
    """ Checks the string ` text ` for mention of Obama. Is
    case - insensitive .
    """
    text = text.lower () # good idea or not ...
    if "obama" in text or "barack" in text:
        return True
    return False
    
def contains_romney (text):
    """ Checks the string ` text ` for mention of Romney. Is
    case - insensitive .
    """
    text = text.lower ()
    if "romney" in text or "mitt" in text:
        return True
    return False

def load_tidy(filename):
    f_O_scores = {}
    f_R_scores = {}
    s_O_scores = {}
    s_R_scores = {}
    try:
        with open(filename) as in_file:
            csv_reader = csv.reader(in_file)
            for row in csv_reader:
                if row[0] == "t_id":
                    continue
                if row[1] == "4_O":
                    f_O_scores[row[0]] = {"neg": row[2], "neu":row[3], "pos":row[4], 
                                          "compound":row[5], "dt_obj":row[6]}
                if row[1] == "4_R":
                    f_R_scores[row[0]] = {"neg": row[2], "neu":row[3], "pos":row[4], 
                                          "compound":row[5], "dt_obj":row[6]}
                if row[1] == "6_O":
                    s_O_scores[row[0]] = {"neg": row[2], "neu":row[3], "pos":row[4], 
                                          "compound":row[5], "dt_obj":row[6]}
                if row[1] == "6_R":
                    s_R_scores[row[0]] = {"neg": row[2], "neu":row[3], "pos":row[4], 
                                          "compound":row[5], "dt_obj":row[6]}
                    
        in_file.close()
        return f_O_scores, f_R_scores, s_O_scores, s_R_scores
    except Exception:
        traceback.print_exc()
        return False, False, False, False

#x, y, z, w = load_tidy("nothing")
#print(x, y, z, w)
########################################################################




##################### ORGANIZE YOUR WORK HERE ##########################
######### Using P.x header comments to separate code blocks ############
########################################################################


######## P.0 ###########################################################

######## P.1 ###########################################################
VADER = SentimentIntensityAnalyzer()
LEX_DICT = VADER.make_lex_dict()
LEN_LEXICON = len(LEX_DICT.keys())
print("There are", LEN_LEXICON, "tokens in the VADER lexicon")
######## P.2 ###########################################################
#P2.1
filename = "HW06_twitterData.json.txt.gz"

#opening file
in_file = gzip.open(filename , 'rt', encoding ='utf -8')
month_conversions = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sept":9, "Oct":10, "Nov":11, "Dec":12}


O_tweets = []
R_tweets = []
HW04_o_tweets = []
HW04_r_tweets = []
for line in in_file:
    if line[0] != "{":
        line = "{" + line
        #error_count["{"] = error_count["{"] + 1
    if line[len(line)-2] != "}":
        line = line + "}"
        #error_count["}"] = error_count["}"] + 1
    
    tweet = json.loads(line.strip())

    text = tweet["text"]
    id_ = tweet["id"]
    dt_obj = datetime.datetime(int(tweet["created_at"][12:16]), month_conversions[tweet["created_at"][8:11]], int(tweet["created_at"][5:7]), int(tweet["created_at"][17:19]))

    
    if contains_obama(text):
        O_tweets.append((id_, text, dt_obj))
    if contains_romney(text):
        R_tweets.append((id_, text, dt_obj))
        
    #P2.2
    #simulating my filtering from HW04
    if "mitt" in text.lower() or "romney" in text.lower():
        HW04_r_tweets.append((id_, text, dt_obj))
    if "barack" in text.lower() or "obama" in text.lower() or "barry" in text.lower():
        HW04_o_tweets.append((id_, text, dt_obj))
in_file.close()      
#print(O_tweets[0]["text"])
#print(R_tweets[0]["text"])

#P2.2 Continued
#comparison between HW04 and HW06
#print(len(HW04_o_tweets))
#print(len(HW04_r_tweets))
#print(len(R_tweets))
#print(len(O_tweets))

one_one = 0
one_two = 0
two_one = 0
two_two = 0

#HW04_o_tweets = set(HW04_o_tweets)
HW04_o_tweets = set(x for x in HW04_o_tweets)
HW04_r_tweets = set(x for x in HW04_r_tweets)
O_tweets = set(x for x in O_tweets)
R_tweets = set(x for x in R_tweets)
total_tweets = O_tweets.union(R_tweets)

one_one = len(O_tweets.intersection(HW04_o_tweets))
one_two = len(R_tweets.intersection(HW04_o_tweets))
two_one = len(O_tweets.intersection(HW04_r_tweets))
two_two = len(R_tweets.intersection(HW04_r_tweets))

print("              Obama(HW04) Romney(HW04)")
print(f"{'Obama(HW06)':>14} {one_one:>7} {one_two:>11}")
print(f"{'Romney(HW06)':>14} {two_one:>7} {two_two:>11}")

###P2.3###
HW04_o_results = None
HW04_r_results = None
O_results = None
R_results = None

HW04_o_results, HW04_r_results, O_results, R_results = load_tidy("OR_tweet_scores_njimmo.csv")
#if csv has not been created, populate our scores now
if HW04_o_results == False:
    print('here')
    HW04_o_results = {}
    HW04_r_results = {}
    O_results = {}
    R_results = {}
    for t in total_tweets:
        if t in HW04_o_tweets:
            HW04_o_results[t[0]] = VADER.polarity_scores(t[1])
        if t in HW04_r_tweets:
            HW04_r_results[t[0]] = VADER.polarity_scores(t[1])
        if t in O_tweets:
            O_results[t[0]] = VADER.polarity_scores(t[1])
        if t in R_tweets:
            R_results[t[0]] = VADER.polarity_scores(t[1])
        
    #print(R_results)

#As well, if .csv done not exist, create and populate it with our scores for next time

    #Creating tidy CSV file
    with open('OR_tweet_scores_njimmo.csv', 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['t_id', 'corpa', 'neg', 'neu', 'pos', 'compound', 'dt_obj'])
        for s in HW04_o_tweets:
            writer.writerow([s[0], '4_O', HW04_o_results[s[0]]["neg"], HW04_o_results[s[0]]["neu"], 
                HW04_o_results[s[0]]["pos"], HW04_o_results[s[0]]["compound"], s[2]])
        for s in HW04_r_tweets:
            writer.writerow([s[0], '4_R', HW04_r_results[s[0]]["neg"], HW04_r_results[s[0]]["neu"], 
                HW04_r_results[s[0]]["pos"], HW04_r_results[s[0]]["compound"], s[2]])
        for s in O_tweets:
            writer.writerow([s[0], '6_O', O_results[s[0]]["neg"], O_results[s[0]]["neu"], 
                O_results[s[0]]["pos"], O_results[s[0]]["compound"], s[2]])
        for s in R_tweets:
            writer.writerow([s[0], '6_R', R_results[s[0]]["neg"], R_results[s[0]]["neu"], 
                R_results[s[0]]["pos"], R_results[s[0]]["compound"], s[2]])
    out_file.close()


### P3 ###
#I am going to just use the HW06 Obama and Romney Results here, rather than
#all 4 corpora

O_values = {"neg":[], "neu":[], "pos":[], "compound":[]}
R_values = {"neg":[], "neu":[], "pos":[], "compound":[]}

for _,o in O_results.items():
    O_values["neg"].append(float(o["neg"]))
    O_values["neu"].append(float(o["neu"]))
    O_values["pos"].append(float(o["pos"]))
    O_values["compound"].append(float(o["compound"]))
   
for _,r in R_results.items():
    R_values["neg"].append(float(r["neg"]))
    R_values["neu"].append(float(r["neu"]))
    R_values["pos"].append(float(r["pos"]))
    R_values["compound"].append(float(r["compound"]))
    
#plotting initial histograms
#Obama neg, neu, pos 
plt.hist(O_values["neg"], bins=50, color="blue", alpha=.5)
plt.hist(O_values["pos"], bins=50, color="red", alpha=.5)
plt.hist(O_values["neu"], bins=50, color="green", alpha=.5)
plt.xlabel("Polarity Values")
plt.ylabel("Counts")
plt.title("Obama")
plt.legend(["Negative", "Positive", "Neutral"])
plt.show()

#Romney neg, neu, pos
plt.hist(R_values["neg"], bins=50, color="blue", alpha=.5)
plt.hist(R_values["pos"], bins=50, color="red", alpha=.5)
plt.hist(R_values["neu"], bins=50, color="green", alpha=.5)
plt.xlabel("Polarity Values")
plt.ylabel("Counts")
plt.title("Romney")
plt.legend(["Negative", "Positive", "Neutral"])
plt.show()

#compound scores
#Obama
plt.hist(O_values["compound"], bins=50, color="blue", alpha=.5)
plt.hist(R_values["compound"], bins=50, color="red", alpha=.5)
plt.xlabel("Polarity Values")
plt.ylabel("Counts")
plt.title("Compound ")
plt.legend(["Obama", "Romney"])
plt.show()

##Remove 0 and 1 values from all value arrays
for k, v in O_values.items():
    arr = []
    for i in v:
        if i > .05 and i < .95:
            arr.append(i)
    O_values[k] = arr

for k, v in R_values.items():
    arr = []
    for i in v:
        if i > .05 and i < .95:
            arr.append(i)
    R_values[k] = arr

###### After removal of "missing" data, plot the same histograms
#plotting initial histograms
#Obama neg, neu, pos 
plt.hist(O_values["neg"], bins=100, color="blue", alpha=.5)
plt.hist(O_values["pos"], bins=100, color="red", alpha=.5)
plt.hist(O_values["neu"], bins=100, color="green", alpha=.5)
plt.xlabel("Polarity Values")
plt.ylabel("Counts")
plt.title("Obama Adjusted")
plt.legend(["Negative", "Positive", "Neutral"])
plt.show()

#Romney neg, neu, pos
plt.hist(R_values["neg"], bins=100, color="blue", alpha=.5)
plt.hist(R_values["pos"], bins=100, color="red", alpha=.5)
plt.hist(R_values["neu"], bins=100, color="green", alpha=.5)
plt.xlabel("Polarity Values")
plt.ylabel("Counts")
plt.title("Romney Adjusted")
plt.legend(["Negative", "Positive", "Neutral"])
plt.show()

#compound scores
#Obama
plt.hist(O_values["compound"], bins=100, color="blue", alpha=.5)
plt.hist(R_values["compound"], bins=100, color="red", alpha=.5)
plt.xlabel("Polarity Values")
plt.ylabel("Counts")
plt.title("Compound ")
plt.legend(["Obama", "Romney"])
plt.show()

###Compute Simple Stats for each Candidate
# Still excluding "0" and "1" values
O_means = {}
R_means = {}
O_tot = 0
R_tot = 0

for k, v in O_values.items():
    O_means[k] = np.mean(v)
    O_tot += len(v)
    
for k, v in R_values.items():
    R_means[k] = np.mean(v)
    R_tot += len(v)

print("        Means:     Neg      Neu    Pos      Compound      NUM(sum)")
print(f"Obama: {O_means['neg']:>15,.2f} {O_means['neu']:>8,.2f} {O_means['pos']:>7,.2f} {O_means['compound']:>10,.2f} {O_tot:>14}")
print(f"Romney: {R_means['neg']:>14,.2f} {R_means['neu']:>8,.2f} {R_means['pos']:>7,.2f} {R_means['compound']:>10,.2f} {R_tot:>14}")

###Time Series Data
O_time_series = []
R_time_series = []
for k, v in O_results.items():
    O_time_series.append([k, v['neg'], v['neu'], v['pos'], v['compound'], v['dt_obj']])
for k, v, in R_results.items():
    R_time_series.append([k, v['neg'], v['neu'], v['pos'], v['compound'], v['dt_obj']])
    
O_time_series.sort(key=lambda x:x[5])
R_time_series.sort(key=lambda x:x[5])


if datetime.datetime.strptime(O_time_series[0][5], '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(R_time_series[0][5], '%Y-%m-%d %H:%M:%S'):
    first_time = datetime.datetime.strptime(O_time_series[0][5], '%Y-%m-%d %H:%M:%S')
else:
    first_time = datetime.datetime.strptime(R_time_series[0][5], '%Y-%m-%d %H:%M:%S')

#I have commented out the lines below which were my attempt at the plotting, so that everying above runs as it should and the program
#does not exit with any errors
'''
if divmod((first_time - datetime.datetime.strptime(O_time_series[len(O_time_series)-1][5], '%Y-%m-%d %H:%M:%S')).total_seconds(), 3600)[5] > divmod((first_time - datetime.datetime.strptime(R_time_series[len(R_time_series)-1][5], '%Y-%m-%d %H:%M:%S')).total_seconds(), 3600)[5]:
    last_time = datetime.datetime.strptime(O_time_series[len(O_time_series)-1][5], '%Y-%m-%d %H:%M:%S')
else:
    last_time = datetime.datetime.strptime(R_time_series[len(R_time_series)-1][5], '%Y-%m-%d %H:%M:%S')

  
time_since_dict = {}
for i in range(int(divmod((last_time-first_time).total_seconds(), 3600)[0])+1):
    time_since_dict[i] = [0,0]
    
for o in range(len(O_time_series)-1):
    time_since_dict[int(divmod((O_time_series[o][0] - first_time).total_seconds(),3600)[0])][0] += 1
for r in range(len(R_time_series)-1):
    time_since_dict[int(divmod((R_time_series[r][0] - first_time).total_seconds(),3600)[0])][1] += 1
    
    
plt.plot(time_since_dict[0],time_since_dict[1], color='C0', label='Obama')
plt.plot(time_since_dict[0],time_since_dict[1], color='C3', label='Romney')

plt.xlabel(r"Time [hours]")
plt.ylabel("Number of tweets")
plt.legend(loc='upper left')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.title("Time Series Polarity Data", fontsize='small')
'''