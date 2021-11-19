import sys

from PyQt5.QtChart import QChartView
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QGroupBox, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, \
    QLabel, QGridLayout
from PyQt5.QtCore import Qt
from Timechart import TimeChart
from pycromanager import Bridge
from functools import partial

class FocusControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.groupbox = QGroupBox("Focus", self)
        self.groupbox.resize(800,400)
        self.lineedit = QLineEdit(self)
        self.lineedit.resize(40, 20)
        self.lineedit.setText("12.0")
        self.lineedit.textChanged.connect(self.setpos)
        self.lineedit.setAlignment(Qt.AlignCenter)

        self.monitorbutton = QPushButton("Monitor")
        self.monitorbutton.resize(40, 23)
        self.monitorbutton.setCheckable(True)
        self.monitorbutton.toggled.connect(self.monitorcontrol)

        self.lockbutton = QPushButton("Lock")
        self.lockbutton.resize(40, 23)
        self.lockbutton.setCheckable(True)
        self.lockbutton.toggled.connect(self.setFocus)

        self.largeedit = QLineEdit(self)
        self.largeedit.resize(30, 23)
        self.largeedit.setText("2.0")
        self.largeedit.setAlignment(Qt.AlignCenter)

        self.smalledit = QLineEdit(self)
        self.smalledit.resize(30, 23)
        self.smalledit.setText("0.2")
        self.smalledit.setAlignment(Qt.AlignCenter)

        self.largeupbutton = QPushButton("^^")
        self.largeupbutton.resize(30, 23)
        self.largeupbutton.clicked.connect(partial(self.setupStep,self.largeedit.text()))

        self.smallupbutton = QPushButton("^")
        self.smallupbutton.resize(30, 23)
        self.smallupbutton.clicked.connect(partial(self.setupStep,self.smalledit.text()))


        self.smalldownbutton = QPushButton("v")
        self.smalldownbutton.resize(30, 23)
        self.smalldownbutton.clicked.connect(partial(self.setdStep, self.smalledit.text()))

        self.largedownbutton = QPushButton("vv")
        self.largedownbutton.resize(30, 23)
        self.largedownbutton.clicked.connect(partial(self.setdStep,self.largeedit.text()))



        self.timechart=TimeChart()

        self.pos_text=QLabel(self)
        self.pos_text.setText("Position:")
        self.pos_text.setAlignment(Qt.AlignCenter)
        self.pos_text.resize(40, 20)

        self.large_text = QLabel(self)
        self.large_text.setText(">> ")
        self.large_text.setAlignment(Qt.AlignCenter)
        self.large_text.resize(20, 20)

        self.small_text = QLabel(self)
        self.small_text.setText("> ")
        self.small_text.setAlignment(Qt.AlignCenter)
        self.small_text.resize(20, 20)

        layout = QGridLayout()
        layout.addWidget(self.pos_text, 0, 1, 2, 3)
        layout.addWidget(self.lineedit, 1, 1, 2, 3)
        layout.addWidget(self.monitorbutton, 4, 1, 2, 3)
        layout.addWidget(self.lockbutton, 5, 1, 2, 3)
        layout.addWidget(self.timechart, 0, 5, 7,6)
        layout.addWidget(self.large_text, 2, 11, 2, 2)
        layout.addWidget(self.small_text, 3, 11, 2, 2)
        layout.addWidget(self.largeupbutton, 0, 13, 2, 3)
        layout.addWidget(self.smallupbutton, 1, 13, 2, 3)
        layout.addWidget(self.largeedit, 2, 13, 2, 3)
        layout.addWidget(self.smalledit, 3, 13, 2, 3)
        layout.addWidget(self.smalldownbutton, 4, 13, 2, 3)
        layout.addWidget(self.largedownbutton, 5, 13, 2, 3)


        self.groupbox.setLayout(layout)





    def monitorcontrol(self):
        self.timechart.curpos=self.lineedit.text()
        if self.monitorbutton.isChecked():
            self.timechart.timer_init()
        else:
            self.timechart.timer.stop()

    def setFocus(self):
        try:
            with Bridge() as bridge:
                self.core = bridge.get_core()
                if self.lockbutton.isChecked():  # cmm core
                    self.core.set_property("PIZStage", "Servo", 0)
                    self.core.set_property("PIZStage", "External sensor", 1)
                    self.core.set_property("PIZStage", "Servo", 1)
                else:
                    self.core.set_property("PIZStage", "Servo", 0)
                    self.core.set_property("PIZStage", "External sensor", 0)
                    self.core.set_property("PIZStage", "Servo", 1)

        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
            if self.lockbutton.isChecked():
                print("lock")
            else:
                print({"unlock"})

    def setupStep(self,step):
        print(step)

        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                self.core.set_property("PIZStage", "Position",min(float(step)+float(self.core.get_property("PIZStage", "Position")),100))
        except:
            self.timechart.curpos = float(self.timechart.curpos) + float(step)
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def setdStep(self,step):
        print(step)
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                self.core.set_property("PIZStage", "Position",max(0,float(self.core.get_property("PIZStage", "Position"))-float(step)))
        except:
            self.timechart.curpos = float(self.timechart.curpos) - float(step)
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def setpos(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                self.core.set_property("PIZStage", "Position",self.lineedit.text())
        except:
            self.timechart.curpos=float(self.lineedit.text())
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)






if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = FocusControlPanel()
    w.show()

    sys.exit(app.exec_())



