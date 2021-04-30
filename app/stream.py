#!/usr/bin/env python3

import json
import websocket
from app import config, record
import time
try:
    import thread
except ImportError:
    import _thread as thread
import time



class Stream:

    __instance__ = None
    __authorized__ = False

    @classmethod
    def is_alive(cls):
        if cls.__instance__ is not None:
            return True
        return False

    def __init__(self):
        self.ws = websocket.WebSocketApp(
            config.WS_ENDPOINT,
            on_message = self.on_message,
            on_error   = self.on_error,
            on_close   = self.on_close,
            on_open    = self.on_open
        )

    def start(self):
        self.ws.run_forever()

    def on_error(self, ws, error):
        print(error)
        del self

    def on_close(self, ws):
        print("### closed ###")
        del self

    def on_open(self, ws):
        if not Stream.__authorized__:
            ws.send(json.dumps(config.WS_AUTH))
    
        ws.send(json.dumps(config.WS_LISTEN))

    def on_message(self, ws, message):
        print("recieved a msg")
        Stream.__authorized__ = record.write_bar(json.loads(message))


def start_streamer():
    print("## starting streamer!")

    if Stream.is_alive():
        return
    else:
        Stream().start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    # start_streamer()   
