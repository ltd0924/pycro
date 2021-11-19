import sys
import random
from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QDateTimeAxis, QValueAxis, QLineSeries
from PyQt5.QtCore import QDateTime, QTimer,Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMessageBox, QApplication
from pycromanager import Bridge


class TimeChart(QChartView):
    def __init__(self):
        super().__init__()
        self.resize(1500,500)
        self.limitminute = 3
        self.maxpos=10
        self.curpos=0
        self.curtime=60
        self.setRenderHint(QPainter.Antialiasing)
        self.initUI()


    def initUI(self):
        self.Timechart = QChart()
        self.posseries = QLineSeries()
        self.Timechart.addSeries(self.posseries)
        self.dtaxisX =  QValueAxis()
        self.dtaxisX.setMin(0)
        self.dtaxisX.setMax(60)
        self.dtaxisX.setTickCount(6)

        self.vlaxisY = QValueAxis()
        self.vlaxisY.setMin(0)
        self.vlaxisY.setMax(self.maxpos)  # 设置y轴最大值
        self.vlaxisY.setTickCount(6)
        self.vlaxisY.setGridLineVisible(True)
        self.vlaxisY.setGridLineColor(Qt.gray)
        self.Timechart.addAxis(self.vlaxisY, Qt.AlignLeft)
        self.Timechart.addAxis(self.dtaxisX, Qt.AlignBottom)
        self.Timechart.legend().setVisible(False)
        self.posseries.attachAxis(self.vlaxisY)
        self.posseries.attachAxis(self.dtaxisX)
        self.dtaxisX.setVisible(False)
        self.setChart(self.Timechart)

    def timer_init(self):
        # 使用QTimer，0.5秒触发一次，更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.drawLine)
        self.timer.start(500)

    def drawLine(self):
        try:
            with Bridge() as bridge:
                self.core = bridge.get_core()  # cmm core
                curpos = self.core.get_property("PIZStage", "Position")
                print(self.core.get_version_info())
        except:
            curpos = self.curpos
            str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
            #QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)


        pass

        self.curtime=self.curtime+1
        maxposs = float(curpos)
        minposs = float(curpos)
        for i in range(self.posseries.count()):
            if self.posseries.at(i).y() > maxposs:
                maxposs = self.posseries.at(i).y()
            if self.posseries.at(i).y() <minposs:
                minposs = self.posseries.at(i).y()
        self.vlaxisY.setMax(float(maxposs) * 1.2)
        self.vlaxisY.setMin(float(minposs)/1.2)
        self.dtaxisX.setMin(self.curtime-60)
        self.dtaxisX.setMax(self.curtime)
        if (self.posseries.count() > 60):
            self.posseries.removePoints(0, self.posseries.count() -60)

        self.posseries.append(self.curtime, float(curpos))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = TimeChart()
    view.show()
    sys.exit(app.exec_())



