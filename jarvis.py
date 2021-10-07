# PR01 Jarvis Instantiantion CS287
# Nolan Jimmo, Tucker Paron, Katey Forsyth, Chris O'Neil

#APP_TOKEN = "xapp-1-A02GFLAUZ0T-2552947742742-90bd24024278ee7f8e78f8b59a2f0fd544ab527688c7b25c2e7d2060dfa81153"

import websocket
import requests
import json


try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    message = json.loads(message)
    envelope_id = message["envelope_id"]
    resp = {"envelope_id": envelope_id }
    ws.send(str.encode(json.dumps(resp )))
    print(message['payload']['event']['text'])

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        #ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(False)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Authorization": "Bearer xapp-1-A02GFLAUZ0T-2552947742742-90bd24024278ee7f8e78f8b59a2f0fd544ab527688c7b25c2e7d2060dfa81153"}
    url = requests.post('https://slack.com/api/apps.connections.open', headers=headers).json()["url"]
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
