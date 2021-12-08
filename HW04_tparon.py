# Homework 04 Problems 1+
# Tucker Paron

# imports
import json 
import gzip
import datetime
from string import punctuation

##############################################################################

tweets = [] # List of tweets
repairs = 0 # Number of repairs

# Open the json file and read the tweets
filename = 'HW04_twitterData.json.txt.gz'
for line in gzip.open(filename, 'rt', encoding='utf-8'):
    
    # Add brackets where necessary and record number of repairs.
    try:
        tweet = json.loads(line.strip())
        tweets.append(tweet) # Add tweet to a list.
    except: 
        if str(line).startswith('{') != True:
            line = '{' + line
            repairs += 1 # Count repairs.
            tweet = json.loads(line.strip())
            tweets.append(tweet) # Add tweet.
        else:
            line = line + '}'
            repairs += 1 # Count repairs.
            tweet = json.loads(line.strip())
            tweets.append(tweet) # Add tweet.
            

print("There were", repairs, "repairs.")
print("There are", len(tweets), "Tweets.")

##############################################################################

obama = ['obama', 'barack', 'barrack', 'barackobama']
romney = ['mitt', 'romney', 'ronmey', 'mittromney']
obama_corpus = [] # Obama tweets
romney_corpus = [] # Romney tweets

# Sort tweets into correct lists.
exclude = set(punctuation) # Keep a set of "bad" characters.
for t in tweets:
    text = t.get('text').lower()
    
    
    ##### THIS CODE TOOK TOO MUCH TIME TO RUN #####
    # # Using punctuation stripping from HW03
    # text_letters_noPunct = [ char for char in text if char not in exclude ]
    # text_noPunct = "".join(text_letters_noPunct) # (http://docs.python.org/3/library/stdtypes.html#str.join)
    # text_list = text_noPunct.strip().split()
    
    
    text_list = text.strip().split()
    for n in text_list:
        if n in obama and t not in obama_corpus:
            obama_corpus.append(t)
        if n in romney and t not in romney_corpus:
            romney_corpus.append(t)

##############################################################################

# Get zero datetime
zero = datetime.datetime.now()
for t in tweets:
    d = datetime.datetime.strptime(t['created_at'], '%a, %d %b %Y %H:%M:%S')
    if d < zero:
        zero = d
zero = zero.replace(minute=0, second=0) # Truncate time


# Iterate through the obama tweets and calculate the difference in hours
# between 'zero' and the current. Keep a dictionary of frequencies for each
# hour.
obama_hours = {} # dictionary for frequency of Obama tweets by hour
for o in obama_corpus:
    d = datetime.datetime.strptime(o['created_at'], '%a, %d %b %Y %H:%M:%S')
    d = d.replace(minute=0, second=0)
    diff = d - zero
    hour = int( diff.total_seconds() / 3600 )
    if hour not in obama_hours:
        obama_hours[hour] = 1
    else:
        obama_hours[hour] += 1

# Do the same for Romney.
romney_hours = {} # dictionary for frequency of Romney tweets by hour
for r in romney_corpus:
    d = datetime.datetime.strptime(r['created_at'], '%a, %d %b %Y %H:%M:%S')
    d = d.replace(minute=0, second=0)
    diff = d - zero
    hour = int( diff.total_seconds() / 3600 )
    if hour not in romney_hours:
        romney_hours[hour] = 1
    else:
        romney_hours[hour] += 1

# Print results in a table by simultaneously iterating through both
# hours dictionaries
f = open('input_p2.txt', 'w')
for h in range(max(len(obama_hours), len(romney_hours))): # Use the larger of the two lists as the range.
    try:    
        print(h, obama_hours[h], romney_hours[h], file = f)
    except:
        if h not in obama_hours and h in romney_hours:
            print(h, 0, romney_hours[h], file = f)
        elif h in obama_hours and h not in romney_hours:
            print(h, obama_hours[h], 0, file = f)
        else:
            print(h, 0, 0, file = f)
f.close() # Close the file!

##############################################################################

oc_freq = {}
for o in obama_corpus:
    o_list = o['text'].strip().split()
    for word in o_list:
        if word not in oc_freq:
            oc_freq[word] = 1
        else:
            oc_freq[word] += 1

rc_freq = {}
for r in romney_corpus:
    r_list = r['text'].strip().split()
    for word in r_list:
        if word not in rc_freq:
            rc_freq[word] = 1
        else:
            rc_freq[word] += 1

combined = {**oc_freq, **rc_freq}
for key in list(combined.keys()):
    if key not in oc_freq or key not in rc_freq:
        del combined[key]
 
coefficient = {}
for key in combined:
    c = ( oc_freq[key] - rc_freq[key] ) / ( oc_freq[key] + rc_freq[key] ) 
    coefficient[key] = c

most_pos = sorted(coefficient, key=coefficient.get, reverse=True)[:100]
most_neg = sorted(coefficient, key=coefficient.get, reverse=False)[:100]
f = open('yule_coefficients.txt', 'w')
for i in range(100):
    print(most_pos[i].rjust(15), str(round(coefficient.get(most_pos[i]), 5)).ljust(10), most_neg[i].rjust(16), str(round(coefficient.get(most_neg[i]), 5)).ljust(10), file=f)
f.close()
    
    
    
#print(coefficient)
#common = {}
 

