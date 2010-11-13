# -*- coding: utf-8 -*-

"""
    ape - elements
    ==============
    Elements used through out the application. Windows, dialogs
    and all sort of different widgets.
"""

__author__="robertbasic"
__date__ ="$Oct 31, 2010 2:45:50 PM$"

import os
import commands
import re
import math

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from apelib import gui, syntaxer


class apeFileBrowser(QWidget):
    """ape file browser widget, by default found on the left side
    of the application.
    """

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
            self.app.addNewDocument(self.model.filePath(i))


class apeDocumentsArea(QWidget):
    """An area which groups together all the opened files/documents"""

    open = {}

    def __init__(self, parent):
        QWidget.__init__(self)

        self.parent = parent

        self.gui = gui.apeDocumentsArea(self)

    def isDocumentAlreadyOpen(self, path):
        path = unicode(path.toUtf8(), 'utf-8')
        if(self.open.has_key(path)):
            return self.open[path]
        else:
            return False

    def getOpenDocumentPath(self, index):
        path = [path for path, i in self.open.iteritems() if i == index]
        if(len(path) == 1):
            return path[0]
        else:
            return False

    def closeTab(self, index):
        documentClosed = self.parent.closeDocument(index)
        if(documentClosed):
            path = self.getOpenDocumentPath(index)
            del self.open[path]
            self.tabs.removeTab(index)


class apeDocument(QWidget):
    """A file/document opened for reading/writing, visually sits
    in an apeDocumentsArea
    """

    file = False
    filePath = False
    fileName = False
    fileInfo = False

    readonly = QIODevice.ReadOnly
    readwrite = QIODevice.ReadWrite

    openMode = readonly

    data = False

    valid = True

    def __init__(self, filePath):
        QWidget.__init__(self)

        file = QFile(filePath)
        fileinfo = QFileInfo(file)

        if(fileinfo.exists() == False):
            self.valid = False

        if(fileinfo.isFile() == False):
            self.valid = False

        if(self.isBinary(filePath)):
            self.valid = False

        if(self.valid):

            self.gui = gui.apeDocument(self)

            self.fileName = fileinfo.fileName()

            if(fileinfo.isReadable() and fileinfo.isWritable()):
                self.openMode = self.readwrite

            if(self.openMode == self.readonly):
                self.fileName = "%s [read-only]" % self.fileName
                self.text.setReadOnly(True)

            file.open(self.openMode)
            data = file.readAll()
            codec = QTextCodec.codecForName("UTF-8")
            str = codec.toUnicode(data)
            self.text.appendPlainText(str)

            self.syntaxer = syntaxer.syntaxer(self.text.document())

            self.setLineNumbers()    

    def isBinary(self,filePath):
        filePath = unicode(filePath.toUtf8(), 'utf-8')
        fileType = commands.getoutput("file -ib " + filePath)
        pattern = re.compile(r"""text/""", re.VERBOSE)
        match = re.search(pattern, fileType)
        if match is not None:
            return False
        else:
            return True

    def setLineNumbers(self):
        self.lineNumbers.clear()
        bc = self.text.blockCount()+1
        
        self.setLineNumbersWidth(bc)

        for l in range(1, bc):
            self.lineNumbers.appendPlainText("%d" % l)

    def scrollLineNumbers(self, rect, dy):
        if(dy != 0):
            m = self.text.verticalScrollBar().value()
            self.lineNumbers.verticalScrollBar().setValue(m)

    def setLineNumbersWidth(self, number):
        # number of digits in a number: (log10(number)/log10(10))+1
        # who'd know you need math to write a text editor :D
        digits = int(math.log10(number)+1)
        width = digits * 20
        self.lineNumbers.setMaximumWidth(width)