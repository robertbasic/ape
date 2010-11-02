__author__="robert"
__date__ ="$Oct 31, 2010 2:18:32 PM$"


from PyQt4.QtCore import SIGNAL, SLOT, Qt
from PyQt4.QtGui import QAction, QIcon, QDockWidget, QTabWidget, QTextEdit, \
                        QGridLayout


class apeMain():

    def __init__(self, parent):
        self.parent = parent
        
        parent.setObjectName("ape")
        parent.setWindowTitle("ape")
        parent.setGeometry(50, 50, 500, 500)

        self.setupDocks()

        self.setupMenubar()

    def setupMenubar(self):
        self.menubar = self.parent.menuBar()

        exit = QAction(QIcon("/icons/exit.png"), "E&xit", self.parent)
        self.parent.connect(exit, SIGNAL("triggered()"), SLOT("close()"))

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
        
        text = QTextEdit(self.parent)

        grid = QGridLayout(self.parent)
        grid.addWidget(text, 0, 0, 1, 1)

        text.append("<?php\n")
        text.append("public function sayHello($name)")
        text.append("{\n\techo 'Hello ' . $name;\n}\n")
        text.append("not a comment # some comment")
        text.append("not a comment // a comment again")
        text.append("not a comment /** oh a comment! */ not a comment")
        text.append("not a comment /** oh a multi")
        text.append("line")
        text.append("comment! doesn't work yet! */")
        text.append("?>")

        self.parent.text = text