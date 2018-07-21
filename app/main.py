import os
import sys
import json
import time
import requests
import subprocess
import threading
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from imutils.video import WebcamVideoStream
from camera import KivyCamera
from storage import Storage
import config

presentation = Builder.load_file("main.kv")
# Config.set('graphics', 'resizeable', '0')


class ScreenManagement(ScreenManager):
    pass

##### WAREHOUSE SCREEN #######   
class MainScreen(Screen):
    pass

##### PARCEL LOADING SCREEN #######
class LoadScreen(Screen):
  def on_enter(self, **kwargs):
    captured = App.get_running_app().check_capture()
    if captured: 
      self.ids.scanner.start(mode="load", capture=capture)
        
  def exit_scan(self):
    self.ids.scanner.stop()
    self.manager.current = "main"
    print("exit scanner called")

  def go_to_unlock(self):
    self.ids.scanner.stop()
    self.manager.current = "unlock"
    
    
##### UNLOCKING LOCKER SCREEN #######  
class UnlockScreen(Screen):
    def on_enter(self):
        start = time.time()
        captured = App.get_running_app().check_capture()
        if captured: 
            self.ids.scanner.start(mode="unlock", capture=capture)
            self.timer = threading.Timer(120.0, self.exit_scan).start()

    def exit_scan(self):
        try: 
            self.timer.cancel()
        except AttributeError:
            pass
        self.ids.scanner.stop()
        self.manager.current = "rest" 


##### UNLOCK REST SCREEN #######
class RestScreen(Screen):
    pass


##### KEYIN SCREEN #######
class KeyinScreen(Screen):

    def unlock(self, string):
        unlocked = Storage().manual_unlock(string)
        self.manager.current = 'rest'

  
class MainApp(App):
    def build(self):
        self.on_capture()
        return ScreenManagement()
    
    def on_capture(self, *args):
        self.t = threading.Thread(target=self.load_websocket).start()
        global capture 
        capture = WebcamVideoStream(src=0).start()
        self.check_capture()
        
    def check_capture(self):
        global capture
        if not capture:
            box = FloatLayout()
            label = Label(text="Camera not detected!", color=(0,0,0,1))
            button = Button(text="Try again", 
                    pos_hint={'center_x':0.5, 'center_y':0.3})
            button.bind(on_press=self.on_capture)
            box.add_widget(label)
            box.add_widget(button)
            
            popup = Popup(title="Error",
                        content=box,
                        size_hint=(None, None), size=(400, 400))
            popup.open()
            self.t.join()
            return False
        return True


    def on_stop(self):
        global capture
        if capture: 
            capture.stop()
            capture = None
            self.t.join()

    def load_resource(self, string):
        return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources/'+string))            
  
    def load_websocket(self):
        # print("loading websocket")
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
