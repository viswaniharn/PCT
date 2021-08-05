from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import threading
import requests
import os
from train_MLP_sklearn import MLP_model_WRK_FRD_BED_1000_89

Window.size = (600, 600)
#Alerts = ["Covid Alerts!!", "Status: Safe", "Number of Associated Infections: 0", "Total Number of Infections: 0"]


class MainWindow(Screen):
    userid = ObjectProperty(None)
    email = ObjectProperty(None)

    def validate_credentials(self):
        cred = {"name": self.userid.text, "password": self.passkey.text}
        try:
            post_call = requests.post("http://127.0.0.1:8000/api/signin/", json=cred)
            if post_call.status_code == 200 and post_call.text == "true":
                return True
        except:
            pass

        self.passkey.text = ""
        return False

class SecondWindow(Screen, BoxLayout):
    location = StringProperty()
    status = StringProperty()
    assoc_infections = StringProperty()
    total_infections = StringProperty()
    total_recoveries = StringProperty()

    def __init__(self, *args, **kwargs):
        super(SecondWindow, self).__init__(*args,**kwargs)
        self.location = 'Updating'
        self.status = "Status: Safe"
        self.total_infections = "Total Number of Infections: 0"
        self.assoc_infections = "Associated Number of infections: 0"
        self.total_recoveries = "Total Number of Recoveries: 0"
        self.thread = None
        self.is_stop_thread = False
        self.userid = ""
        self.passkey = ""
        self.model = MLP_model_WRK_FRD_BED_1000_89()

    def start_location_search(self):
        print("start_location_search")
        self.is_stop_thread = False
        self.location = 'Updating'
        self.thread = threading.Thread(target=self.get_location)
        self.thread.start()

    def get_location(self):
        rssi = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s"
        prev_location = None

        while not self.is_stop_thread:
            try:
                result = os.popen(rssi).read()
                dic = {}
                for line in result.split("\n"):
                    if "TP-LINK_7B75BF" in line:
                        dic["TP-LINK_7B75BF"] = int(line.split(" -")[1].split(" ")[0])
                    elif "ANIL" in line:
                        dic["ANIL"] = int(line.split(" -")[1].split(" ")[0])
                    elif "Tharak" in line:
                        dic["Tharak"] = int(line.split(" -")[1].split(" ")[0])
                self.location = "Location: " + self.model.estimate([dic["TP-LINK_7B75BF"], dic["ANIL"], dic["Tharak"]])
                print(self.location)
            except:
                print("Network not accessable!!")

            if (prev_location == None and self.location != "Updating") or (prev_location != self.location and self.location != "Updating"):

                data = {"name": self.userid, "password": self.passkey,
                 "location": self.location}
                post_call = requests.post("http://127.0.0.1:8000/api/postlocation/", json=data)
                if post_call.status_code == 200 and post_call.text != "User Not Found":
                    print("Status Posted Successfully!!")
                    covid_info = post_call.text.split("_")
                    print(covid_info)
                    #print(root.ids.covid_info.status.txt)
                    #root.ids.covid_info.status.txt = "Status: " + covid_info[0]
                    self.status = "Status: " + covid_info[0][1:]
                    self.assoc_infections = "Associated number of Infections: " + covid_info[1]
                    self.total_infections = "Total Number of Infections: " + covid_info[2]
                    self.total_recoveries = "Total Number of Recoveries: " + covid_info[4][:-1]

            prev_location = self.location

    def stop_location_search(self):
        if self.thread != None and self.thread.is_alive() == True:
            print("stop_location_search")
            self.is_stop_thread = True

    def get_covid_alerts(self):
        try:
            data = {"name": self.userid, "password": self.passkey}
            post_call = requests.get("http://127.0.0.1:8000/api/getcovidalerts/", json = data)
            if post_call.status_code == 200:
                print("Got status successfully!!")
                covid_info = post_call.split("_")
                print(covid_info)
                self.status = "Status: " + covid_info[0][1:]
                self.assoc_infections = "Associated number of Infections: " + covid_info[1]
                self.total_infections = "Total Number of Infections: " + covid_info[2]
                self.total_recoveries = "Total Number of Recoveries: " + covid_info[4][:-1]
        except:
            pass

    def self_declare(self, status):
        try:
            data = {"name": self.userid, "password": self.passkey, "covid_result": status}
            post_call = requests.post("http://127.0.0.1:8000/api/postcovidalert/", json=data)
            if post_call.status_code == 200:
                print("Status Posted Successfully!!")
        except:
            pass
"""
class Table(BoxLayout):
    def __init__(self, **kwargs):
        global STATUS, ASSOC_INFECTIONS,TOTAL_INFECTIONS
        print(STATUS, ASSOC_INFECTIONS, TOTAL_INFECTIONS)
        super(Table, self).__init__(**kwargs)
        self.covid_alerts = Row("Covid Alerts!!")
        self.add_widget(self.covid_alerts)
        self.status = Row("Status: " + STATUS)
        self.add_widget(self.status)
        self.infec_assoc = Row("Number of Associated Infections: " + ASSOC_INFECTIONS)
        self.add_widget(self.infec_assoc)
        self.total= Row("Total Number of Infections: " + TOTAL_INFECTIONS)
        self.add_widget(self.total)
"""

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()
