import sys
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (pyqtSlot, QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QAction, QCheckBox, QComboBox, QFileDialog, QFormLayout,
QGridLayout, QGroupBox, QHBoxLayout, QInputDialog, QLabel, QMainWindow, QMenu, QMessageBox,
QLineEdit, QPushButton, QTabWidget, QTreeView, QVBoxLayout, QWidget, qApp)

from copy import deepcopy as copy

import subprocess

from modules.projectexporter import SGProjectExporter as sgp

class App(QWidget):

    SECTIONNAME, FILENAME, FILEPATH = range(3)
    filelist = []
    namelist = []
    typelist = [[], []]

    def __init__(self):
        super().__init__()

        self.filelist = []
        self.namelist = []

        self.runpath = None
        self.project = sgp()

        self.showDataTypes = True

        '''
        #czytanie listy plików
        typefile = open("settings/filetypes.sc", "r")
        for line in typefile:
            if(line[0]!=';'):
                self.typelist[0].append(line.split("\t")[0])
                self.typelist[1].append(line.split("\t")[1].strip())
        '''

        self.initUI()
        '''
        self.runpath = open("settings/runpath.sc").readline().strip()
        while(self.runpath[0]==';'):
            self.runpath = open("settings/runpath.sc").readline().strip()
        '''

    def initUI(self):
        self.dataGroupBox = QGroupBox("Files to be visualised")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        #self.dataView.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.dataView.customContextMenuRequested.connect(self.openMenu)

        #lista plików
        self.createListView()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)

        #TODO: tutaj dodać przyciski
        self.createButtons()
        mainLayout.addWidget(self.buttonGroupBox)

        #dodawanie widgetów
        self.setLayout(mainLayout)

    def getProject(self):
        return self.project
    
    def setProject(self, project):
        self.project = copy(project)

    def createButtons(self):
        self.buttonGroupBox = QGroupBox('')
        layout = QHBoxLayout()

        loadButton = QPushButton('Select file', self)
        loadButton.clicked.connect(self.ldFile)
        layout.addWidget(loadButton)

        '''
        #loadButton = QPushButton('Load file', self)
        loadButton = QPushButton('Load project', self)
        loadButton.clicked.connect(self.rldFile)
        layout.addWidget(loadButton)
        '''

        mvupButton = QPushButton('Move selection UP', self)
        mvupButton.clicked.connect(self.ListItem_UP)
        layout.addWidget(mvupButton)

        mvdwButton = QPushButton('Move selection DOWN', self)
        mvdwButton.clicked.connect(self.ListItem_DW)
        layout.addWidget(mvdwButton)

        mvdeButton = QPushButton('Delete selection', self)
        mvdeButton.clicked.connect(self.ListItem_DE)
        layout.addWidget(mvdeButton)

        #saveButton = QPushButton('Save settings', self)
        saveButton = QPushButton('Save project', self)
        saveButton.clicked.connect(self.svFile)
        layout.addWidget(saveButton)

        self.buttonGroupBox.setLayout(layout)

    def createListView(self):
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        model = self.createFileModel(self)
        self.model = model
        self.dataView.setModel(model)
        if(self.showDataTypes):
            for o in range(len(self.project.typelist[0])):
                i = len(self.project.typelist[0]) - o - 1
                self.addListFile(model, f"{self.project.typelist[0][i]}", f"{self.project.typelist[1][i]}", "")
            self.addListFile(model, f"Data type", f"Data type description", "")
            self.addListFile(model, "-----", "-----", "-----")
        self.addListFile(model, "Graph generator", self.project.runpath.split("/")[-1], f"{self.project.runpath}")
        self.addListFile(model, "-----", "-----", "-----")

        for o in range(len(self.namelist)):
            i = len(self.namelist) - o - 1
            self.addListFile(model, self.project.typelist[1][self.project.typelist[0].index(self.namelist[i])], self.project.filelist[i].split("/")[-1], self.project.filelist[i])
    
    def updateListView(self):
        model = self.createFileModel(self)
        self.dataView.setModel(model)

        if(self.showDataTypes):
            for o in range(len(self.project.typelist[0])):
                i = len(self.project.typelist[0]) - o - 1
                self.addListFile(model, f"{self.project.typelist[0][i]}", f"{self.project.typelist[1][i]}", "")
            self.addListFile(model, f"Data type", f"Data type description", "")
            self.addListFile(model, "-----", "-----", "-----")
        self.addListFile(model, "Graph generator", self.project.runpath.split("/")[-1], f"{self.project.runpath}")
        self.addListFile(model, "-----", "-----", "-----")

        for o in range(len(self.namelist)):
            i = len(self.namelist) - o - 1
            self.addListFile(model, self.project.typelist[1][self.project.typelist[0].index(self.project.namelist[i])], self.project.filelist[i].split("/")[-1], self.project.filelist[i])
    
    def toggleDataTypes(self):
        if(self.showDataTypes):
            self.showDataTypes = False
        else:
            self.showDataTypes = True
        self.updateListView()

    def createFileModel(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.SECTIONNAME, Qt.Horizontal, "Type")
        model.setHeaderData(self.FILENAME, Qt.Horizontal, "File name")
        model.setHeaderData(self.FILEPATH, Qt.Horizontal, "File path")
        return model

    def addListFile(self, model, filetype, filename, filepath):
        model.insertRow(0)
        model.setData(model.index(0, self.SECTIONNAME), filetype)
        model.setData(model.index(0, self.FILENAME), filename)
        model.setData(model.index(0, self.FILEPATH), filepath)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select data file", "", "All files (*)", options=options)
        foundfiletype = False
        if(len(self.project.typelist[0])==0):
            self.project.insertDefaultTypes()
            self.typelist = copy(self.project.typelist)
        if filename:
            self.filelist.append(filename)
            for i in range(len(self.typelist[0])):
                if(self.typelist[0][i] in filename.split("/")[-1]):
                    self.namelist.append(self.typelist[0][i])
                    foundfiletype=True
                    break
            if(not foundfiletype):
                #self.namelist.append(None)
                temp_filetype = self.getFileType()
                if(temp_filetype==None):
                    return
                self.namelist.append(temp_filetype)
            print(f"New file: {self.filelist[-1].split('/')[-1]}\ttype: {self.namelist[-1]}")
            self.project.addDataFile(filename, self.namelist[-1])
            self.updateListView()

    def openFileNameDialogForList(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select project file", "", "All files (*)", options=options)
        foundfiletype = False
        if(filename):
            file = open(filename, "r")
            for line in file:
                if(line[0]!=';'):
                    ll = line.split("\t")
                    if(not ll[1] in self.filelist):
                        self.namelist.append(ll[0].strip())
                        self.filelist.append(ll[1].strip())
            self.updateListView()

    def loadFileTypes(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select list of types or sgp file", "", "All files (*);; SGrapher list (*.sg);; SGrapher Project (*.sgp)", options=options)
        if(filename):
            typefile = open(filename, "r")
            firstline = typefile.readline().strip()
            print(firstline)
            if(firstline == "# SGrapher List"):
                print("SGrapher list detected")
                for line in typefile:
                    if(line[0]!='#'):
                        self.typelist[0].append(line.split("\t")[0])
                        self.typelist[1].append(line.split("\t")[1].strip())
            if("project" in firstline):
                for line in typefile:
                    if(line[0]!='#'):
                        ll = line.split("=")
                        if(ll[0] == "DATATYPE"):
                            self.typelist[0].append(ll[1].split("\t")[0])
                            self.typelist[1].append(ll[1].split("\t")[1].strip())
            self.project.updateArrays(typelist=self.typelist)
            print(f"type of typelist: {type(self.typelist)}")
            print("Loaded file types:")
            print(self.project.typelist)
            self.updateListView()

    def getFileType(self):
        item, okPressed = QInputDialog.getItem(self, "Choice box", "Choose data type:", self.project.typelist[1], 0, False)
        if okPressed and item:
            return self.project.typelist[0][self.project.typelist[1].index(item)]
    
    def prepareFile(self):
        output = open("settings/paths.sc", "w")
        output.write(";This file was prepared using launcher.\n")
        if(len(self.filelist)==0):
            output.write(";File purposefuly left blank by the user.")
        for i in range(len(self.filelist)):
            output.write(f"{self.namelist[i]}\t{self.filelist[i]}\n")
        output.close()

    def openMenu(self, position):
        indexes = self.sender().selectedIndexes()
        mdlIdx = self.dataView.indexAt(position)
        if not mdlIdx.isValid():
            return
        print(mdlIdx)
        item = self.model.itemFromIndex(mdlIdx)

        rclick_menu = QMenu()
        imdlIdx = len(self.filelist) - mdlIdx - 1
        if(imdlIdx>0):
            act_UP = rclick_menu.addAction(self.tr("Move Up"))
            act_UP.triggered.connect(partial(self.ListItem_UP, mdlIdx))
        
        if(imdlIdx<len(self.filelist)-1):
            act_DW = rclick_menu.addAction(self.tr("Move Down"))
            act_DW.triggered.connect(partial(self.ListItem_DW, mdlIdx))

        act_DE = rclick_menu.addAction(self.tr("Delete"))
        act_DE.triggered.connect(partial(self.ListItem_DE, mdlIdx))
        
        rclick_menu.exec_(self.sender().viewport().mapToGlobal(position))

    def readProject(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select project", "", "SGrapher files (*.sgp)", options=options)
        if filename:
            self.clearProject()
            self.project.setFileName(filename)
            self.project.loadProject()
            self.runpath = self.project.runpath
            self.filelist = self.filelist+self.project.filelist
            self.typelist[0] = self.typelist[0] + self.project.typelist[0]
            self.typelist[1] = self.typelist[1] + self.project.typelist[1]
            self.namelist = self.namelist + self.project.namelist
            self.updateListView()

    def chooseExportFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save project", "", "SGrapher files (*.sgp)", options=options)
        if filename:
            if(".sgp" not in filename[-4:]):
                filename = filename+".sgp"
            self.project.setFileName(filename, save=True)
            return 1
        return 0

    def clearProject(self):
        del(self.filelist)
        del(self.namelist)
        del(self.typelist[0])
        del(self.typelist[0])
        self.filelist = []
        self.namelist = []
        self.typelist = [[], []]
        self.project.close()
        self.updateListView()

    @pyqtSlot()
    def ldFile(self):
        print("Selecting file")
        self.openFileNameDialog()

    def rldFile(self):
        print("Loading file")
        #self.openFileNameDialogForList()
        self.readProject()

    def svFile(self):
        print("Saving settings")
        # if the file is empty, show warning
        if(len(self.project.typelist[0])==0):
            buttonReply = QMessageBox.question(self, "Warning", "No data types selected. Proceed?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if(buttonReply == QMessageBox.No):
                return
        if(len(self.project.filelist)==0):
            buttonReply = QMessageBox.question(self, "Warning", "Saving empty file. Proceed?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if(buttonReply == QMessageBox.No):
                return
        # save project file
        #self.prepareFile()
        if(self.project.filename==None):
            exportFile = self.chooseExportFile()
            if(not exportFile):
                return
        #self.project.updateArrays(self.filelist, self.namelist, self.typelist)
        self.project.exportProject()
        buttonReply = QMessageBox.question(self, "Message", "File saved. Run graph generator?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if(buttonReply == QMessageBox.Yes):
            self.runGenerator()

    def runGenerator(self):
        try:
            p1 = subprocess.Popen([self.project.python_exec, self.project.runpath,"-p",str(self.project.filename)])
            while(p1.returncode is None):
                p1.poll()
            QMessageBox.question(self, "Message", "Graph generator has finished.", QMessageBox.Ok)
        except:
            QMessageBox.question(self, "Error", "Graph generator has crashed.\n", QMessageBox.Ok)

    def svNewFile(self):
        print("Saving settings")
        # if the file is empty, show warning
        if(len(self.filelist)==0):
            buttonReply = QMessageBox.question(self, "Warning", "Saving empty file. Proceed?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if(buttonReply == QMessageBox.No):
                return
        # save project file
        #self.prepareFile()
        if (self.chooseExportFile()):
            #self.project.updateArrays(self.filelist, self.namelist, self.typelist)
            self.project.exportProject()
            buttonReply = QMessageBox.question(self, "Message", "File saved. Run graph generator?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if(buttonReply == QMessageBox.Yes):
                self.runGenerator()

    def ListItem_UP(self):
        if(len(self.dataView.selectedIndexes())==0):
            return
        sIdx = self.dataView.selectedIndexes()[0]
        cr = sIdx.model().itemFromIndex(sIdx).row()
        #mdlIdx = len(self.filelist) - cr
        mdlIdx=cr
        if(mdlIdx==0):
            return
        mem = [self.namelist[mdlIdx], self.filelist[mdlIdx]]
        self.namelist[mdlIdx] = self.namelist[mdlIdx-1]
        self.filelist[mdlIdx] = self.filelist[mdlIdx-1]
        self.namelist[mdlIdx-1] = mem[0]
        self.filelist[mdlIdx-1] = mem[1]
        self.project.moveEntryUP(mdlIdx)
        self.updateListView()

    def ListItem_DW(self):
        if(len(self.dataView.selectedIndexes())==0):
            return
        sIdx = self.dataView.selectedIndexes()[0]
        cr = sIdx.model().itemFromIndex(sIdx).row()
        #mdlIdx = len(self.filelist) - cr
        mdlIdx=cr
        if(mdlIdx>=len(self.filelist)-1):
            return
        mem = [self.namelist[mdlIdx], self.filelist[mdlIdx]]
        self.namelist[mdlIdx] = self.namelist[mdlIdx+1]
        self.filelist[mdlIdx] = self.filelist[mdlIdx+1]
        self.namelist[mdlIdx+1] = mem[0]
        self.filelist[mdlIdx+1] = mem[1]
        self.project.moveEntryDOWN(mdlIdx)
        self.updateListView()
    
    def ListItem_DE(self):
        if(len(self.dataView.selectedIndexes())==0):
            return
        sIdx = self.dataView.selectedIndexes()[0]
        cr = sIdx.model().itemFromIndex(sIdx).row()
        #mdlIdx = len(self.filelist) - cr
        mdlIdx=cr
        self.filelist.pop(mdlIdx)
        self.namelist.pop(mdlIdx)
        self.project.removeEntry(mdlIdx)
        self.updateListView()
    
    def toggleShowSaving(self):
        if(self.project.getSaveToggle()):
            self.project.setSavingGraph(savegraph=False)
        else:
            self.project.setSavingGraph()

    def assignNewRunpath(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select generator file", "", "All files (*)", options=options)
        if filename:
            self.project.setRunPath(filename)
            self.updateListView()
