import sys

from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QLabel, QSlider, QPushButton, QGridLayout, QMessageBox, \
    QApplication
from PyQt5.QtCore import Qt
from pycromanager import Bridge


class LaserPowerPanel(QWidget):
    def __init__(self):
        super(LaserPowerPanel, self).__init__()
        self.Lasername="iBeamSmartCW405"
        self.initUI()

    def initUI(self):
        self.groupbox=QGroupBox("Power",self)
        self.groupbox.resize(300,100)

        self.powtext=QLabel(self)
        self.powtext.resize(80,40)
        self.powtext.setText("Power(mW): ")

        self.powline=QLineEdit(self)
        self.powline.resize(80,40)
        self.powline.setText("100")
        self.powline.textEdited.connect(self.setLaserPower)

        self.startbutton=QPushButton("Start")
        self.startbutton.resize(40,40)
        self.startbutton.setCheckable(True)
        self.startbutton.toggled.connect(self.startLaser)

        self.slider=QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.resize(200, 40)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.setSliderChange)

        layout=QGridLayout()
        layout.addWidget(self.powtext,0,0,1,1)
        layout.addWidget(self.powline,0,1,1,1)
        layout.addWidget(self.startbutton,0,2,1,1)
        layout.addWidget(self.slider,1,0,1,3)

        self.groupbox.setLayout(layout)

    def setLaserPower(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if self.core.get_property(self.Lasername, "Laser Operation") == "On":
                    self.core.set_property(self.Lasername, "Power (mW)",int(self.powline.text()))
                    self.slider.setValue(int(self.powline.text()))
                else:
                    str0 = ("Open the Laser")
                    QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def startLaser(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if self.core.get_property(self.Lasername, "Laser Operation") == "Off":
                    self.core.set_property(self.Lasername, "Laser Operation", "On")
                else:
                    self.core.set_property(self.Lasername, "Laser Operation", "Off")
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def setSliderChange(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if self.core.get_property(self.Lasername, "Laser Operation") == "On":
                    self.core.set_property(self.Lasername, "Power (mW)",int(self.slider.value()))
                    self.powline.setText(int(self.slider.value()))
                else:
                    str0 = ("Open the Laser")
                    QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LaserPowerPanel()
    w.show()
    sys.exit(app.exec_())
