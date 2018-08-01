
from kivy.app import App
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
import os
import time
import threading
from ws import dodoWebsocket

Config.set('graphics', 'resizeable', '0')
#Config.set('graphics', 'width', '800')
#Config.set('graphics', 'height', '480')

class DriveAnim(FloatLayout):
    drive_angle = NumericProperty()
    brake_pic = StringProperty()
    accel_pic = StringProperty()

    def __init__(self, **kwargs):
        super(DriveAnim, self).__init__(**kwargs)
        self.ws = dodoWebsocket()
        app = App.get_running_app()
        self.brake_pic = app.load_resource('brake-on.png')
        self.accel_pic = app.load_resource('accel-on.png')
        self.drive_angle = 0
        self.t1 = threading.Thread(target=self.drive_thread).start()
        self.t2 = threading.Thread(target=self.pedal_thread).start()

    def drive_thread(self):
        while True: 
            angle = self.ws.angle 
            if angle: 
                self.drive(float(self.ws.angle))
        
    def pedal_thread(self):
        while True:
            if self.ws.letter == 'b':
                self.toggle_brake()
            elif self.ws.letter == 'a': 
                self.toggle_accel()
            else:
                self.ids.brake.color = 0,0,0,1
                self.ids.accel.color = 0,0,0,1

    def drive(self, angle):
        self.drive_angle = -angle
    
    def toggle_brake(self):
        self.ids.brake.color = 1,1,1,1

    def toggle_accel(self):
        self.ids.accel.color = 1,1,1,1
        


class MainApp(App):
    def build(self):
        self.driving = DriveAnim()
        return self.driving
        
    def load_resource(self, string):
        return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources/'+string))    


if __name__ == '__main__':
    MainApp().run()
