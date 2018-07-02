import websocket
import subprocess
import os
import signal
import random

try:
    import thread
except ImportError:
    import _thread as thread
import time

WSSERVER = 'ws://localhost:8080'
STREAMSERVER = 'http://localhost:8080'
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1YjEyODczZGQ1ZDU3NmZmMTQ0MDNlMDMiLCJsZWFzZXJfaWQiOiI1YjBlNDE2NWY3ZGI5MTZkMjIwOWU0Y2YiLCJtb2RlbCI6IlYxIiwic3RhcnRfZGF0ZSI6IjIwMTgtMDYtMDJUMTI6MDI6MDUuMDcyWiIsIl9fdiI6MCwiaXNfcm9ib3QiOnRydWUsImlhdCI6MTUyODQyMTkwMX0.N7wCginHLLpL92mo9yQExbrY-4xxhwImRnldZydo5cA'

def on_message(ws, message):
    if message == 'start':
        print('starting...')
        cmd = 'ffmpeg -s 1280x720 -f avfoundation -framerate 30 -i "0" -f mpegts -codec:v mpeg1video -b 800k -r 30 ' + \
            STREAMSERVER + '/api/robot/stream?token=' + TOKEN
        pro = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                               preexec_fn=os.setsid)
        ws.proid = pro.pid
    elif message == 'end':
        os.killpg(os.getpgid(ws.proid), signal.SIGTERM)
        ws.proid = None
        print('killed')
    else:
        print('received', message)


def on_error(ws, error):
    if hasattr(ws, 'proid') and ws.proid != None:
        os.killpg(os.getpgid(ws.proid), signal.SIGTERM)
        ws.proid = None
    print(error)


def on_close(ws):
    if hasattr(ws, 'proid') and ws.proid != None:
        os.killpg(os.getpgid(ws.proid), signal.SIGTERM)
        ws.proid = None
    print("### closed ###")


def on_open(ws):
    print('### opened ###')
    

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WSSERVER + "/robot?token=" + TOKEN,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    while True:
          sample_gps_data = '{ "x": %.4f, "y": %.4f }' % (random.random() * 100, random.random() * 100)
          print('sending', sample_gps_data)
          print(time.time() * 1000)
          ws.send(sample_gps_data)
          time.sleep(3)

