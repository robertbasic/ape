__author__="robert"
__date__ ="$Oct 31, 2010 2:18:32 PM$"


from PyQt4.QtCore import SIGNAL, SLOT, Qt
from PyQt4.QtGui import QAction, QIcon, QDockWidget, QTabWidget, QTextEdit, \
                        QGridLayout, QLabel, QPlainTextEdit


class apeMain():

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

    def __init__(self, parent):
        self.parent = parent

        self.parent.tabs = QTabWidget(self.parent)
        self.parent.parent.setCentralWidget(self.parent.tabs)


class apeDocument():

    def __init__(self, parent):
        self.parent = parent
        
        text = QPlainTextEdit(self.parent)

        lineNumbers = QPlainTextEdit(self.parent)
        lineNumbers.setMaximumWidth(50)
        lineNumbers.setEnabled(False)

        grid = QGridLayout(self.parent)
        grid.addWidget(lineNumbers, 0, 0, 1, 1)
        grid.addWidget(text, 0, 1, 1, 1)

        text.appendPlainText("<?php\n")
        text.appendPlainText("public function sayHello($name)")
        text.appendPlainText("{\n\techo 'Hello ' . $name;\n}\n")
        text.appendPlainText("not a comment # some comment")
        text.appendPlainText("not a comment // a comment again")
        text.appendPlainText("not a comment /** oh a comment! */ not a comment")
        text.appendPlainText("not a comment /** oh a multi")
        text.appendPlainText("line")
        text.appendPlainText("comment! doesn't work yet! */")
        text.appendPlainText("?>")

        text.blockCountChanged.connect(self.parent.setLineNumbers)

        self.parent.text = text
        self.parent.lineNumbers = lineNumbers