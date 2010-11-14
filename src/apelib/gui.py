# -*- coding: utf-8 -*-

"""
    ape - gui
    =========
    All GUI elements. Besides setting all those pretty stuff up,
    windows, menus, layouts and possibly connecting signals to slots,
    other work shouldn't be here.
"""

__author__="robertbasic"
__date__ ="$Oct 31, 2010 2:18:32 PM$"


from PyQt4.QtCore import SIGNAL, SLOT, Qt
from PyQt4.QtGui import QAction, QIcon, QDockWidget, QTabWidget, QTextEdit, \
                        QGridLayout, QLabel, QPlainTextEdit, QFrame, QPalette


class apeMain():
    """GUI for the main ape window"""

    def __init__(self, parent):
        self.parent = parent
        
        parent.setObjectName("ape")
        parent.setWindowTitle("ape")
        parent.setGeometry(50, 50, 800, 500)

        self.setupDocks()

        self.setupMenubar()

    def setupMenubar(self):
        self.menubar = self.parent.menuBar()

        exit = QAction(QIcon("/icons/exit.png"), "E&xit", self.parent)
        exit.triggered.connect(self.parent.close)

        fileMenu = self.menubar.addMenu("&File")
        fileMenu.addAction(exit)

        viewMenu = self.menubar.addMenu("&View")
        viewMenu.addAction(self.filesDock.toggleViewAction())

    def setupDocks(self):
        self.filesDock = QDockWidget("Files", self.parent)
        self.filesDock.setAllowedAreas(Qt.LeftDockWidgetArea | \
                                        Qt.RightDockWidgetArea)

        self.parent.addDockWidget(Qt.LeftDockWidgetArea, self.filesDock)


class apeDocumentsArea():
    """GUI for the documents area."""

    def __init__(self, parent):
        self.parent = parent

        self.parent.tabs = QTabWidget(self.parent)
        self.parent.parent.setCentralWidget(self.parent.tabs)

        self.parent.tabs.setTabsClosable(True)

        self.parent.tabs.tabCloseRequested.connect(self.parent.closeTab)


class apeDocument():
    """GUI for an ape document."""

    def __init__(self, parent):
        self.parent = parent

        self.parent.setAttribute(Qt.WA_DeleteOnClose)
        
        text = QPlainTextEdit(self.parent)

        lineNumbers = QPlainTextEdit(self.parent)
        lineNumbers.setMaximumWidth(20)
        lineNumbers.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        lineNumbers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        lineNumbers.setFrameShape(QFrame.StyledPanel)
        lineNumbers.setFrameShadow(QFrame.Plain)
        lineNumbers.setEnabled(False)

        grid = QGridLayout(self.parent)
        grid.addWidget(lineNumbers, 0, 0, 1, 1)
        grid.addWidget(text, 0, 1, 1, 1)

        text.blockCountChanged.connect(self.parent.setLineNumbers)
        text.updateRequest.connect(self.parent.scrollLineNumbers)
        text.cursorPositionChanged.connect(self.parent.highlightCurrentLine)

        self.parent.text = text
        self.parent.lineNumbers = lineNumbers