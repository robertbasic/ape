__author__="robert"
__date__ ="$Oct 31, 2010 2:45:50 PM$"

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from apelib import gui, syntaxer


class apeFileBrowser(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self)

        homePath = os.path.expanduser('~')

        model = QFileSystemModel()
        model.setRootPath(homePath)

        index = model.index(homePath)

        tree = QTreeView(self)
        tree.setHeaderHidden(True)

        tree.setModel(model)
        tree.setRootIndex(index)

        tree.hideColumn(1)
        tree.hideColumn(2)
        tree.hideColumn(3)

        parent.setWidget(tree)


class apeDocumentsArea(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self)

        self.parent = parent

        self.gui = gui.apeDocumentsArea(self)

        self.tabs.addTab(apeDocument(), 'Test')


class apeDocument(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.gui = gui.apeDocument(self)

        self.syntaxer = syntaxer.syntaxer(self.text.document())
