import cv2
import threading 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
from scanner import Scanner

presentation = Builder.load_file("main.kv")
   
class ScanWindow(Image):
    mode = StringProperty('')
    
    def __init__(self, **kwargs):
        super(ScanWindow, self).__init__(**kwargs)
        if (self.mode == 'load'):
            self.load_parcels
        elif (self.mode == 'unlock'):
            pass
        else: 
            pass
    
        
    def load_parcels(self):
        print("load parcels called")
        threading.Thread(target=self.call_scanner).start()
        pass
        
    def stop_scan(self):
        self.scanner.exit()
        
    def call_scanner(self):
        print("scanner called")
        while(True):
            img = self.scanner.callback()
            # convert image to texture
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
            cv2.waitKey(1)
        self.scanner.exit()
            
       
class Storage():
    def __init__(self, *args):
        self.store =  JsonStore("store.json")

class ScreenManagement(ScreenManager):
  pass
    
class MainScreen(Screen):
  pass
  
class LoadScreen(Screen):

  scan_window = ObjectProperty(None)
  
  def __init__(self, **kwargs):
    super(LoadScreen, self).__init__(**kwargs)
    self.scanner = Scanner()

  def load_scanner(self, **kwargs):
    pass
    
  
class UnlockScreen(Screen):
  pass
  
  
class MainApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == '__main__':
    MainApp().run()
