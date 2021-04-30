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

    @classmethod
    def get_stream(cls):
        if cls.__instance__ is None:
            cls.__instance__ = cls()

        return cls.__instance__

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

    def on_close(self, ws):
        print("### closed ###")
        restart()

    def on_open(self, ws):
        ws.send(json.dumps(config.WS_AUTH))
        ws.send(json.dumps(config.WS_LISTEN))

    def on_message(self, ws, message):
        print("recieved a msg")
        record.write_bar(json.loads(message))


def start_streamer():
    print("## starting streamer!")
    Stream.get_stream()
    Stream.__instance__.start()

def restart():
    print("## going to sleep")
    time.sleep(1)

    print("## collecting garbage")
    Stream.__instance__ = None
    time.sleep(1)

    start_streamer()
    


if __name__ == "__main__":
    websocket.enableTrace(True)
    # start_streamer()   
