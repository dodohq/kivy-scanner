
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import threading

class LoadingPopup():
    def __init__(self):
        self.popup = Popup(title="Loading!", 
                    content=Label(text="Please wait...", color=(0,0,0,1)),
                    size_hint=(None, None), size=(400, 400))
        self.t = threading.Thread(target=self.open_t)
        self.t.start() 

    def open_t(self):
        self.popup.open() 

    def stop_t(self, *args):
        self.popup.dismiss()
        if hasattr(self, 't'):
            self.t.join()  
