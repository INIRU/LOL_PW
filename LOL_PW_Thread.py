import os
import json
import utility
import requests
import time
import sys
import urllib3
import pyautogui
import keyboard

from PyQt5.QtCore import *
from base64 import b64encode
from python_imagesearch.imagesearch import imagesearch

import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
import pywinauto

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LOL_LINE(QThread):
    def __init__(self, ui, parent = None):
        super(LOL_LINE, self).__init__(parent)
        self.game = False
        self.working = True
        self.ui = ui

    def lockfile(self):
        with open('./Database/config.json', 'r') as f:
            gamedir = (json.load(f))["game_dirs"]
        lockpath = gamedir + "/lockfile"

        if os.path.isfile(lockpath):
            lock_file =  open(gamedir + "/lockfile", 'r')
            lockdata = lock_file.read()
            lock_file.close()
            lock = lockdata.split(':')
            return {"procname": lock[0], "pid": lock[1], "port": lock[2], "password": lock[3], "protocol": lock[4], "username": "riot"}

    def request(self, method, path, query = None, data = None):
        lock = self.lockfile()
        if lock == None:
            return lock
        headers = {"Authorization": "Basic " + b64encode(bytes(f"{lock['username']}:{lock['password']}", "utf-8")).decode("ascii")}
        url = ("%s://127.0.0.1:%s%s" % (lock["protocol"], lock["port"], path)) + (f"%{query}" if query else "")

        fn = getattr(requests.session(), method)

        if not data:
            r = fn(url, verify=False, headers=headers)
        else:
            r = fn(url, verify=False, headers=headers, json=data)
        return r

    def run(self):
        while self.working:
            while not [x for x in pywinauto.findwindows.find_elements() if x.name == "League of Legends"] and self.working:
                time.sleep(1.5)
                continue
            r_status = self.request('get', '/lol-gameflow/v1/gameflow-phase')
            if r_status == None: 
                continue
            elif r_status != None: 
                status = r_status.json()
            if self.game == True and status == "Lobby":
                self.game = False
            elif self.game == True and status != "Lobby":
                continue
            ready = False
            if status == "Lobby":
                ready = True
                lobby = self.request('get', '/lol-lobby/v2/lobby').json()
            if ready == False:
                continue
            chat_box_img, connecting_img = utility.path("./Source/chat_box.PNG"), utility.path("./Source/connect.PNG")
            chat_box = imagesearch(chat_box_img, 0.8)
            if status == "ChampSelect" and lobby["gameConfig"]["gameMode"] == "CLASSIC" and not lobby["gameConfig"]["showPositionSelector"]:
                self.game = True
                connecting = imagesearch(connecting_img, 0.8)
                while not connecting[0] == -1:
                    connecting = imagesearch(connecting_img, 0.8)
                pyautogui.click(chat_box[0], chat_box[1])
                for i in range(10):
                    keyboard.write(self.ui.Line.text())
                    keyboard.press('enter')
                    time.sleep(0.15)
            time.sleep(1.5)