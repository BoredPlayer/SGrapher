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

class GraphEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.project = sgp()
        self.initUI()

    def initUI(self):
        self.createGraphSettings()
        self.createDomainSettings()
        self.createLogScaleChecks()
        self.createFileSettings()

        self.createUpdateButton()

        HorizontalBox = QGroupBox()
        horizontalLayout = QHBoxLayout()

        InnerVerticalBox = QGroupBox("Domain settings")
        innerVerticalLayout = QVBoxLayout()

        horizontalLayout.addWidget(self.graphSettingsBox)

        innerVerticalLayout.addWidget(self.domainSettingsBox)
        innerVerticalLayout.addWidget(self.logScaleCheckBox)
        InnerVerticalBox.setLayout(innerVerticalLayout)

        horizontalLayout.addWidget(InnerVerticalBox)
        HorizontalBox.setLayout(horizontalLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(HorizontalBox)
        mainLayout.addWidget(self.fileSettingsBox)
        mainLayout.addWidget(self.updateButton, alignment=Qt.AlignRight)
        self.updateButton.resize(100, self.updateButton.height())

        self.setLayout(mainLayout)

    def createGraphSettings(self):
        self.graphSettingsBox = QGroupBox("Graph settings")
        layout = QFormLayout()

        self.imagetitle = QLineEdit(str(self.project.OUTPUTGRAPHTITLE))
        self.xaxisname = QLineEdit(str(self.project.OUTPUTGRAPHXAXISNAME))
        self.yaxisname = QLineEdit(str(self.project.OUTPUTGRAPHYAXISNAME))

        self.imageheightline = QLineEdit(str(self.project.OUTPUTGRAPHHEIGHT))
        self.imagewidthline = QLineEdit(str(self.project.OUTPUTGRAPHWIDTH))
        self.imagedpi = QLineEdit(str(self.project.getGraphDPI()))
        imagesave_text = "[Currently] Image saving mode"
        if(self.project.getSaveToggle(False)):
            imagesave_text = "Image showing mode"
        self.imagesave = QPushButton(imagesave_text, self)
        self.imagesave.clicked.connect(self.toggleShowSaving)

        self.imagetitle.textChanged.connect(self.onLineChanged)
        self.xaxisname.textChanged.connect(self.onLineChanged)
        self.yaxisname.textChanged.connect(self.onLineChanged)
        self.imagewidthline.textChanged.connect(self.onLineChanged)
        self.imageheightline.textChanged.connect(self.onLineChanged)
        self.imagedpi.textChanged.connect(self.onLineChanged)

        layout.addRow("Graph title", self.imagetitle)
        layout.addRow("X axis title", self.xaxisname)
        layout.addRow("Y axis title", self.yaxisname)
        layout.addRow("image width [in]", self.imagewidthline)
        layout.addRow("image height [in]", self.imageheightline)
        layout.addRow("image DPI", self.imagedpi)
        layout.addRow(self.imagesave)

        self.graphSettingsBox.setLayout(layout)

    def createDomainSettings(self):
        self.domainSettingsBox = QGroupBox("Axis scale")
        layout = QFormLayout()

        self.domainminx = QLineEdit(str(self.project.OUTPUTDOMAINMINX))
        self.domainmaxx = QLineEdit(str(self.project.OUTPUTDOMAINMAXX))
        self.domainminy = QLineEdit(str(self.project.OUTPUTDOMAINMINY))
        self.domainmaxy = QLineEdit(str(self.project.OUTPUTDOMAINMAXY))

        self.domainmaxx.textChanged.connect(self.onLineChanged)
        self.domainminx.textChanged.connect(self.onLineChanged)
        self.domainmaxy.textChanged.connect(self.onLineChanged)
        self.domainminy.textChanged.connect(self.onLineChanged)

        layout.addRow("Min X value", self.domainminx)
        layout.addRow("Max X value", self.domainmaxx)
        layout.addRow("Min Y value", self.domainminy)
        layout.addRow("Max Y value", self.domainmaxy)

        self.domainSettingsBox.setLayout(layout)

    def createLogScaleChecks(self):
        self.logScaleCheckBox = QGroupBox("Set log scale on axis")
        layout = QGridLayout()

        self.xlogscalecheck = QCheckBox("X-axis log scale")
        self.ylogscalecheck = QCheckBox("Y-axis log scale")
        self.flogscalecheck = QCheckBox("Force absolute")

        self.xlogscalecheck.stateChanged.connect(lambda:self.logScaleCheckBoxChanged(self.xlogscalecheck))
        self.ylogscalecheck.stateChanged.connect(lambda:self.logScaleCheckBoxChanged(self.ylogscalecheck))
        self.flogscalecheck.stateChanged.connect(lambda:self.logScaleCheckBoxChanged(self.flogscalecheck))

        layout.addWidget(self.xlogscalecheck, 0, 0)
        layout.addWidget(self.ylogscalecheck, 0, 1)
        layout.addWidget(self.flogscalecheck, 1, 0)

        self.logScaleCheckBox.setLayout(layout)

    def createFileSettings(self):
        self.fileSettingsBox = QGroupBox("File settings")
        layout = QHBoxLayout()
        self.outputfilename = QLineEdit(str(self.project.OUTPUTGRAPHFILENAME))
        self.outputfilename.textChanged.connect(self.onLineChanged)
        
        self.searchForFileButton = QPushButton("Set directory")
        self.searchForFileButton.clicked.connect(self.dialogWindow)
        layout.addWidget(self.outputfilename)
        layout.addWidget(self.searchForFileButton)
        self.fileSettingsBox.setLayout(layout)

    def createUpdateButton(self):
        self.updateButton = QPushButton("Edit data")
        self.updateButton.clicked.connect(self.enableDataEditing)

    def getProject(self):
        return self.project
    
    def setProject(self, project):
        self.project = project
        self.disableDataEditing()
        self.reloadText()
    
    @pyqtSlot()
    def toggleShowSaving(self):
        if(self.project.getSaveToggle()):
            self.project.setSavingGraph(savegraph=False)
        else:
            self.project.setSavingGraph()
        imagesave_text = "[Currently] Image saving mode"
        if(self.project.getSaveToggle(False)):
            imagesave_text = "[Currently] Image showing mode"
        self.imagesave.setText(imagesave_text)
        pass

    def dialogWindow(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save project", "", "PNG files (*.png)", options=options)
        if filename:
            self.project.OUTPUTGRAPHFILENAME = filename
            self.outputfilename.setText(filename)
            return 1
        return 0

    def onLineChanged(self):
        if(self.dataEdiatble):
            self.updateData()

    def toggleDataEditing(self, state):
        self.imagetitle.setEnabled(state)
        self.xaxisname.setEnabled(state)
        self.yaxisname.setEnabled(state)

        self.imagewidthline.setEnabled(state)
        self.imageheightline.setEnabled(state)
        self.imagedpi.setEnabled(state)
        self.imagesave.setEnabled(state)

        self.domainminx.setEnabled(state)
        self.domainmaxx.setEnabled(state)
        self.domainminy.setEnabled(state)
        self.domainmaxy.setEnabled(state)

        self.xlogscalecheck.setEnabled(state)
        self.ylogscalecheck.setEnabled(state)
        self.flogscalecheck.setEnabled(state)

        self.outputfilename.setEnabled(state)
        self.searchForFileButton.setEnabled(state)

    def disableDataEditing(self):
        self.dataEdiatble = False
        self.toggleDataEditing(False)

    def enableDataEditing(self):
        self.dataEdiatble = True
        self.toggleDataEditing(True)

    def updateData(self):
        try:
            self.project.OUTPUTGRAPHHEIGHT = float(self.imageheightline.text())
        except:
            self.project.OUTPUTGRAPHHEIGHT = 0.0
        try:
            self.project.OUTPUTGRAPHWIDTH = float(self.imagewidthline.text())
        except:
            self.project.OUTPUTGRAPHWIDTH = 0.0
        try:
            self.project.OUTPUTGRAPHDPI = float(self.imagedpi.text())
        except:
            self.project.OUTPUTGRAPHDPI = 0.0
        self.project.setDomainSize(self.domainminx.text(), self.domainmaxx.text(), self.domainminy.text(), self.domainmaxy.text())
        self.project.OUTPUTGRAPHTITLE = self.imagetitle.text()
        self.project.OUTPUTGRAPHXAXISNAME = self.xaxisname.text()
        self.project.OUTPUTGRAPHYAXISNAME = self.yaxisname.text()
        self.project.OUTPUTGRAPHFILENAME = self.outputfilename.text()

    def logScaleCheckBoxChanged(self, b):
        lcstring = ''
        if(self.xlogscalecheck.isChecked()):
            lcstring = lcstring+'x'
        if(self.ylogscalecheck.isChecked()):
            lcstring = lcstring+'y'
        self.project.setScaleType(lcstring)
        if(self.flogscalecheck.isChecked()):
            self.project.setScaleForceType(lcstring)
        else:
            self.project.setScaleForceType('')

    def reloadText(self):
        self.imageheightline.setText(str(self.project.OUTPUTGRAPHHEIGHT))
        self.imagewidthline.setText(str(self.project.OUTPUTGRAPHWIDTH))
        self.imagedpi.setText(str(self.project.OUTPUTGRAPHDPI))
        self.domainminx.setText(str(self.project.OUTPUTDOMAINMINX))
        self.domainmaxx.setText(str(self.project.OUTPUTDOMAINMAXX))
        self.domainminy.setText(str(self.project.OUTPUTDOMAINMINY))
        self.domainmaxy.setText(str(self.project.OUTPUTDOMAINMAXY))
        self.imagetitle.setText(str(self.project.OUTPUTGRAPHTITLE))
        self.xaxisname.setText(str(self.project.OUTPUTGRAPHXAXISNAME))
        self.yaxisname.setText(str(self.project.OUTPUTGRAPHYAXISNAME))
        self.outputfilename.setText(self.project.OUTPUTGRAPHFILENAME)

        if('x' in self.project.OUTPUTDOMAINLOGSCALE):
            self.xlogscalecheck.setChecked(True)
        else:
            self.xlogscalecheck.setChecked(False)
        if('y' in self.project.OUTPUTDOMAINLOGSCALE):
            self.ylogscalecheck.setChecked(True)
        else:
            self.ylogscalecheck.setChecked(False)
        if(self.project.isYLogScaleForced() or self.project.isXLogScaleForced()):
            self.flogscalecheck.setChecked(True)
        else:
            self.flogscalecheck.setChecked(False)
