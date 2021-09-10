from PyQt5.QtWidgets import QComboBox, QMessageBox

from untitled import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QDateTimeAxis,QValueAxis,QSplineSeries,QChart,QChartView
import sys

from pycromanager import Bridge


class queryWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)





    def button_call_back_1(self, q):

        rows = self.ui.tableWidget.rowCount()
        if 1 == q:
            self.ui.tableWidget.setRowCount(rows + 1)
            list1 = ['list' + str(rows), 'chemistry', "data1", "data2"]
            self.set_table1_Property(rows, 3, list1)

            print(rows + 1)
        elif 2 == q:
            self.ui.tableWidget.setRowCount(rows - 1 if rows > 1 else rows)
        elif 3 == q:

            talbe = self.ui.tableWidget
            row3 = talbe.rowCount()
            col3 = talbe.columnCount()
            print("value[{0},{1}]".format(row3, col3))

            # talbe.update()
            try:
                with Bridge() as bridge:
                        core = bridge.get_core()#cmm core
                        print(core.get_device_adapter_names())
                        #core.get_version_info()
                        size = 3
                        data = [None] * size
                        for i in range(row3):

                            for j in range(size):  # core.set_property 一般就三个变量，根据需要自行修改

                                try:
                                    data[j] = talbe.item(i, j).text()
                                    # print("value[{0} ,{1}] == {2}".format(i, j, talbe.item(i, j).text()))
                                except:
                                    str1 = "表格[{0} ,{1}] 内容为空，没值".format(i, j)
                                    QMessageBox.question(self, "消息框", str1, QMessageBox.Yes | QMessageBox.No)
                                    print(str1)

                            # core.get_property("Core", 'TimeoutMs')
                            # core.set_property('Core', 'TimeoutMs', 20000)
                            str2 = "core.set_property({0},{1} ,{2})".format(data[0], data[1], data[2])
                            str2_0="第{0}行指令设置失败：".format(i+1)
                            try:
                                core.set_property(data[0], data[1], data[2])
                            except:
                                QMessageBox.question(self, str2_0, str2, QMessageBox.Yes | QMessageBox.No)

                            print(str2)
                            # core.set_property(data[0],data[1] ,data[2])

            except:
                str0 = ("本软件依赖pycromanager库 ，请先打开Micro-Manager 2.0gamma，用于打开对应端口")
                QMessageBox.question(self, "消息框", str0, QMessageBox.Yes)



            pass

    def slider_call_back(self, q):
        if 1 == q:
            values = self.ui.horizontalSlider.value()
            self.ui.label.setText("value: " + str(values))


        elif 2 == q:
            pass
        elif 3 == q:
            pass

    def set_table1_Property(self, row, col, content_list):

        genderComb = QComboBox()

        for i in content_list:
            genderComb.addItem(i)

        self.ui.tableWidget.setCellWidget(row, col, genderComb)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = queryWindow()
    window.show()
    sys.exit(app.exec_())
