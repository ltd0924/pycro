import sys

from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QLabel, QSlider, QPushButton, QGridLayout, QMessageBox, \
    QApplication, QVBoxLayout
from PyQt5.QtCore import Qt
from pycromanager import Bridge

from LaserPowerPanel import LaserPowerPanel


class LaserFinePanel(QWidget):
    def __init__(self):
        super(LaserFinePanel, self).__init__()
        self.Lasername = "iBeamSmartCW405"
        self.initUI()

    def initUI(self):
        self.ww=QWidget(self)
        self.ww.resize(300,300)

        self.Lpower=LaserPowerPanel()

        self.groupbox = QGroupBox("Fine", self)
        self.groupbox.resize(300, 200)

        self.startbutton = QPushButton("Start")
        self.startbutton.resize(40, 40)
        self.startbutton.setCheckable(True)
        self.startbutton.toggled.connect(self.startLaser)

        self.atext = QLabel(self)
        self.atext.resize(80, 40)
        self.atext.setText("Fine A")

        self.btext = QLabel(self)
        self.btext.resize(80, 40)
        self.btext.setText("Fine B")

        self.a1text = QLabel(self)
        self.a1text.resize(80, 40)
        self.a1text.setText("100%")

        self.b1text = QLabel(self)
        self.b1text.resize(80, 40)
        self.b1text.setText("100%")

        self.slidera = QSlider(self)
        self.slidera.setOrientation(Qt.Horizontal)
        self.slidera.resize(200, 40)
        self.slidera.setMinimum(0)
        self.slidera.setMaximum(100)
        self.slidera.valueChanged.connect(self.setSlideraChange)

        self.sliderb = QSlider(self)
        self.sliderb.setOrientation(Qt.Horizontal)
        self.sliderb.resize(200, 40)
        self.sliderb.setMinimum(0)
        self.sliderb.setMaximum(100)
        self.sliderb.valueChanged.connect(self.setSliderbChange)

        self.externeltrigger = QGroupBox("External trigger", self)
        self.externeltrigger .resize(300, 50)

        self.startTributton = QPushButton("Start")
        self.startTributton.resize(40, 40)
        self.startTributton.setCheckable(True)
        self.startTributton.toggled.connect(self.starttriLaser)

        layout = QGridLayout()
        layout.addWidget(self.startbutton, 0, 0, 1, 1)
        layout.addWidget(self.atext, 1, 0, 1, 1)
        layout.addWidget(self.slidera, 1, 1, 1, 1)
        layout.addWidget(self.a1text, 1, 2, 1, 1)
        layout.addWidget(self.btext, 2, 0, 1, 1)
        layout.addWidget(self.sliderb, 2, 1, 1, 1)
        layout.addWidget(self.b1text, 2, 2, 1, 1)
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.startTributton)
        self.externeltrigger.setLayout(vbox)

        #layout.addWidget(self.externeltrigger,3,0,2,3)

        self.groupbox.setLayout(layout)

        v1box = QVBoxLayout()
        v1box.setAlignment(Qt.AlignCenter)
        v1box.addWidget(self.Lpower.groupbox)
        v1box.addWidget(self.groupbox)
        v1box.addWidget(self.externeltrigger)

        self.ww.setLayout(v1box)


    def startLaser(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if self.core.get_property(self.Lasername, "Laser Operation") == "On":
                    if self.core.get_property(self.Lasername, "Enable Fine") == "Off":
                        self.core.set_property(self.Lasername, "Enable Fine", "On")
                    else:
                        self.core.set_property(self.Lasername, "Enable Fine", "Off")
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def starttriLaser(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if self.core.get_property(self.Lasername, "Laser Operation") == "On":
                    if self.core.get_property(self.Lasername, "Enable ext trigger") == "Off":
                        self.core.set_property(self.Lasername, "Enable ext trigger", "On")
                    else:
                        self.core.set_property(self.Lasername, "Enable ext trigger", "Off")
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def setSlideraChange(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if self.core.get_property(self.Lasername, "Laser Operation") == "On" and self.core.get_property(self.Lasername, "Enable Fine") == "On":
                    self.core.set_property(self.Lasername, "Fine A (%)",float(self.slidera.value()))
                else:
                    str0 = ("Open the Laser and Fine")
                    QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def setSliderbChange(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if self.core.get_property(self.Lasername, "Laser Operation") == "On" and self.core.get_property(self.Lasername, "Enable Fine") == "On":
                    self.core.set_property(self.Lasername, "Fine B (%)", float(self.sliderb.value()))
                else:
                    str0 = ("Open the Laser and Fine")
                    QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LaserFinePanel()
    w.show()
    sys.exit(app.exec_())
