import cv2
import threading
import pyzbar.pyzbar as pyzbar 
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from storage import Storage

code = ''
class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)

    def start(self, mode, capture, fps=30):
        self.store = Storage()
        self.mode = mode
        self.capture = capture
        global code
        code = ''
        self.t = threading.Thread(target=self.listen_thread)
        self.t.start()
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        try:    
            Clock.unschedule(self.update)
            Clock.unschedule(self.listening)
            self.t.join()
            self.capture = None
        except AttributeError: 
            pass

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
            global code
            code = obj.data.decode("utf-8")
            print(code)
        return decodedObjects
  
    # Display barcode and QR code location  
    def __display(self, im, decodedObjects):
        for decodedObject in decodedObjects: 
          points = decodedObject.polygon  
          if len(points) == 4 : 
            cv2.rectangle(im, (points[0].x, points[0].y), (points[2].x, points[2].y), (0,255,0), 3)
        return im
            
    def listening(self, dt):
        if (code and self.mode=="load"):
            self.store.load_parcel(code)
        elif (code and self.mode=="unlock"):
            got_code = self.store.unlock_parcel(code)
            self.t.join()
            self.parent.parent.exit_scan()
       
    def listen_thread(self):
        Clock.schedule_interval(self.listening, 2)
            
    