import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import threading
import json
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

config = {
    "apiKey": "AIzaSyDmLjTHyFMMLg7RyIWpHCtrabgPe15Eyh8",
    "authDomain": "smart-aquarium-804ab.firebaseapp.com",
    "databaseURL": "https://smart-aquarium-804ab-default-rtdb.firebaseio.com",
    "storageBucket": "smart-aquarium-804ab.appspot.com"
}
cred = credentials.Certificate("smart-aquarium.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-aquarium-e9439-default-rtdb.firebaseio.com/'
})

USER_ID = "-N0E8J3ItyjCsWAJ-0l4"


class Ui_MainWindow(object):

    def update_user_data(self, value):
        ref = db.reference('/')
        ref.child(USER_ID).update(value)

    def get_user_data(self, key):
        ref = db.reference('/')
        user = ref.child(USER_ID)
        json_object = json.loads(json.dumps(user.get()))
        return json_object[key]

    def get_led_white(self):
        return self.get_user_data("led_white")

    def get_led_yellow(self):
        return self.get_user_data("led_yellow")

    def get_filter(self):
        return self.get_user_data("filter")

    def get_heater(self):
        return self.get_user_data("heater")

    def get_feed(self):
        return self.get_user_data("feed")

    def initData(self):
        while True:
            ref = db.reference('/')
            user = ref.child(USER_ID)
            user_data = json.loads(json.dumps(user.get()))
            humidity = user_data["humidity"]
            water_temp = user_data["water_temperature"]
            temp = user_data["temperature"]
            water_acidity = user_data["water_acidity"]
            self.temperatura.setText(self._translate("MainWindow", "     " + str(temp) + " C"))
            self.humidity.setText(self._translate("MainWindow", "     " + str(humidity) + " %"))
            self.waterTemp.setText(self._translate("MainWindow", "     " + str(water_temp) + " C"))
            self.acidity.setText(self._translate("MainWindow", "     " + str(water_acidity)))

    def filterData(self):
        while True:
            filter = self.get_filter()
            if not filter:
                self.filterButton.setStyleSheet('QPushButton {background-color: #FFFFFF; color: black;}')
            else:
                self.filterButton.setStyleSheet('QPushButton {background-color: #FFDD00; color: black;}')

    def heaterData(self):
        while True:
            heater = self.get_heater()
            if not heater:
                self.heaterButton.setStyleSheet('QPushButton {background-color: #FFFFFF; color: black;}')
            else:
                self.heaterButton.setStyleSheet('QPushButton {background-color: #FFDD00; color: black;}')

    def whiteData(self):
        while True:
            white_led = self.get_led_white()
            if not white_led:
                self.whiteLedButton.setStyleSheet('QPushButton {background-color: #FFFFFF; color: black;}')
            else:
                self.whiteLedButton.setStyleSheet('QPushButton {background-color: #FFDD00; color: black;}')

    def yellowData(self):
        while True:
            yellow_led = self.get_led_yellow()
            if not yellow_led:
                self.yellowButton.setStyleSheet('QPushButton {background-color: #FFFFFF; color: black;}')
            else:
                self.yellowButton.setStyleSheet('QPushButton {background-color: #FFDD00; color: black;}')

    def feedData(self):
        while True:
            feed = self.get_feed()
            if not feed:
                self.feedButton.setStyleSheet('QPushButton {background-color: #FFFFFF; color: black;}')
            else:
                self.feedButton.setStyleSheet('QPushButton {background-color: #FFDD00; color: black;}')

    def initFirebase(self):
        dataInitThread = threading.Thread(target=self.initData)
        filterDataThread = threading.Thread(target=self.filterData)
        heaterDataThread = threading.Thread(target=self.heaterData)
        whiteDataThread = threading.Thread(target=self.whiteData)
        yellowDataThread = threading.Thread(target=self.yellowData)
        feedDataThread = threading.Thread(target=self.feedData)

        dataInitThread.start()
        filterDataThread.start()
        heaterDataThread.start()
        whiteDataThread.start()
        yellowDataThread.start()
        feedDataThread.start()

    def clickedFilterButton(self):
        self.update_user_data({"filter": not self.get_filter()})
        print("Clicked filter")

    def clickedHeaterButton(self):
        self.update_user_data({"heater": not self.get_heater()})
        print("Clicked heater")

    def clickedwhiteLedButton(self):
        self.update_user_data({"led_white": not self.get_led_white()})
        print("Clicked white led")

    def clickedYellowLedButton(self):
        self.update_user_data({"led_yellow": not self.get_led_yellow()})
        print("Clicked yellow led")

    def clickedFeedButton(self):
        self.update_user_data({"feed": 1})
        print("Clicked feed")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 500)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        MainWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
        MainWindow.setAcceptDrops(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QTextEdit(self.centralwidget)
        self.title.setEnabled(False)
        self.title.setGeometry(QtCore.QRect(0, -10, 591, 61))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title.setAutoFillBackground(False)
        self.title.setFrameShape(QtWidgets.QFrame.HLine)
        self.title.setFrameShadow(QtWidgets.QFrame.Plain)
        self.title.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.title.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.title.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.title.setTabChangesFocus(False)
        self.title.setUndoRedoEnabled(False)
        self.title.setReadOnly(False)
        self.title.setOverwriteMode(False)
        self.title.setAcceptRichText(True)
        self.title.setObjectName("title")
        self.yellowButton = QtWidgets.QPushButton(self.centralwidget)
        self.yellowButton.setGeometry(QtCore.QRect(10, 80, 91, 61))
        self.yellowButton.clicked.connect(self.clickedYellowLedButton)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.yellowButton.setFont(font)
        self.yellowButton.setObjectName("yellowButton")
        self.whiteLedButton = QtWidgets.QPushButton(self.centralwidget)
        self.whiteLedButton.setGeometry(QtCore.QRect(10, 190, 91, 61))
        self.whiteLedButton.clicked.connect(self.clickedwhiteLedButton)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.whiteLedButton.setFont(font)
        self.whiteLedButton.setObjectName("whiteLedButton")
        self.heaterButton = QtWidgets.QPushButton(self.centralwidget)
        self.heaterButton.setGeometry(QtCore.QRect(474, 190, 91, 61))
        self.heaterButton.clicked.connect(self.clickedHeaterButton)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.heaterButton.setFont(font)
        self.heaterButton.setObjectName("heaterButton")
        self.filterButton = QtWidgets.QPushButton(self.centralwidget)
        self.filterButton.setGeometry(QtCore.QRect(474, 80, 91, 61))
        # self.filterButton.setCheckable(True)
        self.filterButton.clicked.connect(self.clickedFilterButton)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.filterButton.setFont(font)
        self.filterButton.setObjectName("filterButton_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 70, 241, 181))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("aquarium_poto.png"))
        self.label.setObjectName("label")
        self.feedButton = QtWidgets.QPushButton(self.centralwidget)
        self.feedButton.setGeometry(QtCore.QRect(250, 270, 91, 61))
        self.feedButton.clicked.connect(self.clickedFeedButton)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.feedButton.setFont(font)
        self.feedButton.setObjectName("feedButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 350, 600, 100))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget.setFont(font)
        self.tableWidget.setTabletTracking(False)
        self.tableWidget.setAcceptDrops(False)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self._translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(self._translate("MainWindow", "MainWindow"))
        self.title.setHtml(self._translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'Arial Black\'; font-size:18pt; font-weight:600; font-style:normal;\">\n"
                                           "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400;\"><br /></p>\n"
                                           "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-weight:400;\">SMART AQUARIUM</span></p></body></html>"))
        self.yellowButton.setText(self._translate("MainWindow", "Yellow led"))
        self.whiteLedButton.setText(self._translate("MainWindow", "White led"))
        self.heaterButton.setText(self._translate("MainWindow", "Heater"))
        self.filterButton.setText(self._translate("MainWindow", "Filter"))
        self.feedButton.setText(self._translate("MainWindow", "Feed"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(self._translate("MainWindow", "  Humidity  "))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(self._translate("MainWindow", "Water Acidity"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(self._translate("MainWindow", "Water Temp"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(self._translate("MainWindow", "Temperature"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.humidity = self.tableWidget.item(0, 0)
        self.humidity.setText(self._translate("MainWindow", ""))
        self.acidity = self.tableWidget.item(0, 1)
        self.acidity.setText(self._translate("MainWindow", ""))
        self.waterTemp = self.tableWidget.item(0, 2)
        self.waterTemp.setText(self._translate("MainWindow", ""))
        self.temperatura = self.tableWidget.item(0, 3)
        self.temperatura.setText(self._translate("MainWindow", ""))
        self.tableWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.initFirebase()
    MainWindow.show()
    MainWindow.statusBar().setSizeGripEnabled(False)
    MainWindow.setFixedSize(600, 500)
    sys.exit(app.exec_())
