import os
import json
import requests
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
Config.set('graphics', 'resizeable', '0')


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
        res = requests.post(config.URL+'api/parcel/unlock', json=data, headers=robot_auth)
        print(res.json)
        if (res.status_code == requests.codes.ok):
            Storage().get_parcel(id)
        else: 
            print("Server error")
        self.manager.current = 'main'


  
class MainApp(App):
    
    def build(self):
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
  
if __name__ == '__main__':
    MainApp().run()
