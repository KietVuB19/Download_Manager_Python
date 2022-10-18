from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import os
import os.path

ui,_ = loadUiType('assets/UI/Download.ui')

class MainApp(QMainWindow, ui):
  def __init__(self, parent=None):
    super(MainApp, self).__init__(parent)
    QMainWindow.__init__(self)
    self.setupUi(self)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainApp()
  window.show()
  app.exec_()

