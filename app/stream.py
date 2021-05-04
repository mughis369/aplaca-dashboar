#!/usr/bin/env python3

import json
import websocket
from app import record
import config
try:
    import thread
except ImportError:
    import _thread as thread

import time


websocket.enableTrace(True)


class Stream:
    ''' 
    this class implements the structure to communicates with api and manages the 
    websocket connection state to record the incoming messages in a csv 
    '''


    __authorized__ = False
    '''
    this check holds holds the connection state
    '''


    def __init__(self):
        '''
        initilizes the websocket with endpoint and methods to call
        when a specific event ocurs in the stream 
        '''
        self.ws = websocket.WebSocketApp(
            config.WS_ENDPOINT,
            on_message = self.on_message,
            on_error   = self.on_error,
            on_close   = self.on_close,
            on_open    = self.on_open
        )


    def run(self):
        '''
        starts the websocket connection
        '''
        self.ws.run_forever()



    def on_error(self, ws, error):
        '''
        called by websocket when error in connection recieved
        '''
        print(error)
        del self



    def on_close(self, ws):
        '''
        called by websocket when error in connection recieved
        '''
        print("### closed ###")
        del self



    def on_open(self, ws):
        '''
        this methods is called connection open for the first time, 
        '''

        # this check makes sure we only send one authorization 
        # request in the scope of stream 
        if not Stream.__authorized__:
            ws.send(json.dumps(config.WS_AUTH))
    
        # send the json message to start recieveing messages for 
        # symbols set in WS_LISTEN object
        ws.send(json.dumps(config.WS_LISTEN))



    def on_message(self, ws, message):
        '''
        when a message is recieved this method is called
        '''
        print("recieved a msg")

        # message recieved from connection
        message = json.loads(message)

        # analyze the message to detemine its type
        msg_type = self.parse_msg(message)
        
        # record the message into csv if it's data
        if msg_type == 'data':
            print('data')
            # record.write_bar(message)



    def parse_msg(self, msg):
        '''
        analyzes different types of message to determine whether to record
        the message or not 
        '''
        
        alert = ""
        msg_type = 'alpha-beta'
        data = msg.get("data")
        stream_type = msg.get("stream")

        if stream_type == 'listening':
            if data.get('error'):
                Stream.__authorized__ = False
                alert = f"Recieved an error msg:\n {msg}"
                msg_type = 'error'
            else:
                alert = f"Recieved Other Message:\n {msg}"
                msg_type = 'notification'

        elif stream_type == 'authorization':
            if data.get('status') == 'authorized':
                Stream.__authorized__ = True
                alert = f"Auth Success:\n {msg}"
                msg_type = "auth-sxx"
            else:
                Stream.__authorized__ = False
                alert = f"Auth Failed:\n {msg}"
                msg_type = "auth-flx"

        else:
            alert = f"Recieved data:\n {msg}"
            msg_type = 'data'

        print(alert)
        return msg_type


def start():
    '''
    Intilizes and start the stream
    '''
    try:
        print("## starting streamer!")
        s = Stream()
        s.run()
    except Exception as e:
        print(f"Exception: {e}")



# if __name__ == "__main__":

    # start_streamer()
    # start_streamer()   
