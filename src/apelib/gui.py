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
                        QGridLayout, QLabel, QPlainTextEdit, QFrame, QPalette, \
                        QLineEdit, QPushButton, QWidget


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

        newFileAction = QAction("&New file", self.parent)
        newFileAction.triggered.connect(self.parent.newFile)
        self.parent.newFileAction = newFileAction

        newDirectoryAction = QAction("New &directory", self.parent)
        newDirectoryAction.triggered.connect(self.parent.newDirectory)
        self.parent.newDirectoryAction = newDirectoryAction

        exitAction = QAction(QIcon("icons/exit.png"), "E&xit", self.parent)
        exitAction.triggered.connect(self.parent.close)

        fileMenu = self.menubar.addMenu("&File")
        newMenu = fileMenu.addMenu("New")

        fileMenu.addAction(exitAction)

        newMenu.addAction(newFileAction)
        newMenu.addAction(newDirectoryAction)

        viewMenu = self.menubar.addMenu("&View")
        viewMenu.addAction(self.filesDock.toggleViewAction())

    def setupDocks(self):
        self.filesDock = QDockWidget("Files", self.parent)
        self.filesDock.setAllowedAreas(Qt.LeftDockWidgetArea | \
                                        Qt.RightDockWidgetArea)

        self.parent.addDockWidget(Qt.LeftDockWidgetArea, self.filesDock)


class apeNewFileDialog():

    def __init__(self, parent):
        parent.setWindowTitle("Create a new file")
        parent.resize(400, 250)

        descriptionLabel = QLabel(parent)
        descriptionLabel.setText("Enter the name for the new file " \
                                    + "and choose a directory for it")

        newFileLabel = QLabel(parent)
        newFileLabel.setText("Name of the new file")

        directoryLabel = QLabel(parent)
        directoryLabel.setText("Directory for the new file")

        parent.newFilenameInput = QLineEdit(parent)
        parent.directoryInput = QLineEdit(parent.home, parent)
        parent.directoryInput.setReadOnly(True)

        browseButton = QPushButton("&Browse", parent)
        browseButton.clicked.connect(parent.browseDirectory)

        okButton = QPushButton("&Done", parent)
        okButton.clicked.connect(parent.createNewFile)

        cancelButton = QPushButton("&Cancel", parent)
        cancelButton.clicked.connect(parent.close)

        frame = QFrame(parent)
        frame.setFrameStyle(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)

        space = QWidget(parent)
        space.resize(400, 50)

        grid = QGridLayout(parent)
        grid.addWidget(descriptionLabel, 0, 0, 1, 3)
        grid.addWidget(newFileLabel, 1, 0, 1, 3)
        grid.addWidget(parent.newFilenameInput, 2, 0, 1, 3)
        grid.addWidget(directoryLabel, 3, 0, 1, 3)
        grid.addWidget(parent.directoryInput, 4, 0, 1, 2)
        grid.addWidget(browseButton, 4, 2, 1, 1)
        grid.addWidget(space, 5, 0, 1, 3)
        grid.addWidget(frame, 6, 0, 1, 3)
        grid.addWidget(cancelButton, 7, 0, 1, 1)
        grid.addWidget(okButton, 7, 2, 1, 1)


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