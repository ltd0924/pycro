import sys

from PyQt5.QtWidgets import QWidget, QGroupBox, QLabel, QSlider, QComboBox, QGridLayout, QLineEdit, QApplication, \
    QMessageBox
from PyQt5.QtCore import Qt
from pycromanager import Bridge

class LasertriggerPanel(QWidget):
    def __init__(self,n):
        super(LasertriggerPanel, self).__init__()
        self.num=n
        self.initUI()

    def initUI(self):
        self.groupbox=QGroupBox("Laser",self)
        self.groupbox.resize(300,200)

        self.triggermode=QLabel(self)
        self.triggermode.setText("Trigger mode:")
        self.triggermode.setAlignment(Qt.AlignLeft)
        self.triggermode.resize(40, 20)

        self.pulse = QLabel(self)
        self.pulse.setText("Pulse length(us):")
        self.pulse.setAlignment(Qt.AlignLeft)
        self.pulse.resize(40, 20)

        self.sequences = QLabel(self)
        self.sequences.setText("Trigger sequence:")
        self.sequences.setAlignment(Qt.AlignLeft)
        self.sequences.resize(40, 20)

        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.resize(100, 20)
        self.slider.setMaximum(65535)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.slidersetpulse)



        self.pulseedit = QLineEdit(self)
        self.pulseedit.resize(40, 23)
        self.pulseedit.setAlignment(Qt.AlignCenter)
        self.pulseedit.textChanged.connect(self.setpulse)

        self.seqedit = QLineEdit(self)
        self.seqedit.resize(40, 23)
        self.seqedit.setAlignment(Qt.AlignCenter)
        self.seqedit.textChanged.connect(self.setsequence)



        self.Trigger_LasercomboBox = QComboBox()
        self.Trigger_LasercomboBox.addItems(["Off","On","Rising","Falling","Camera"])
        self.Trigger_LasercomboBox.activated.connect(self.modeselect)

        self.Tlayout = QGridLayout(self)
        self.Tlayout.addWidget(self.pulse, 1, 0, 1, 1)
        self.Tlayout.addWidget(self.slider, 2, 0, 1, 2)
        self.Tlayout.addWidget(self.pulseedit, 1, 1, 1, 1)
        self.Tlayout.addWidget(self.sequences, 3, 0, 1, 1)
        self.Tlayout.addWidget(self.seqedit, 3, 1, 1, 1)
        self.Tlayout.addWidget(self.triggermode, 0, 0, 1, 1)
        self.Tlayout.addWidget(self.Trigger_LasercomboBox, 0, 1, 1, 1)

        self.groupbox.setLayout(self.Tlayout)

    def setsequence(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if (self.Trigger_LasercomboBox.currentIndex() == 2 or self.Trigger_LasercomboBox.currentIndex() == 3) or self.Trigger_LasercomboBox.currentIndex() == 4:
                    d=int(self.seqedit.text())
                    if d>65535 or d <0:
                        str0 = ("请输入 0-65535")
                        QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
                    else:
                        self.core.set_property("Mojo-LaserTrig", "Sequence"+str(self.num), d)

                else:
                    str0 = ("请在 Failing 或 Rising 模式使用")
                    QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def setpulse(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                if self.Trigger_LasercomboBox.currentIndex()==2 or self.Trigger_LasercomboBox.currentIndex()==3:
                    d = int(self.pulseedit.text())
                    if d > 65535 or d < 0:
                        str0 = ("请输入 0-65535")
                        QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
                    else:
                        self.core.set_property("Mojo-LaserTrig", "Duration"+str(self.num), d)
                        self.slider.setValue(d)
                else:
                    str0 = ("请在 Failing ,Rising 或 Camera 模式使用")
                    QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def slidersetpulse(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                self.core.set_property("Mojo-LaserTrig", "Duration"+str(self.num), int(self.slider.value()))
                self.pulseedit.setText(self.slider.value())
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)

    def modeselect(self):
        try:
            with Bridge() as bridge:
                self.core=bridge.get_core()
                self.core.set_property("Mojo-LaserTrig","Mode"+str(self.num),self.Trigger_LasercomboBox.currentIndex())
        except:
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = LasertriggerPanel(1)
    w.show()

    sys.exit(app.exec_())

