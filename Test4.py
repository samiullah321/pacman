from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def clicked(self):
        print(self.depthin.text())
        print(self.NoGin.text())
        print(self.iterationin.text())
        print(self.comboBox.currentText())
        print(self.comboBox_2.currentText())
        print(self.comboBox_3.currentText())
        if (self.Displaycheck.isChecked() == True):
            CheckState = True
        else:
            CheckState = False
        self.plainTextEdit.show()
        self.label_2.show()

    def quitclicked(self):
         app.quit()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(837, 848)
        MainWindow.setStyleSheet("#MainWindow { border-image: url(dasdasdascx.jpg) 0 0 0 0 stretch stretch; }")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.picture1 = QtWidgets.QLabel(self.centralwidget)
        self.picture1.setGeometry(QtCore.QRect(-330, -170, 1531, 1021))
        self.picture1.setStyleSheet(".playbutton{\n"
"background:#FDE402;\n"
"}")
        self.picture1.setText("")
        self.picture1.setScaledContents(False)
        self.picture1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.picture1.setObjectName("picture1")
        self.playbutton = QtWidgets.QPushButton(self.centralwidget)
        self.playbutton.setGeometry(QtCore.QRect(670, 770, 151, 61))
        self.playbutton.setStyleSheet("background:#FDE402;\n"
"font: 87 18pt \"Source Sans Pro Black\";\n"
"color: #0C1735;")
        self.playbutton.setAutoDefault(False)
        self.playbutton.setDefault(False)
        self.playbutton.setFlat(False)
        self.playbutton.setObjectName("playbutton")
        self.QUIT = QtWidgets.QPushButton(self.centralwidget)
        self.QUIT.setGeometry(QtCore.QRect(20, 770, 151, 61))
        self.QUIT.setStyleSheet("background:#FDE402;\n"
"font: 87 18pt \"Source Sans Pro Black\";\n"
"color: #0C1735;")
        self.QUIT.setAutoDefault(False)
        self.QUIT.setDefault(False)
        self.QUIT.setFlat(False)
        self.QUIT.setObjectName("QUIT")
        self.paclabel = QtWidgets.QLabel(self.centralwidget)
        self.paclabel.setGeometry(QtCore.QRect(20, 120, 251, 41))
        self.paclabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.paclabel.setObjectName("paclabel")
        self.ghostlabel = QtWidgets.QLabel(self.centralwidget)
        self.ghostlabel.setGeometry(QtCore.QRect(20, 220, 231, 31))
        self.ghostlabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.ghostlabel.setObjectName("ghostlabel")
        self.maplabel = QtWidgets.QLabel(self.centralwidget)
        self.maplabel.setGeometry(QtCore.QRect(20, 310, 131, 41))
        self.maplabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.maplabel.setObjectName("maplabel")
        self.DepthLabel = QtWidgets.QLabel(self.centralwidget)
        self.DepthLabel.setGeometry(QtCore.QRect(20, 400, 181, 41))
        self.DepthLabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.DepthLabel.setObjectName("DepthLabel")
        self.IterationLabel = QtWidgets.QLabel(self.centralwidget)
        self.IterationLabel.setGeometry(QtCore.QRect(20, 490, 181, 41))
        self.IterationLabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.IterationLabel.setObjectName("IterationLabel")
        self.NoOfGhostLabel = QtWidgets.QLabel(self.centralwidget)
        self.NoOfGhostLabel.setGeometry(QtCore.QRect(20, 580, 221, 41))
        self.NoOfGhostLabel.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.NoOfGhostLabel.setObjectName("NoOfGhostLabel")
        self.Displaycheck = QtWidgets.QCheckBox(self.centralwidget)
        self.Displaycheck.setGeometry(QtCore.QRect(20, 670, 221, 41))
        self.Displaycheck.setStyleSheet("font: 87 18pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.Displaycheck.setObjectName("Displaycheck")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(20, 200, 191, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 170, 191, 22))
        self.comboBox.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"font: 87 16pt \"Source Sans Pro Black\";")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(20, 260, 191, 22))
        self.comboBox_2.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"font: 87 16pt \"Source Sans Pro Black\";")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(20, 350, 191, 22))
        self.comboBox_3.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"font: 87 16pt \"Source Sans Pro Black\";")
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(20, 290, 191, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(20, 370, 191, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.depthin = QtWidgets.QLineEdit(self.centralwidget)
        self.depthin.setGeometry(QtCore.QRect(20, 430, 191, 31))
        self.depthin.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"border:none;\n"
"font: 87 16pt \"Source Sans Pro Black\";\n"
"")
        self.depthin.setObjectName("depthin")
        self.NoGin = QtWidgets.QLineEdit(self.centralwidget)
        self.NoGin.setGeometry(QtCore.QRect(20, 610, 191, 31))
        self.NoGin.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"border:none;\n"
"font: 87 16pt \"Source Sans Pro Black\";")
        self.NoGin.setObjectName("NoGin")
        self.iterationin = QtWidgets.QLineEdit(self.centralwidget)
        self.iterationin.setGeometry(QtCore.QRect(20, 520, 191, 31))
        self.iterationin.setStyleSheet("background:transparent;\n"
"color:#FFE400;\n"
"border:none;\n"
"font: 87 16pt \"Source Sans Pro Black\";")
        self.iterationin.setObjectName("iterationin")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(20, 460, 191, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(20, 550, 191, 16))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(20, 640, 191, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 131, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("580b57fcd9996e24bc43c313.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(320, 180, 521, 561))
        self.plainTextEdit.hide()
        self.plainTextEdit.setStyleSheet("background-color: rgba(34,36,38,230);\n"
"border:2px solid #FFE400;\n"
"color:white;\n"
"font: 87 12pt \"Source Sans Pro Black\";\n"
"")
        self.plainTextEdit.setDocumentTitle("")
        self.plainTextEdit.setReadOnly(False)
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setCenterOnScroll(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(330, 150, 201, 21))
        self.label_2.hide()
        self.label_2.setStyleSheet("font: 87 12pt \"Source Sans Pro Black\";\n"
"color: white;")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.playbutton.setText(_translate("MainWindow", "P L A Y"))
        self.QUIT.setText(_translate("MainWindow", "QUIT"))
        self.paclabel.setText(_translate("MainWindow", "Choose Pacman Agent"))
        self.ghostlabel.setText(_translate("MainWindow", "Choose Ghost Agent"))
        self.maplabel.setText(_translate("MainWindow", "Maps"))
        self.DepthLabel.setText(_translate("MainWindow", "Depth"))
        self.IterationLabel.setText(_translate("MainWindow", "Iteration"))
        self.NoOfGhostLabel.setText(_translate("MainWindow", "Number OF Ghost"))
        self.Displaycheck.setText(_translate("MainWindow", "Show Display"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Reflex Agent"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Alpha Beta Agent"))
        self.comboBox.setItemText(2, _translate("MainWindow", "ExpectiMax Agent"))
        self.comboBox.setItemText(3, _translate("MainWindow", "MiniMax Agent"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Reflex Agent"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "MiniMax Agent"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Expectimax Agent"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "Alpha Beta Agent"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "Box"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "Classic"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "Trapped"))
        self.label_2.setText(_translate("MainWindow", "Terminal Output"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.playbutton.clicked.connect(ui.clicked)
    ui.QUIT.clicked.connect(ui.quitclicked)
    MainWindow.show()
    sys.exit(app.exec_())
