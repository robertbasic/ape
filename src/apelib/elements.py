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
        self.tree = tree

    def treeContextMenu(self, point):
        menu = QMenu(self.app)
        menu.addAction(self.app.newFileAction)
        menu.addAction(self.app.newDirectoryAction)
        menu.popup(QCursor.pos())

        idx = self.tree.selectedIndexes()[0]
        path = self.model.filePath(idx)
        self.app.newFileAction.setData(path)
        self.app.newDirectoryAction.setData(path)

    def treeItemActivated(self, i):
        if(self.model.isDir(i) == False):
            self.app.addNewDocument(self.model.filePath(i))


class apeNewFileDirectoryDialogAbstract(QDialog):

    def __init__(self, parent, possibleDirectory=''):
        QDialog.__init__(self)

        self.home = os.path.expanduser("~")
        self.startDirectory = self.home

        if(possibleDirectory != ''):
            possibleDirInfo = QFileInfo(possibleDirectory)
            if(possibleDirInfo.isDir() and possibleDirInfo.isWritable()):
                self.startDirectory = possibleDirectory


    def browseDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select directory", \
                                                        self.home)
        if(directory == ''):
            directory = self.home

        self.directoryInput.clear()
        self.directoryInput.insert(directory)


class apeNewFileDialog(apeNewFileDirectoryDialogAbstract):

    fileCreated = pyqtSignal(str)

    def __init__(self, parent, possibleDirectory=''):
        apeNewFileDirectoryDialogAbstract.__init__(self, parent, possibleDirectory)

        self.gui = gui.apeNewFileDialog(self)

    def createNewFile(self):
        filename = self.newFilenameInput.text()
        directory = self.directoryInput.text()
        directoryInfo = QFileInfo(directory)
        if(directoryInfo.isDir() and directoryInfo.isWritable()):
            filePath = "%s/%s" % (directory, filename)
            filePathInfo = QFileInfo(filePath)
            if(filePathInfo.exists() == False):
                newFile = open(filePath, 'wb')
                # UTF-8
                newFile.write("\xEF\xBB\xBF")
                newFile.close()
                self.fileCreated.emit(QString(filePath))
                self.done(1)
            else:
                pass
        else:
            pass


class apeNewDirectoryDialog(apeNewFileDirectoryDialogAbstract):

    def __init__(self, parent, possibleDirectory=''):
        apeNewFileDirectoryDialogAbstract.__init__(self, parent, possibleDirectory)

        self.gui = gui.apeNewDirectoryDialog(self)

    def createNewDirectory(self):
        newDir = self.newDirectoryInput.text()
        directory = self.directoryInput.text()
        directoryInfo = QFileInfo(directory)
        if(directoryInfo.isDir() and directoryInfo.isWritable()):
            dirPath = "%s/%s" % (directory, newDir)
            dirPathInfo = QFileInfo(dirPath)
            if(dirPathInfo.exists() == False):
                os.mkdir(dirPath, 0755)
                self.done(1)
            else:
                pass
        else:
            pass


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

    def closeOtherTabs(self, index):
        print index

    def closeAllTabs(self):
        numOfTabs = self.tabs.count()
        if(numOfTabs > 0):
            # if not reversed the world ends
            # also document closing fails miserably
            for idx in reversed(range(0, numOfTabs)):
                self.closeTab(idx)

    def tabsContextMenu(self, point):
        widget = self.tabs.childAt(point)
        if(isinstance(widget, QTabBar) is False):
            return False
        else:
            # index of the tab on which we requested the context menu
            index = widget.tabAt(point)
            menu = QMenu(self)

            closeTabAction = QAction("Close tab", self)
            # so that we can pass the index which needs to be closed
            closeTabAction.triggered.connect(lambda i=index: self.closeTab(i))

            closeOtherTabsAction = QAction("Close other tabs", self)
            closeOtherTabsAction.triggered.connect(lambda i=index: \
                                                    self.closeOtherTabs(i))

            closeAllTabsAction = QAction("Close all tabs", self)
            closeAllTabsAction.triggered.connect(self.closeAllTabs)

            menu.addAction(closeTabAction)
            menu.addAction(closeOtherTabsAction)
            menu.addAction(closeAllTabsAction)

            menu.popup(QCursor().pos())


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

    """A dirty hack flag to circumvent the calling of the
    documentModified slot on opening a document. Actually it gets called
    but does nothing if this is set to True.
    """
    openningDocument = False

    isModified = False

    def __init__(self, filePath, app):
        QWidget.__init__(self)

        self.app = app

        self.filePath = filePath

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
            self.openningDocument = True
            self.text.appendPlainText(str)

            self.syntaxer = syntaxer.syntaxer(self.text.document())

            self.text.document().setModified(False)

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

    def highlightCurrentLine(self):
        extraSelections = [QTextEdit.ExtraSelection()]
        selection = QTextEdit.ExtraSelection()
        color = QColor(209, 220, 236)

        selection.format.setBackground(color)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.text.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)

        self.text.setExtraSelections(extraSelections)

    def documentModified(self):
        if(self.text.document().isModified() \
                and self.openningDocument == False):
            
            if(self.isModified == False):
                idx = self.app.documents.tabs.currentIndex()
                tabText = self.app.documents.tabs.tabText(idx)
                tabText = "%s [*]" % tabText
                self.app.documents.tabs.setTabText(idx, tabText)

            self.isModified = True
            
        elif(self.text.document().isModified() \
                and self.openningDocument == True):
            self.openningDocument = False

    def save(self, documentIndex):
        if(self.isModified):
            file = open(self.filePath, 'w')
            data = self.text.toPlainText()
            file.write(data)
            file.close()

            tabText = self.app.documents.tabs.tabText(documentIndex)
            tabText = tabText[:-4]
            self.app.documents.tabs.setTabText(documentIndex, tabText)

            self.isModified = False