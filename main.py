import cv2
import threading
import pyzbar.pyzbar as pyzbar 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty, ObjectProperty
from imutils.video import WebcamVideoStream

presentation = Builder.load_file("main.kv")
   
class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.code = ''
        self.capture = None

    def start(self, fps=30):
        self.capture = capture
        self.t = threading.Thread(target=self.listen_thread)
        self.t.start()
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule(self.update)
        Clock.unschedule(self.listening)
        self.t.join()
        self.capture = None

    def update(self, dt):
        frame = self.capture.read()
        if frame.any():
            decodedObjs = self.__decode(frame)
            frame = self.__display(frame, decodedObjs)
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()
            
    def __decode(self, im): 
        # Find barcodes and QR codes
        decodedObjects = pyzbar.decode(im)
        # Print results
        for obj in decodedObjects:
            self.code = obj.data
        return decodedObjects
  
    # Display barcode and QR code location  
    def __display(self, im, decodedObjects):
        for decodedObject in decodedObjects: 
          points = decodedObject.polygon  
          if len(points) == 4 : 
            cv2.rectangle(im, (points[0].x, points[0].y), (points[2].x, points[2].y), (0,255,0), 3)
        return im
            
    def listening(self, dt):
        if self.code:
            Storage().load_parcel(self.code)
       
    def listen_thread(self):
        Clock.schedule_interval(self.listening, 1)
            
              
            
       
class Storage():
    def __init__(self, *args):
        self.store =  JsonStore("store.json")
        
    def load_parcel(self, parcel_id):
        print(parcel_id)
        for locker in self.store['lockers']:
            print(locker)
        return 

class ScreenManagement(ScreenManager):
  pass

##### HOME SCREEN #######   
class MainScreen(Screen):
  pass
  
##### PARCEL LOADING SCREEN #######
class LoadScreen(Screen):
  

  def load_scanner(self, **kwargs):
    Storage().load_parcel('test')
    self.ids.scanner.start()
    
  def exit_scan(self):
    self.ids.scanner.stop()
    print("exit scanner called")

    
##### UNLOCKING LOCKER SCREEN #######  
class UnlockScreen(Screen):
  pass
  
  
class MainApp(App):
    
    def build(self):
        global capture 
        capture = WebcamVideoStream(src=2).start()
        
        return ScreenManagement()
    
    def on_stop(self):
        global capture
        if capture: 
            capture.stop()
            capture = None

if __name__ == '__main__':
    MainApp().run()
