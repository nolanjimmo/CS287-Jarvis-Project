# PR02 Jarvis Instantiantion CS287
# Nolan Jimmo, Tucker Paron, Katey Forsyth, Chris O'Neil

# TOKENS

with open("tokens.txt", 'r') as infile:
    lines = infile.readlines()
infile.close()

API_TOKEN = lines[0].strip()
APP_TOKEN = lines[1].strip()

# IMPORTS
import websocket
import requests
import json
import time
import pickle
from dataInsertion import addVals
from Event import Event
from Weather import Weather
try:
    import thread
except ImportError:
    import _thread as thread


# Global Variables for training mode switch and testing mode switch
training_time = False # Training Mode Switch
testing_time = False # Testing Mode Switch
scheduler_time = False # Scheduling app switch
action_received = False
classified = False
q1 = False
q2 = False
q3 = False
w1 = True
w2 = False
action = ''
test = ''
date_time = ''
event_class = ''
event_description = ''
result = None
schedule = []
w = None

    
def send_message(channel, text):
    data = {'token': API_TOKEN,
            'channel': channel,
            'text': text}
    requests.post(url='https://slack.com/api/chat.postMessage', data=data)
    

def on_message(ws, message):
    
    # Get global variables
    global training_time
    global testing_time
    global scheduler_time
    global action_received
    global classified
    global q1, q2, q3, w1, w2
    global action, test
    global date_time, event_class, event_description
    global result
    global schedule
    global w
    text = ''
    
    # This is the user value for when our bot sends messsages
    # We will be using this to make sure Jarvis doesn't respond to itself
    bot = 'U02GCL03FSR'

    # Use envelope_id field to send a response of acknowledgement back to Slack.
    message = json.loads(message)
    print(message['payload']['event']['text'])
    envelope_id = message['envelope_id']
    resp = {'envelope_id': envelope_id}
    ws.send(str.encode(json.dumps(resp)))

    channel = message['payload']['event']['channel']
    text = message['payload']['event']['text']
    sent_from = message['payload']['event']['user']
    
    if sent_from == bot:
        return
    
    # print("CURRENT TEXT:", text)
    
 ##### TRAINING TIME
    
    # Get the first action and ask for more.
    if text.lower() != 'training time' and training_time == True and testing_time == False:
        if action_received == False and text.lower() != 'done':
            action = text.upper()
            send_message(channel, "Ok, let's call this action `{}`. Now give me some training text!".format(action))
            action_received = True # First action receieved.
            
        # Receive next action.
        elif action_received == True and text.lower() != 'done':
            action = text.upper()
            print(f"Entering {action}: {text}     in to database")
            send_message(channel, "OK, I've got it! what else?")
            addVals(text, action)
        
        # Finish training if requested.
        else:
            action_received = False
            training_time = False
            send_message(channel, "OK, I'm finished training")
    
    # Start training upon user request!
    elif text.lower() == 'training time' and training_time == False and testing_time == False:
        
        # Respond asking for action name using requests.posts method.
        send_message(channel, "OK, I'm ready for training. What NAME should this ACTION be?")
                
        # Enable training mode!
        training_time = True
    
##### TESTING TIME
    if text.lower() == 'testing time' and testing_time == False and training_time == False:
        send_message(channel, "I'm training my brain with the data you've already given me...\nOK, I'm ready for testing. Write me something and I'll try to figure it out.")
        testing_time = True
        return
        
    if text.lower() != 'testing_time' and testing_time == True:
        send_message(channel, "Type something for me to classify and test if I am correct")
        brain = pickle.load(open("jarvis_MOUNTAINTIGER.pkl", 'rb'))
        result = brain.predict([text.lower()])
        send_message(channel, "Ok, I think the action you mean is `{}`.".format(result[0])) 
        return 
 
