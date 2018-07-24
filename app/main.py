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
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from imutils.video import WebcamVideoStream
from camera import KivyCamera
from storage import Storage
from keyboard import Keyboard
from ffmpeg import dodoWebsocket
from popup import LoadingPopup
import config

# presentation = Builder.load_file("main.kv")
Config.set('graphics', 'resizeable', '0')
#Config.set('graphics', 'width', '800')
#Config.set('graphics', 'height', '480')


class ScreenManagement(ScreenManager):
    pass

##### WAREHOUSE SCREEN #######   
class MainScreen(Screen):
    pass

##### PARCEL LOADING SCREEN #######
class LoadScreen(Screen):
    def on_enter(self, **kwargs):
        global socket
        socket.stop_video()
        self.ids.scanner.start(mode="load")
        
    def exit_scan(self):
        global socket
        socket.start_video()
        self.ids.scanner.stop()
        self.manager.current = "main"
        print("exit scanner called")

    def go_to_unlock(self):
        global socket
        socket.start_video()
        self.ids.scanner.stop()
        self.manager.current = "unlock"
    
    
##### UNLOCKING LOCKER SCREEN #######  
class UnlockScreen(Screen):
    def on_enter(self):
        start = time.time()
        global socket
        socket.stop_video()
        self.ids.scanner.start(mode="unlock")
        self.timer = threading.Timer(120.0, self.exit_scan).start()

    def exit_scan(self):
        try: 
            self.timer.cancel()
        except AttributeError:
            pass
        global socket
        socket.start_video()
        self.ids.scanner.stop()
        self.manager.current = "rest" 


##### UNLOCK REST SCREEN #######
class RestScreen(Screen):
    pass

##### KEYIN SCREEN #######
class KeyinScreen(Screen):
    def on_enter(self):
        self.txt = TextInput(size_hint=(.5, .1),
            pos_hint={'center_x': .5, 'center_y': .6},
            id="id",
            keyboard_mode='managed',
            unfocus_on_touch=True)
        self.txt.bind(focus=self.on_focus)
        self.txt.bind(on_touch_up=self.on_touch_up)
        self.add_widget(self.txt)
        
    def on_focus(self, instance, value):
        if value:
            self.kb = Keyboard("number", self.txt)
        else: 
            instance.hide_keyboard()
            return False

    def on_touch_up(self, *args):
        touch = args[0]
        print("touch", *touch.pos)
        if not self.txt.collide_point(*touch.pos):
            print('touched outside keyboard')
            self.txt.focus = False
            Window.release_keyboard(self.kb)
        return super(TextInput, self.txt).on_touch_up(touch)

    def unlock(self):
        string = self.txt.text
        print(string)
        unlocked = Storage().manual_unlock(string)
        self.manager.current = 'rest'


##### LOGIN SCREEN #######
class LoginScreen(Screen):
    def on_enter(self):
        self.username = TextInput(size_hint=(.4, .1),
            pos_hint={'center_x': .6, 'center_y': .7},
            id="username",
            keyboard_mode='managed',
            unfocus_on_touch=True)
        self.username.bind(focus=self.on_focus)
        self.username.bind(on_touch_up=lambda *args:self.on_touch_up('username'))
        self.add_widget(self.username)
        
        self.password = TextInput(size_hint=(.4, .1), 
            pos_hint={'center_x': .6, 'center_y': .5},
            id="password", 
            keyboard_mode='managed',
            unfocus_on_touch=True)

        self.password.bind(focus=self.on_focus)
        self.password.bind(on_touch_up=lambda *args:self.on_touch_up('password'))
        self.add_widget(self.password)

    def on_focus(self, instance, value):
        print('instance:', instance)
        if value:
            if instance == self.username:
                self.u_kb = Keyboard("text", instance)
            elif instance == self.password:
                self.p_kb = Keyboard("text", instance)
        else: 
            instance.release()
            return False

    def on_touch_up(self, *args):
        print(*args)
        touch = args[0]
        if hasattr(args, 'mode'):
            mode = args.mode
            print('mode: ', mode)
            if mode == "username":
                if not self.username.collide_point(*touch.pos):
                    print('touched outside keyboard')
                    self.username.focus = False
                    self.u_kb.submit()
                return super(TextInput, self.txt).on_touch_up(touch)
            elif mode == "password":
                if not self.password.collide_point(*touch.pos):
                    print('touched outside keyboard')
                    self.password.focus = False
                    self.p_kb.submit()
                return super(TextInput, self.txt).on_touch_up(touch)

    def login(self, username, password):
        loader = LoadingPopup()
        header = {'Content-Type': 'application/json'}
        data= {'username': username, 'password': password}
        req = requests.post(config.URL+'/api/user/login', headers=header, json=data)
        print(req)
        if (req.status_code == requests.codes.ok):
            loader.stop_t()
            popup = Popup(title="Success",
                        content=Label(text="Logged in!", font_size=18, color=(0,0,0,1)),
                        size_hint=(None, None), size=(400, 400))
            popup.open()
            self.manager.current = 'main'

class RoundedButton(Button):
    pass

class MainApp(App):
    def build(self):
        global socket
        socket = dodoWebsocket()
        return ScreenManagement()
        
    # def check_capture(self):
    #     global capture
    #     if not capture:
    #         box = FloatLayout()
    #         label = Label(text="Camera not detected!", color=(0,0,0,1))
    #         button = Button(text="Try again", 
    #                 pos_hint={'center_x':0.5, 'center_y':0.3})
    #         button.bind(on_press=self.on_capture)
    #         box.add_widget(label)
    #         box.add_widget(button)
            
    #         popup = Popup(title="Error",
    #                     content=box,
    #                     size_hint=(None, None), size=(400, 400))
    #         popup.open()
    #         self.t.join()
    #         return False
    #     return True

    def on_stop(self):
        global socket
        socket.stop_video()
        socket.t.join()

    def load_resource(self, string):
        return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources/'+string))    

# for the admin login
            # BorderlessButton:
            # text: "[u]Login as admin[/u]" 
            # size_hint: (.3, .1)
            # font_size: 18
            # pos_hint: {'center_x': .15, 'center_y': .1}
            # on_press: root.manager.current = 'login'        

if __name__ == '__main__':
    MainApp().run()
