from os.path import isfile
import time
from copy import deepcopy as copy
import sys

class SGProjectExporter():
    def __init__(self, filename=None, defaultTypes=False):
        self.filename=None
        self.runpath = "modules/engine.py"
        self.typelist = [[], []]# stores dictionary of filetypes
        self.filelist = []# stores list of files
        self.legends = []# stores list of legends
        self.styles = []# stores list of line styles
        self.colors = []# stores list of colors
        self.namelist = []# stores names of file types
        self.widthlist = []# stores widths of lines
        self.alphalist = []# stores opacity of lines
        self.defaultWidth = 1.2
        self.PROJECTCREATED = ""
        self.PROJECTUPDATED = ""
        self.OUTPUTGRAPHFILENAME = ""
        self.OUTPUTGRAPHSAVETOGGLE = 'T'
        self.OUTPUTGRAPHDPI = 500
        self.OUTPUTGRAPHTITLE = "Graph title"
        self.OUTPUTGRAPHXAXISNAME = "X"
        self.OUTPUTGRAPHYAXISNAME = "Y"
        self.OUTPUTGRAPHWIDTH = 20/2.54
        self.OUTPUTGRAPHHEIGHT = 10/2.54
        self.OUTPUTDOMAINMINX = 'auto'
        self.OUTPUTDOMAINMAXX = 'auto'
        self.OUTPUTDOMAINMINY = 'auto'
        self.OUTPUTDOMAINMAXY = 'auto'
        self.OUTPUTDOMAINLOGSCALE = 'none'
        self.FORCEGRAPHLOGSCALE = 'none'
        self.len = 0

        if sys.platform.startswith('linux'):
            self.python_exec = "python3"
        elif sys.platform.startswith('win32'):
            self.python_exec = "python"

        if(filename is not None):
            self.setFileName(filename)
            self.loadProject()
        
        if(defaultTypes):
            self.insertDefaultTypes()

    def __len__(self):
        return self.len

    def setFileName(self, filename, save = False):
        if("\\" in filename):
            ftab = filename.split("\\")
            ftab = [var for var in ftab if var]
            filename = '/'.join(ftab)
        if(isfile(filename)):
            self.filename = filename
        else:
            if(not save):
                raise Exception("Selected project file is not available.")
            else:
                self.filename = filename
                print(f"New file name: {filename}")
        print(f"After setFileName: {self.filename}")

    def setRunPath(self, runpath):
        if(isfile(runpath)):
            self.runpath = runpath
            return 0
        else:
            print("Warning: Selected run path for graph generator is not available.")
            return 1

    def insertDefaultTypes(self, numberOfTypes=1, overwrite=False):
        if(overwrite):
            self.clearTypelist()
        for i in range(numberOfTypes):
            self.typelist[0].append(f"type{i}")
            self.typelist[1].append(f"Type {i}")

    def clearTypelist(self):
        del self.typelist[0]
        del self.typelist[1]
        self.typelist = [[], []]
    
    def loadProject(self, filename = None, commentSign = '#'):
        if(filename is None):
            filename = self.filename

        file = open(filename, "r")
        for linenum, line in enumerate(file):
            knowncommand = False
            if(line[0]!=commentSign):
                ll = line.strip().split('=')
                if(ll[0] == "PROJECTCREATED"):
                    self.PROJECTCREATED = ll[1]
                    knowncommand = True
                if(ll[0] == "PROJECTUPDATED"):
                    self.PROJECTUPDATED = ll[1]
                    knowncommand = True
                if(ll[0] == "GRAPHRUNPATH"):
                    self.setRunPath(ll[1])
                    knowncommand = True
                if(ll[0] == "DATATYPE"):
                    ls = ll[1].split("\t")
                    self.typelist[0].append(ls[0])
                    self.typelist[1].append(ls[1])
                    knowncommand = True
                if(ll[0] == "FILE"):
                    lmk = ll[1]
                    # This part fixes bug destroing file notation
                    # in project, when '=' sign is used in legend.
                    if(len(ll)>2):
                        lmk = '='.join(ll[1:])
                    ls = lmk.split("\t")
                    self.namelist.append(ls[0])
                    self.filelist.append(ls[1])
                    if(len(ls)>2):
                        self.legends.append(ls[2])
                    else:
                        self.legends.append(None)
                    if(len(ls)>3):
                        self.styles.append(ls[3])
                    else:
                        self.styles.append(None)
                    if(len(ls)>4):
                        self.colors.append(ls[4])
                    else:
                        self.colors.append(None)
                    if(len(ls)>5):
                        try:
                            self.widthlist.append(float(ls[5]))
                        except:
                            print(f"Warning: Could not read line width at line {linenum}!\nSetting line width to 1.3")
                            self.widthlist.append(1.3)
                    else:
                        self.widthlist.append(1.3)
                    if(len(ls)>6):
                        try:
                            self.alphalist.append(float(ls[6]))
                        except:
                            print(f"Warning: Could not read line opacity at line {linenum}!\nSetting opacity to 1.0")
                            self.alphalist.append(1.0)
                    else:
                        self.alphalist.append(1.0)
                    self.len = self.len+1
                    knowncommand = True
                if(ll[0] == "OUTPUTGRAPHFILENAME"):
                    self.OUTPUTGRAPHFILENAME = ll[1]
                    knowncommand = True
                if(ll[0] == "OUTPUTGRAPHDPI"):
                    try:
                        self.OUTPUTGRAPHDPI = float(ll[1])
                    except:
                        print("Warning! Could not convert graph dpi (OUTPUTGRAPHDPI) to a proper number.\n Setting to 500.")
                    knowncommand = True
                if(ll[0] == "OUTPUTGRAPHSAVETOGGLE"):
                    self.OUTPUTGRAPHSAVETOGGLE = ll[1]
                    knowncommand = True
                if(ll[0] == "OUTPUTGRAPHTITLE"):
                    lmk = ll[1]
                    # This part fixes bug destroing file notation
                    # in project, when '=' sign is used in legend.
                    if(len(ll)>2):
                        lmk = '='.join(ll[1:])
                    self.setGraphTitle(lmk)
                    knowncommand = True
                if(ll[0] == "OUTPUTGRAPHXAXISNAME"):
                    self.OUTPUTGRAPHXAXISNAME = ll[1]
                    knowncommand = True
                if(ll[0] == "OUTPUTGRAPHYAXISNAME"):
                    self.OUTPUTGRAPHYAXISNAME = ll[1]
                    knowncommand = True
                if(ll[0] == "OUTPUTGRAPHLOGSCALE"):
                    self.setScaleType(ll[1])
                    knowncommand=True
                if(ll[0] == "FORCEGRAPHLOGSCALE"):
                    self.setScaleForceType(ll[1])
                    knowncommand=True
                if(ll[0] == "OUTPUTGRAPHWIDTH"):
                    self.OUTPUTGRAPHWIDTH = float(ll[1])
                    knowncommand = True
                if(ll[0] == "OUTPUTGRAPHHEIGHT"):
                    self.OUTPUTGRAPHHEIGHT = float(ll[1])
                    knowncommand = True
                if(ll[0] == "OUTPUTDOMAINMINX"):
                    try:
                        self.OUTPUTDOMAINMINX = float(ll[1])
                    except:
                        if(ll[1]=='auto'):
                            self.OUTPUTDOMAINMINX = ll[1]
                        else:
                            print("Warning! Could not read OUTPUTDOMAINMINX project variable.")
                    knowncommand = True
                if(ll[0] == "OUTPUTDOMAINMAXX"):
                    try:
                        self.OUTPUTDOMAINMAXX = float(ll[1])
                    except:
                        if(ll[1]=='auto'):
                            self.OUTPUTDOMAINMAXX = ll[1]
                        else:
                            print("Warning! Could not read OUTPUTDOMAINMAXX project variable.")
                    knowncommand = True
                if(ll[0] == "OUTPUTDOMAINMINY"):
                    try:
                        self.OUTPUTDOMAINMINY = float(ll[1])
                    except:
                        if(ll[1]=='auto'):
                            self.OUTPUTDOMAINMINY = ll[1]
                        else:
                            print("Warning! Could not read OUTPUTDOMAINMINY project variable.")
                    knowncommand = True
                if(ll[0] == "OUTPUTDOMAINMAXY"):
                    try:
                        self.OUTPUTDOMAINMAXY = float(ll[1])
                    except:
                        if(ll[1]=='auto'):
                            self.OUTPUTDOMAINMAXY = ll[1]
                        else:
                            print("Warning! Could not read OUTPUTDOMAINMAXY project variable.")
                    knowncommand = True

                if(not knowncommand):
                    print(f"Warning! Uknown command: {ll[0]} at line {linenum}.")
        file.close()

    def setDomainSize(self, domainMinX, domainMaxX, domainMinY, domainMaxY):
        if(domainMinX == 'auto' or domainMaxX == 'auto'):
            self.OUTPUTDOMAINMAXX = 'auto'
            self.OUTPUTDOMAINMINX = 'auto'
        else:
            try:
                self.OUTPUTDOMAINMAXX = float(domainMaxX)
                self.OUTPUTDOMAINMINX = float(domainMinX)
            except:
                print("Error: Wrong domain values.\nSetting domain X range to [0, 1]")
                self.OUTPUTDOMAINMAXX = 0.0
                self.OUTPUTDOMAINMINX = 1.0
        if(domainMinY == 'auto' or domainMaxY == 'auto'):
            self.OUTPUTDOMAINMAXY = 'auto'
            self.OUTPUTDOMAINMINY = 'auto'
        else:
            try:
                self.OUTPUTDOMAINMAXY = float(domainMaxY)
                self.OUTPUTDOMAINMINY = float(domainMinY)
            except:
                print("Error: Wrong domain values.\nSetting domain Y range to [0, 1]")
                self.OUTPUTDOMAINMAXY = 0.0
                self.OUTPUTDOMAINMINY = 1.0

    def addDataFile(self, filename, filetype, legend=None, style=None, color=None, width=None, alpha=None):
        if(filename in self.filelist):
            print("Warning: This file already exists in list!")
        if(isinstance(filename, str)):
            self.filelist.append(filename)
        else:
            print(f"Warning: Wrong type of filename. Expected str, got {type(filename)}")
        if(isinstance(filetype, str)):
            self.namelist.append(filetype)
        else:
            print(f"Warning: Wrong type of filetype. Expected str, got {type(filetype)}")
        if(legend==None):
            self.legends.append(filename.split("/")[-1])
        else:
            if(isinstance(legend, str)):
                self.legends.append(legend)
            else:
                print(f"Warning: Wrong type of legend. Expected str, got {type(legend)}")
        if(style==None):
            self.styles.append("-")
        else:
            if(isinstance(style, str)):
                self.styles.append(style)
            else:
                print(f"Warning: Wrong type of style. Expected str, got {type(legend)}")
        if(color==None):
            self.colors.append("black")
        else:
            if(isinstance(color, str)):
                self.colors.append(color)
            else:
                print(f"Warning: Wrong type of color. Expected str, got {type(legend)}")
        if(width==None):
            self.widthlist.append(self.defaultWidth)
        else:
            if(isinstance(width, float) or isinstance(width, int)):
                self.widthlist.append(width)
            else:
                print(f"Warning: Wrong type of width. Expected float or int, got {type(legend)}")
        if(alpha==None):
            self.alphalist.append(1.0)
        else:
            if(isinstance(width, float) or isinstance(width, int)):
                self.alphalist.append(alpha)
            else:
                print(f"Warning: Wrong type of alpha. Expected float or int, got {type(legend)}")
        self.len+=1

    def getDomainXSize(self):
        '''
        Function returning array of domain X-axis size.
        It is prepared to work with matgrapher library.

        If domain X-axis sizes are set to auto, returns
        None. Else it returns array of values.
        '''
        if(self.OUTPUTDOMAINMINX=='auto' or self.OUTPUTDOMAINMAXX=='auto'):
            return None
        return [self.OUTPUTDOMAINMINX, self.OUTPUTDOMAINMAXX]

    def getDomainYSize(self):
        '''
        Function returning array of domain Y-axis size.
        It is prepared to work with matgrapher library.

        If domain Y-axis sizes are set to auto, returns
        None. Else it returns array of values.
        '''
        if(self.OUTPUTDOMAINMINY=='auto' or self.OUTPUTDOMAINMAXY=='auto'):
            return None
        return [self.OUTPUTDOMAINMINY, self.OUTPUTDOMAINMAXY]

    def getLineStyle(self, fileindex):
        try:
            return self.styles[fileindex]
        except:
            return "-"

    def getLineColor(self, fileindex):
        try:
            return self.colors[fileindex]
        except:
            return "black"
    
    def getLegend(self, fileindex):
        try:
            return self.legends[fileindex]
        except:
            return ""

    def getLineAlpha(self, fileindex):
        try:
            return self.alphalist[fileindex]
        except:
            return 1.0
    
    def getLineWidth(self, fileindex):
        try:
            return self.widthlist[fileindex]
        except:
            return 1.3
        
    def getGraphFileName(self):
        '''
        Function returning output file name from
        project. Returns string.
        '''
        return self.OUTPUTGRAPHFILENAME
    
    def getGraphTitle(self, decode = True):
        '''
        Function returning string with output
        graph title. If decode is set to True,
        returned title will contain "\\n" sign.
        '''
        Title = self.OUTPUTGRAPHTITLE
        if("\n" in Title and decode):
            Title = r"\n".join(Title.split("\n"))
        return Title
    
    def getAxisNames(self, decode = True):
        '''
        Function returning array with axis names.
        Works with matgrapher library standard.
        '''
        XAxisName = self.OUTPUTGRAPHXAXISNAME
        YAxisName = self.OUTPUTGRAPHYAXISNAME
        if("\n" in XAxisName and decode):
            XAxisName = "\\n".join(XAxisName.split("\n"))
        if("\n" in YAxisName and decode):
            YAxisName = "\\n".join(YAxisName.split("\n"))
        return [XAxisName, YAxisName]


    def setLegend(self, legend, fileindex = None):
        if(legend!="--!"):
            if(not isinstance(fileindex, int)):
                self.legends.append(legend)
            else:
                self.legends[fileindex] = legend
        else:
            if(not isinstance(fileindex, int)):
                self.legends.append(None)

    def setColor(self, color, fileindex=None):
        if(not isinstance(fileindex, int)):
            self.colors.append(color)
        else:
            self.colors[fileindex] = color

    def setLineStyle(self, style, fileindex=None):
        if(not isinstance(fileindex, int)):
            self.styles.append(style)
        else:
            self.styles[fileindex] = style
    
    def setLineWidth(self, width, fileindex=None):
        if(not isinstance(fileindex, int)):
            self.widthlist.append(width)
        else:
            self.widthlist[fileindex] = width

    def setLineAlpha(self, alpha, fileindex=None):
        if(not isinstance(fileindex, int)):
            self.alphalist.append(alpha)
        else:
            self.alphalist[fileindex] = alpha

    def setSavingGraph(self, savegraph = True):
        '''
        Function setting graph toggle to a value.
        If true, graph will be saved. If false,
        graph will be shown.
        '''
        if(savegraph):
            self.OUTPUTGRAPHSAVETOGGLE = 'T'
        else:
            self.OUTPUTGRAPHSAVETOGGLE = 'N'

    def getSaveToggle(self, save=True):
        '''
        Function returning save-or-show toggle state.
        Takes boolean as argument. If save=True,
        function returns toggle state for
        matgrapher.generateGraph save option, else it
        returns toggle state for matgrapher.generateGraph
        show option.
        '''
        if(save):
            if(self.OUTPUTGRAPHSAVETOGGLE == 'T'):
                return True
            return False
        if(self.OUTPUTGRAPHSAVETOGGLE == 'T'):
            return False
        return True

    def setGraphTitle(self, title):
        if("\\n" in title):
            title = "\n".join(title.split("\\n"))
        self.OUTPUTGRAPHTITLE = title

    
    def setXAxisName(self, AxisName):
        if("\\n" in AxisName):
            AxisName = "\n".join(AxisName.split("\\n"))
        self.OUTPUTGRAPHXAXISNAME = AxisName
    
    def setYAxisName(self, AxisName):
        if("\\n" in AxisName):
            AxisName = "\n".join(AxisName.split("\\n"))
        self.OUTPUTGRAPHYAXISNAME = AxisName

    def setAxisNames(self, XAxisName, YAxisName):
        self.setXAxisName(XAxisName)
        self.setYAxisName(YAxisName)
    
    def getGraphDPI(self):
        '''
        Function returning int value of graph DPI.
        '''
        return int(self.OUTPUTGRAPHDPI)

    def getGraphSize(self):
        '''
        Function returning array of graph size.
        Works with matgrapher library standard.
        '''
        return [self.OUTPUTGRAPHWIDTH, self.OUTPUTGRAPHHEIGHT]

    def getScaleType(self):
        return self.OUTPUTDOMAINLOGSCALE

    def setScaleType(self, scaleType):
        if(isinstance(scaleType, str)):
            odomlsc = ''
            if('x' in scaleType):
                odomlsc += 'x'
            if('y' in scaleType):
                odomlsc += 'y'
            if(odomlsc == ''):
                self.OUTPUTDOMAINLOGSCALE = 'none'
            else:
                self.OUTPUTDOMAINLOGSCALE = odomlsc
        else:
            if(isinstance(scaleType, list)):
                if(len(scaleType==2) and (isinstance(scaleType[0], int) or isinstance(scaleType[0], bool)) and (isinstance(scaleType[1], int) or isinstance(scaleType[1], bool))):
                    self.OUTPUTDOMAINLOGSCALE = ''
                    if(scaleType[0]==1):
                        self.OUTPUTDOMAINLOGSCALE += 'x'
                    if(scaleType[1]==1):
                        self.OUTPUTDOMAINLOGSCALE += 'y'
                    if(self.OUTPUTDOMAINLOGSCALE==''):
                        self.OUTPUTDOMAINLOGSCALE = 'none'
        print(f"Scale type: {self.OUTPUTDOMAINLOGSCALE}")
    
    def setScaleForceType(self, scaleForce):
        if(isinstance(scaleForce, str)):
            odomlsc = ''
            if('x' in scaleForce):
                odomlsc += 'x'
            if('y' in scaleForce):
                odomlsc += 'y'
            if(odomlsc == ''):
                self.FORCEGRAPHLOGSCALE = ''
            else:
                self.FORCEGRAPHLOGSCALE = odomlsc
        else:
            if(isinstance(scaleForce, list)):
                if(len(scaleForce==2) and (isinstance(scaleForce[0], int) or isinstance(scaleForce[0], bool)) and (isinstance(scaleForce[1], int) or isinstance(scaleForce[1], bool))):
                    self.FORCEGRAPHLOGSCALE = ''
                    if(scaleForce[0]==1):
                        self.FORCEGRAPHLOGSCALE += 'x'
                    if(scaleForce[1]==1):
                        self.FORCEGRAPHLOGSCALE += 'y'
        print(f"Scale forcing on: {self.FORCEGRAPHLOGSCALE}")
    
    def isYLogScaleForced(self):
        if('y' in self.FORCEGRAPHLOGSCALE):
            return True
        return False

    def isXLogScaleForced(self):
        if('x' in self.FORCEGRAPHLOGSCALE):
            return True
        return False

    def exportProject(self, filename = None, commentSign = '#'):
        if(filename is None):
            filename = self.filename
        try:
            file = open(filename, "w")
        except:
            return 2
        file.write("# This is software-generated project file for SGrapher\n")
        file.write("# \n# ---META INFO---\n# Time of initial project creation\n")
        if(self.PROJECTCREATED==""):
            file.write(f"PROJECTCREATED={time.asctime(time.localtime(time.time()))}\n")
        else:
            file.write(f"PROJECTCREATED={self.PROJECTCREATED}\n")
        file.write("# \n# Time of last project update\n")
        file.write(f"PROJECTUPDATED={time.asctime(time.localtime(time.time()))}\n")
        file.write("# \n# ---GENERATOR INFO---\n# Path to graph generator\n")
        file.write(f"GRAPHRUNPATH={self.runpath}\n")
        file.write("# \n# ---DATA INFO---\n# Types of data\n")
        for i in range(len(self.typelist[0])):
            file.write(f"DATATYPE={self.typelist[0][i]}\t{self.typelist[1][i]}\n")
        file.write("# \n# Files to read\n")
        file.write("#\tfile type\tfile path\tlegend\tline style\tline color\tline width\tline opacity\n")
        for i in range(len(self.filelist)):
            file.write(f"FILE={self.namelist[i]}\t{self.filelist[i]}\t{self.legends[i]}\t{self.styles[i]}\t{self.colors[i]}\t{self.widthlist[i]}\t{self.alphalist[i]}\n")
        file.write("# \n# --- GRAPH SETTINGS ---\n# Output file name\n")
        file.write(f"OUTPUTGRAPHFILENAME={self.OUTPUTGRAPHFILENAME}\n")
        file.write("# \n# Graph DPI\n")
        file.write(f"OUTPUTGRAPHDPI={self.OUTPUTGRAPHDPI}\n")
        file.write("# \n# Show or save (T=save, N=show)\n")
        file.write(f"OUTPUTGRAPHSAVETOGGLE={self.OUTPUTGRAPHSAVETOGGLE}\n")
        file.write("# \n# Graph title\n")
        file.write(f"OUTPUTGRAPHTITLE={self.getGraphTitle(decode=True)}\n")
        file.write("# \n# Graph X-axis name\n")
        file.write(f"OUTPUTGRAPHXAXISNAME={self.getAxisNames(decode=True)[0]}\n")
        file.write("# \n# Graph Y-axis name\n")
        file.write(f"OUTPUTGRAPHYAXISNAME={self.getAxisNames(decode=True)[1]}\n")
        file.write("# \n# Scale type\n")
        file.write(f"OUTPUTGRAPHLOGSCALE={self.getScaleType()}\n")
        file.write(f"FORCEGRAPHLOGSCALE={self.FORCEGRAPHLOGSCALE}\n")
        file.write("# \n# Graph size\n")
        file.write(f"OUTPUTGRAPHWIDTH={self.OUTPUTGRAPHWIDTH}\n")
        file.write(f"OUTPUTGRAPHHEIGHT={self.OUTPUTGRAPHHEIGHT}\n")
        file.write("# \n# Domain size (auto for auto-sizing)\n")
        file.write(f"OUTPUTDOMAINMINX={self.OUTPUTDOMAINMINX}\n")
        file.write(f"OUTPUTDOMAINMAXX={self.OUTPUTDOMAINMAXX}\n")
        file.write(f"OUTPUTDOMAINMINY={self.OUTPUTDOMAINMINY}\n")
        file.write(f"OUTPUTDOMAINMAXY={self.OUTPUTDOMAINMAXY}\n")
        
        file.close()
        return 0

    def moveOneUP(self, list_to_change, i):
        if(i>0):
            temp_var = copy(list_to_change[i-1])
            list_to_change[i-1] = list_to_change[i]
            list_to_change[i] = temp_var
        return list_to_change
    
    def moveOneDOWN(self, list_to_change, i):
        if(i<len(list_to_change)-1):
            temp_var = copy(list_to_change[i+1])
            list_to_change[i+1] = list_to_change[i]
            list_to_change[i] = temp_var
        return list_to_change

    def moveEntryUP(self, index):
        self.filelist = self.moveOneUP(self.filelist, index)
        self.legends = self.moveOneUP(self.legends, index)
        self.styles = self.moveOneUP(self.styles, index)
        self.colors = self.moveOneUP(self.colors, index)
        self.namelist = self.moveOneUP(self.namelist, index)
        self.widthlist = self.moveOneUP(self.widthlist, index)
        self.alphalist = self.moveOneUP(self.alphalist, index)
            
    def moveEntryDOWN(self, index):
        self.filelist = self.moveOneDOWN(self.filelist, index)
        self.legends = self.moveOneDOWN(self.legends, index)
        self.styles = self.moveOneDOWN(self.styles, index)
        self.colors = self.moveOneDOWN(self.colors, index)
        self.namelist = self.moveOneDOWN(self.namelist, index)
        self.widthlist = self.moveOneDOWN(self.widthlist, index)
        self.alphalist = self.moveOneDOWN(self.alphalist, index)

    def removeEntry(self, index):
        if(index<len(self.filelist)):
            self.filelist.pop(index)
            self.legends.pop(index)
            self.styles.pop(index)
            self.colors.pop(index)
            self.namelist.pop(index)
            self.widthlist.pop(index)
            self.alphalist.pop(index)
            self.len -= 1

    def updateArrays(self, filelist=None, namelist=None, typelist=None, legends=None, styles=None, widths=None, alphas=None):
        print("Updating arrays")
        if(isinstance(filelist, list)):
            self.filelist = filelist
        if(isinstance(namelist, list)):
            self.namelist = namelist
        if(isinstance(typelist, list)):
            print("Updating list")
            self.typelist = copy(typelist)
        if(isinstance(legends, list)):
            self.legends = legends
        if(isinstance(styles, list)):
            self.styles = styles
        if(isinstance(styles, list)):
            self.widthlist = widths

    def readData(self, filename, separationChar = ' ', labelSeparationChar = ' ', stringTerminator = '"', returnLabels = False, lessInfo = True):
        '''
        Funkcja do odczytu plików tekstowych z wynikami. Może być stosowana do plików eksportowanych przez ANSYS Fluent,
        XFoil lub arkuszy csv. Funkcja może zwrócić zarówno wartości, jak i oznaczenia kolumn. Założono, że linia
        oznaczenia kolumn jest linią bezpośrednio poprzedzającą dane.
        Do każdej linii oznaczenia kolumn dodano jako pierwszą wartość indeks tabeli wartości, od którego zaczyna się
        kolejny zestaw danych opisywany nazwą kolumn.
        Argumenty:
        -> filename (string) - ścieżka do wybranego pliku
        -> expectMultiple (bool) - flaga możliwości wystąpienia wielu zestawów danych
        -> separationChar (string) - znak lub znaki separacji wartości w kolumnach
        -> labelSeparationChar (string) - znak lub znaki separacji nazw kolumn
        -> returnLabels (bool) - flaga uruchomienia zwracania nazw kolumn. Domyślnie wyłączona.
        -> lessInfo (bool) - flaga wyłączenia wypisywania informacji debugujących. Domyślnie włączona.
        Wartości zwracane:
        -> label ([[int, string, ...], ...]) - dwuwymiarowa tabela zawierająca indeksy linii danych oraz nazwy kolumn.
        -> array ([[float, ...], ...]) - dwuwymiarowa tabela zawierająca poszczególne kolumny czytanego pliku.
        '''
        if(not lessInfo):
            print("Opening file")
        file = open(filename, 'r')# otwórz plik
        if(not lessInfo):
            print("Initiating arrays")
        array = []# tabela przesyłana na zewnątrz funkcji. Zawiera odczytane z pliku wartości
        valline = False# flaga linii wartości. Jeżeli jest postawiona, funkcja będzie zapisywać nowo odczytane wartości do tabeli array
        prevLine = []# tabela poprzednią linię tekstu. Służy do uzupełniania tabeli labels
        labels = []# tabela zawieracjąca nazwy kolumn. Uzupełniana gdy flaga valline jest postawiona, a flaga prevStat nie. 
        prevStat = False# flaga poprzedniego statusu valline. Wykorzystywana do włączania/wyłączania zapisu nazw kolumn.
        for line in file:# dla każdej linii w pliku
            if(not lessInfo):
                print("Reading line")
            ll = line.split(separationChar)# rozbij linię po spacjach
            if(not lessInfo):
                print("Clearing line")
            ll = [var for var in ll if var]# usuń wszystkie puste komórki
            if("\n" in ll):
                ll = ll[:-1]
            #wykrywanie, czy pierwszy element linii zawiera liczbę
            if(not lessInfo):
                print("Looking for a float number in the line")
            try:
                float(ll[0])# prymitywne sprawdzenie, czy pierwszy element linii jest liczbą
                valline = True# ustaw flagę linii wartości tak, aby mogł nastąpić zapis do tabeli
            except:
                if(not lessInfo):
                    print(f"First cell of the line does not contain number. Ignoring line: \"{line}\"")
                valline = False
            #jeżeli flaga linii wartości jest postawiona, dopisz linię do tabeli
            if(valline):
                #jeśli tabela ma za mało kolumn, rozszerz ją
                if(len(array)<len(ll)):
                    if(not lessInfo):
                        print("Appending array")
                    for i in range(len(ll)-len(array)):
                        array.append([])
                #jeżeli dostępny jest opis kolumn
                if(valline and (not prevStat)):
                    if(not lessInfo):
                        print("Saving column")
                    #może się zdarzyć, że znak rozdzielający poszczególne kolumny w ich opisie jest inny, niż znak rozdzielający kolumny
                    #wartości (przykład: pliki fluenta). Dlatego właśnie należy dodatkowo rozdzielić kolumny opisów.
                    if(separationChar!=labelSeparationChar):
                        prevLine = (separationChar.join(prevLine)).split(labelSeparationChar)
                    if(stringTerminator!=None):
                        glnum = 0
                        for num, inst in enumerate(prevLine):
                            if(num+glnum>=len(prevLine)):
                                break
                            localstring = inst
                            ct = inst.count(stringTerminator)
                            if(ct%2==1):
                                localcounter = 0
                                for localnum, nextword in enumerate(prevLine[num+1:]):
                                    if(nextword.count(stringTerminator)%2==1 or nextword.count(stringTerminator)==0):
                                        localstring = localstring+labelSeparationChar+nextword
                                        prevLine.pop(localnum-localcounter)
                                        localcounter = localcounter+1
                                    else:
                                        break
                                prevLine[num] = localstring
                                glnum+=localcounter

                    #jeżeli linia kończy się bezpośrednio za ostatnim elementem oznaczeń, na oznaczeniu może zostać znak '\n', który
                    #powinien być usunięty.
                    if('\n' in prevLine[-1]):
                        prevLine[-1] = prevLine[-1][:-1]# usuń ostatni znak z ostatniego elementu tabeli ('\n').
                    #pliki XFoila mają brzydką cechę zostawiania znaku '#' w linii nazw kolumn. Znak ten powinien być bezwzględnie tępiony.
                    if('#' in prevLine):
                        prevLine = [var for o, var in enumerate(prevLine) if o!=prevLine.index('#')]# skopiuj tabelę prevLine bez znaku '#'
                    labels.append([len(array[0])]+prevLine)
                #przypisz kolejne wartości z linii do odpowiednich kolumn
                if(not lessInfo):
                    print("Zapisywanie zawartości linii")
                for i in range(len(ll)):
                    array[i].append(float(ll[i]))
            prevLine = ll.copy()
            prevStat = valline
        if not lessInfo:
            print(labels)
            print(array)
        file.close()# zamknij plik
        #użytkownika mogą nie interesować nazwy kolumn, więc ma wybór w postaci flagi returnLabels.
        if(returnLabels):
            return labels, array
        else:
            return array

    def close(self):
        self.__init__()