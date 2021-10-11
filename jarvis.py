# PR01 Jarvis Instantiantion CS287
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
from dataInsertion import addVals


try:
    import thread
except ImportError:
    import _thread as thread
import time

##Global Variables for training mode switch
training_time = False # Training Mode Switch
action_received = False
action = ''

def send_message(channel, text):
    data = {
        'token': API_TOKEN,
        'channel': channel,
        'text': text
        }
    requests.post(url='https://slack.com/api/chat.postMessage', data=data)
    

def on_message(ws, message):
    global training_time
    global action_received
    global action
    text = ''
    
    #This is the user value for when our bot sends messsages
    #We will be using this to make sure Jarvis doesn't respond to itself
    sender = 'U02GCL03FSR'

    # Use envelope_id field to send a response of acknowledgement back to Slack.
    message = json.loads(message)
    envelope_id = message['envelope_id']
    resp = {'envelope_id': envelope_id}
    ws.send(str.encode(json.dumps(resp)))

    channel = message['payload']['event']['channel']
    text = message['payload']['event']['text']
    sent_from = message['payload']['event']['user']
    
    #input message validation, making sure that Jarvis does not respond to
    #itself, and that the message text is not empty
    if sent_from == sender:
        return
    if text == '':
        return
    
    print("CURRENT TEXT:", text)
    print(action_received)
    
    # ACTIONS - Get the first action and ask for more.
    if text.lower() != 'training time' and text.lower() != "done" and training_time == True:
        if action_received == False:
            action = text.upper()
            print(action)
            send_message(channel, "Ok, let's call this action `{}`. Now give me some training text!".format(action))
            action_received = True # First action receieved.
            
        # Receive next action.
        elif action_received == True:
            #action = text.upper()
            print(f"Entering {action}: {text}     in to database")
            addVals(text, action)
            send_message(channel, "OK, I've got it! what else?")
    
    
    # TRAINING TIME - start training upon user request!
    elif text.lower() == 'training time' and training_time == False:
        # Respond asking for action name using requests.posts method.
        send_message(channel, "OK, I'm ready for training. What NAME should this ACTION be?")
                
        # Enable training mode!
        training_time = True
        
    #finish training time on keyword "done"
    elif text.lower() == "done":
        send_message(channel, "OK, I'm finished training")
        training_time = False
        action_received = False
        action = ''

    

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
        print("thread starting...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(False)
    headers = {'Content-type':'application/x-www-form-urlencoded', 'Authorization':f'Bearer {APP_TOKEN}'}
    url = requests.post('https://slack.com/api/apps.connections.open', headers=headers).json()["url"]
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
        