##### IMPLEMENTATION
    # help message
    if text.lower() == 'help':
        send_message(channel, "This is an app that will help with routine, automatable things/")
        send_message(channel, "Type something to do with time and follow the prompts!")
        send_message(channel, "Follow the prompts to assign a date/time, category and name for each event you would like to add.")
        send_message(channel, "Dates must be entered in DD-MM-YYYY HH:MMAM, where AM can be AM or PM, and must not be separated from the time numbers with a space")
                     
    # Identify action.
    if text.lower() == 'day planner time' and scheduler_time == False:
        send_message(channel, "Opening day planner app...")
        scheduler_time = True
    
    elif text.lower() != 'testing time' and text.lower() != "day planner time" and scheduler_time == True and text.lower() != 'done' and text.lower() != 'help':
        if classified == False:
            brain = pickle.load(open("jarvis_MOUNTAINTIGER.pkl", 'rb'))
            result = brain.predict([text.lower()])
            #send_message(channel, "Ok, I think the action you mean is `{}`.".format(result[0]))  
        if classified == False and result[0] == 'TIME':
            classified = True
            send_message(channel, "Do you wanna start a schedule: yes or no?")
        elif classified == True and result[0] == 'TIME':
            if text[0].lower() == 'y':
                send_message(channel, "What do you want the date and time to be?")
                q1 = True
                return
            elif text[0].lower() == 'n':
                classified = False
                result = None
                send_message(channel, "Here is your schedule: ")
                for event in schedule:
                    send_message(channel, f"{event.get_date_time()}:  {event.get_event_description()}")
                send_message(channel, "Type something new to be classified")
                return
            if q1:
                date_time = text
                send_message(channel, "What is the event for?")
                q2 = True
                q1 = False
                return
            if q2:
                event_class = text
                send_message(channel, "What is the event?")
                q3 = True
                q2 = False
                return
            if q3:
                event_description = text
                q3 = False
            if len(schedule) == 0:
                schedule.append(Event(date_time, event_class, event_description))
                send_message(channel, f"Event added to your schedule: {schedule[len(schedule)-1].get_date_time()} {schedule[len(schedule)-1].get_event_description()}")
            else:
                new_event = Event(date_time, event_class, event_description)
                for event in schedule:
                    if event.get_date_time() == new_event.get_date_time():
                        send_message(channel, "There is conflicting times with this new event with: ")
                        send_message(channel, event.get_event_description())
                        send_message(channel, "New Event not added to your schedule")
                        continue
                    else:
                        schedule.append(new_event)
                        send_message(channel, f"Event added to your schedule: {schedule[len(schedule)-1].get_date_time()} {schedule[len(schedule)-1].get_event_description()}")
                        break
            send_message(channel, "Want to continue: yes or no? ")
            
        #Weather section of the app
        if classified == False and result[0] == 'WEATHER':
            classified = True
            send_message(channel, "What is the zipcode of your desired weather?")
        elif classified == True and result[0] == 'WEATHER':
            if w1:
                w = Weather(text)
                send_message(channel, "Okay, do you want the full report or a specific? (enter the corresponding number)")
                send_message(channel, "1. Temp 2. Description 3. Wind Speed 4. Humidity 5. Full report")
                w1 = False
                w2 = True
                return
            if w2:
                if text == "1":
                    send_message(channel, f"Temp: {w.get_temp()}F")
                elif text == "2":
                    send_message(channel, f"Description: {w.get_weather_description()}")
                elif text == "3":
                    send_message(channel, f"Wind Speed: {w.get_wind_speed()} mph")
                elif text == "4":
                    send_message(channel, f"Humidity: {w.get_humidity()}")
                elif text == "5":
                    send_message(channel, f"{w.get_weather()}")
                elif text.lower() == "d":
                    w1 = True
                    w2 = False
                    classified == False
                    result = None
                    return
                send_message(channel, "Choose another detail or press 'd' to be done.")
                
                    
    
    # Finish training if requested.
    elif text.lower() == 'done':
        if testing_time:
            send_message(channel, "OK, I'm done testing")
        testing_time = False
        if training_time:
            send_message(channel, "OK, I'm done training")
        training_time = False
        if scheduler_time:
            send_message(channel, "OK, scheduler app will now close")
        scheduler_time = False            

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        # for i in range(3):
        #     time.sleep(1)
        #     ws.send("Hello %d" % i)
        # time.sleep(20)
        # ws.close()
        print("Thread starting...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(False)
    headers = {'Content-type':'application/x-www-form-urlencoded', 'Authorization': f'Bearer {APP_TOKEN}'}
    url = requests.post('https://slack.com/api/apps.connections.open', headers=headers).json()["url"]
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
