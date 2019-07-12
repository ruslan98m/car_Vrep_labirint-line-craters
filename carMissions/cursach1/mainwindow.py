from PyQt5 import QtCore, QtGui, QtWidgets
import vrep
import vrepConst
import lineFollow as LF
import labirint as lab
import ballManipulation as bm

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(743, 467)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.StartButton = QtWidgets.QPushButton(self.centralWidget)
        self.StartButton.setGeometry(QtCore.QRect(490, 320, 101, 61))
        self.StartButton.setObjectName("StartButton")

        self.StopButton = QtWidgets.QPushButton(self.centralWidget)
        self.StopButton.setGeometry(QtCore.QRect(600, 320, 101, 61))
        self.StopButton.setObjectName("StopButton")

        self.radioButton = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton.setGeometry(QtCore.QRect(30, 290, 95, 20))
        self.radioButton.setObjectName("radioButton")

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 320, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")

        self.radioButton_3 = QtWidgets.QRadioButton(self.centralWidget)
        self.radioButton_3.setGeometry(QtCore.QRect(30, 350, 95, 20))
        self.radioButton_3.setObjectName("radioButton_3")

        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 40, 113, 22))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 70, 113, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(40, 100, 113, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(140, 300, 331, 101))
        self.textEdit.setObjectName("textEdit")

        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 81, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 81, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 81, 16))
        self.label_3.setObjectName("label_3")

        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(160, 30, 256, 256))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.frame_2 = QtWidgets.QFrame(self.centralWidget)
        self.frame_2.setGeometry(QtCore.QRect(430, 30, 256, 256))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")


        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(40, 200, 113, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")


        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(10, 200, 81, 16))
        self.label_4.setObjectName("label_4")

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 743, 26))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)

        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.StartButton.setText(_translate("MainWindow", "Start"))
        self.StopButton.setText(_translate("MainWindow", "Stop"))
        self.radioButton.setText(_translate("MainWindow", "lineFollow"))
        self.radioButton_2.setText(_translate("MainWindow", "labirint"))
        self.radioButton_3.setText(_translate("MainWindow", "ballDetection"))
        self.label.setText(_translate("MainWindow", "x"))
        self.label_2.setText(_translate("MainWindow", "y"))
        self.label_3.setText(_translate("MainWindow", "dir"))
        self.label_4.setText(_translate("MainWindow", "time"))

        self.makeConects()



    def convertToQtFormat(self,image,label):
        qtFormat = QtGui.QImage(image.data, rgbImage.shape[1], rgbImage.shape[0],QtGui.QImage.Format_RGB888)                                        
        qtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QtGui.QPixmap(qtFormat)

        resizeImage = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        QtWidgets.QApplication.processEvents()
        label.setPixmap(resizeImage)

    def makeConects(self):
        self.StartButton.clicked.connect(self.startButtonClick)
        self.StopButton.clicked.connect(self.stopButtonClick)
        
    def startButtonClick(self):
       if self.radioButton.isChecked():
           print(1)
           LF.lineFollow()
       elif self.radioButton_2.isChecked():
           print(2)
           lab.labirintAlgorithm()
       elif self.radioButton_3.isChecked():
           print(3)
           bm.startMission()
            
    
    def stopButtonClick(self):
        vrep.simxFinish(-1)