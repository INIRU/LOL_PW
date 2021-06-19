import sys
import os
import json
import webbrowser
import utility
import LOL_PW_Dialog
import LOL_PW_Thread

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

# 메인 화면
class LOL_PW_MAIN(QMainWindow, uic.loadUiType(utility.path("LOL_PW.ui"))[0]):
    __version__ = "0.0.1"

    def closeEvent(self, QCloseEvent):
        self.status = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.update()

        self.setFixedSize(323, 116)
        self.TOP.clicked.connect(self.TOP_Button_Event)
        self.JUNGLE.clicked.connect(self.JUG_Button_Event)
        self.MID.clicked.connect(self.MID_Button_Event)
        self.ADC.clicked.connect(self.ADC_Button_Event)
        self.SUPPORT.clicked.connect(self.SUP_Button_Event)
        self.BTN.clicked.connect(self.start_btn)

        self.thread = LOL_PW_Thread.LOL_LINE(ui = self)

        self.start_message_box = True

    def start_btn(self):
        if self.BTN.text() == "시작" and self.Line.text() in ["탑", "정글", "미드", "원딜", "서폿"]:
            if self.League_of_Legends() == False: # 리그 오브 레전드가 프로그램데이터에 있는 디렉토리에 있는지
                LOL_PW_Dialog.LOL_PW_Dialog().showModal()
                return
            if self.start_message_box == True: # 주의 사항
                que = QMessageBox.information(self, "주의사항", '1. 리그 오브 레전드 클라이언트 화면이 보이도록 해주세요.\n\n2. 매칭 수락 후 로비에 접속 시 마우스를 건드리지 말아 주세요.', QMessageBox.Ok | QMessageBox.No, QMessageBox.Ok)
                if que == QMessageBox.No: 
                    return
                elif que == QMessageBox.Ok: 
                    self.start_message_box = False
            self.BTN.setText("종료")
            self.BTN_SET(False)
            self.thread.working = True
            self.thread.start()
        elif self.BTN.text() == "종료":
            self.BTN.setText("시작")
            self.BTN_SET(True)
            self.thread.working = False
        else:
            QMessageBox.warning(self, "라인선택", '선호하는 라인을 선택하여주세요.', QMessageBox.Ok | QMessageBox.No, QMessageBox.Ok)

    def TOP_Button_Event(self):
        self.Line.setText("탑")

    def JUG_Button_Event(self):
        self.Line.setText("정글")

    def MID_Button_Event(self):
        self.Line.setText("미드")

    def ADC_Button_Event(self):
        self.Line.setText("원딜")

    def SUP_Button_Event(self):
        self.Line.setText("서폿")

    def BTN_SET(self, typed: bool):
        for btn in [self.TOP, self.JUNGLE, self.MID, self.ADC, self.SUPPORT]:
            btn.setEnabled(typed)

    def League_of_Legends(self):
        with open('./Database/config.json', 'r') as f:
            gamedir = (json.load(f))["game_dirs"]
        league_client = False
        if os.path.isfile(gamedir + "/LeagueClient.exe") and league_client == False:
            league_client = True
        return league_client

    def update(self):
        if int(self.__version__.replace(".", "")) < int((utility.last_version()).replace(".", "")):
            que = QMessageBox.information(self, "업데이트", '새로운 버전이 Github에 올라왔습니다.\n업데이트를 진행하시겠습니까?', QMessageBox.Ok | QMessageBox.No, QMessageBox.Ok)
            if que == QMessageBox.Ok: 
                webbrowser.open('https://github.com/INIRU/LOL_PW/releases')

if __name__ == "__main__":
    if not os.path.exists("./Database"):
        os.mkdir("./Database")
        if not os.path.isfile("./Database/config.json"):
            with open("./database/config.json", "w", encoding="utf-8") as f:
                json.dump({"game_dirs": "C:/Riot Games/League of Legends"}, f, indent=4)
    app = QApplication(sys.argv)
    LOL_PW_Main_Window = LOL_PW_MAIN()
    app.exec_()

