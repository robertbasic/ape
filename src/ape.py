#!/usr/bin/python

__author__="robert"
__date__ ="$Oct 30, 2010 5:43:01 PM$"

import sys

#from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QMainWindow

from apelib import gui, elements


class apeMain(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.gui = gui.apeMain(self)

        elements.apeDocumentsArea(self)

        elements.apeFileBrowser(self.gui.filesDock)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ape = apeMain()
    ape.showMaximized()
    sys.exit(app.exec_())