from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import unlock
import json
import os


STORE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'store'))    

class Storage():
    def __init__(self, *args):
        self.parcels = {}   # parcel id to locker 
        self.qrs = {}       # 9digit concat to locker
        self.popups = []

    def load(self, parcel_id):
        parcel_id = str(parcel_id)
        if parcel_id in self.barcodes:
            locker = self.barcodes[parcel_id]
            box = FloatLayout()
            label = Label(text="Load parcel into \n[size=55][color=ffb355]"+' '*6+locker.strip('L')+"[/color][/size]", pos_hint={'center_x':.5, 'center_y':.7},
                        markup=True, color=(0,0,0,1))
            btn = RoundedButton(text='Unlock', pos_hint={'center_x':0.5, 'center_y':0.4}, 
                        size_hint=(0.45, 0.2), color=(0,0,0,1))
            self.bindFn = lambda *args:self.open(locker, btn)
            btn.bind(on_press=self.bindFn)
            box.add_widget(label)
            box.add_widget(btn)
            popup = Popup(title="Parcel Registered!",
                        content=box, auto_dismiss=False,
                        size_hint=(None, None), size=(400, 400))
            popup.open()
            self.popups.append(popup)
        else: 
            popup = Popup(title="Error",
                        content=Label(text="Oops, wrong parcel!", pos_hint={'center_x':0.5, 'center_y':0.7}),
                        size_hint=(None, None), size=(400, 400))
            popup.open()
            self.popups.append(popup)

    def unlock(self, code):
        qr = json.loads(code)
        concat = qr['uuid'] + qr['password']
        if concat in self.qrs:
            locker = self.qrs[concat]
            box = FloatLayout()
            label = Label(text="Open locker\n"+" "*8+"[size=65][color=ffb355]"+locker['id'].strip('L')+"[/color][/size]", pos_hint={'center_x':.5, 'center_y':.7},
                            markup=True, color=(0,0,0,1))
            btn = RoundedButton(text="Unlock", pos_hint={'center_x':0.5, 'center_y':0.35}, size_hint=(0.45, 0.2), color=(0,0,0,1))
            self.bindFn = lambda *args: self.open(locker, btn)
            btn.bind(on_press=self.bindFn)
            box.add_widget(label)
            box.add_widget(btn)
            popup = Popup(title="Locker unlocked!", 
                        content=box,
                        auto_dismiss=False,
                        size_hint=(None, None), size=(400, 400))
            
            popup.open()
            self.popups.append(popup)

    def open(self, locker, btn):
        btn.text = 'Unlocked!'
        unlock.unlock(locker)
        for p in self.popups:
            p.dismiss()
            



