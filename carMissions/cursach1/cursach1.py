
from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow
import sys
from camera import Cam

import lineFollow as LF
import labirint as lab
import ballManipulation as bm

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_()) 

#bm.startMission()
#lab.labirintAlgorithm()
#LF.lineFollow()
#if __name__ == "__main__":
#    main()