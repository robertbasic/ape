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
        tree.doubleClicked.connect(self.treeDoubleClicked)

        tree.setModel(self.model)
        tree.setRootIndex(index)

        tree.hideColumn(1)
        tree.hideColumn(2)
        tree.hideColumn(3)

        parent.setWidget(tree)

    def treeContextMenu(self):
        print 'context menu called'

    def treeDoubleClicked(self, i):
        if(self.model.isDir(i) == False):
            self.app.addNewDocument(self.model.filePath(i), \
                                    self.model.fileName(i))


class apeDocumentsArea(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self)

        self.parent = parent

        self.gui = gui.apeDocumentsArea(self)


class apeDocument(QWidget):

    def __init__(self, filePath):
        QWidget.__init__(self)

        self.gui = gui.apeDocument(self)

        self.syntaxer = syntaxer.syntaxer(self.text.document())
