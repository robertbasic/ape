#!/usr/bin/python

# -*- coding: utf-8 -*-

"""
    ape - ape is a PHP editor
    =========================
    ape is a simple editor/IDE for PHP. It is written in python and pyqt.

    copyright: (c) 2010 Robert Basic
    license: GNU GPL v2, see LICENSE for more details
"""

__author__="robertbasic"
__date__ ="$Oct 30, 2010 5:43:01 PM$"

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog

from apelib import gui, elements


class apeMain(QMainWindow):
    """The main ape object/window."""

    def __init__(self):
        QMainWindow.__init__(self)

        self.gui = gui.apeMain(self)

        self.documents = elements.apeDocumentsArea(self)

        self.fileBrowser = elements.apeFileBrowser(self.gui.filesDock, self)

    def newFile(self):
        possibleDirectory = self.newFileAction.data().toString()
        newFileDialog = elements.apeNewFileDialog(self, possibleDirectory)
        newFileDialog.fileCreated.connect(self.addNewDocument)
        newFileDialog.exec_()

    def newDirectory(self):
        pass

    def addNewDocument(self, path):
        alreadyOpen = self.documents.isDocumentAlreadyOpen(path)
        # 0 == False gives True!
        if(alreadyOpen is False):
            document = elements.apeDocument(path)
            if(document.valid):
                index = self.documents.tabs.addTab(document, document.fileName)

                self.documents.open[unicode(path.toUtf8(), 'utf-8')] = index

                self.documents.tabs.setCurrentIndex(index)
        else:
            self.documents.tabs.setCurrentIndex(alreadyOpen)

    def closeDocument(self, index):
        document = self.documents.tabs.widget(index)
        closed = document.close()
        return closed
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ape = apeMain()
    ape.show()
    sys.exit(app.exec_())