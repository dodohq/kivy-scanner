import websocket
import subprocess
import os
import signal
import config

try:
    import thread
except ImportError:
    import _thread as thread
import time

WSSERVER = 'wss://backdemo.herokuapp.com'
STREAMSERVER = config.URL
TOKEN = config.ROBOT_TOKEN + 'wrong'


def on_message(ws, message):
    if message == 'start':
        cmd = 'ffmpeg -s 1280x720 -f avfoundation -framerate 30 -i "1" -f mpegts -codec:v mpeg1video -b 800k -r 30 ' + \
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
    # raise 
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