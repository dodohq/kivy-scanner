import os
import sys
import json
import requests
import subprocess
import threading
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from imutils.video import WebcamVideoStream
from camera import KivyCamera
from auth import HEADERS
import config

presentation = Builder.load_file("main.kv")
# Config.set('graphics', 'resizeable', '0')


class ScreenManagement(ScreenManager):
  pass

##### HOME SCREEN #######   
class MainScreen(Screen):
    pass

##### PARCEL LOADING SCREEN #######
class LoadScreen(Screen):
  def load_scanner(self, **kwargs):
    self.ids.scanner.start(mode="load", capture=capture)
    
  def exit_scan(self):
    self.ids.scanner.stop()
    self.manager.current = "main"
    print("exit scanner called")
    
##### UNLOCKING LOCKER SCREEN #######  
class UnlockScreen(Screen):
  def on_enter(self):
    self.ids.scanner.start(mode="unlock", capture=capture)

  def exit_scan(self):
    self.ids.scanner.stop()
    self.manager.current = "main" 
    print("exit scanner called")

##### UNLOCK LOGIN SCREEN #######
class LoginScreen(Screen):
    def unlock(self, id, password):
        robot_auth = {'Content-Type': 'application/json', 'Authorization': config.ROBOT_TOKEN}
        data = {"id" : id, "password": password}
        res = requests.post(config.URL+'/api/parcel/unlock', json=data, headers=robot_auth)
        print(res.json)
        if (res.status_code == requests.codes.ok):
            Storage().get_parcel(id)
        else: 
            print("Server error")
        self.manager.current = 'main'


  
class MainApp(App):
    
    def build(self):
        t = threading.Thread(target=self.load_websocket).start()
        global capture 
        capture = WebcamVideoStream(src=1).start()
        return ScreenManagement()
    
    def on_stop(self):
        global capture
        if capture: 
            capture.stop()
            capture = None

    def load_resource(self, string):
        return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources/'+string))            
  
    def load_websocket(self):
        print("loading websocket")
        path = os.path.abspath(os.path.dirname(__file__))

        try:
          p = subprocess.Popen([sys.executable, path+'/testffmpeg.py'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
       
          # while child process has not yet terminated 
          while p.poll() is not None and p.poll() is not None:
            print("comm: ", p.communicate())
            print("return: ", p.returncode)
          error = p.communicate()[0]
        except ValueError:
          popup = Popup(title="Error",
                        content=Label(text="""Internal Websocket Error:
                        \nThe robot couldn't connect to the websocket.
                        \nTrying again..\n""",
                        color=(0,0,0,1) ),
                        size_hint=(None, None), size=(400, 400))
          popup.open()
        
        self.load_websocket()
        
        
if __name__ == '__main__':
    MainApp().run()
