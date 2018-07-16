import websocket
import subprocess
import os
import signal
import gpsd
import config

try:
    import thread
except ImportError:
    import _thread as thread
import time

WSSERVER = 'ws://10.12.54.167:8080'
STREAMSERVER = 'http://10.12.54.167:8080'
TOKEN = config.ROBOT_TOKEN



def get_gpsloc():
    gpsd.connect()
    packet = gpsd.get_current()
    print(packet)
    return packet.lat, packet.lon 
    

def on_message(ws, message):
    if message == 'start':
        print('starting...')
        
        # for mac: ffmpeg -s 1280x720 -f avfoundation -framerate 30 -i "0" -f mpegts -codec:v mpeg1video -b 800k -r 30 
        cmd = 'ffmpeg -s 640x480 -f video4linux2 -i /dev/video0 -f mpegts -codec:v mpeg1video -b 147456k -r 30 ' + \
            STREAMSERVER + '/api/robot/stream?token=' + TOKEN
        pro = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                               preexec_fn=os.setsid)
        print(cmd)
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
    print("error: ", error)


def on_close(ws):
    if hasattr(ws, 'proid') and ws.proid != None:
        os.killpg(os.getpgid(ws.proid), signal.SIGTERM)
        ws.proid = None
    print("### closed ###")
    raise Exception('Websocket closed')


def on_open(ws):
    print('### opened ###')
    def run(*args):
        while True:
        # x, y = get_gpsloc()
            sample_gps_data = '{ "x": %.4f, "y": %.4f }' % (100, 100)
            print('sending', sample_gps_data)
            ws.send(sample_gps_data)
            time.sleep(3) 
    thread.start_new_thread(run, ())
    

        
    
    

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WSSERVER + "/robot?token=" + TOKEN,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    # ws.run_forever()
    
    ws.run_forever()

