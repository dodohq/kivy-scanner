from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from random import randint
from popup import LoadingPopup
import os
import json
import requests
import threading
import config
import unlock

STORE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'store'))    

class Storage():
    def __init__(self, *args):
        self.lockers_path =  STORE_DIR + "/lockers.json"
        self.parcels_path =  STORE_DIR + "/parcels.json"
        with open(self.parcels_path) as f:
            self.parcels = json.load(f)['parcels']
        
    def load_parcel(self, parcel_id):
        print('loading parcel')
        # if parcel is already loaded in robot
        if parcel_id in [p['id'] for p in self.parcels]:
            print("parcel already loaded")
            return False

        # if parcel is not yet loaded 
        with open(self.lockers_path) as f:
            self.lockers = json.load(f)['lockers']

        # get the first empty locker    
        for locker in self.lockers:
            if locker["has_parcel"] == False:
                loader = LoadingPopup()
                locker["uuid"] = randint(100,999)
                data = {'id': parcel_id, 'robot_compartment': locker['id'], 'uuid':locker["uuid"]}
                self.req = requests.post(config.URL+'/api/parcel/load', headers=config.HEADERS, json=data)
                print(self.req)
                if(self.req.status_code == requests.codes.ok):
                    loader.stop_t()
                    box = FloatLayout()
                    label = Label(text="Load parcel into \n[size=55][color=ffb355]"+' '*6+locker['id'].strip('L')+"[/color][/size]", pos_hint={'center_x':.5, 'center_y':.7},
                                markup=True, color=(0,0,0,1))
                    btn = RoundedButton(text="Finish", pos_hint={'center_x':0.5, 'center_y':0.4}, 
                                size_hint=(0.45, 0.2), color=(0,0,0,1))
                    btn.bind(on_press=lambda *args:self.do_load(locker))
                    box.add_widget(label)
                    box.add_widget(btn)
                    self.popup = Popup(title="Parcel Registered!",
                                content=box, auto_dismiss=False,
                                size_hint=(None, None), size=(400, 400))
                    self.popup.open()
                    return True
                else: 
                    loader.stop_t()
                    raise ValueError(self.req.json())
                    return False

    def do_load(self, locker):
        try:
            self.popup.dismiss()
            unlock.unlock(locker['id'])
        except FileNotFoundError as e:
            popup = Popup(title="Hiccup",
                        content=Label(text="There was a minor error:\n "+str(e), 
                        color=(0,0,0,1), font_size=18, pos_hint={'center_x':.5, 'center_y':.6}), 
                        size_hint=(None, None), size=(400,400))
            popup.open()
            return False
        for p in self.parcels:  
            if p['locker_id'] == locker['id']:
                locker['parcel_id'] = p['id']
                locker['has_parcel'] = True
                self.parcels.append({'id': p['id'], 'locker_id': locker['id']})
                self.write_to_store()
        
        # check if all lockers are filled 
        if all(l['has_parcel']==True for l in self.lockers):
            box = FloatLayout()
            box.add_widget(Label(text="All the lockers are filled!\nDo you want to finish loading?", pos_hint={'center_x':0.5, 'center_y':0.7}, font_size=18, color=(0,0,0,1)))
            btn = RoundedButton(text="Finish", pos_hint={'center_x':0.5, 'center_y':0.4}, size_hint=(0.45, 0.2), color=(0,0,0,1))
            btn.bind(on_press=self.go_to_unlock)
            box.add_widget(btn)
            popup = Popup(title="Finished!", content=box, size_hint=(None, None), size=(400, 400))
            popup.open()
            return "Filled"
        return True



    def unlock_parcel(self, code):
        code = json.loads(code)
        uuid = code['uuid']
        with open(self.lockers_path) as f:
            self.lockers = json.load(f)['lockers']
        if uuid in [str(l['uuid']) for l in self.lockers]:
            for locker in self.lockers:
                print(locker)
                try: 
                    if str(locker['uuid']) == uuid:
                        print('unlock', code)
                        loader = LoadingPopup()
                        req = requests.post(config.URL+'/api/parcel/unlock', headers=config.HEADERS, json=code)
                        print(req)
                        if (req.status_code == requests.codes.ok):
                            loader.stop_t()
                            # load successful unlock popup
                            box = FloatLayout()
                            label = Label(text="Open locker\n"+" "*8+"[size=65][color=ffb355]"+locker['id'].strip('L')+"[/color][/size]",
                                          markup=True, color=(0,0,0,1))
                            btn = RoundedButton(text="Finish", pos_hint={'center_x':0.5, 'center_y':0.4}, size_hint=(0.45, 0.2), color=(0,0,0,1),
                                            on_dismiss=lambda *args: self.do_unlock(locker['id']))
                            btn.bind(on_press=lambda *args: self.do_unlock(locker['id']))
                            box.add_widget(label)
                            box.add_widget(btn)
                            popup = Popup(title="Locker unlocked!", 
                                        content=box,
                                        size_hint=(None, None), size=(400, 400))
                            popup.bind(on_dismiss=lambda *args: self.do_unlock(locker['id']))
                            popup.open()
                            return True
                        else: 
                            return False
 
                except Exception as e:
                    popup = Popup(title="Hiccup",
                                content=Label(text="There was a minor error:\n "+str(e), 
                                color=(0,0,0,1), font_size=18, pos_hint={'center_x':.5, 'center_y':.6}), 
                                size_hint=(None, None), size=(400,400))
                    popup.open()
                    pass
        else: 
            popup = Popup(title="Error",
                        content=Label(text="""This robot doesn't have your parcel.
                        \nCheck your robot location again, or 
                        \ncall our helpline at 96959382.""",
                        font_size=18,
                        color=(0,0,0,1),pos_hint={'center_x':.5, 'center_y':.6} ),
                        size_hint=(None, None), size=(400, 400))
            popup.open()

            return False


    def do_unlock(self, id):
        locker = ''
        for index, parcel in enumerate(self.parcels):
            if parcel['locker_id'] == id:
                self.parcels.pop(index)
        for index, lock in enumerate(self.lockers):
            try:
                if lock['parcel_id'] == id: 
                    locker = lock
                    self.lockers[index]['parcel_id'] = ''
                    self.lockers[index]['has_parcel'] = False
                    self.lockers[index]['uuid'] = ''
            except KeyError:
                pass
        self.write_to_store()
        unlock.unlock(id)
        return True

    def write_to_store(self):
        with open(self.parcels_path, 'w') as f:
            f.write(json.dumps({"parcels": self.parcels}, indent=2, sort_keys=True))
        with open(self.lockers_path, 'w') as f:
            f.write(json.dumps({"lockers": self.lockers}, indent=2, sort_keys=True))
    
    def manual_unlock(self, input):
        if input: 
            uuid = input[:2]
            password = input[3:]
            with open(self.lockers_path) as f:
                self.lockers = json.load(f)['lockers']
            try: 
                for l in self.lockers:
                    if l['uuid'] == uuid:
                        code = {'uuid': uuid, 'password': password}
                        return self.unlock_parcel(code)  
                return False
            except KeyError: 
                pass
        else: 
            print("user submitted empty input")
            popup = Popup(title="Empty input!", 
                    content=Label(text="Please input the 9-digit\n` number in your SMS.", color=(0,0,0,1)),
                    size_hint=(None, None), size=(400, 400))
            popup.open()

class RoundedButton(Button):
    pass
