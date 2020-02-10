import os
import sys
import getpass
import cv2
import time
import tensorflow as tf
import cvlib as cv
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QApplication, QStatusBar

# UI Files
from ui import mainwindow
# from inputmonitor_ui import App

#Detection Files
from detection.utils import *
from detection import adaptive_gamma


class Worker(QtCore.QRunnable):
    def __init__(self, func):
        super(Worker, self).__init__()
        self.func = func

    def run(self):
        while(1):
            self.func()
            time.sleep(.2)

class VideoThread(QtCore.QRunnable):
    def __init__(self, func):
        super(VideoThread, self).__init__()
        self.func = func

    def run(self):
        while(1):
            self.func()


class GUI(mainwindow.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, maya=False):
        super(GUI, self).__init__()
        self.setupUi(self)
        self.statusBar = QStatusBar()
        self.statusbar.showMessage('Ready')
        self.maya = maya
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()
        self.build_functions()

        #Threading
        # self.inputMonitor = App()
        self.worker = Worker(self.updateLabel)
        self.videoThread = VideoThread(self.video)
        self.threadpool = QtCore.QThreadPool()

        #Triggering Thread
        self.threadpool.start(self.worker)
    
        #Extras
        self.handTrigger = 40
        self.face = False
        self.falseTimer = 0.0
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.actionTimer = 0.0

        #Set Graph and Sess
        self.graph, self.sess = load_graph("detection/pretrained_model.pb")
    def closeEvent(self, event):
        self.menuExit()

    def menuExit(self):
        try:
            os.system("vlc-ctrl quit -c command -r 2,1 -f 2")
        except:
            pass
        sys.exit()

    # def menuMonitor_Input(self):
    #     self.inputMonitor.show()


    def detectFace(self, frame):
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces, confidence = cv.detect_face(frame)

        if len(faces) == 0:
            # self.face = False
            if self.falseTimer == 0.0:
                self.falseTimer = time.time()
            else:
                if (time.time() - self.falseTimer) >=  1:
                    self.face = False
                else:
                    self.face = True
        else:
            self.face = True
            self.falseTimer = 0.0
        # print(self.falseTimer/1000000000)

    def video(self):
        ret, frame = self.camera.read()
        frame = cv2.flip(frame, 1)
        
        # self.draw(frame)
        cv2.waitKey(1)
        self.detectFace(frame)
        self.perform_vlc_play_pause(self.face)

        #Preprocessing Image
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if(self.face == True):
            self.handTrigger = total_predict(frame, self.graph, self.sess)
            self.perform_vlc_action(self.handTrigger)
        self.statusbar.showMessage("Face : " + str(self.face) + "  Trigger : " + str(self.handTrigger))

    def perform_vlc_action(self, action):
        if action == 1:
            os.system("vlc-ctrl volume -0.05")
        if action == 2:
            os.system("vlc-ctrl volume +0.05")
        # print(time.time() - self.actionTimer)
        if (time.time() - self.actionTimer) > 5 or self.actionTimer == 0:
            if action == 6:
                os.system("vlc-ctrl prev")
                self.prevAction = action
                self.actionTimer = time.time()
            if action == 7:
                os.system("vlc-ctrl next")
                self.prevAction = action
                self.actionTimer = time.time()
            

    def perform_vlc_play_pause(self, face):
        if(face == True):
            os.system("vlc-ctrl play")
        else:
            os.system("vlc-ctrl pause")

    def updateLabel(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        fileName = file_path.split('/')[-1]
        if('.' in fileName):
            # print('Changed')
            self.label.setText(fileName)
        else:
            self.label.setText("")


    def build_functions(self):
        self.actionExit.triggered.connect(self.menuExit)
        # self.actionInput_Monitor.triggered.connect(self.menuMonitor_Input)
        self.pushButton.clicked.connect(self.open_file)

    def populate(self):
        path = "/home/" + getpass.getuser() +  "/"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Play")
        open.triggered.connect(self.open_file)
        openAll = menu.addAction("Play All")
        openAll.triggered.connect(self.openAll_file)

        if self.maya:
            open_file = menu.addAction("Open file")
            open_file.triggered.connect(lambda: self.maya_file_operations(open_file=True))

            import_to_maya = menu.addAction("Import to Maya")
            import_to_maya.triggered.connect(self.maya_file_operations)

            reference_to_maya = menu.addAction("Add reference to Maya")
            reference_to_maya.triggered.connect(lambda: self.maya_file_operations(reference=True))

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        valid_extensions = ['avi', 'mp4', 'mkv', 'mp3']
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        full_command = "vlc-ctrl play -p " + file_path
        print(file_path.split('.')[-1])
        if file_path.split('.')[-1] in valid_extensions:
            fileName = file_path.split('/')[-1]
            self.label.setText(str(fileName))
            print(full_command)
            self.threadpool.start(self.videoThread)
            os.system(full_command)
        
    def openAll_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        dir = "/"
        for i in file_path.split('/')[:-1]:
            dir += i + '/'
        full_command = "vlc-ctrl play -p " + dir
        self.threadpool.start(self.videoThread)
        os.system(full_command)
        

    def maya_file_operations(self, reference=False, open_file=False):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        import maya.cmds as cmds
        if reference:
            cmds.file(file_path, reference=True, type='mayaAscii', groupReference=True)
        elif open_file:
            file_location = cmds.file(query=True, location=True)
            if file_location == 'unknown':
                cmds.file(file_path, open=True, force=True)
            else:
                modify_file = cmds.file(query=True, modified=True)
                if modify_file:
                    result = cmds.confirmDialog(title='Opening new maya file',
                                                message='This file is modified. do you want to save this file.?',
                                                button=['yes', 'no'],
                                                defaultButton='yes',
                                                cancelButton='no',
                                                dismissString='no')
                    if result == 'yes':
                        cmds.file(save=True, type='mayaAscii')
                        cmds.file(file_path, open=True, force=True)
                    else:
                        cmds.file(file_path, open=True, force=True)
                else:
                    cmds.file(file_path, open=True, force=True)
        else:
            cmds.file(file_path, i=True, groupReference=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    app.exec_()