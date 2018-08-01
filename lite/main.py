import os
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from camera import KivyCamera
from ws import dodoWebsocket
from . import config


Config.set('graphics', 'resizeable', '0')
#Config.set('graphics', 'width', '800')
#Config.set('graphics', 'height', '480')


class ScreenManagement(ScreenManager):
    pass

##### MAIN HOME SCREEN #######   
class MainScreen(Screen):
    pass

##### PARCEL LOADING SCREEN #######
class LoadScreen(Screen):
    def on_enter(self):
        self.ids.scanner.start(mode="load")

    def exit_scan(self):
        self.ids.scanner.stop()
        self.manager.current = "main" 

##### UNLOCKING LOCKER SCREEN #######  
class UnlockScreen(Screen):
    def on_enter(self):
        self.ids.scanner.start(mode="unlock")

    def exit_scan(self):
        self.ids.scanner.stop()
        self.manager.current = "main" 

class MainApp(App):
    def build(self):
        dodo = dodoWebsocket()
        return ScreenManagement()

    def load_resource(self, string):
        return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources/'+string))    

if __name__ == '__main__':
    MainApp().run()
