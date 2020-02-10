import os
import sys
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# # UI Files
# from ui import inputmonitor
# class Thread(QThread):
#     changePixmap = pyqtSignal(QImage)
#     def run(self):
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, frame = cap.read()
#             # rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             h, w, ch = frame.shape
#             bytesPerLine = ch * w
#             cv2.imshow('a', frame)
#             convertToQtFormat = QtGui.QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
#             p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
#             self.changePixmap.emit(p)
    
# class InputMonitor(inputmonitor.Ui_MainWindow ,QMainWindow):
#     def __init__(self):
#         super(InputMonitor, self).__init__()
#         MainWindow = QtWidgets.QMainWindow()
#         self.setupUi(MainWindow)
#         self.initUI()
#         MainWindow.show()
#         sys.exit(app.exec_())
        

#     @pyqtSlot(QImage)
#     def setImage(self, image):
#         self.label.setPixmap(QPixmap.fromImage(image))

#     def initUI(self):
#         th = Thread(self)
#         th.changePixmap.connect(self.setImage)
#         th.start()

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = InputMonitor()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())