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
    '''contain all ui changes in loading'''
    pass

  def handleBtn(self):
    self.pushButton.clicked.connect(self.download)
    self.pushButton_2.clicked.connect(self.pickSaveFileLocation)
    self.pushButton_3.clicked.connect(self.pickSaveVideoLocation)
    self.pushButton_4.clicked.connect(self.downloadVideo)
    self.pushButton_5.clicked.connect(self.getVideoData)
    self.pushButton_6.clicked.connect(self.pickSavePlaylistLocation)
    self.pushButton_7.clicked.connect(self.downloadPlaylist)
    
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
    else: 
      print(videoUrl)
      video = pafy.new(videoUrl)
      print(video.title)
      print(video.duration)

      videoStreams = video.videostreams
      for stream in videoStreams:
        size = humanize.naturalsize(stream.get_filesize()) 
        data = '{} {} {} {}'.format(stream.mediatype, stream.extension, stream.quality, size)
        self.comboBox.addItem(data)

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

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainApp()
  window.show()
  app.exec_()