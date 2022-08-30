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

class LegendEdit(QWidget):

    DATATYPE, DATANAME, DATALEGEND, DATASTYLE, DATACOLOR, DATAWIDTH, DATAALPHA = range(7)

    def __init__(self):
        super().__init__()
        self.filelist = []
        self.legends = []
        self.styles = []
        self.types = []
        self.project = sgp()
        self.initUI()

    def getProject(self):
        return self.project
    
    def setProject(self, project):
        self.project = copy(project)
        self.dataEditable = False

    def initUI(self):
        self.dataGroupBox = QGroupBox("List of datasets")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.model = self.createModel(self)
        self.dataView.setModel(self.model)
        self.updateListView()

        self.dataView.setColumnWidth(self.DATATYPE, 8)
        self.dataView.setColumnWidth(self.DATALEGEND, 150)
        self.dataView.setColumnWidth(self.DATASTYLE, 5)
        self.dataView.doubleClicked.connect(self.setUpdateButtonEditable)

        self.dataView.model().dataChanged.connect(self.getModelData)

        self.createUpdateButton()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        mainLayout.addWidget(self.buttonGroupBox)
        self.setLayout(mainLayout)

        self.show()

    def createUpdateButton(self):
        self.buttonGroupBox = QGroupBox('')
        layout = QHBoxLayout()

        self.legendButton = QPushButton("Edit Legend")
        self.legendButton.clicked.connect(self.getNewLegend)

        self.styleButton = QPushButton("Edit line style")
        self.styleButton.clicked.connect(self.getNewStyle)

        self.colorButton = QPushButton("Edit color")
        self.colorButton.clicked.connect(self.getNewColor)

        self.updateButton = QPushButton("Save changes")
        self.updateButton.clicked.connect(self.getModelData)
        self.updateButton.setEnabled(False)

        layout.addWidget(self.legendButton)
        layout.addWidget(self.styleButton)
        layout.addWidget(self.colorButton)
        layout.addWidget(self.updateButton)

        self.buttonGroupBox.setLayout(layout)

    def setUpdateButtonEditable(self):
        self.updateButton.setEnabled(True)

    def getNew(self, legend=False, color=False, style=False):
        sIdx = self.dataView.selectedIndexes()[0]
        idx = sIdx.model().itemFromIndex(sIdx).row()
        filename = self.project.filelist[int(idx)].split("/")[-1]

        intro = f"Input for file {filename}"
        if(legend):
            intro = f"Legend for file {filename}"
        if(color):
            intro = f"Line color for file {filename}"
        if(style):
            intro = f"Line style for file {filename}"

        item, okPressed = QInputDialog.getText(self, "Choice box", f"{intro} (--! for None):")
        if okPressed and item:
            return item
        return None

    def getNewLegend(self):
        try:
            sIdx = self.dataView.selectedIndexes()[0]
        except:
            QMessageBox.question(self, "Error", "No file selected!", QMessageBox.Ok)
            return
        idx = sIdx.model().itemFromIndex(sIdx).row()
        ot = self.getNew(legend=True)
        if(ot!=None):
            self.project.setLegend(ot, fileindex=int(idx))
            self.updateListView()

    def getNewColor(self):
        try:
            sIdx = self.dataView.selectedIndexes()[0]
        except:
            QMessageBox.question(self, "Error", "No file selected!", QMessageBox.Ok)
            return
        idx = sIdx.model().itemFromIndex(sIdx).row()
        ot = self.getNew(color=True)
        if(ot!=None):
            self.project.setColor(ot, fileindex=int(idx))
            self.updateListView()
        
    def getNewStyle(self):
        try:
            sIdx = self.dataView.selectedIndexes()[0]
        except:
            QMessageBox.question(self, "Error", "No file selected!", QMessageBox.Ok)
            return
        idx = sIdx.model().itemFromIndex(sIdx).row()
        ot = self.getNew(style=True)
        if(ot!=None):
            self.project.setLineStyle(ot, fileindex=int(idx))
            self.updateListView()

    def onLineChanged(self, i):
        if(self.dataEdiatble):
            self.updateData()

    def createModel(self, parent):
        model = QStandardItemModel(0, 7, parent)
        model.setHeaderData(self.DATATYPE, Qt.Horizontal, "Type")
        model.setHeaderData(self.DATANAME, Qt.Horizontal, "Dataset name")
        model.setHeaderData(self.DATALEGEND, Qt.Horizontal, "Legend")
        model.setHeaderData(self.DATASTYLE, Qt.Horizontal, "Style")
        model.setHeaderData(self.DATACOLOR, Qt.Horizontal, "Color")
        model.setHeaderData(self.DATAWIDTH, Qt.Horizontal, "Line width")
        model.setHeaderData(self.DATAALPHA, Qt.Horizontal, "Opacity")
        return model

    def getModelData(self):
        for o in range(len(self.project)):
            print(f"Model legend [{o}]: {self.dataView.model().item(o, self.DATALEGEND).text()}")
            self.project.setLegend(self.dataView.model().item(o, self.DATALEGEND).text(), fileindex=o)
            self.project.setColor(self.dataView.model().item(o, self.DATACOLOR).text(), fileindex=o)
            self.project.setLineStyle(self.dataView.model().item(o, self.DATASTYLE).text(), fileindex=o)
            self.project.setLineWidth(self.dataView.model().item(o, self.DATAWIDTH).text(), fileindex=o)
            self.project.setLineAlpha(self.dataView.model().item(o, self.DATAALPHA).text(), fileindex=o)
            
        self.updateButton.setEnabled(False)

    def addEntry(self, model, datatype, dataname, datalegend, datastyle, datacolor, datawidth, dataalpha):
        model.insertRow(0)
        model.setData(model.index(0, self.DATATYPE), datatype)
        model.setData(model.index(0, self.DATANAME), dataname)
        model.setData(model.index(0, self.DATALEGEND), datalegend)
        model.setData(model.index(0, self.DATASTYLE), datastyle)
        model.setData(model.index(0, self.DATACOLOR), datacolor)
        model.setData(model.index(0, self.DATAWIDTH), datawidth)
        model.setData(model.index(0, self.DATAALPHA), dataalpha)
    
    def updateListView(self):
        self.model = self.createModel(self)
        self.dataView.setModel(self.model)

        for o in range(len(self.project.filelist)):
            i = len(self.project.filelist) - o - 1
            self.addEntry(self.model,
                          self.project.namelist[i],
                          self.project.filelist[i].split("/")[-1],
                          self.project.getLegend(i),
                          self.project.getLineStyle(i),
                          self.project.getLineColor(i),
                          self.project.getLineWidth(i),
                          self.project.getLineAlpha(i)
                )
        self.model.dataChanged.connect(self.getModelData)
