import sys
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (pyqtSlot, QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QAction, QCheckBox, QComboBox, QFileDialog, QFormLayout,
QGridLayout, QGroupBox, QHBoxLayout, QInputDialog, QLabel, QMainWindow, QMenu, QMessageBox,
QLineEdit, QPushButton, QTabWidget, QTreeView, QVBoxLayout, QWidget, qApp)

from copy import deepcopy as copy

from functools import partial
import subprocess

from modules.App import App
from modules.GraphEdit import GraphEdit
from modules.LegendEdit import LegendEdit

from modules.projectexporter import SGProjectExporter as sgp

class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.FileTab = App()
        self.GraphTab = GraphEdit()
        self.LegendTab = LegendEdit()
        self.addTab(self.FileTab, "Files")
        self.addTab(self.GraphTab, "Graph settings")
        self.addTab(self.LegendTab, "Legend editor")

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title = 'Pressure Coefficient Comparator launcher'
        self.left = 10
        self.top = 40
        self.width = 640
        self.height = 480

        self.previousTab = 0
        self.currentTab = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.window = QWidget()
        self.layout = QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

        #self.widget = App()
        self.widget = Tabs()

        self.widget.blockSignals(True)

        self.layout.addWidget(self.widget)

        #self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        projectMenu = mainMenu.addMenu("Project")
        viewMenu = mainMenu.addMenu("View")
        helpMenu = mainMenu.addMenu("Help")

        file_newProject = QAction("New project", self)
        file_newProject.setShortcut('Ctrl+N')
        file_newProject.setStatusTip('Clear current project.')
        file_newProject.triggered.connect(self.widget.FileTab.clearProject)

        file_saveProject = QAction("Save project", self)
        file_saveProject.setShortcut('Ctrl+S')
        file_saveProject.setStatusTip('Save current project.')
        file_saveProject.triggered.connect(self.sendToSave)

        file_saveNewProject = QAction("Save project as", self)
        file_saveNewProject.setShortcut('Ctrl+B')
        file_saveNewProject.setStatusTip('Select file name for curent project and save it.')
        file_saveNewProject.triggered.connect(self.widget.FileTab.svNewFile)

        file_loadProject = QAction("Load project", self)
        file_loadProject.setShortcut('Ctrl+O')
        file_loadProject.setStatusTip("Select file name for project to be loaded.")
        file_loadProject.triggered.connect(self.loadNewProject)

        file_runGenerator = QAction("Generate graph", self)
        file_runGenerator.setShortcut('Ctrl+R')
        file_runGenerator.setStatusTip("Run the graph generator.")
        file_runGenerator.triggered.connect(self.widget.FileTab.runGenerator)

        fileMenu.addAction(file_newProject)
        fileMenu.addAction(file_saveProject)
        fileMenu.addAction(file_saveNewProject)
        fileMenu.addAction(file_loadProject)
        fileMenu.addAction(file_runGenerator)

        project_selectRunPath = QAction("Select generator", self)
        project_selectRunPath.setShortcut("Ctrl+P")
        project_selectRunPath.setStatusTip("Select graph generator file")
        project_selectRunPath.triggered.connect(self.widget.FileTab.assignNewRunpath)

        project_loadFileTypes = QAction("Load data types", self)
        project_loadFileTypes.setShortcut("Ctrl+T")
        project_loadFileTypes.setStatusTip("Select file with list of data types")
        project_loadFileTypes.triggered.connect(self.widget.FileTab.loadFileTypes)

        project_graphToggle_title = "Toggle showing graph"
        if(self.widget.FileTab.project.getSaveToggle(False)):
            project_graphToggle_title = "Toggle saving graph"
        self.project_graphToggle = QAction(project_graphToggle_title, self)
        self.project_graphToggle.setShortcut("Ctrl+.")
        self.project_graphToggle.setStatusTip("Show or save graph.")
        self.project_graphToggle.triggered.connect(self.projectGraphToggle)

        projectMenu.addAction(project_selectRunPath)
        projectMenu.addAction(project_loadFileTypes)
        projectMenu.addAction(self.project_graphToggle)

        view_toggleDataTypes = QAction("Show data types", self)
        view_toggleDataTypes.triggered.connect(self.widget.FileTab.toggleDataTypes)

        viewMenu.addAction(view_toggleDataTypes)

        self.widget.currentChanged.connect(self.onChange)

        self.widget.blockSignals(False)

        #pokazywanie okna
        self.show()
    
    def projectGraphToggle(self):
        self.widget.FileTab.toggleShowSaving()
        project_graphToggle_title = "Toggle showing graph"
        imagesave_text = "[Currently] Image saving mode"
        if(self.widget.FileTab.project.getSaveToggle(False)):
            project_graphToggle_title = "Toggle saving graph"
            imagesave_text = "[Currently] Image showing mode"
        self.project_graphToggle.setText(project_graphToggle_title)
        self.widget.GraphTab.imagesave.setText(imagesave_text)

    def sendToSave(self):
        '''
        Function repairing not saving current project
        via 'Ctrl+S' shortcut.
        '''
        self.updateAllTabs()
        self.widget.FileTab.svFile()

    def updateAllTabs(self):
        if(self.previousTab == 0):
            self.previousProject = copy(self.widget.FileTab.getProject())
            print("Loading project from File Tab")
        if(self.previousTab == 1):
            self.previousProject = copy(self.widget.GraphTab.getProject())
            print("Loading project from Graph Tab")
        if(self.previousTab == 2):
            self.previousProject = copy(self.widget.LegendTab.getProject())
            print("Loading project from Legend Tab")
        
        self.widget.FileTab.setProject(self.previousProject)
        self.widget.GraphTab.setProject(self.previousProject)
        self.widget.LegendTab.setProject(self.previousProject)

    def loadNewProject(self):
        '''
        Function repairing not updating projects throughout
        tabs after loading new project from other tab.
        '''
        self.widget.FileTab.clearProject()
        self.updateAllTabs()
        self.widget.FileTab.rldFile()
        #self.previousProject = copy(self.widget.FileTab.getProject())
        #self.widget.GraphTab.setProject(self.previousProject)
        self.updateAllTabs()
        self.widget.GraphTab.reloadText()
        self.widget.LegendTab.setProject(self.previousProject)
        self.widget.LegendTab.updateListView()

    def onChange(self, i):
        self.previousTab = copy(self.currentTab)
        self.currentTab = i
        self.previousProject = None
        if(self.previousTab == 0):
            self.previousProject = copy(self.widget.FileTab.getProject())
        if(self.previousTab == 1):
            self.previousProject = copy(self.widget.GraphTab.getProject())
        if(self.previousTab == 2):
            self.previousProject = copy(self.widget.LegendTab.getProject())
        
        if(self.currentTab == 0):
            self.widget.FileTab.setProject(self.previousProject)
        if(self.currentTab == 1):
            self.widget.GraphTab.setProject(self.previousProject)
        if(self.currentTab == 2):
            self.widget.LegendTab.setProject(self.previousProject)
            self.widget.LegendTab.updateListView()
        self.previousTab = copy(self.currentTab)

if(__name__ == "__main__"):
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
