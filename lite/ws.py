import websocket
import subprocess
import os
import signal
import threading
import gpsd

try:
    import thread
except ImportError:
    import _thread as thread
import time

WSSERVER = 'ws://backdemo.herokuapp.com'
STREAMSERVER = 'http://backdemo.herokuapp.com'
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1YjU3MmI2ZGE2MTAzZjAwMTRlZDljOTEiLCJsZWFzZXJfaWQiOiI1YjU3MmIyZWE2MTAzZjAwMTRlZDljOGYiLCJtb2RlbCI6IlYxIiwic3RhcnRfZGF0ZSI6IjIwMTgtMDctMjRUMTM6MzY6NDUuMjQ1WiIsIl9fdiI6MCwiaXNfcm9ib3QiOnRydWUsImlhdCI6MTUzMjQzOTQxMH0.STLB_m5NK4YYaxTcEOEaoZIMO2eOHgmeZbUu68Yrgz8"


class dodoWebsocket():
    def __init__(self):
        
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(WSSERVER + "/robot?token=" + TOKEN,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.t = threading.Thread(target=self.start).start()
        self.proid = None

    def start(self):
        self.ws.run_forever()

    def on_message(self, ws, message):
        print('received', message)


    def on_error(self, ws, error):
        print('error', error)


    def on_close(self, ws):
        self.t.join()
        print("### closed ###")


    def on_open(self, ws):
        print('### opened ###')
        def run(*args):
            if self.get_gpsloc():
                x, y = self.get_gpsloc()
            else: 
                x = 100
                y = 100
            sample_gps_data = '{ "x": %.4f, "y": %.4f }' % (x, y)
            print('sending', sample_gps_data)
            ws.send(sample_gps_data)
            time.sleep(3) 
        thread.start_new_thread(run, ())

    def get_gpsloc(self):
        try:
            gpsd.connect()
            packet = gpsd.get_current()
            print(packet)
            return packet.lat, packet.lon 
        except Exception as e:
            print(e)
            pass
