from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import os
import os.path
import urllib.request

ui,_ = loadUiType('assets/UI/Download.ui')

class MainApp(QMainWindow, ui):
  def __init__(self, parent=None):
    super(MainApp, self).__init__(parent)
    QMainWindow.__init__(self)
    self.setupUi(self)
    self.initialize()
    self.handleBtn()

  def initialize(self):
    '''contain all ui changes in loading'''
    pass

  def handleBtn(self):
    self.pushButton.clicked.connect(self.download)
    self.pushButton_2.clicked.connect(self.handleBrowse)
    

  def handleProgress(self, blocknum, blocksize, totalsize):
    '''calculate the progress downloading'''
    readedData = blocknum * blocksize
    if totalsize > 0:
      downloadPercentage = readedData * 100 / totalsize
      self.progressBar.setValue(downloadPercentage)
      QApplication.processEvents() # pending events to process

  def handleBrowse(self):
    '''enable browse to pick save location'''
    try:
      saveLocation = QFileDialog.getSaveFileName(self, caption='Save as', directory='.', filter='All Files(*.*)')

      print(saveLocation)

      self.lineEdit_2.setText(saveLocation[0])
    except:
      pass
    

  def download(self):
    print('downloading...')

    downloadUrl = self.lineEdit.text()
    saveLocation = self.lineEdit_2.text()

    if downloadUrl == '' or saveLocation == '':
      QMessageBox.warning(self, 'Data Error', 'URL hoặc save location không hợp lệ')
    else:
      try:
        urllib.request.urlretrieve(downloadUrl, saveLocation, self.handleProgress)
      except Exception:
        QMessageBox.warning(self, 'Download Error', 'URL hoặc save location không hợp lệ')
        return 
    self.progressBar.setValue(100)
    QMessageBox.information(self, 'Tải thành công', 'Tải xuống thành công!')

    # Reset
    self.lineEdit.setText('')
    self.lineEdit_2.setText('')
    self.progressBar.setValue(0)

  def save(self):
    pass

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainApp()
  window.show()
  app.exec_()