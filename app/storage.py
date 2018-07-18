from kivy.uix.label import Label
from kivy.uix.popup import Popup
import os
import json
import requests
import config
import unlock
from auth import HEADERS

STORE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'store'))    

class Storage():
    def __init__(self, *args):
        self.lockers_path =  STORE_DIR + "/lockers.json"
        self.parcels_path =  STORE_DIR + "/parcels.json"
        with open(self.parcels_path) as f:
            self.parcels = json.load(f)['parcels']
        self.server_parcels = requests.get(config.URL+'/api/parcel', headers=HEADERS).json()['parcels']
        
    def load_parcel(self, parcel_id):
        # if parcel is already loaded in robot
        if parcel_id in [p['id'] for p in self.parcels]:
            print("parcel already loaded")
            return False

        # if parcel is not yet loaded & is a company parcel
        elif parcel_id in [p['_id'] for p in self.server_parcels]:  
            print(parcel_id, " found")
            with open(self.lockers_path) as f:
                self.lockers = json.load(f)['lockers']

            # get the first empty locker    
            for locker in self.lockers:
                if locker["has_parcel"] == False:
                    robot_auth = {'Content-Type': 'application/json', 'Authorization': config.ROBOT_TOKEN}
                    data = {'id': parcel_id, 'robot_compartment': locker['id']}
                    req = requests.post(config.URL+'/api/parcel/load', headers=robot_auth, json=data)
                    print(req)
                    if(req.status_code == requests.codes.ok):
                        for p in self.server_parcels:
                            if p['_id'] == parcel_id:
                                print('locker chosen: ', locker['id'])
                                locker['parcel_id'] = parcel_id
                                locker['has_parcel'] = True
                                self.parcels.append({'id': parcel_id, 'address': p['address'], 'contact': p['customer_contact'], 'date_of_delivery': p['date_of_delivery']})
                                self.write_to_store()
                                popup = Popup(title="Parcel Registered!",
                                            content=Label(text="Load parcel [color=ffb355]\'"+str(parcel_id)+"\'[/color] onto "+locker['id']+".",
                                            markup=True, color=(0,0,0,1)),
                                            size_hint=(None, None), size=(400, 400))
                                popup.open()
                                return True

            # check if all lockers are filled 
            if all(l['has_parcels']==True for l in self.lockers):
                box = FloatLayout()
                box.add_widget(Label(text="All the lockers are filled! Do you want to finish loading?",
                                    pos_hint={'center_x':0.5, 'center_y':0.7}))
                box.add_widget(Button(text="Finish",
                                    pos_hint={'center_x':0.5, 'center_y':0.4}))

                popup = Popup(title="Finished!",
                            content=box, color=(0,0,0,1),
                            size_hint=(None, None), size=(400, 400))
                popup.open()
                return "Filled"

            else: 
                print("server error: ", req.json())
        else: 
            print(parcel_id, " not recognized, or lockers are full")

    def unlock_parcel(self, code):
        print(code)
        code = json.loads(code)
        if code['id'] in [p['id'] for p in self.parcels]:
            with open(self.lockers_path) as f:
                self.lockers = json.load(f)['lockers']
            for locker in self.lockers:
                try: 
                    if locker['parcel_id'] == code['id']:
                        robot_auth = {'Content-Type': 'application/json', 'Authorization': config.ROBOT_TOKEN}
                        req = requests.post(config.URL+'/api/parcel/unlock', headers=robot_auth, json=code)
                        print(req)
                        if (req.status_code == requests.codes.ok):
                            unlock.unlock(locker['id'])  
                            return self.get_parcel(code['id'])
                except KeyError:
                    pass
        else: 
            popup = Popup(title="Error",
                        content=Label(text="""This robot doesn't have your parcel.
                        \nCheck your robot location again, or 
                        \ncall our helpline at 96959382.""",
                        color=(0,0,0,1) ),
                        size_hint=(None, None), size=(400, 400))
            popup.open()
            return False

    def get_parcel(self, id):
        print('get_parcel called')
        locker = ''
        for index, parcel in enumerate(self.parcels):
            if parcel['id'] == id:
                self.parcels.pop(index)
        for index, lock in enumerate(self.lockers):
            try:
                if lock['parcel_id'] == id: 
                    locker = lock
                    self.lockers[index]['parcel_id'] = ''
                    self.lockers[index]['has_parcel'] = False
            except KeyError:
                pass
        self.write_to_store()
        text = "Take your parcel from locker [color=ffb355]\'"+str(locker['id'])+"\'[/color]"
        popup = Popup(title="Locker unlocked!", 
                    content=Label(text=text, markup=True, color=(0,0,0,1)),
                    size_hint=(None, None), size=(400, 400))
        popup.open()
        return True

    def write_to_store(self):
        with open(self.parcels_path, 'w') as f:
            f.write(json.dumps({"parcels": self.parcels}, indent=2, sort_keys=True))
        with open(self.lockers_path, 'w') as f:
            f.write(json.dumps({"lockers": self.lockers}, indent=2, sort_keys=True))
    
