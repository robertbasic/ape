#!/usr/bin/python

__author__="robert"
__date__ ="$Oct 30, 2010 5:43:01 PM$"

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import QApplication, QMainWindow

from apelib import gui, elements


class apeMain(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.gui = gui.apeMain(self)

        self.documents = elements.apeDocumentsArea(self)

        self.fileBrowser = elements.apeFileBrowser(self.gui.filesDock, self)

    def addNewDocument(self, path, name):
        document = elements.apeDocument(path, name)
        if(document.valid):
            index = self.documents.tabs.addTab(document, document.fileName)
            self.documents.tabs.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ape = apeMain()
    ape.show()
    sys.exit(app.exec_())