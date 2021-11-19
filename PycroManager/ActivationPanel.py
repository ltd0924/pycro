import sys

from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QLabel, QSlider, QPushButton, QGridLayout, QMessageBox, \
    QApplication, QCheckBox
from PyQt5.QtCore import Qt
from pycromanager import Bridge
from actChart import actChart


class ActivationPanel(QWidget):
    def __init__(self):
        super(ActivationPanel, self).__init__()
        self.initUI()

    def initUI(self):
        self.ww=QWidget(self)
        self.ww.resize(450,400)
        self.sdcoefftext=QLabel(self)
        self.sdcoefftext.setText("Sd coeff:")
        self.sdcoefftext.resize(40,20)
        self.sdline = QLineEdit(self)
        # The higher the Sd coefficient, the higher the auto cutoff value.double
        self.sdline.setText("1.5")
        self.sdline.resize(40, 20)
        #self.sdline.textEdited.connect(self.setsd)

        self.feedbacktext=QLabel(self)
        self.feedbacktext.setText("Feedback:")
        #The higher the Feedback coefficient, the faster the activation ramps up.double
        self.feedbacktext.resize(40,20)
        self.fdline = QLineEdit(self)
        self.fdline.setText("0.4")
        self.fdline.resize(40, 20)
        #self.fdline.textEdited.connect(self.setfd)

        self.avertext=QLabel(self)
        self.avertext.setText("Average:")
        #Averaging time (in number of frames) of the auto cutoff.double
        self.avertext.resize(40,20)
        self.avline=QLineEdit(self)
        self.avline.setText("1.0")
        self.avline.resize(40,20)
       # self.avline.textEdited.connect(self.setav)

        self.actibox=QCheckBox("Activate")
        #Turn on activation
        self.actibox.resize(30,20)
       # self.activtext.stateChanged.connect(self.setact)

        self.getN = QPushButton("Get N:")
        # Averaging time (in number of frames) of the auto cutoff.
        self.getN.resize(40, 20)
        '''
         public void actionPerformed(java.awt.event.ActionEvent evt) {
                String val = String.valueOf(graph_.getLastPoint());
                textfieldN0_.setText(val);
                N0_ = graph_.getLastPoint();
            }
        '''
        self.getnline=QLineEdit(self)
        self.getnline.setText("1.0")
        #Target number of emitters.
        self.avline.resize(40,20)

        self.cutline=QLineEdit(self)
        self.cutline.setText("100.0")
        #Cutoff of the detected peak pixel value.
        self.cutline.resize(30,20)

        self.runButton = QPushButton("Run")
        self.runButton.resize(40, 30)
        #Start/stop the emitter estimation script.
        #runActivation(b)

        self.autoButton = QPushButton("Auto")
        #Turn on automated cutoff.bool
        self.autoButton.resize(40, 20)

        self.clearButton=QPushButton("Clear")
        # public void actionPerformed(java.awt.event.ActionEvent evt) {graph_.clearChart();}});
        self.clearButton.resize(40,20)

        self.nmsbox = QCheckBox("NMS")
        self.nmsbox.resize(30, 20)
        #Show/hide the last image with the detected emitters. bool

        self.graphh=actChart(float(self.getnline.text()))
        self.graphh.resize(300,240)

        layout=QGridLayout()
        layout.addWidget(self.sdcoefftext,0,0,1,1)
        layout.addWidget(self.sdline,1,0,1,1)
        layout.addWidget(self.feedbacktext,2,0,1,1)
        layout.addWidget(self.fdline,3,0,1,1)
        layout.addWidget(self.avertext,4,0,1,1)
        layout.addWidget(self.avline,5,0,1,1)
        layout.addWidget(self.getN,7,0,1,1)
        layout.addWidget(self.getnline,8,0,1,1)
        layout.addWidget(self.graphh,0,1,11,6)
        layout.addWidget(self.actibox,12,0,1,1)
        layout.addWidget(self.runButton,13,0,2,1)
        layout.addWidget(self.cutline,14,3,1,1)
        layout.addWidget(self.autoButton,14,4,1,1)
        layout.addWidget(self.clearButton,14,5,1,1)
        layout.addWidget(self.nmsbox,14,6,1,1)

        self.ww.setLayout(layout)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = ActivationPanel()
    view.show()
    sys.exit(app.exec_())



