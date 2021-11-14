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
action_received = False
action = ''
test = ''

    
def send_message(channel, text):
    data = {'token': API_TOKEN,
            'channel': channel,
            'text': text}
    requests.post(url='https://slack.com/api/chat.postMessage', data=data)
    

def on_message(ws, message):
    
    # Get global variables
    global training_time
    global testing_time
    global action_received
    global action
    global test
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
 
    # Start training upon user request!
    if text.lower() == 'testing time' and testing_time == False and training_time == False:
        send_message(channel, "I'm training my brain with the data you've already given me...\nOK, I'm ready for testing. Write me something and I'll try to figure it out.")
        testing_time = True
        
    # Identify action.
    elif text.lower() != 'testing time' and testing_time == True and training_time == False and text.lower() != 'done':
        brain = pickle.load(open("jarvis_MOUNTAINTIGER.pkl", 'rb'))
        result = brain.predict([text.lower()])
        send_message(channel, "Ok, I think the action you mean is `{}`.\nWrite me something else an I'll try and figure it out.".format(result[0]))  
        if result[0] == "TIME":
            send_message(channel, "Do you wanna start a schedule: yes or no?")
            if text[0].lower== 'y':
                schedule =[]
                while True:
                    send_message(channel, "What do you want the date and time to be?")
                    date_time = text
                    send_message(channel, "What is the event for?")
                    event_class = text
                    send_message(channel, "What is the event?")
                    event_description = text
                    if len(schedule) == 0:
                        schedule.append(Event(date_time, event_class, event_description))
                    else:
                        for event in schedule:
                            if event == Event(date_time, event_class, event_description):
                                send_message(channel, "There is conflicting times with this new event with: ")
                                send_message(channel, event)
                                continue
                            else:
                                schedule.append(Event(date_time, event_class, event_description))
                    
                    flag = send_message(channel, "Want to continue: yes or no? ")
                    
                    if flag[0].lower() == 'n':
                        break
                for event in schedule:
                        send_message(channel, event)
    
    # Finish training if requested.
    elif text.lower() == 'done' and testing_time == True:
        testing_time = False
        send_message(channel, "OK, I'm finished testing")            

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
