import utility
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic

class LOL_PW_Dialog(QDialog, uic.loadUiType(utility.path("LOL_PW_Dialog.ui"))[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.setFixedSize(382, 70)
        self.add.clicked.connect(self.Dir_Add)
    
    def Dir_Add(self):
        if len(self.dir.text()) > 0:
            with open('./Database/config.json', 'r') as f:
                data = json.load(f)
            data["game_dirs"] = (self.dir.text()).replace("\\", "/")
            with open('./Database/config.json', 'w') as f:
                json.dump(data, f, indent=4)
            self.close()
    
    def showModal(self):
        return super().exec_()