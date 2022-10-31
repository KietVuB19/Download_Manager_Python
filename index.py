from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import os
import os.path
import urllib.request
import pafy
import humanize
import youtube_dl
from pytube import Playlist

ui,_ = loadUiType('assets/UI/Download.ui')
pafy.set_api_key('AIzaSyDAeZgCfL0vcZEvyDKnwBvnR9buakJMc4M')

class MainApp(QMainWindow, ui):
  def __init__(self, parent=None):
    super(MainApp, self).__init__(parent)
    QMainWindow.__init__(self)
    self.setupUi(self)
    self.initialize()
    self.handleBtn()

  def initialize(self):
    self.tabWidget.tabBar().setVisible(False)
    self.darkorangeStyle()
    # self.Move_Box_1()
    # self.Move_Box_2()
    # self.Move_Box_3()
    # self.Move_Box_4()
    
  def handleBtn(self):
    self.pushButton.clicked.connect(self.download)
    self.pushButton_2.clicked.connect(self.pickSaveFileLocation)
    self.pushButton_3.clicked.connect(self.pickSaveVideoLocation)
    self.pushButton_4.clicked.connect(self.downloadVideo)
    self.pushButton_5.clicked.connect(self.getVideoData)
    self.pushButton_6.clicked.connect(self.pickSavePlaylistLocation)
    self.pushButton_7.clicked.connect(self.downloadPlaylist)
    self.pushButton_8.clicked.connect(self.openHome)
    self.pushButton_9.clicked.connect(self.openDownload)
    self.pushButton_10.clicked.connect(self.openYoutube)
    self.pushButton_11.clicked.connect(self.openSetting)
    self.pushButton_12.clicked.connect(self.darkorangeStyle)
    self.pushButton_13.clicked.connect(self.qdarkStyle)
    # self.pushButton_14.clicked.connect(self.darkgrayStyle)
    self.pushButton_15.clicked.connect(self.darkbluStyle)
    
  def handleProgress(self, blocknum, blocksize, totalsize):
    '''calculate the progress downloading'''
    readedData = blocknum * blocksize
    if totalsize > 0:
      downloadPercentage = readedData * 100 / totalsize
      self.progressBar.setValue(downloadPercentage)
      QApplication.processEvents() # pending events to process

  def pickSaveFileLocation(self):
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
      return
   
    try:
      urllib.request.urlretrieve(downloadUrl, saveLocation, self.handleProgress)
    except Exception as e:
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

  def pickSaveVideoLocation(self):
    try:
      saveLocation = QFileDialog.getSaveFileName(self, caption='Save as', directory='.', filter='All Files(*.*)')

      self.lineEdit_4.setText(saveLocation[0])
    except:
      pass

  def getVideoData(self): 
    '''Lấy thông tin của video'''
    videoUrl = self.lineEdit_3.text()

    if videoUrl == '':
      QMessageBox.warning(self, 'Data Error', 'URL không hợp lệ')
      return

    try:
      print(videoUrl)
      video = pafy.new(videoUrl)
      print(video.title)
      print(video.duration)

      videoStreams = video.videostreams
      for stream in videoStreams:
        size = humanize.naturalsize(stream.get_filesize()) 
        data = '{} {} {} {}'.format(stream.mediatype, stream.extension, stream.quality, size)
        self.comboBox.addItem(data)
    except Exception as e:
      print(e)
      return

  def downloadVideo(self):
    videoUrl = self.lineEdit_3.text()
    saveLocation = self.lineEdit_4.text()

    if videoUrl == '' or saveLocation == '':
      QMessageBox.warning(self, 'Data Error', 'URL hoặc Location không hợp lệ')
      return 
    
    try:
      video = pafy.new(videoUrl)
      # bestaudio = video.getbestaudio()
      # bestaudio.download()
      videoStream = video.videostreams
      videoQuality = self.comboBox.currentIndex()
      download = videoStream[videoQuality].download(filepath=saveLocation, callback=self.videoProgress)
    except Exception as e:
      print(e)
      return
    
    QMessageBox.information(self, 'Tải thành công', 'Tải xuống thành công!')

    # Reset
    self.lineEdit_3.setText('')
    self.lineEdit_4.setText('')
    self.progressBar_2.setValue(0)
    self.label_5.setText ('')
    self.comboBox.clear()

  def videoProgress(self, totalsize, received, ratio, rate, time):
    readedData = received
    if totalsize > 0:
      downloadPercentage = readedData * 100 / totalsize
      self.progressBar_2.setValue(downloadPercentage)
      
      if time < 60: 
        self.label_5.setText('{} seconds remaining'.format(time))
      elif time < 60*60: 
        self.label_5.setText('{} minutes remaining'.format(time//60))
      else:
        self.label_5.setText('{} hours remaining'.format(time//3600))

      QApplication.processEvents()

  def downloadPlaylist(self):
    playlistUrl = self.lineEdit_5.text()
    saveLocation = self.lineEdit_6.text()

    if playlistUrl == '' or saveLocation == '':
      QMessageBox.warning(self, 'Data Error', 'URL hoặc Location không hợp lệ')
      return 
    
      # ydl_opts= {}
      # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      #   playlistVideos = ydl.extract_info(playlistUrl, download=False)
      #   print(playlistVideos)   
    # try:
    playlistVideos = pafy.get_playlist2(playlistUrl)
    self.lcdNumber_2.display(len(playlistVideos))
    title = playlistVideos.title
    print(title)

    os.chdir(saveLocation)
    if os.path.exists(title):
      os.chdir(title)
    else:
      os.mkdir(title)
      os.chdir(title)
    
    currentVideo = 1 
    quality = self.comboBox_2.currentIndex()
    QApplication.processEvents()

    for video in playlistVideos:
      try:
        self.lcdNumber.display(currentVideo)
        cur_stream = video.videostreams
        print(quality)
        download = cur_stream[quality].download(callback=self.playlistProgress)
        QApplication.processEvents()

        currentVideo += 1
      except Exception as e:
        print(e)
        return

  def playlistProgress(self, totalsize, received, ratio, rate, time):
    readedData = received
    if totalsize > 0:
      downloadPercentage = readedData * 100 / totalsize
      self.progressBar_3.setValue(downloadPercentage)
      
      if time < 60: 
        self.label_6.setText('{} seconds remaining'.format(time))
      elif time < 60*60: 
        self.label_6.setText('{} minutes remaining'.format(time//60))
      else:
        self.label_6.setText('{} hours remaining'.format(time//3600))

      QApplication.processEvents()

  def pickSavePlaylistLocation(self): 
    saveLocation = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
    self.lineEdit_6.setText(saveLocation)

  # Change UI
  def openHome(self):
    self.tabWidget.setCurrentIndex(0)

  def openDownload(self):
    self.tabWidget.setCurrentIndex(1)

  def openYoutube(self):
    self.tabWidget.setCurrentIndex(2)

  def openSetting(self):
    self.tabWidget.setCurrentIndex(3)

  def darkorangeStyle(self):
    style = open(r'assets/themes/darkorange.css')
    style = style.read()
    self.setStyleSheet(style)

  def qdarkStyle(self):
    style = open(r'assets/themes/qdark.css')
    style = style.read()
    self.setStyleSheet(style)

  # def darkgrayStyle(self):
  #   style = open(r'assets/themes/qdarkgray.css')
  #   style = style.read()
  #   self.setStyleSheet(style)

  def darkbluStyle(self):
    style = open(r'assets/themes/darkblu.css')
    style = style.read()
    self.setStyleSheet(style)

  def Move_Box_1(self):
    box_animation1 = QPropertyAnimation(self.groupBox , b"geometry")
    box_animation1.setDuration(2500)
    box_animation1.setStartValue(QRect(0,0,0,0))
    box_animation1.setEndValue(QRect(60,40,281,141))
    box_animation1.start()
    self.box_animation1 = box_animation1


  def Move_Box_2(self):
    box_animation2 = QPropertyAnimation(self.groupBox_2 , b"geometry")
    box_animation2.setDuration(2500)
    box_animation2.setStartValue(QRect(0,0,0,0))
    box_animation2.setEndValue(QRect(380,40,281,141))
    box_animation2.start()
    self.box_animation2 = box_animation2


  def Move_Box_3(self):
    box_animation3 = QPropertyAnimation(self.groupBox_3 , b"geometry")
    box_animation3.setDuration(2500)
    box_animation3.setStartValue(QRect(0,0,0,0))
    box_animation3.setEndValue(QRect(60,210,281,141))
    box_animation3.start()
    self.box_animation3 = box_animation3


  def Move_Box_4(self):
    box_animation4 = QPropertyAnimation(self.groupBox_4 , b"geometry")
    box_animation4.setDuration(2500)
    box_animation4.setStartValue(QRect(0,0,0,0))
    box_animation4.setEndValue(QRect(380,210,281,141))
    box_animation4.start()
    self.box_animation4 = box_animation4

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainApp()
  window.show()
  app.exec_()