import warnings

class fileclass():
    def __init__(self, **kwargs):
        #name of the file
        self.filename=""
        #type of the file
        self.filetype=""
        #legends associated with the file
        self.legends = []
        #styles of file columns
        self.styles = []
        #colors of file columns
        self.colors = []
        #opacity of file columns
        self.alpha = []
        #width of the file columns
        self.width = []
        #column pairs
        self.columns = []
        self.widths = []
        self.defaultLegend = ""
        self.defaultWidth = 1.2
        self.defaultAlpha = 1.0
        self.defaultStyle = "-"
        self.defaultColor = "#000000"

        columnsSet = False
        autolegend = True
        autocolor =  True
        autowidth =  True
        autoalpha =  True
        autostyle = True

        # check kwargs for basic data
        if("filename" in kwargs):
            self.setFileName(kwargs["filename"])
        if("filetype" in kwargs):
            self.setFileType(kwargs["filetype"])
        if("defaultWidth" in kwargs):
            self.defaultWidth = kwargs["defaultWidth"]
        if("defaultAlpha" in kwargs):
            self.defaultAlpha = kwargs["defaultAlpha"]
        if("autocolor" in kwargs):
            autocolor = kwargs["autocolor"]
        if("autocolor" in kwargs):
            autowidth = kwargs["autowidth"]
        if("autoalpha" in kwargs):
            autowidth = kwargs["autoalpha"]
        if("setXColumn" in kwargs and "setYColumn" in kwargs):
            self.setColumns(kwargs["setXColumn"], kwargs["setYColumn"])
            columnsSet=True
        if("setColumns" in kwargs):
            if(kwargs["setColumns"]!=None):
                self.setColumns(kwargs["setColumns"][0], kwargs["setColumns"][1])
                columnsSet=True

        if("legend" in kwargs):
            if(kwargs["legend"]!=None):
                self.setLegend(kwargs["legend"])
                self.autolegend=False
        if("color" in kwargs):
            if(kwargs["color"]!=None):
                self.setColor(kwargs["color"])
                autocolor = False
        if("width" in kwargs):
            if(kwargs["width"]!=None):
                self.setWidth(kwargs["width"])
                autowidth = False
        if("alpha" in kwargs):
            if(kwargs["alpha"]!=None):
                self.setAlpha(kwargs["alpha"])
                autoalpha = False
        if("style" in kwargs):
            if(kwargs["style"]!=None):
                self.setStyle(kwargs["style"])
                autostyle = False
        
        # If no columns were set, automatically assign 0 as X column
        # and 1 as Y column
        if(not columnsSet):
            if("legend" in kwargs):
                self.setColumns(0, 1, autolegend=autolegend, autocolor=autocolor, autowidth=autowidth, autoalpha=autoalpha, autostyle=autostyle)
        
    
    def setFileName(self, filename):
        '''
        Sets file name of the certain file
        Arguments:
        -> filename (string)
        '''
        if(isinstance(filename, str)):
            self.filename = filename
        else:
            raise Exception(f"Wrong filename type! Expected str, got {type(filename)}")
    
    def getFileName(self):
        '''
        Returns name of file.
        '''
        return self.filename

    def setFileType(self, filetype):
        '''
        Sets file type of the certain file.
        Arguments:
        -> filetype (string)
        '''
        if(isinstance(filetype, str)):
            self.filetype = filetype
        else:
            raise Exception(f"Wrong filetype type! Expected str, got {type(filename)}")
    
    def getFileType(self):
        '''
        Returns type of file.
        '''
        return self.filetype

    def setColumns(self, x, y, index=None, autolegend=False, autocolor=False, autowidth=False, autoalpha=False, autostyle=False):
        '''
        Sets columns to be read from file.
        Allows for multiple combinations
        of arguments' types:
        -> int, int   - one column is assigned as x
                        and other as y
        -> int, list  - all y columns have one x
                        column assigned
        -> list, int  - all x columns have one y
                        column assigned
        -> list, list - all columns are assigned
                        individually
        '''
        if(isinstance(x, int) and isinstance(y, int)):
            if(index==None):
                self.columns.append([x, y])
            else:
                self.columns[index] = [x, y]
        if(isinstance(x, int) and isinstance(y, list)):
            for i in y:
                self.columns.append([x, i])
        if(isinstance(x, list) and isinstance(y, int)):
            for i in x:
                self.columns.append([i, y])
        if(isinstance(x, list) and isinstance(y, list)):
            if(len(x)!=len(y)):
                raise Exception(f"Expected equal ammount of x and y arguments.\nGot [x]={len(x)} and [y]={len(y)}.")
            for i, o in zip(x, y):
                self.columns.append([i, o])
        if(autolegend):
            self.setLegend([self.defaultLegend for var in self.columns])
        if(autocolor):
            self.setColor([self.defaultColor for var in self.columns])
        if(autowidth):
            self.setWidth([self.defaultWidth for var in self.columns])
        if(autoalpha):
            self.setAlpha([self.defaultAlpha for var in self.columns])
        if(autostyle):
            self.setStyle([self.defaultStyle for var in self.columns])
    
    def getColumns(self, index=None, asstring=False):
        columns = []
        if(index==None):
            columns = self.columns
        if(isinstance(index, int)):
            columns.append(self.columns[index])
        if(isinstance(index, list)):
            for i in index:
                if(i < len(self.columns)):
                    columns.append(self.columns[index])
        if(len(columns)==0):
            raise Exception("Could not load columns")
        if(asstring):
            s = ""
            for i, c in enumerate(columns):
                s = s+str(c[0])+","+str(c[1])
                if(i<len(columns)-1):
                    s=s+","
            return s
        if(len(columns)==1):
            return columns[0]
        return columns
    def setLegend(self, legend, index=None):
        '''
        Sets legends to selected index. If no index
        provided, the method will append array of
        legends. Arguments can be:
        -> string - append with a new legend entry
        -> string, int - change selected legend entry
        -> string, list(int) - change multiple legend entries
        -> list(string) - append with multiple legend entries
        -> list(string), list(int) - change multiple legend entries
        '''
        knownInstances = False
        if(isinstance(legend, str)):
            if(index==None):
                self.legends.append(legend)
                knownInstances=True
            if(isinstance(index, int)):
                if(index<len(self.legends)):
                    self.legends[index] = legend
                else:
                    warnings.warn(f"Index too high! Could not write legend to index {index}.")
                knownInstances=True
            if(isinstance(index, list)):
                for i in index:
                    if(i<len(self.legends)):
                        self.legends[i] = legend
                    else:
                        Warning.warn(f"Index too high! Could not write legend to index {i}.")
                knownInstances=True
        if(isinstance(legend, list)):
            if(isinstance(index, list)):
                if(len(legend)!=len(index)):
                    raise Exception(f"Expected equal ammount of legends and indexes.\nGot [legend]={len(legend)} and [index]={len(index)}.")
                for l, i in zip(legend, index):
                    self.setLegend(l, i)
                knownInstances=True
            if(index==None):
                for l in legend:
                    self.setLegend(l)
                knownInstances=True
            if(isinstance(index, int)):
                Warning.warn(f"Wrong combination of legends and index. Trying to assign only first legend.")
                self.setLegend(legend[0], index)
                knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instances of legend or index")

    def getLegend(self, index=None):
        '''
        Returns one or more legends for given index(es).
        Accepts:
        -> None - returns full array of legends
        -> int - returns legend from given index
        -> list(int) - returns array of legends from given indexes
        '''
        knownInstances=False
        if(index==None):
            if(len(self.legends)>1):
                return self.legends
            return self.legends[0]
        if(isinstance(index, int)):
            if(index<len(self.legends)):
                return self.legends[index]
            else:
                raise Exception(f"Index {index} beyond legends array.")
            knownInstances=True
        if(isinstance(index, list)):
            temp_array = []
            for i in index:
                temp_array.append(self.getLegend(i))
            knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instance of index")
        

    def setColor(self, color, index=None):
        '''
        Sets colors to selected index. If no index
        provided, the method will append array of
        colors. Arguments can be:
        -> string - append with a new color entry
        -> string, int - change selected color entry
        -> string, list(int) - change multiple color entries
        -> list(string) - append with multiple color entries
        -> list(string), list(int) - change multiple color entries
        '''
        knownInstances = False
        if(isinstance(color, str)):
            if(index==None):
                self.colors.append(color)
                knownInstances=True
            if(isinstance(index, int)):
                if(index<len(self.colors)):
                    self.colors[index] = color
                else:
                    warnings.warn(f"Index too high! Could not write color to index {index}.")
                knownInstances=True
            if(isinstance(index, list)):
                for i in index:
                    if(i<len(self.colors)):
                        self.colors[i] = color
                    else:
                        Warning.warn(f"Index too high! Could not write color to index {i}.")
                knownInstances=True
        if(isinstance(color, list)):
            if(isinstance(index, list)):
                if(len(color)!=len(index)):
                    raise Exception(f"Expected equal ammount of colors and indexes.\nGot [color]={len(color)} and [index]={len(index)}.")
                for l, i in zip(color, index):
                    self.setColor(l, i)
                knownInstances=True
            if(index==None):
                for l in color:
                    self.setColor(l)
                knownInstances=True
            if(isinstance(index, int)):
                Warning.warn(f"Wrong combination of colors and index. Trying to assign only first color.")
                self.setColor(color[0], index)
                knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instances of color or index")

    def getColor(self, index=None):
        '''
        Returns one or more colors for given index(es).
        Accepts:
        -> None - returns full array of colors
        -> int - returns color from given index
        -> list(int) - returns array of colors from given indexes
        '''
        knownInstances=False
        if(index==None):
            if(len(self.colors)>1):
                return self.colors
            return self.colors[0]
        if(isinstance(index, int)):
            if(index<len(self.colors)):
                return self.colors[index]
            else:
                raise Exception(f"Index {index} beyond colors array.")
            knownInstances=True
        if(isinstance(index, list)):
            temp_array = []
            for i in index:
                temp_array.append(self.getColor(i))
            knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instance of index")

    def setStyle(self, style, index=None):
        '''
        Sets styles to selected index. If no index
        provided, the method will append array of
        styles. Arguments can be:
        -> string - append with a new style entry
        -> string, int - change selected style entry
        -> string, list(int) - change multiple style entries
        -> list(string) - append with multiple style entries
        -> list(string), list(int) - change multiple style entries
        '''
        knownInstances = False
        if(isinstance(style, str)):
            if(index==None):
                self.styles.append(style)
                knownInstances=True
            if(isinstance(index, int)):
                if(index<len(self.styles)):
                    self.styles[index] = style
                else:
                    warnings.warn(f"Index too high! Could not write style to index {index}.")
                knownInstances=True
            if(isinstance(index, list)):
                for i in index:
                    if(i<len(self.styles)):
                        self.styles[i] = style
                    else:
                        Warning.warn(f"Index too high! Could not write style to index {i}.")
                knownInstances=True
        if(isinstance(style, list)):
            if(isinstance(index, list)):
                if(len(style)!=len(index)):
                    raise Exception(f"Expected equal ammount of styles and indexes.\nGot [style]={len(style)} and [index]={len(index)}.")
                for l, i in zip(style, index):
                    self.setStyle(l, i)
                knownInstances=True
            if(index==None):
                for l in style:
                    self.setStyle(l)
                knownInstances=True
            if(isinstance(index, int)):
                Warning.warn(f"Wrong combination of styles and index. Trying to assign only first style.")
                self.setStyle(style[0], index)
                knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instances of style or index")

    def getStyle(self, index=None):
        '''
        Returns one or more styles for given index(es).
        Accepts:
        -> None - returns full array of styles
        -> int - returns style from given index
        -> list(int) - returns array of styles from given indexes
        '''
        knownInstances=False
        if(index==None):
            if(len(self.styles)>1):
                return self.styles
            return self.styles[0]
        if(isinstance(index, int)):
            if(index<len(self.styles)):
                return self.styles[index]
            else:
                raise Exception(f"Index {index} beyond styles array.")
            knownInstances=True
        if(isinstance(index, list)):
            temp_array = []
            for i in index:
                temp_array.append(self.getStyle(i))
            knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instance of index")
    
    def setAlpha(self, alpha, index=None):
        '''
        Sets opacity to selected index. If no index
        provided, the method will append array of
        opacities. Arguments can be:
        -> float - append with a new alpha entry
        -> float, int - change selected alpha entry
        -> float, list(int) - change multiple alpha entries
        -> list(float) - append with multiple alpha entries
        -> list(float), list(int) - change multiple alpha entries
        '''
        knownInstances = False
        if(isinstance(alpha, float)):
            if(index==None):
                self.alpha.append(alpha)
                knownInstances=True
            if(isinstance(index, int)):
                if(index<len(self.alpha)):
                    self.alpha[index] = alpha
                else:
                    warnings.warn(f"Index too high! Could not write alpha to index {index}.")
                knownInstances=True
            if(isinstance(index, list)):
                for i in index:
                    if(i<len(self.alpha)):
                        self.alpha[i] = alpha
                    else:
                        Warning.warn(f"Index too high! Could not write alpha to index {i}.")
                knownInstances=True
        if(isinstance(alpha, list)):
            if(isinstance(index, list)):
                if(len(alpha)!=len(index)):
                    raise Exception(f"Expected equal ammount of alphas and indexes.\nGot [alpha]={len(alpha)} and [index]={len(index)}.")
                for l, i in zip(alpha, index):
                    self.setAlpha(l, i)
                knownInstances=True
            if(index==None):
                for l in alpha:
                    self.setAlpha(l)
                knownInstances=True
            if(isinstance(index, int)):
                Warning.warn(f"Wrong combination of alphas and index. Trying to assign only first alpha.")
                self.setAlpha(alpha[0], index)
                knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instances of alpha or index")

    def getAlpha(self, index=None):
        '''
        Returns one or more alphas for given index(es).
        Accepts:
        -> None - returns full array of alphas
        -> int - returns alpha from given index
        -> list(int) - returns array of alphas from given indexes
        '''
        knownInstances=False
        if(index==None):
            if(len(self.alpha)>1):
                return self.alpha
            return self.alpha[0]
        if(isinstance(index, int)):
            if(index<len(self.alpha)):
                return self.alpha[index]
            else:
                raise Exception(f"Index {index} beyond alphas array.")
            knownInstances=True
        if(isinstance(index, list)):
            temp_array = []
            for i in index:
                temp_array.append(self.getAlpha(i))
            knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instance of index")

    def setWidth(self, width, index=None):
        '''
        Sets width to selected index. If no index
        provided, the method will append array of
        widths. Arguments can be:
        -> float - append with a new width entry
        -> float, int - change selected width entry
        -> float, list(int) - change multiple width entries
        -> list(float) - append with multiple width entries
        -> list(float), list(int) - change multiple width entries
        '''
        knownInstances = False
        if(isinstance(width, float)):
            if(index==None):
                self.width.append(width)
                knownInstances=True
            if(isinstance(index, int)):
                if(index<len(self.width)):
                    self.width[index] = width
                else:
                    warnings.warn(f"Index too high! Could not write width to index {index}.")
                knownInstances=True
            if(isinstance(index, list)):
                for i in index:
                    if(i<len(self.width)):
                        self.width[i] = width
                    else:
                        Warning.warn(f"Index too high! Could not write width to index {i}.")
                knownInstances=True
        if(isinstance(width, list)):
            if(isinstance(index, list)):
                if(len(width)!=len(index)):
                    raise Exception(f"Expected equal ammount of widths and indexes.\nGot [width]={len(width)} and [index]={len(index)}.")
                for l, i in zip(width, index):
                    self.setWidth(l, i)
                knownInstances=True
            if(index==None):
                for l in width:
                    self.setWidth(l)
                knownInstances=True
            if(isinstance(index, int)):
                Warning.warn(f"Wrong combination of widths and index. Trying to assign only first width.")
                self.setWidth(width[0], index)
                knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instances of width or index")

    def getWidth(self, index=None):
        '''
        Returns one or more widths for given index(es).
        Accepts:
        -> None - returns full array of widths
        -> int - returns width from given index
        -> list(int) - returns array of widths from given indexes
        '''
        knownInstances=False
        if(index==None):
            if(len(self.width)>1):
                return self.width
            return self.width[0]
        if(isinstance(index, int)):
            if(index<len(self.width)):
                return self.width[index]
            else:
                raise Exception(f"Index {index} beyond widths array.")
            knownInstances=True
        if(isinstance(index, list)):
            temp_array = []
            for i in index:
                temp_array.append(self.getWidth(i))
            knownInstances=True
        if(not knownInstances):
            raise Exception("Wrong instance of index")