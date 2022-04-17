# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'command.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from CommandUi import *
import Common
from Common import *
from Logger import log


class Command(QtWidgets.QWidget, Ui_Command):
    deleteSignal = QtCore.pyqtSignal(QtWidgets.QWidget)
    def __init__(self, line: str):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.commandLEdit.setText(line)
        self.commandLEdit.editingFinished.connect(self.UpdateCommand)

        self.count = len(line)
        self.byteLabel.setText(repr(line)[1:-1])

        self.crlfCBox.currentIndexChanged.connect(self.UpdateCommand)

        self.sendButton.clicked.connect(self.Send)

        self.cancelButton.setIcon(QtGui.QIcon('Ressource\\trash.png'))
        self.cancelButton.setStyleSheet("background-color:transparent ;")
        self.cancelButton.clicked.connect(self.Delete)

        self.UpdateCommand()

    def getCmd(self) -> str:
        return self.commandLEdit.text()

    def UpdateCommand(self):
        line = self.GetAppendice(self.commandLEdit.text())
        self.nbcharLab.setText(f"{len(line)} caractères")
        line = repr(line)[1:-1] #Text with special character apparent.

        self.byteLabel.setText(line)

    def Send(self):
        try:
            if Common.serTh is not None and Common.serTh.running:

                line = self.commandLEdit.text()
                line = self.GetAppendice(line)
                Common.serTh.write(line.encode())

            else :
                Common.LogWidget.Log("Pas de port série ouvert", log.ERROR)

        except Exception as e :
            print(e)


    def Delete(self):
        self.deleteLater()
        self.deleteSignal.emit(self)


    def GetAppendice(self, msg: str):
        if msg.endswith("\r"):
            if self.crlfCBox.currentText() == "Pas de CR+LF":
                return msg[-1]
            if self.crlfCBox.currentText() == "LF":
                return msg[:-1] + "\n"
            if self.crlfCBox.currentText() == "CR+LF":
                return msg + "\n"
            return msg

        if msg.endswith("\n"):
            if not msg.endswith("\r\n"):
                if self.crlfCBox.currentText() == "Pas de CR+LF":
                    return msg[-2]
                if self.crlfCBox.currentText() == "CR+LF":
                    return msg[:-1] + "\r\n"

            if self.crlfCBox.currentText() == "CR":
                return msg[:-1] + "\r"
            if self.crlfCBox.currentText() == "Pas de CR+LF":
                return msg[-1]

            return msg

        else:
            if self.crlfCBox.currentText() == "LF":
                return msg + "\n"
            if self.crlfCBox.currentText() == "CR":
                return msg + "\r"
            if self.crlfCBox.currentText() == "CR+LF":
                return msg + "\r\n"
            return msg