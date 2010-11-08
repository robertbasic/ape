__author__="robert"
__date__ ="$Oct 31, 2010 2:45:50 PM$"

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from apelib import gui, syntaxer


class apeFileBrowser(QWidget):

    def __init__(self, parent, app):
        QWidget.__init__(self)

        self.app = app

        homePath = os.path.expanduser('~')

        self.model = QFileSystemModel()
        self.model.setRootPath(homePath)

        index = self.model.index(homePath)

        tree = QTreeView(self)
        tree.setHeaderHidden(True)
        tree.setContextMenuPolicy(Qt.CustomContextMenu)

        tree.customContextMenuRequested.connect(self.treeContextMenu)
        tree.activated.connect(self.treeItemActivated)

        tree.setModel(self.model)
        tree.setRootIndex(index)

        tree.hideColumn(1)
        tree.hideColumn(2)
        tree.hideColumn(3)

        parent.setWidget(tree)

    def treeContextMenu(self):
        print 'context menu called'

    def treeItemActivated(self, i):
        if(self.model.isDir(i) == False):
            self.app.addNewDocument(self.model.filePath(i), \
                                    self.model.fileName(i))


class apeDocumentsArea(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self)

        self.parent = parent

        self.gui = gui.apeDocumentsArea(self)


class apeDocument(QWidget):

    file = False
    filePath = False
    fileName = False
    fileInfo = False

    readonly = QIODevice.ReadOnly
    readwrite = QIODevice.ReadWrite

    openMode = readonly

    data = False

    valid = True

    def __init__(self, filePath, fileName):
        QWidget.__init__(self)

        file = QFile(filePath)
        fileinfo = QFileInfo(file)

        if(fileinfo.exists() == False):
            self.valid = False

        if(fileinfo.isFile() == False):
            self.valid = False

        if(self.valid):
            if(fileinfo.isReadable() and fileinfo.isWritable()):
                self.openMode = self.readwrite

            if(self.openMode == self.readonly):
                fileName = "%s [read-only]" % fileName

            self.fileName = fileName

            self.gui = gui.apeDocument(self)

            file.open(self.openMode)
            data = file.readAll()
            codec = QTextCodec.codecForName("UTF-8")
            str = codec.toUnicode(data)
            self.text.appendPlainText(str)

            self.syntaxer = syntaxer.syntaxer(self.text.document())

            self.setLineNumbers()

    def setLineNumbers(self):
        self.lineNumbers.clear()
        bc = self.text.blockCount()+1
        for l in range(1, bc):
            self.lineNumbers.appendPlainText("%d" % l)